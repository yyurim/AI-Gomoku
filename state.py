from board import Board
import copy
import operator

class State(object):
    
    #####################################################################
    #
    #   State
    #   - init(dimension)
    #       Alpha-Beta Search의 state을 생성합니다.
    #       Problem : (dimension x dimension) 크기의 판 위에서 진행되는 오목
    #
    #   - on_board(coordinate)
    #       현재 state에서 오목판의 coordinate위에 있는 돌의 색을 반환합니다.
    #
    #   - set_current_coordinate(coordinate)
    #       이전 state에서 현재 state으로의 transition에 사용된 action 정보를 세팅합니다.
    #       action : coordinate위에 돌을 올려놓음
    #       
    #   - get_current_coordinate()
    #       이전 state에서 현재 state으로의 transition에 사용된 action 정보를 반환합니다.
    #       action 정보 : 새로 올려진 돌의 좌표
    #
    #   - get_valid_transitions(player, sorting)
    #       현재 state에서 가능한 action과, action의 결과인 state(child)을 반환합니다.
    #       sorting에 값이 주어지면 현재 state의 action과 transition으로의 action사이의
    #       거리가 짧은 순으로 정렬됩니다.
    #       
    #   - new_state(new_marker, player)
    #       새로운 state을 생성합니다.
    #
    #   - heuristic_evaluation(player, phase)
    #       현재 state의 heuristic을 평가합니다.
    #
    #
    ######################################################################
    
    def __init__(self, dimension):
        super(State, self).__init__()
        self.dimension = dimension
        self.board = Board(self.dimension)
        self.current_coordinate = None

    def on_board(self, coordinate):
        return self.board.on(coordinate)

    def set_current_coordinate(self, coordinate):
        self.current_coordinate = coordinate
    
    def get_current_coordinate(self):
        return self.current_coordinate

    def get_valid_transitions(self, player, sort=None):  

        # 현재 state의 오목판에서 비어있는 좌표들을 저장합니다.                         
        valid_actions = self.board.all_possible_coordinate()

        # 현재 state의 children을 저장할 리스트입니다.             
        transitions = []   

        # 가능한 좌표에 돌을 놓아 새로운 state을 생성합니다.                                                
        for action in valid_actions:                                       
            new_state = self.new_state(action, player)
            transitions.append((action, new_state))

        # 최근에 돌을 둔 위치와 새로운 돌의 위치 사이의 거리가 짧은 순으로 transition을 정렬합니다.
        if sort != None:
            transitions_dist = {}

            action_current = self.get_current_coordinate()

            for transition in transitions:
                dist = max(abs(transition[0][0]-action_current[0]),abs(transition[0][1]-action_current[1]))
                transitions_dist[transition] = dist
            
            transitions_temp = sorted(transitions_dist.items(), key = lambda item: item[1])
            transitions = []
            for transition in transitions_temp:
                transitions.append(transition[0])

        return transitions
    

    def new_state(self, new_marker, player):
        new_state = State(self.dimension)

        # 현재 state의 오목판을 복사합니다.
        new_state.board = copy.deepcopy(self.board)      

        # 현재 state의 오목판 위에 새로운 돌을 올려놓습니다.                  
        new_state.board.make_marker(new_marker,player)    
        
        # 새로운 돌의 위치를 새로운 state을 생성한 action 정보로 저장합니다.                 
        new_state.set_current_coordinate(new_marker)                      

        return new_state


    # 현재 state의 heuristic을 평가합니다.
    # 돌이 놓인 패턴으로 state의 heuristic 값을 도출합니다.
    # 함수값은 0부터 100까지 10단위 입니다.
    # 100 : 연속된 돌이 5개인 경우 
    #       ex) BBBBB
    #  80 : 연속된 돌이 4개이며 양 끝이 막히지 않은 경우 
    #       ex) .BBBB.
    #  70 : 돌이 4개이지만 다음 턴에 막힐 수 있는 경우 
    #       ex) .BBBBW / BB.BB / BBB.B
    #  60 : 돌이 3개이며 양 끝이 막히지 않은 경우
    #       ex) .BBB. / .B.BB.
    #  50 : 돌이 3개이지만 다음 턴에 막힐 수 있는 경우
    #       ex) .BBBW / .B.BBW / .BB.BW
    #  40 : 돌이 2개이며 양 끝이 막히지 않은 경우
    #       ex) .BB. / .B.B.
    #  30 : 돌이 2개이지만 다음 턴에 막힐 수 있는 경우
    #       ex) .BBW / .B.BW
    #  10 : 돌이 1개이거나 2개이며 다음 턴에 막힐 수 있는 경우
    #   0 : 양 끝이 막힌 경우
    def heuristic_evaluation(self, player, phase):
 
        board_info = {}

        for y in range(self.dimension):
            for x in range(self.dimension):
                cur_color = self.board.on((y,x))
                
                if (cur_color != '.'):
                    continue

                # 현재 좌표(y,x)를 기준으로 8 방향에 대해 돌들을 탐색합니다.
                # (y,x): (0, 1) / (1, 1) / (1, 0) / (1, -1) / (0, -1) / (-1, -1) / (-1, 0) / (-1, 1)
             
                # 8 방향에 대한 연속된 돌의 정보를 저장합니다.
                markers = []

                dy = [0,1,1,1,0,-1,-1,-1]
                dx = [1,1,0,-1,-1,-1,0,1]  
                
                for direction in range(8):
                    count_player = 0
                    stucked = False
                    for dist in range(1,6):
                        
                        y_check = y + dist*dy[direction]
                        x_check = x + dist*dx[direction]

                        # 돌을 카운팅 할 때, 오목판을 넘어가지 않도록 합니다.
                        if (y_check < 0) or (y_check >= self.dimension) or (x_check < 0) or (x_check >= self.dimension ):
                            break

                        # 시작점(y,x)의 돌의 direction의 방향으로 상대 플레이어에의해 돌의 막혔으면 멈춥니다.
                        if self.board.on((y_check,x_check)) != player.color:
                            if self.board.on((y_check,x_check)) != '.':
                                stucked = True
                            break
                        count_player +=1

                    info = {"count_player":count_player, "stucked":stucked}

                    # 방향별로 돌의 갯수를 저장합니다.
                    markers.append(info)


                # 4 방향에 대해 돌을 조사합니다.
                board_info_direction = []
                for direction in range(4):
                    now = None

                    if markers[direction]["count_player"] > 3 or markers[direction+4]["count_player"] > 3:
                        now  = (markers[direction]["count_player"],80)

                    elif markers[direction]["count_player"] == 3 or markers[direction+4]["count_player"] == 3:

                        if markers[direction]["count_player"] == 3:

                            if markers[direction]["stucked"] == False:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 3:
                                    if markers[direction+4]["stucked"] == False:
                                        now  = (marker,60)
                                    else:
                                        now  = (marker,50)
                                elif marker == 4:
                                    now  = (marker,70)                 
                                elif marker >= 5:
                                    now  = (marker,70)
                            else:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 3:
                                    if markers[direction+4]["stucked"] == False:
                                        now  = (marker,50)
                                    else:
                                        now  = (marker,0)
                                elif marker == 4:
                                    now  = (marker,70)   
                                elif marker >= 5:
                                    now  = (marker,70)

                        elif markers[direction+4]["count_player"] == 3:

                            if markers[direction+4]["stucked"] == False:
                                marker = markers[direction+4]["count_player"] + markers[direction]["count_player"]
                                if marker == 3:
                                    if markers[direction]["stucked"] == False:
                                        now  = (marker,60)
                                    else:
                                        now  = (marker,50)
                                elif marker == 4:
                                    now  = (marker,70)                 
                                elif marker >= 5:
                                    now  = (marker,70)
                            else:
                                marker = markers[direction+4]["count_player"] + markers[direction]["count_player"]
                                if marker == 3:
                                    if markers[direction]["stucked"] == False:
                                        now  = (marker,50)
                                    else:
                                        now = (marker,0)
                                elif marker == 4:
                                    now = (marker,70)   
                                elif marker >= 5:
                                    now = (marker,70)

                    elif markers[direction]["count_player"] == 2 or markers[direction+4]["count_player"] == 2:

                        if markers[direction]["count_player"] == 2:

                            if markers[direction]["stucked"] == False:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 2:
                                    if markers[direction+4]["stucked"] == False:
                                        now  = (marker,40)
                                    else:
                                        now  = (marker,30)
                                elif marker == 3:
                                    if markers[direction+4]["stucked"] == False:
                                        now  = (marker,60)
                                    else:
                                        now  = (marker,50)
                                elif marker >= 4:
                                    now  = (marker,70)
                                    
                            else:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 2:
                                    if markers[direction+4]["stucked"] == False:
                                        now  = (marker,30)
                                    else:
                                        now = (marker,0)
                                elif marker == 3:
                                    if markers[direction+4]["stucked"] == False:
                                        now  = (marker,50)
                                    else:
                                        now = (marker,0)
                                elif marker >= 4:
                                    now  = (marker,70)
                        else :

                            if markers[direction+4]["stucked"] == False:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 2:
                                    if markers[direction]["stucked"] == False:
                                        now  = (marker,40)
                                    else:
                                        now  = (marker,30)
                                elif marker == 3:
                                    if markers[direction]["stucked"] == False:
                                        now = (marker,60)
                                    else:
                                        now = (marker,50)
                                elif marker >= 4:
                                    now = (marker,70)
                                    
                            else:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 2:
                                    if markers[direction]["stucked"] == False:
                                        now  = (marker,30)
                                    else:
                                        now = (marker,0)
                                elif marker == 3:
                                    if markers[direction]["stucked"] == False:
                                        now  = (marker,50)
                                    else:
                                        now = (marker,0)
                                elif marker >= 4:
                                    now  = (marker,70)

                    elif markers[direction]["count_player"] == 1 or markers[direction+4]["count_player"] == 1:

                        if markers[direction]["count_player"] == 1:

                            if markers[direction]["stucked"] == False:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 1:
                                    now = (marker,10)
                                    
                                elif marker == 2:
                                    if markers[direction+4]["stucked"] == False:
                                        now = (marker,40)
                                    else:
                                        now = (marker,30)
                                    
                            else:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 1:
                                    if markers[direction+4]["stucked"] == False:
                                       now  = (marker,10)
                                    else:
                                        now  = (marker,0)
                                elif marker == 2:
                                    if markers[direction+4]["stucked"] == False:
                                        now  = (marker,30)
                                    else:
                                        now  = (marker,0)
  
                        else :

                            if markers[direction+4]["stucked"] == False:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 1:
                                    now  = (marker,10)
                                    
                                elif marker == 2:
                                    if markers[direction]["stucked"] == False:
                                        now  = (marker,40)
                                    else:
                                        now = (marker,30)

                                    
                            else:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 1:
                                    if markers[direction]["stucked"] == False:
                                        now = (marker,10)
                                    else:
                                        now = (marker,0)
                                elif marker == 2:
                                    if markers[direction]["stucked"] == False:
                                        now  = (marker,30)
                                    else:
                                        now = (marker,0)

                    elif markers[direction]["count_player"] == 0 or markers[direction+4]["count_player"] == 0:

                        if markers[direction]["count_player"] == 0:

                            if markers[direction]["stucked"] == False:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 0:
                                    now = (marker,0)
                                    
                                elif marker == 1:
                                    if markers[direction+4]["stucked"] == False:
                                        now = (marker,10)
                                    else:
                                        now = (marker,0)
                                    
                            else:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 0:
                                    now  = (marker,0)

                                elif marker == 1:
                                    if markers[direction+4]["stucked"] == False:
                                        now = (marker,10)
                                    else:
                                        now = (marker,0)

                        else :

                            if markers[direction+4]["stucked"] == False:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 0:
                                    now  = (marker,0)
                                    
                                elif marker == 1:
                                    if markers[direction]["stucked"] == False:
                                        now  = (marker,10)
                                    else:
                                        now = (marker,0)

                                    
                            else:
                                marker = markers[direction]["count_player"] + markers[direction+4]["count_player"]
                                if marker == 0:
                                    now  = (marker,0)
                                    
                                elif marker == 1:
                                    if markers[direction]["stucked"] == False:
                                        now = (marker,10)
                                    else:
                                        now = (marker,0)

                    board_info_direction.append(now)

                # 4 방향을 조사하고, 그 중 가장 높은 값을 갖는 방향의 값을 
                # 현재 위치의 heuristic value로 합니다.
                board_info[(y,x)] = max(board_info_direction, key=lambda x:x[1])

        # 전체 오목판에서 가장 큰 heuristic value를
        # 현재 state의 heuristic value로 합니다.
        h = max(board_info.values(), key=lambda x:x[1])

        return h

        



