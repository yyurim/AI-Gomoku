from player import Player
from state import State
import random
import signal
import time
import copy


def signal_handler(signum, frame):
    raise Exception("제한 시간을 초과했습니다.")

class Gomoku(object):

    #####################################################################
    #
    #   오목
    #   - init()
    #       오목 게임을 생성합니다.       
    #
    #   - start()
    #       오목 게임을 시작하고, 게임의 결과를 반환합니다.
    #
    #   - mode_menu()
    #       게임의 모드를 출력하고, 유저가 선택한 모드를 반환합니다.
    #
    #   - mode_user()
    #       유저와 유저의 대결입니다. 유저들의 입력으로 게임이 진행됩니다.
    #
    #   - mode_AI()
    #       AI와 AI의 대결입니다. AI들의 게임을 관전합니다.
    #
    #   - mode_user_AI()
    #       유저와 AI의 대결입니다.
    #
    #   - finished()
    #       게임의 종료여부를 반환합니다.
    #       게임은 두 플레이어 중 한 플레이어가 승리할 시 종료됩니다.
    #       오목판에 돌을 새로 둘 곳이 더이상 없다면 게임을 종료합니다.
    #
    #   - alpha_beta_search(player, max_depth)
    #       Alpha-Beta search를 활용하여 플레이어의 최적의 전략을 찾습니다.
    #
    #   - max_value(state, player, alpha, beta, depth)
    #       Max 플레이어의 최적의 전략을 찾습니다.
    #       
    #   - min_value(state, player, alpha, beta, depth)
    #       Min 플레이어는 Max 플레이어의 utility가 최소가 되도록 action을 선택합니다. 
    #
    #
    #####################################################################
    
    def __init__(self):
        super(Gomoku, self).__init__()
        self.player_b = Player('B')
        self.player_w = Player('W')

        # 턴에는 제한시간이 있습니다.
        self.timer = 10

        # 오목판의 크기를 결정합니다.
        self.dimension = 19

        # 초기 state입니다.
        self.state = State(self.dimension)

        # Alpha-Beta search가 끝나지 않았을때 time out이 발생한다면
        # 현재까지 진행된 search 정보만을 가지고 최적의 전략을 찾습니다.
        # Iterative Deepening Search의 각 Depth의 transition 정보를 담습니다.
        # Depth마다 초기화 되는 리스트입니다.
        self.time_out_continuity = []                                   
        self.time_out_transition = [] 

        # 가장 최근의 action 정보를 저장하는 변수입니다.                                  
        self.current_action = (-1,-1)                                   

    def start(self):
        
        # 빈 오목판으로 초기화합니다.
        self.state.board.initialize()

        # 모드를 선택합니다.                  
        mode = self.mode_menu()                                         
        self.timer = int(input("제한 시간을 입력해주세요 (30 이상 / 단위 : 초) >> "))
        if self.timer < 30 :
            print("주어진 시간을 늘려주세요")
            print("게임을 종료합니다.") 
            return ""

        winner = ""
        if mode == 1:
            winner = self.mode_user()
                
        elif mode ==2 :
            winner = self.mode_AI()
        
        elif mode == 3:
            winner = self.mode_user_AI()

        else :
            # 선택된 모드가 세 모드가 아니라면 게임을 종료합니다.
            print("게임을 종료합니다.")                                     
        
        if winner == "":
            print("승자는 없습니다.")
        elif winner =="비겼습니다.":
            print(winner)
        else:
            print("{} 승리!!!".format(winner))

        return winner

    def user_input(self, now_playing):
        try:
            while(True):
                y_temp , x = input("y좌표(A-S), x좌표(0-18)를 순서대로 입력하세요 ").split()
                y = ord(y_temp)-ord("A")
                x = int(x)

                # 선택된 좌표에 돌이 있거나, 돌을 둠으로써 쌍삼이라면 돌을 둘 수 없습니다.
                if self.state.on_board((y,x)) != '.' or self.state.board.double_three((y,x), now_playing):
                    print("돌을 둘 수 없습니다. 다른 곳을 선택하세요")
                    continue
                else:
                    return y, x
        except Exception:
            print("제한 시간을 초과했습니다.")
            
            return -1, -1
                
    def mode_menu(self):
        print("------------------------- Welcome to GOMOKU ------------------------- ")
        print(". . . . . . . . . . 1. USER VS USER . . . . . . . . . . . . . . . . .  ")
        print(". . . . . . . . . . . . . . . . . . . . . 2. AI VS AI . . . . . . . .")
        print(". . . . . . . . . . . . . . 3. USER VS AI. . . . . . . . . . . . . . . ")
        print("--------------------------------------------------------------------- ")
        mode = int(input("모드를 선택하세요 >> "))
        return mode
    
    def mode_user(self):

        print("흑돌이 먼저 돌을 둡니다.")
        now_playing = self.player_b

        # 승자가 결정될 때까지 턴을 반복합니다.
        while(1):

            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(self.timer)

            # 플레이어 유저는 돌을 올릴 좌표를 입력합니다.
            y, x = self.user_input(now_playing)

            if (y,x) == (-1,-1):
                if now_playing==self.player_b :
                    now_playing = self.player_w
                else:
                    now_playing = self.player_b
                print("돌을 두지 않아 패배했습니다.")
                return now_playing.color

            self.state.board.make_marker((y,x),now_playing)
            
            # 다음 턴을 위해 플레이어를 전환합니다.
            if now_playing==self.player_b :
                now_playing = self.player_w
            else:
                now_playing = self.player_b
            
            # 현재 state의 오목판을 출력합니다.
            self.state.board.print_board()

            print("플레이어 {}가 ( {} , {} )위에 돌을 두었습니다.".format(now_playing.color,chr(ord("A")+y),x))

            # 게임의 종료 여부를 판단합니다.
            is_winner = self.finished()

            if is_winner == "" :
                continue
            else:
                return is_winner

    def mode_AI(self):

        print("흑돌이 먼저 돌을 둡니다.")
        now_playing = self.player_b
        print("플레이어 {}를 기다립니다....".format(now_playing.color))
        time.sleep(1)

        # 첫 흑돌은 오목판의 중앙부에 랜덤으로 돌을 올려놓습니다.
        init_coordinate = [random.randrange( -1 + int(self.dimension/2), 1 + int(self.dimension/2) ) for i in range(2)]
        self.state.board.make_marker(init_coordinate, now_playing)
        print("플레이어 {}가 ( {} , {} )위에 돌을 두었습니다.".format(now_playing.color,chr(ord("A")+init_coordinate[0]),init_coordinate[1]))
        self.state.board.print_board()
        self.state.set_current_coordinate(init_coordinate)
        self.current_action = init_coordinate

        while(1):
            # 현재 턴을 위해 플레이어를 전환합니다.
            if now_playing==self.player_b :
                now_playing = self.player_w
            else:
                now_playing = self.player_b

            print("플레이어 {}를 기다립니다....".format(now_playing.color))

            # 현재 턴의 시간 제한이 시작됩니다.
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(self.timer)

            # Optimal strategy 정보를 저장할 변수들입니다.
            heuristic_best_actions = {}
            continuity = 0

            # 제한 시간동안 Iterative Deepening Alpha-Beta Search를 진행합니다.
            try:
                # depth limit를 증가시키며 alpha-beta search를 합니다.
                max_depth = 0
                while(1):

                    heuristic_best_action, continuity = self.alpha_beta_search(now_playing,max_depth)

                    # alpha-beta search가 완료됐다면 best action은 한 개 입니다.
                    heuristic_best_actions[heuristic_best_action] = 1

                    # 현재 state에 대한 goal test를 진행합니다.
                    if continuity == 5 :
                        print("Solution Depth ----> {}".format(max_depth))
                        break
                    else :
                        print("Cut-off Depth ----> {}".format(max_depth))
                        max_depth += 1
                        heuristic_best_actions = {}

            except Exception:
                print("제한 시간을 초과했습니다.")

                # 제한 시간을 초과한 경우, 현재까지 탐색한 transition들에 대한 utility를 탐색하여 max utility를 갖는 action을 선택합니다.
                # time_out_transition에는 max lev의 transition 정보들이 저장돼있습니다.
                # 현재까지 transition 정보들 중 가장 큰 utility 값을 갖는 transition의 action 정보를 저장합니다.
                # max_value search 결과, 동일한 action이 선택되는 경우가 있습니다.
                # 이 때 중복되는 action 수를 세어, 결과에 반영합니다.

                # 현재 탐색 중이던 depth에서 search가 끝난 node들의 정보로 action를 선택합니다.
                # 가장 큰 utility를 갖는 transition의 action을 찾습니다.
                # action과 utility가 중복된다면 그 중복횟수를 카운팅합니다.
                max_time_out = max(self.time_out_transition,key=lambda x:x["utility"])["utility"]
                for transition in self.time_out_transition:
                    if max_time_out == transition["utility"]:
                        if transition["action"] in heuristic_best_actions.keys():
                            heuristic_best_actions[transition["action"]] += 1
                        else:
                            heuristic_best_actions[transition["action"]] = 1
            
                # 다음 턴을 위해 변수를 초기화합니다.
                self.time_out_transition = []
                self.time_out_continuity = []

            # alpha-beta search의 결과가 없다면, 현재 비어있는 좌표 정보를 저장합니다.
            if heuristic_best_actions == {}:
                heuristic_best_actions = []
                heuristic_best_actions = self.state.board.all_possible_coordinate()
                heuristic_value = self.state.board.find_current_closest(self.current_action, heuristic_best_actions)

            # 중복횟수가 큰 action -> 중복횟수가 모두 동일하다면 최근의 action과 거리가 가까운 action 순으로
            # action을 결정합니다.
            else:
                multiple = max(heuristic_best_actions.items(), key=lambda x:x[1])
                if multiple[1] > 1:
                        print("{}번 선택된 action  ---> ( {} , {} )".format(multiple[1], chr(ord("A")+multiple[0][0]),multiple[0][1]))
                        heuristic_value = multiple[0]
                else:
                    heuristic_value = self.state.board.find_current_closest(self.current_action, list(heuristic_best_actions.keys()))
                    print("가장 가까운 action ---> ( {} , {} )".format(chr(ord("A")+heuristic_value[0]),heuristic_value[1]))

            # 선택된 좌표위에 돌을 올려둡니다.
            self.state.board.make_marker(heuristic_value, now_playing)

            # 현재 action정보를 저장합니다.
            self.state.set_current_coordinate(heuristic_value)
            self.current_action = heuristic_value
        
            # 현재 state의 오목판을 출력합니다.
            self.state.board.print_board()

            print("플레이어 {}가 ( {} , {} )위에 돌을 두었습니다.".format(now_playing.color,chr(ord("A")+heuristic_value[0]),heuristic_value[1]))
            print('\n')

            # 게임의 종료 여부를 판단합니다.
            is_winner = self.finished()

            if is_winner == "" :
                continue
            else:
                return is_winner

            time.sleep(1)

    def mode_user_AI(self):
        # USER가 돌을 두지 않은 경우를 카운팅 할 변수입니다.
        flag_too_much_auto = 0

        # USER는 돌의 색을 결정할 수 있습니다.
        # 흑이 먼저 돌을 둡니다.
        me = input("돌을 선택해주세요. 흑은 B을, 백은 W를 입력해주세요. >> ")

        if me == 'B':
            self.player_b.set_player("USER")
            self.player_w.set_player("AI")
        elif me =='W':
            self.player_w.set_player("USER")
            self.player_b.set_player("AI")
        else:
            print("돌이 선택되지 않았습니다.")
            return ""
        
        print("흑돌이 먼저 돌을 둡니다.")
        now_playing = copy.deepcopy(self.player_b)


        # 첫 수가 컴퓨터라면
        # 컴퓨터는 오목판의 중앙부근에 랜덤으로 착수합니다.
        if now_playing.get_player() =="AI":
            print("플레이어 {}를 기다립니다....".format(now_playing.player))
            time.sleep(1)

            # 첫 흑돌은 오목판의 중앙부에 랜덤으로 돌을 올려놓습니다.
            init_coordinate = [random.randrange( -1 + int(self.dimension/2), 1 + int(self.dimension/2) ) for i in range(2)]
            self.state.board.make_marker(init_coordinate, now_playing)
            print("플레이어 {}가 ( {} , {} )위에 돌을 두었습니다.".format(now_playing.player,chr(ord("A")+init_coordinate[0]),init_coordinate[1]))
            self.state.board.print_board()
            self.state.set_current_coordinate(init_coordinate)
            self.current_action = init_coordinate

        elif now_playing.get_player() == "USER":

            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(self.timer)
            y, x = self.user_input(now_playing)
                
            if (y,x) ==(-1,-1):
                flag_too_much_auto += 1
                print("좌표를 랜덤으로 선택합니다..")
                random_choice = self.state.board.all_possible_coordinate()
                y = random.randrange( -1 + int(self.dimension/2), 1 + int(self.dimension/2) ) 
                x = random.randrange( -1 + int(self.dimension/2), 1 + int(self.dimension/2) )

            self.state.board.make_marker((y,x),now_playing)

            # 현재 state의 오목판을 출력합니다.
            self.state.board.print_board()
            self.state.set_current_coordinate((y,x))
            self.current_action = (y,x)

            print("플레이어 {}가 ( {} , {} )위에 돌을 두었습니다.".format(now_playing.player,chr(ord("A")+y),x))



        while(1):

            # 자동 수가 많은 경우
            # 컴퓨터의 승리입니다.
            if flag_too_much_auto > 5 :
                print("자동 수가 너무 많습니다. 게임을 종료합니다.")
                return "AI"

            # 다음 턴을 위해 플레이어를 전환합니다.
            if now_playing.color == self.player_b.color :
                now_playing = copy.deepcopy(self.player_w)
            else:
                now_playing = copy.deepcopy(self.player_b)

            if now_playing.get_player() == "USER":
                # 현재 턴의 시간 제한이 시작됩니다.
                signal.signal(signal.SIGALRM, signal_handler)
                signal.alarm(self.timer)

                # 플레이어 유저는 돌을 올릴 좌표를 입력합니다.
                y, x = self.user_input(now_playing)
                
                if (y,x) ==(-1,-1):
                    flag_too_much_auto += 1
                    print("좌표를 랜덤으로 선택합니다..")
                    random_choice = self.state.board.all_possible_coordinate()
                    y , x = self.state.board.find_current_closest(self.current_action, random_choice)

                self.state.board.make_marker((y,x),now_playing)

                # 현재 state의 오목판을 출력합니다.
                self.state.board.print_board()
                self.state.set_current_coordinate((y,x))
                self.current_action = (y,x)

                print("플레이어 {}가 ( {} , {} )위에 돌을 두었습니다.".format(now_playing.get_player(),chr(ord("A")+y),x))

                # 게임의 종료 여부를 판단합니다.
                is_winner = self.finished()

                if is_winner == "" :
                    continue
                else:
                    return is_winner

                

            elif now_playing.get_player() == "AI":

                print("플레이어 {}를 기다립니다....".format(now_playing.get_player()))

                # 현재 턴의 시간 제한이 시작됩니다.
                signal.signal(signal.SIGALRM, signal_handler)
                signal.alarm(self.timer)

                # Optimal strategy 정보를 저장할 변수들입니다.
                heuristic_best_actions = {}
                continuity = 0

                # 제한 시간동안 Iterative Deepening Alpha-Beta Search를 진행합니다.
                try:
                    # depth limit를 증가시키며 alpha-beta search를 합니다.
                    max_depth = 0
                    while(1):

                        heuristic_best_action, continuity = self.alpha_beta_search(now_playing,max_depth)
                        heuristic_best_actions[heuristic_best_action[0]] = 1

                        # 현재 state에 대한 goal test를 진행합니다.
                        if continuity == 5 :
                            print("Solution Depth ----> {}".format(max_depth))
                            break
                        else :
                            print("Cut-off Depth ----> {}".format(max_depth))
                            max_depth += 1
                            heuristic_best_actions = {}

                except Exception:
                    print("제한 시간을 초과했습니다.")

                    # 제한 시간을 초과한 경우, 현재까지 탐색한 transition들에 대한 utility를 탐색하여 max utility를 갖는 action을 선택합니다.
                    # time_out_transition에는 max lev의 transition 정보들이 저장돼있습니다.
                    # 현재까지 transition 정보들 중 가장 큰 utility 값을 갖는 transition의 action 정보를 저장합니다.
                    # max_value search 결과, 동일한 action이 선택되는 경우가 있습니다.
                    # 이 때 중복되는 action 수를 세어, 결과에 반영합니다.

                    # 현재 탐색 중이던 depth에서 search가 끝난 node들의 정보로 action를 선택합니다.
                    # 가장 큰 utility를 갖는 transition의 action을 찾습니다.
                    # action과 utility가 중복된다면 그 중복횟수를 카운팅합니다.
                    max_time_out = max(self.time_out_transition,key=lambda x:x["utility"])["utility"]
                    for transition in self.time_out_transition:
                        if max_time_out == transition["utility"]:
                            if transition["action"] in heuristic_best_actions.keys():
                                heuristic_best_actions[transition["action"]] += 1
                            else:
                                heuristic_best_actions[transition["action"]] = 1
                
                    # 다음 턴을 위해 변수를 초기화합니다.
                    self.time_out_transition = []
                    self.time_out_continuity = []

                # alpha-beta search의 결과가 없다면, 현재 비어있는 좌표 정보를 저장합니다.
                if heuristic_best_actions == {}:
                    heuristic_best_actions = []
                    heuristic_best_actions = self.state.board.all_possible_coordinate()
                    heuristic_value = self.state.board.find_current_closest(self.current_action, heuristic_best_actions)

                # 중복횟수가 큰 action -> 중복횟수가 모두 동일하다면 최근의 action과 거리가 가까운 action 순으로
                # action을 결정합니다.
                else:
                    multiple = max(heuristic_best_actions.items(), key=lambda x:x[1])
                    if multiple[1] > 1:
                        print("{}번 선택된 action  ---> ( {} , {} )".format(multiple[1], chr(ord("A")+multiple[0][0]),multiple[0][1]))
                        heuristic_value = multiple[0]
                    else:
                        heuristic_value = self.state.board.find_current_closest(self.current_action, list(heuristic_best_actions.keys()))
                        print("가장 가까운 action ---> ( {} , {} )".format(chr(ord("A")+heuristic_value[0]),heuristic_value[1]))
                
                
                if self.state.board.double_three(heuristic_value, now_playing):
                    print("플레이어 {}의 쌍삼입니다!".format(now_playing.get_player()))

                # 선택된 좌표위에 돌을 올려둡니다.
                
                if (self.state.board.make_marker(heuristic_value, now_playing)) == (-1, -1):
                    print("잘못된 곳에 돌을 두었습니다. 상대방이 이겼습니다.")
                    if now_playing.color == self.player_b.color :
                        now_playing = copy.deepcopy(self.player_w)
                    else:
                        now_playing = copy.deepcopy(self.player_b)
                    return now_playing.get_player()


                # 현재 action정보를 저장합니다.
                self.state.set_current_coordinate(heuristic_value)
                self.current_action = heuristic_value
            
                # 현재 state의 오목판을 출력합니다.
                self.state.board.print_board()

                print("플레이어 {}가 ( {} , {} )위에 돌을 두었습니다.".format(now_playing.player,chr(ord("A")+heuristic_value[0]),heuristic_value[1]))
                print('\n')


                # 게임의 종료 여부를 판단합니다.
                is_winner = self.finished()

                if is_winner == "" :
                    continue
                else:
                    return is_winner

                time.sleep(1)

    def finished(self):
        winner = ""
        count = 0
        # 오목판을 탐색합니다.
        for y in range(self.dimension):
            for x in range(self.dimension):
                cur_color = self.state.on_board((y,x))
                if cur_color == '.':
                    continue
                count += 1
                dy = [0,1,1,1,0,-1,-1,-1]
                dx = [1,1,0,-1,-1,-1,0,1]
                for direction in range(8):
                    continuous = 0
                    for continuous in range(6):
                        
                        y_check = y + continuous*dy[direction]
                        x_check = x + continuous*dx[direction]
                        if (y_check < 0) or (y_check >= self.dimension) or (x_check < 0) or (x_check >= self.dimension ):
                            break
                        
                        
                        if self.state.on_board((y_check, x_check)) != cur_color :
                            break

                    # 연속된 돌의 개수가 5개라면, 그 돌들의 색깔로 승자를 결정합니다.
                    if continuous == 5:
                        winner = cur_color
                        break

        if count == (self.dimension*self.dimension):            
            return "비겼습니다."
        
        return winner

    # 현재 state를 root로 하는 alpha-beta search를 진행합니다.
    def alpha_beta_search(self, player, max_depth):
        # 알파 = - infinity / 베타 = infinity 로 초기화 합니다.
        alpha = float("-inf")
        beta = float("inf")
	
        valid_transitions = self.state.get_valid_transitions(player, sort="sorting")
        utilities = {}
        
        # 현재 state에 대해 utility의 max value를 탐색합니다.
        for action, new_state in valid_transitions:
            continuity, utility = self.max_value(new_state, player, alpha, beta, max_depth)
            utilities[action] = (continuity, utility)

        # 현재 state에서 가능한 action들로 얻은 children의 utility 중
        # 가장 큰 utility를 갖는 child를 선택하여
        # 그때의 action과 그 state에서 가장 긴 돌의 쌍에 포함된 돌의 수를 저장합니다.
        best_action = max(utilities.items(), key=lambda u:u[1][1])[0]
        max_continuity = max(utilities.items(), key=lambda u:u[1][1])[1][1]

        # 이때 돌의 수를 반환하는 것은 게임의 종료여부를 판단하기 위함입니다.
        return best_action, max_continuity

    # 플레이어 Max의 utility값을 탐색합니다.
    def max_value(self, state, player, alpha, beta, depth):
        if depth == 0 :

            markers , utility = state.heuristic_evaluation(player, "max")
            action = state.get_current_coordinate()

            return (markers, utility)

        utility = float("-inf")

        # 현재 노드의 children을 현재 노드와의 거리를 기준으로 정렬합니다.
        # 현재 노드와 child 노드의 거리가 가까울수록 먼저 탐색됩니다.
        transitions = state.get_valid_transitions(player, "sorting")

        transition_info = []
        markers_info = []

        # 현재 노드의 children을 탐색합니다.
        for action, s in transitions:
            # 자식노드의 heuristic을 평가합니다.
            markers, utility = s.heuristic_evaluation(player, "max")
            markers_info.append(markers)
            transition_info.append({"action":action,"state":s,"markers":markers,"utility":utility})

            utility = max(utility, self.min_value(s,player,alpha, beta, depth-1)[1])

            if utility >= beta:
                self.time_out_transition.append({"action":action,"state":state,"markers":markers,"utility":utility})
                print("action ( {} , {} ) markers {}  utility {}".format(chr(ord("A")+action[0]),action[1],markers,utility))
                return (markers, utility)
            alpha = max(alpha, utility)
        
        max_markers = max(markers_info)
        valid_actions = [action[0] for action in transitions]
        action = state.board.find_current_closest(state.get_current_coordinate(), valid_actions)
        print("action ( {} , {} ) markers {}  utility {}".format(chr(ord("A")+action[0]),action[1],markers,utility))
        self.time_out_transition.append({"action":action,"state":state,"markers":markers,"utility":utility})
        return (max_markers, utility)

    # 플레이어 Min의 utility 값을 탐색합니다.
    def min_value(self, state, player, alpha, beta, depth):
        # 상대 플레이어의 관점에서 evaluation을 진행합니다.
        player_min = player

        if player == self.player_b:
            player_min = self.player_w
        else:
            player_min = self.player_b

        if depth == 0 :

            markers, utility = state.heuristic_evaluation(player_min, "min")
            action = state.get_current_coordinate()

            return (markers, utility)

        utility = float('inf')

        # 현재 노드의 children을 현재 노드와의 거리를 기준으로 정렬합니다.
        # 현재 노드와 child 노드의 거리가 가까울수록 먼저 탐색됩니다.
        transitions = state.get_valid_transitions(player_min, "sorting")

        transition_info = []
        markers_info = []

        # 현재 노드의 children을 탐색합니다.
        for action, s in transitions:
            # 자식노드의 heuristic을 평가합니다.
            markers, utility = s.heuristic_evaluation(player_min, "min")
            markers_info.append(markers)
            transition_info.append({"action":action,"state":s,"markers":markers,"utility":utility})

            utility = min(utility,
                            self.max_value(s, player,
                                        alpha, beta, depth-1)[1])

            if utility <= alpha:
                return (action, markers, utility)
            beta = min(beta, utility)

        max_markers = min(markers_info)

        return (max_markers, utility)

