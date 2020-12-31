class Player(object):

    #####################################################################
    #
    #   플레이어
    #   - init(color)
    #       color를 가진 돌을 사용하는 플레이어를 생성합니다.
    #       player : USER / AI
    #
    #   - set_player(player)
    #       플레이어를 세팅합니다.
    #
    #   - get_player()
    #       플레이어를 반환합니다.
    #
    #####################################################################
    
    def __init__(self, color):
        self.color = color
        self.player = None
    
    def set_player(self, player):
        self.player = player

    def get_player(self):
        return self.player
