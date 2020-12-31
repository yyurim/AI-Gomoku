import random
import copy

class Board(object):

    #####################################################################
    #
    #  오목판
    #   - init(dimension)
    #       (dimension x dimension) 크기의 오목판을 생성합니다.
    #
    #   - initialize()
    #       오목판을 초기화합니다.
    #       '.' : 해당 좌표에는 돌이 존재하지 않습니다.
    #
    #   - on(coordinate)
    #       coordinate 위에 존재하는 돌의 색을 반환합니다.
    #
    #   - print_board()
    #       오목판을 출력합니다.
    #
    #   - make_marker(coordinate, player)
    #       coordinate 위에 player의 돌을 올려놓습니다.
    #
    #   - is_valid_coordinate(coordinate)
    #       coordinate 위에 돌을 놓을 수 있는지 없는지 여부를 반환합니다.
    #       coordinate 위에 돌이 존재하지 않는다면 True 를,
    #                      돌이 존재한다면 False를 반환합니다.
    #
    #   - all_possible_coordinate()
    #       오목판의 비어 있는 좌표들의 리스트를 반환합니다.
    #
    #   - find_current_closest(current, valid_actions)
    #       가능한 action(비어있는 좌표에 돌을 올려 놓는 것)의 좌표들 중에서,
    #       최근에 놓인 돌의 좌표(current)와 가장 가까운 좌표를 반환합니다.
    #       가까운 좌표가 여러 개라면 랜덤으로 선택합니다.
    # 
    #   - double_three(coordinate, player)
    #       오목판의 coordinate위에 player의 돌을 두었을때, 쌍삼의 성립여부를 반환합니다.
    #
    #####################################################################

    def __init__(self, dimension):
        super(Board, self).__init__()
        self.board = {}
        self.dimension = dimension

    def initialize(self):
        for y in range(self.dimension):
            for x in range(self.dimension):
                self.board[(y, x)] = '.'

    def on(self, coordinate):
        if (coordinate[0] < 0) or (coordinate[0] >= self.dimension) \
             or (coordinate[1]< 0) or (coordinate[1] >= self.dimension ):
            return "not on board"
        return self.board[coordinate]

    def print_board(self):
        print("  ", end=" ")
        for x in range(self.dimension):
            print("%2d"%(x), end="  ")
        print("\n")
        for y in range(self.dimension):
            print(chr(ord("A")+y), end="   ")
            for x in range(self.dimension):
                print(self.board[(y, x)],end="   ")

            print("\n")

    def make_marker(self, coordinate, player):
        if self.is_valid_coordinate(coordinate):
            self.board[(coordinate[0], coordinate[1])] = player.color
            if self.double_three((coordinate[0],coordinate[1]), player):
                print("플레이어 {}의 쌍삼입니다!".format(player.get_player()))
                return [-1, -1]
            return coordinate
        else:
            return [-1, -1]
    
    def delete_marker(self, coordinate):
        if self.on(coordinate) != '.':
            self.board[(coordinate[0], coordinate[1])] = '.'

    def is_valid_coordinate(self, coordinate):
        # coordinate의 y좌표나 x좌표가 오목판 밖에 존재한다면 False를 반환합니다.
        if(coordinate[0]<0) or (coordinate[0]>=self.dimension) \
            or  (coordinate[1]<0) or (coordinate[1]>=self.dimension) :

            return False
        if self.board[(coordinate[0], coordinate[1])] == '.':
            return True
        else:
            return False

    def all_possible_coordinate(self):
        coordinates = []
        
        for y in range(self.dimension):
            for x in range(self.dimension):
                temp = (y, x)
                if self.is_valid_coordinate(temp):
                    coordinates.append(temp)

        return coordinates

    def find_current_closest(self, current, valid_actions):
      distances = []
      for i, action in enumerate(valid_actions):
        dist = max(abs(current[0]-action[0]),abs(current[1]-action[1]))
        distances.append(dist)
      
      count = 0
      for i in range(len(distances)):
          if distances[i]==min(distances):
              count += 1
      min_distance_index = random.randrange(count)
      return valid_actions[min_distance_index]

    # 쌍삼을 판별합니다.
    # coordinate위의 돌을 기준으로, 돌의 수를 새어봅니다.
    def double_three(self, coordinate, player, nested=False):
        
        self.board[(coordinate[0], coordinate[1])] = player.color

        cur_color = self.on(coordinate)
        y, x = coordinate

        # 8 방향에 대한 연속된 돌의 정보를 저장합니다.
        continuous_marker = []

        # (y,x)를 기준으로 8개의 방향에 대해 최대 돌의 개수를 조사합니다.
        dy = [0,1,1,1,0,-1,-1,-1]
        dx = [1,1,0,-1,-1,-1,0,1]  

        # 현재 좌표(y,x)를 기준으로 8 방향에 대해 연속된 돌들을 탐색합니다.
        # (y,x): (0, 1) / (1, 1) / (1, 0) / (1, -1) / (0, -1) / (-1, -1) / (-1, 0) / (-1, 1) 
        for direction in range(8):
            count_marker = 0
            # 방향별로 최대 거리 3만큼 떨어진 곳까지 존재하는 돌을 조사합니다.
            for continuous in range(1,4):
                
                y_check = y + continuous*dy[direction]
                x_check = x + continuous*dx[direction]

                # 돌을 카운팅 할 때, 오목판을 넘어가지 않도록 합니다.
                if (y_check < 0) or (y_check >= self.dimension) \
                     or (x_check < 0) or (x_check >= self.dimension ):
                    break

                # 시작점(y,x)의 돌의 색과 현재 위치의 돌의 색이 다르다면 카운팅을 멈춥니다.
                # 돌이 존재하지 않는다면 카운팅을 멈추지 않습니다.
                if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                    break
                
                # 시작점(y,x)의 돌의 색과 현재 위치의 돌의 색이 같다면 카운팅을 합니다.
                if self.on((y_check, x_check)) == cur_color :
                    count_marker += 1
            
            # 방향별로 최대 거리 3만큼 떨어진 곳까지 존재하는 돌을 조사합니다.
            continuous_marker.append(count_marker)
        
        # 양 끝이 막히지 않았으며, 3개의 돌로 구성된 쌍을 조사합니다.
        # 이와 같은 조건을 갖는 쌍의 수를 저장합니다.
        count_three = 0

        # 돌의 분포 유형을 조사합니다. 한 쌍의 구성은 다음과 같습니다.
        # (가로/기울기 1 대각선/세로/기울기 -1 대각선) : (음의 방향에 놓인 돌의 수 / 중앙의 돌 / 양의 방향에 놓인 돌의 수) : 연속여부
        # 유형 1 -->  (가로/기울기 1 대각선/세로/기울기 -1 대각선)  : (2/1/0) : 연속
        # 유형 2 -->  (가로/기울기 1 대각선/세로/기울기 -1 대각선)  : (2/1/0) : 불연속
        # 유형 3 -->  (가로/기울기 1 대각선/세로/기울기 -1 대각선)  : (1/1/1) : 불연속
        # 유형 4 -->  (가로/기울기 1 대각선/세로/기울기 -1 대각선)  : (1/1/1) : 불연속
        # 유형 5 -->  (가로/기울기 1 대각선/세로/기울기 -1 대각선)  : (1/1/1) : 연속
        # 유형 6 -->  (가로/기울기 1 대각선/세로/기울기 -1 대각선)  : (0/1/2) : 연속
        # 유형 7 -->  (가로/기울기 1 대각선/세로/기울기 -1 대각선)  : (0/1/2) : 불연속

        # 유형을 저장하는 변수
        three_direction = 0

        for direction in range(4):

            if continuous_marker[direction] == 0 and continuous_marker[direction+4]==2 :
                y_check_side1 = y + dy[direction]
                x_check_side1 = x + dx[direction]
                y_check_side2 = y + 3*dy[direction+4]
                x_check_side2 = x + 3*dx[direction+4]
                y_check_side3 = y + 4*dy[direction+4]
                x_check_side3 = x + 4*dx[direction+4]

                if self.on((y_check_side1, x_check_side1)) == '.':
                    if self.on((y_check_side2, x_check_side2)) == '.':
                        #print("연속된 3으로 양 쪽이 뚤려있네요")
                        count_three += 1
                        three_direction = direction*10 + 1
                    elif self.on((y_check_side3, x_check_side3)) == '.':
                        #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                        count_three += 1
                        three_direction = direction*10 + 2
                       
            elif continuous_marker[direction] == 1 and continuous_marker[direction+4]==1 :
                y_check_side0 = y + 3*dy[direction]
                x_check_side0 = x + 3*dx[direction]
                y_check_side1 = y + 2*dy[direction]
                x_check_side1 = x + 2*dx[direction]
                y_check_side2 = y + 1*dy[direction]
                x_check_side2 = x + 1*dx[direction]
                y_check_side3 = y + 1*dy[direction+4]
                x_check_side3 = x + 1*dx[direction+4]
                y_check_side4 = y + 2*dy[direction+4]
                x_check_side4 = x + 2*dx[direction+4]
                y_check_side5 = y + 3*dy[direction+4]
                x_check_side5 = x + 3*dx[direction+4]
                if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                    flag = 0
                elif self.on((y_check_side1, x_check_side1)) == cur_color:
                    if self.on((y_check_side3, x_check_side3)) == cur_color:
                        #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                        count_three += 1
                        three_direction = direction*10 + 3
                    else :
                        flag = 0
                else:
                    if self.on((y_check_side4, x_check_side4)) == cur_color:
                        #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                        count_three += 1
                        three_direction = direction*10 +4
                    else:
                        #print("연속된 3으로 양 쪽이 뚤려있네요")
                        count_three += 1
                        three_direction = direction*10 +5
                        
                                 
            elif continuous_marker[direction] == 2 and continuous_marker[direction+4]==0 :
                y_check_side1 = y + dy[direction+4]
                x_check_side1 = x + dx[direction+4]
                y_check_side2 = y + 3*dy[direction]
                x_check_side2 = x + 3*dx[direction]
                y_check_side3 = y + 4*dy[direction]
                x_check_side3 = x + 4*dx[direction]

                if self.on((y_check_side1, x_check_side1)) == '.':
                    if self.on((y_check_side2, x_check_side2)) == '.':
                        #print("연속된 3으로 양 쪽이 뚤려있네요")
                        count_three += 1
                        three_direction = direction*10 +6
                    elif self.on((y_check_side3, x_check_side3)) == '.':
                        #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                        count_three += 1
                        three_direction = direction*10+7
                    
                                                       
        # 양 끝이 막히지 않은 쌍이 2개 이상 존재한다면
        if count_three > 1 :
            print("플레이어 {}의 쌍삼입니다!".format(player.get_player()))
            self.board[(coordinate[0], coordinate[1])] = '.'
            return True
        # 양 끝이 막히지 않은 쌍이 존재하지 않는다면
        elif count_three == 0 :
            return False

        # 양 끝이 막히지 않은 쌍이 하나 존재한다면
        # 쌍을 이루는 모든 돌에 대해 또 다른 쌍이 존재하는지 확인해야합니다.
        # 확인과정은 위와 동일합니다.

        # 연속의 방향에 대한 변수 (0:가로 / 1: 기울기 1인 대각선 / 2: 세로 / 3:기울기 -1인 대각선)
        direct = int(three_direction/10)

        # 유형 정보를 저장하는 변수
        dist = three_direction%10
        
        # 유형 1을 구성하는 돌들에 대해 다른 쌍이 존재하는지 확인합니다.
        if dist == 1:
            for i in range(1,3):
                continuous_marker_nested = []
                y_check_side0_n = y + i*dy[direct+4]
                x_check_side0_n = x + i*dx[direct+4]

                for direction in range(8):
                    count_marker = 0
                    for continuous in range(1,4):
                        
                        y_check = y_check_side0_n + continuous*dy[direction]
                        x_check = x_check_side0_n + continuous*dx[direction]

                        if (y_check < 0) or (y_check >= self.dimension) \
                            or (x_check < 0) or (x_check >= self.dimension ):
                            break

                        if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                            break

                        if self.on((y_check, x_check)) == cur_color :
                            count_marker += 1
                    
                    continuous_marker_nested.append(count_marker)
                
                for direction in range(4):

                    if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                        y_check_side1 = y_check_side0_n + dy[direction]
                        x_check_side1 = x_check_side0_n + dx[direction]
                        y_check_side2 = y_check_side0_n + 3*dy[direction+4]
                        x_check_side2 = x_check_side0_n + 3*dx[direction+4]
                        y_check_side3 = y_check_side0_n + 4*dy[direction+4]
                        x_check_side3 = x_check_side0_n + 4*dx[direction+4]

                        if self.on((y_check_side1, x_check_side1)) == '.':
                            if self.on((y_check_side2, x_check_side2)) == '.':
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            elif self.on((y_check_side3, x_check_side3)) == '.':
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                        

                            
                    elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                        y_check_side0 = y_check_side0_n + 3*dy[direction]
                        x_check_side0 = x_check_side0_n + 3*dx[direction]
                        y_check_side1 = y_check_side0_n + 2*dy[direction]
                        x_check_side1 = x_check_side0_n + 2*dx[direction]
                        y_check_side2 = y_check_side0_n + 1*dy[direction]
                        x_check_side2 = x_check_side0_n + 1*dx[direction]
                        y_check_side3 = y_check_side0_n + 1*dy[direction+4]
                        x_check_side3 = x_check_side0_n + 1*dx[direction+4]
                        y_check_side4 = y_check_side0_n + 2*dy[direction+4]
                        x_check_side4 = x_check_side0_n + 2*dx[direction+4]
                        y_check_side5 = y_check_side0_n + 3*dy[direction+4]
                        x_check_side5 = x_check_side0_n + 3*dx[direction+4]
                        if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                            flag = 0
                        elif self.on((y_check_side1, x_check_side1)) == cur_color:
                            if self.on((y_check_side3, x_check_side3)) == cur_color:
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            else :
                                flag = 0
                        else:
                            if self.on((y_check_side4, x_check_side4)) == cur_color:
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            else:
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                                
                

                    elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                        y_check_side1 = y_check_side0_n + dy[direction+4]
                        x_check_side1 = x_check_side0_n + dx[direction+4]
                        y_check_side2 = y_check_side0_n + 3*dy[direction]
                        x_check_side2 = x_check_side0_n + 3*dx[direction]
                        y_check_side3 = y_check_side0_n + 4*dy[direction]
                        x_check_side3 = x_check_side0_n + 4*dx[direction]

                        if self.on((y_check_side1, x_check_side1)) == '.':
                            if self.on((y_check_side2, x_check_side2)) == '.':
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            elif self.on((y_check_side3, x_check_side3)) == '.':
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1

        # 유형 2을 구성하는 돌들에 대해 다른 쌍이 존재하는지 확인합니다.
        elif dist == 2:
            for i in range(1,4):
                continuous_marker_nested = []
                y_check_side0_n = y + i*dy[direct+4]
                x_check_side0_n = x + i*dx[direct+4]

                for direction in range(8):
                    count_marker = 0
                    for continuous in range(1,4):
                        
                        y_check = y_check_side0_n + continuous*dy[direction]
                        x_check = x_check_side0_n + continuous*dx[direction]

                        if (y_check < 0) or (y_check >= self.dimension) \
                            or (x_check < 0) or (x_check >= self.dimension ):
                            break

                        if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                            break

                        if self.on((y_check, x_check)) == cur_color :
                            count_marker += 1
                    
                    continuous_marker_nested.append(count_marker)
                
                for direction in range(4):

                    if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                        y_check_side1 = y_check_side0_n + dy[direction]
                        x_check_side1 = x_check_side0_n + dx[direction]
                        y_check_side2 = y_check_side0_n + 3*dy[direction+4]
                        x_check_side2 = x_check_side0_n + 3*dx[direction+4]
                        y_check_side3 = y_check_side0_n + 4*dy[direction+4]
                        x_check_side3 = x_check_side0_n + 4*dx[direction+4]

                        if self.on((y_check_side1, x_check_side1)) == '.':
                            if self.on((y_check_side2, x_check_side2)) == '.':
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            elif self.on((y_check_side3, x_check_side3)) == '.':
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                        

                            
                    elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                        y_check_side0 = y_check_side0_n + 3*dy[direction]
                        x_check_side0 = x_check_side0_n + 3*dx[direction]
                        y_check_side1 = y_check_side0_n + 2*dy[direction]
                        x_check_side1 = x_check_side0_n + 2*dx[direction]
                        y_check_side2 = y_check_side0_n + 1*dy[direction]
                        x_check_side2 = x_check_side0_n + 1*dx[direction]
                        y_check_side3 = y_check_side0_n + 1*dy[direction+4]
                        x_check_side3 = x_check_side0_n + 1*dx[direction+4]
                        y_check_side4 = y_check_side0_n + 2*dy[direction+4]
                        x_check_side4 = x_check_side0_n + 2*dx[direction+4]
                        y_check_side5 = y_check_side0_n + 3*dy[direction+4]
                        x_check_side5 = x_check_side0_n + 3*dx[direction+4]
                        if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                            #print("삼이 아닙니다")
                            flag = 0
                        elif self.on((y_check_side1, x_check_side1)) == cur_color:
                            if self.on((y_check_side3, x_check_side3)) == cur_color:
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            else :
                                #print("삼이 아닙니다.")
                                flag = 0
                        else:
                            if self.on((y_check_side4, x_check_side4)) == cur_color:
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            else:
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                                
                

                    elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                        y_check_side1 = y_check_side0_n + dy[direction+4]
                        x_check_side1 = x_check_side0_n + dx[direction+4]
                        y_check_side2 = y_check_side0_n + 3*dy[direction]
                        x_check_side2 = x_check_side0_n + 3*dx[direction]
                        y_check_side3 = y_check_side0_n + 4*dy[direction]
                        x_check_side3 = x_check_side0_n + 4*dx[direction]

                        if self.on((y_check_side1, x_check_side1)) == '.':
                            if self.on((y_check_side2, x_check_side2)) == '.':
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            elif self.on((y_check_side3, x_check_side3)) == '.':
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
       
        # 유형 3을 구성하는 돌들에 대해 다른 쌍이 존재하는지 확인합니다.
        elif dist == 3:
            continuous_marker_nested = []
            y_check_side0_n = y + 2*dy[direct]
            x_check_side0_n = x + 2*dx[direct]
            for direction in range(8):
                count_marker = 0
                for continuous in range(1,4):
                    
                    y_check = y_check_side0_n + continuous*dy[direction]
                    x_check = x_check_side0_n + continuous*dx[direction]

                    if (y_check < 0) or (y_check >= self.dimension) \
                        or (x_check < 0) or (x_check >= self.dimension ):
                        break

                    if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                        break

                    if self.on((y_check, x_check)) == cur_color :
                        count_marker += 1
                
                continuous_marker_nested.append(count_marker)

            for direction in range(4):

                if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                    y_check_side1 = y_check_side0_n + dy[direction]
                    x_check_side1 = x_check_side0_n + dx[direction]
                    y_check_side2 = y_check_side0_n + 3*dy[direction+4]
                    x_check_side2 = x_check_side0_n + 3*dx[direction+4]
                    y_check_side3 = y_check_side0_n + 4*dy[direction+4]
                    x_check_side3 = x_check_side0_n + 4*dx[direction+4]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                    

                        
                elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                    y_check_side0 = y_check_side0_n + 3*dy[direction]
                    x_check_side0 = x_check_side0_n + 3*dx[direction]
                    y_check_side1 = y_check_side0_n + 2*dy[direction]
                    x_check_side1 = x_check_side0_n + 2*dx[direction]
                    y_check_side2 = y_check_side0_n + 1*dy[direction]
                    x_check_side2 = x_check_side0_n + 1*dx[direction]
                    y_check_side3 = y_check_side0_n + 1*dy[direction+4]
                    x_check_side3 = x_check_side0_n + 1*dx[direction+4]
                    y_check_side4 = y_check_side0_n + 2*dy[direction+4]
                    x_check_side4 = x_check_side0_n + 2*dx[direction+4]
                    y_check_side5 = y_check_side0_n + 3*dy[direction+4]
                    x_check_side5 = x_check_side0_n + 3*dx[direction+4]
                    if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                        #print("삼이 아닙니다")
                        flag = 0
                    elif self.on((y_check_side1, x_check_side1)) == cur_color:
                        if self.on((y_check_side3, x_check_side3)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else :
                            #print("삼이 아닙니다.")
                            flag = 0
                    else:
                        if self.on((y_check_side4, x_check_side4)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else:
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                            
            

                elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                    y_check_side1 = y_check_side0_n + dy[direction+4]
                    x_check_side1 = x_check_side0_n + dx[direction+4]
                    y_check_side2 = y_check_side0_n + 3*dy[direction]
                    x_check_side2 = x_check_side0_n + 3*dx[direction]
                    y_check_side3 = y_check_side0_n + 4*dy[direction]
                    x_check_side3 = x_check_side0_n + 4*dx[direction]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1


            continuous_marker_nested = []
            y_check_side1_n = y + 1*dy[direct+4]
            x_check_side1_n = x + 1*dx[direct+4]

            for direction in range(8):
                count_marker = 0
                for continuous in range(1,4):
                    
                    y_check = y_check_side1_n + continuous*dy[direction]
                    x_check = x_check_side1_n + continuous*dx[direction]

                    if (y_check < 0) or (y_check >= self.dimension) \
                        or (x_check < 0) or (x_check >= self.dimension ):
                        break

                    if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                        break

                    if self.on((y_check, x_check)) == cur_color :
                        count_marker += 1
                
                continuous_marker_nested.append(count_marker)
            
            for direction in range(4):

                if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                    y_check_side1 = y_check_side1_n + dy[direction]
                    x_check_side1 = x_check_side1_n + dx[direction]
                    y_check_side2 = y_check_side1_n + 3*dy[direction+4]
                    x_check_side2 = x_check_side1_n + 3*dx[direction+4]
                    y_check_side3 = y_check_side1_n + 4*dy[direction+4]
                    x_check_side3 = x_check_side1_n + 4*dx[direction+4]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                    

                        
                elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                    y_check_side0 = y_check_side1_n + 3*dy[direction]
                    x_check_side0 = x_check_side1_n + 3*dx[direction]
                    y_check_side1 = y_check_side1_n + 2*dy[direction]
                    x_check_side1 = x_check_side1_n + 2*dx[direction]
                    y_check_side2 = y_check_side1_n + 1*dy[direction]
                    x_check_side2 = x_check_side1_n + 1*dx[direction]
                    y_check_side3 = y_check_side1_n + 1*dy[direction+4]
                    x_check_side3 = x_check_side1_n + 1*dx[direction+4]
                    y_check_side4 = y_check_side1_n + 2*dy[direction+4]
                    x_check_side4 = x_check_side1_n + 2*dx[direction+4]
                    y_check_side5 = y_check_side1_n + 3*dy[direction+4]
                    x_check_side5 = x_check_side1_n + 3*dx[direction+4]
                    if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                        #print("삼이 아닙니다")
                        flag = 0
                    elif self.on((y_check_side1, x_check_side1)) == cur_color:
                        if self.on((y_check_side3, x_check_side3)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else :
                            #print("삼이 아닙니다.")
                            flag = 0
                    else:
                        if self.on((y_check_side4, x_check_side4)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else:
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                            
            

                elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                    y_check_side1 = y_check_side1_n + dy[direction+4]
                    x_check_side1 = x_check_side1_n + dx[direction+4]
                    y_check_side2 = y_check_side1_n + 3*dy[direction]
                    x_check_side2 = x_check_side1_n + 3*dx[direction]
                    y_check_side3 = y_check_side1_n + 4*dy[direction]
                    x_check_side3 = x_check_side1_n + 4*dx[direction]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1

        # 유형 4을 구성하는 돌들에 대해 다른 쌍이 존재하는지 확인합니다.
        elif dist == 4:
            continuous_marker_nested = []
            y_check_side0_n = y + 1*dy[direct]
            x_check_side0_n = x + 1*dx[direct]

            for direction in range(8):
                count_marker = 0
                for continuous in range(1,4):
                    
                    y_check = y_check_side0_n + continuous*dy[direction]
                    x_check = x_check_side0_n + continuous*dx[direction]

                    if (y_check < 0) or (y_check >= self.dimension) \
                        or (x_check < 0) or (x_check >= self.dimension ):
                        break

                    if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                        break

                    if self.on((y_check, x_check)) == cur_color :
                        count_marker += 1
                

                continuous_marker_nested.append(count_marker)


            for direction in range(4):

                if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                    y_check_side1 = y_check_side0_n + dy[direction]
                    x_check_side1 = x_check_side0_n + dx[direction]
                    y_check_side2 = y_check_side0_n + 3*dy[direction+4]
                    x_check_side2 = x_check_side0_n + 3*dx[direction+4]
                    y_check_side3 = y_check_side0_n + 4*dy[direction+4]
                    x_check_side3 = x_check_side0_n + 4*dx[direction+4]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                    

                        
                elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                    y_check_side0 = y_check_side0_n + 3*dy[direction]
                    x_check_side0 = x_check_side0_n + 3*dx[direction]
                    y_check_side1 = y_check_side0_n + 2*dy[direction]
                    x_check_side1 = x_check_side0_n + 2*dx[direction]
                    y_check_side2 = y_check_side0_n + 1*dy[direction]
                    x_check_side2 = x_check_side0_n + 1*dx[direction]
                    y_check_side3 = y_check_side0_n + 1*dy[direction+4]
                    x_check_side3 = x_check_side0_n + 1*dx[direction+4]
                    y_check_side4 = y_check_side0_n + 2*dy[direction+4]
                    x_check_side4 = x_check_side0_n + 2*dx[direction+4]
                    y_check_side5 = y_check_side0_n + 3*dy[direction+4]
                    x_check_side5 = x_check_side0_n + 3*dx[direction+4]
                    if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                        #print("삼이 아닙니다")
                        flag = 0
                    elif self.on((y_check_side1, x_check_side1)) == cur_color:
                        if self.on((y_check_side3, x_check_side3)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else :
                            #print("삼이 아닙니다.")
                            flag = 0
                    else:
                        if self.on((y_check_side4, x_check_side4)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else:
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                            
            

                elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                    y_check_side1 = y_check_side0_n + dy[direction+4]
                    x_check_side1 = x_check_side0_n + dx[direction+4]
                    y_check_side2 = y_check_side0_n + 3*dy[direction]
                    x_check_side2 = x_check_side0_n + 3*dx[direction]
                    y_check_side3 = y_check_side0_n + 4*dy[direction]
                    x_check_side3 = x_check_side0_n + 4*dx[direction]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1


            continuous_marker_nested = []
            y_check_side1_n = y + 2*dy[direct+4]
            x_check_side1_n = x + 2*dx[direct+4]

            for direction in range(8):
                count_marker = 0
                for continuous in range(1,4):
                    
                    y_check = y_check_side1_n + continuous*dy[direction]
                    x_check = x_check_side1_n + continuous*dx[direction]

                    if (y_check < 0) or (y_check >= self.dimension) \
                        or (x_check < 0) or (x_check >= self.dimension ):
                        break

                    if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                        break

                    if self.on((y_check, x_check)) == cur_color :
                        count_marker += 1
                
                continuous_marker_nested.append(count_marker)
            
            for direction in range(4):

                if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                    y_check_side1 = y_check_side1_n + dy[direction]
                    x_check_side1 = x_check_side1_n + dx[direction]
                    y_check_side2 = y_check_side1_n + 3*dy[direction+4]
                    x_check_side2 = x_check_side1_n + 3*dx[direction+4]
                    y_check_side3 = y_check_side1_n + 4*dy[direction+4]
                    x_check_side3 = x_check_side1_n + 4*dx[direction+4]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                    

                        
                elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                    y_check_side0 = y_check_side1_n + 3*dy[direction]
                    x_check_side0 = x_check_side1_n + 3*dx[direction]
                    y_check_side1 = y_check_side1_n + 2*dy[direction]
                    x_check_side1 = x_check_side1_n + 2*dx[direction]
                    y_check_side2 = y_check_side1_n + 1*dy[direction]
                    x_check_side2 = x_check_side1_n + 1*dx[direction]
                    y_check_side3 = y_check_side1_n + 1*dy[direction+4]
                    x_check_side3 = x_check_side1_n + 1*dx[direction+4]
                    y_check_side4 = y_check_side1_n + 2*dy[direction+4]
                    x_check_side4 = x_check_side1_n + 2*dx[direction+4]
                    y_check_side5 = y_check_side1_n + 3*dy[direction+4]
                    x_check_side5 = x_check_side1_n + 3*dx[direction+4]
                    if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                        #print("삼이 아닙니다")
                        flag = 0
                    elif self.on((y_check_side1, x_check_side1)) == cur_color:
                        if self.on((y_check_side3, x_check_side3)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else :
                            #print("삼이 아닙니다.")
                            flag = 0
                    else:
                        if self.on((y_check_side4, x_check_side4)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else:
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                            
            

                elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                    y_check_side1 = y_check_side1_n + dy[direction+4]
                    x_check_side1 = x_check_side1_n + dx[direction+4]
                    y_check_side2 = y_check_side1_n + 3*dy[direction]
                    x_check_side2 = x_check_side1_n + 3*dx[direction]
                    y_check_side3 = y_check_side1_n + 4*dy[direction]
                    x_check_side3 = x_check_side1_n + 4*dx[direction]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1

        # 유형 5을 구성하는 돌들에 대해 다른 쌍이 존재하는지 확인합니다.
        elif dist == 5:
            continuous_marker_nested = []
            y_check_side0_n = y + 1*dy[direct]
            x_check_side0_n = x + 1*dx[direct]

            for direction in range(8):
                count_marker = 0
                for continuous in range(1,4):
                    
                    y_check = y_check_side0_n + continuous*dy[direction]
                    x_check = x_check_side0_n + continuous*dx[direction]

                    if (y_check < 0) or (y_check >= self.dimension) \
                        or (x_check < 0) or (x_check >= self.dimension ):
                        break

                    if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                        break

                    if self.on((y_check, x_check)) == cur_color :
                        count_marker += 1
                
                continuous_marker_nested.append(count_marker)

            for direction in range(4):

                if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                    y_check_side1 = y_check_side0_n + dy[direction]
                    x_check_side1 = x_check_side0_n + dx[direction]
                    y_check_side2 = y_check_side0_n + 3*dy[direction+4]
                    x_check_side2 = x_check_side0_n + 3*dx[direction+4]
                    y_check_side3 = y_check_side0_n + 4*dy[direction+4]
                    x_check_side3 = x_check_side0_n + 4*dx[direction+4]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                    

                        
                elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                    y_check_side0 = y_check_side0_n + 3*dy[direction]
                    x_check_side0 = x_check_side0_n + 3*dx[direction]
                    y_check_side1 = y_check_side0_n + 2*dy[direction]
                    x_check_side1 = x_check_side0_n + 2*dx[direction]
                    y_check_side2 = y_check_side0_n + 1*dy[direction]
                    x_check_side2 = x_check_side0_n + 1*dx[direction]
                    y_check_side3 = y_check_side0_n + 1*dy[direction+4]
                    x_check_side3 = x_check_side0_n + 1*dx[direction+4]
                    y_check_side4 = y_check_side0_n + 2*dy[direction+4]
                    x_check_side4 = x_check_side0_n + 2*dx[direction+4]
                    y_check_side5 = y_check_side0_n + 3*dy[direction+4]
                    x_check_side5 = x_check_side0_n + 3*dx[direction+4]
                    if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                        #print("삼이 아닙니다")
                        flag = 0
                    elif self.on((y_check_side1, x_check_side1)) == cur_color:
                        if self.on((y_check_side3, x_check_side3)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else :
                            #print("삼이 아닙니다.")
                            flag = 0
                    else:
                        if self.on((y_check_side4, x_check_side4)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else:
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                            
            

                elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                    y_check_side1 = y_check_side0_n + dy[direction+4]
                    x_check_side1 = x_check_side0_n + dx[direction+4]
                    y_check_side2 = y_check_side0_n + 3*dy[direction]
                    x_check_side2 = x_check_side0_n + 3*dx[direction]
                    y_check_side3 = y_check_side0_n + 4*dy[direction]
                    x_check_side3 = x_check_side0_n + 4*dx[direction]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1



            continuous_marker_nested = []
            y_check_side1_n = y + 1*dy[direct+4]
            x_check_side1_n = x + 1*dx[direct+4]
            for direction in range(8):
                count_marker = 0
                for continuous in range(1,4):
                    
                    y_check = y_check_side1_n + continuous*dy[direction]
                    x_check = x_check_side1_n + continuous*dx[direction]

                    if (y_check < 0) or (y_check >= self.dimension) \
                        or (x_check < 0) or (x_check >= self.dimension ):
                        break

                    if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                        break

                    if self.on((y_check, x_check)) == cur_color :
                        count_marker += 1
                
                continuous_marker_nested.append(count_marker)
            
            for direction in range(4):

                if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                    y_check_side1 = y_check_side1_n + dy[direction]
                    x_check_side1 = x_check_side1_n + dx[direction]
                    y_check_side2 = y_check_side1_n + 3*dy[direction+4]
                    x_check_side2 = x_check_side1_n + 3*dx[direction+4]
                    y_check_side3 = y_check_side1_n + 4*dy[direction+4]
                    x_check_side3 = x_check_side1_n + 4*dx[direction+4]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                    

                        
                elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                    y_check_side0 = y_check_side1_n + 3*dy[direction]
                    x_check_side0 = x_check_side1_n + 3*dx[direction]
                    y_check_side1 = y_check_side1_n + 2*dy[direction]
                    x_check_side1 = x_check_side1_n + 2*dx[direction]
                    y_check_side2 = y_check_side1_n + 1*dy[direction]
                    x_check_side2 = x_check_side1_n + 1*dx[direction]
                    y_check_side3 = y_check_side1_n + 1*dy[direction+4]
                    x_check_side3 = x_check_side1_n + 1*dx[direction+4]
                    y_check_side4 = y_check_side1_n + 2*dy[direction+4]
                    x_check_side4 = x_check_side1_n + 2*dx[direction+4]
                    y_check_side5 = y_check_side1_n + 3*dy[direction+4]
                    x_check_side5 = x_check_side1_n + 3*dx[direction+4]
                    if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                        #print("삼이 아닙니다")
                        flag = 0
                    elif self.on((y_check_side1, x_check_side1)) == cur_color:
                        if self.on((y_check_side3, x_check_side3)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else :
                            #print("삼이 아닙니다.")
                            flag = 0
                    else:
                        if self.on((y_check_side4, x_check_side4)) == cur_color:
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        else:
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                            
            

                elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                    y_check_side1 = y_check_side1_n + dy[direction+4]
                    x_check_side1 = x_check_side1_n + dx[direction+4]
                    y_check_side2 = y_check_side1_n + 3*dy[direction]
                    x_check_side2 = x_check_side1_n + 3*dx[direction]
                    y_check_side3 = y_check_side1_n + 4*dy[direction]
                    x_check_side3 = x_check_side1_n + 4*dx[direction]

                    if self.on((y_check_side1, x_check_side1)) == '.':
                        if self.on((y_check_side2, x_check_side2)) == '.':
                            #print("연속된 3으로 양 쪽이 뚤려있네요")
                            count_three += 1
                        elif self.on((y_check_side3, x_check_side3)) == '.':
                            #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                            count_three += 1

        # 유형 6을 구성하는 돌들에 대해 다른 쌍이 존재하는지 확인합니다.
        elif dist == 6:
            for i in range (1,3):
                continuous_marker_nested = []
                y_check_side0_n = y + i*dy[direct]
                x_check_side0_n = x + i*dx[direct]

                for direction in range(8):
                    count_marker = 0
                    for continuous in range(1,4):
                        
                        y_check = y_check_side0_n + continuous*dy[direction]
                        x_check = x_check_side0_n + continuous*dx[direction]

                        if (y_check < 0) or (y_check >= self.dimension) \
                            or (x_check < 0) or (x_check >= self.dimension ):
                            break

                        if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                            break

                        if self.on((y_check, x_check)) == cur_color :
                            count_marker += 1
                    
                    continuous_marker_nested.append(count_marker)
                

                for direction in range(4):

                    if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                        y_check_side1 = y_check_side0_n + dy[direction]
                        x_check_side1 = x_check_side0_n + dx[direction]
                        y_check_side2 = y_check_side0_n + 3*dy[direction+4]
                        x_check_side2 = x_check_side0_n + 3*dx[direction+4]
                        y_check_side3 = y_check_side0_n + 4*dy[direction+4]
                        x_check_side3 = x_check_side0_n + 4*dx[direction+4]

                        if self.on((y_check_side1, x_check_side1)) == '.':
                            if self.on((y_check_side2, x_check_side2)) == '.':
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            elif self.on((y_check_side3, x_check_side3)) == '.':
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                        

                            
                    elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                        y_check_side0 = y_check_side0_n + 3*dy[direction]
                        x_check_side0 = x_check_side0_n + 3*dx[direction]
                        y_check_side1 = y_check_side0_n + 2*dy[direction]
                        x_check_side1 = x_check_side0_n + 2*dx[direction]
                        y_check_side2 = y_check_side0_n + 1*dy[direction]
                        x_check_side2 = x_check_side0_n + 1*dx[direction]
                        y_check_side3 = y_check_side0_n + 1*dy[direction+4]
                        x_check_side3 = x_check_side0_n + 1*dx[direction+4]
                        y_check_side4 = y_check_side0_n + 2*dy[direction+4]
                        x_check_side4 = x_check_side0_n + 2*dx[direction+4]
                        y_check_side5 = y_check_side0_n + 3*dy[direction+4]
                        x_check_side5 = x_check_side0_n + 3*dx[direction+4]
                        if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                            #print("삼이 아닙니다")
                            flag = 0
                        elif self.on((y_check_side1, x_check_side1)) == cur_color:
                            if self.on((y_check_side3, x_check_side3)) == cur_color:
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            else :
                                #print("삼이 아닙니다.")
                                flag = 0
                        else:
                            if self.on((y_check_side4, x_check_side4)) == cur_color:
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            else:
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                                
                

                    elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                        y_check_side1 = y_check_side0_n + dy[direction+4]
                        x_check_side1 = x_check_side0_n + dx[direction+4]
                        y_check_side2 = y_check_side0_n + 3*dy[direction]
                        x_check_side2 = x_check_side0_n + 3*dx[direction]
                        y_check_side3 = y_check_side0_n + 4*dy[direction]
                        x_check_side3 = x_check_side0_n + 4*dx[direction]

                        if self.on((y_check_side1, x_check_side1)) == '.':
                            if self.on((y_check_side2, x_check_side2)) == '.':
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            elif self.on((y_check_side3, x_check_side3)) == '.':
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1

        # 유형 7을 구성하는 돌들에 대해 다른 쌍이 존재하는지 확인합니다.   
        elif dist == 7:
            for i in range (1,4):
                continuous_marker_nested = []
                y_check_side0_n = y + i*dy[direct]
                x_check_side0_n = x + i*dx[direct]

                for direction in range(8):
                    count_marker = 0
                    for continuous in range(1,4):
                        
                        y_check = y_check_side0_n + continuous*dy[direction]
                        x_check = x_check_side0_n + continuous*dx[direction]

                        if (y_check < 0) or (y_check >= self.dimension) \
                            or (x_check < 0) or (x_check >= self.dimension ):
                            break

                        if self.on((y_check, x_check)) != cur_color and self.on((y_check, x_check)) != '.':
                            break

                        if self.on((y_check, x_check)) == cur_color :
                            count_marker += 1
                    
                    continuous_marker_nested.append(count_marker)
                
                for direction in range(4):

                    if continuous_marker_nested[direction] == 0 and continuous_marker_nested[direction+4]==2 :
                        y_check_side1 = y_check_side0_n + dy[direction]
                        x_check_side1 = x_check_side0_n + dx[direction]
                        y_check_side2 = y_check_side0_n + 3*dy[direction+4]
                        x_check_side2 = x_check_side0_n + 3*dx[direction+4]
                        y_check_side3 = y_check_side0_n + 4*dy[direction+4]
                        x_check_side3 = x_check_side0_n + 4*dx[direction+4]

                        if self.on((y_check_side1, x_check_side1)) == '.':
                            if self.on((y_check_side2, x_check_side2)) == '.':
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            elif self.on((y_check_side3, x_check_side3)) == '.':
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                        

                            
                    elif continuous_marker_nested[direction] == 1 and continuous_marker_nested[direction+4]==1 :
                        y_check_side0 = y_check_side0_n + 3*dy[direction]
                        x_check_side0 = x_check_side0_n + 3*dx[direction]
                        y_check_side1 = y_check_side0_n + 2*dy[direction]
                        x_check_side1 = x_check_side0_n + 2*dx[direction]
                        y_check_side2 = y_check_side0_n + 1*dy[direction]
                        x_check_side2 = x_check_side0_n + 1*dx[direction]
                        y_check_side3 = y_check_side0_n + 1*dy[direction+4]
                        x_check_side3 = x_check_side0_n + 1*dx[direction+4]
                        y_check_side4 = y_check_side0_n + 2*dy[direction+4]
                        x_check_side4 = x_check_side0_n + 2*dx[direction+4]
                        y_check_side5 = y_check_side0_n + 3*dy[direction+4]
                        x_check_side5 = x_check_side0_n + 3*dx[direction+4]
                        if self.on((y_check_side0, x_check_side0)) == cur_color or self.on((y_check_side5, x_check_side5)) == cur_color:
                            #print("삼이 아닙니다")
                            flag = 0
                        elif self.on((y_check_side1, x_check_side1)) == cur_color:
                            if self.on((y_check_side3, x_check_side3)) == cur_color:
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            else :
                                #print("삼이 아닙니다.")
                                flag = 0
                        else:
                            if self.on((y_check_side4, x_check_side4)) == cur_color:
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            else:
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                                
                

                    elif continuous_marker_nested[direction] == 2 and continuous_marker_nested[direction+4]==0 :
                        y_check_side1 = y_check_side0_n + dy[direction+4]
                        x_check_side1 = x_check_side0_n + dx[direction+4]
                        y_check_side2 = y_check_side0_n + 3*dy[direction]
                        x_check_side2 = x_check_side0_n + 3*dx[direction]
                        y_check_side3 = y_check_side0_n + 4*dy[direction]
                        x_check_side3 = x_check_side0_n + 4*dx[direction]

                        if self.on((y_check_side1, x_check_side1)) == '.':
                            if self.on((y_check_side2, x_check_side2)) == '.':
                                #print("연속된 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
                            elif self.on((y_check_side3, x_check_side3)) == '.':
                                #print("띄엄띄엄 3으로 양 쪽이 뚤려있네요")
                                count_three += 1
        
        # 한 쌍을 구성하는 모든 돌에 대해 조사한 결과이므로, direct 방향에 대해 중복된 수가 있습니다.
        # 따라서 count_three는 한 쌍을 구성하는 돌의 수인 3보다 커야 쌍삼의 조건이 성립합니다.
        if count_three > 3 :
            print("플레이어 {}의 쌍삼입니다!".format(player.get_player()))
            self.board[(coordinate[0], coordinate[1])] = '.'
            return True
        else:
            return False




  

    















