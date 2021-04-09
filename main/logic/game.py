

class Game:
    players = []
    player_turn = 0

    def __init__(self):
        self.matrix = [["" for x in range(3)] for j in range(3)]
        self.players = []
        self.player_turn = 0
        self.game_over = False
        self.victory = ""

    def add_player(self, player):
        if(len(self.players) == 2):
            return ""
        else:
            self.players += [player]
            if len(self.players) == 1:
                return "X"
            else:
                return "O"

    def remove_player(self, player):
        for i in range(len(self.players)):
            if self.players[i] == player:
                self.players = self.players[:i] + self.players[i+1:]
                break

    def check_game_over(self):
        conditions = []
        conditions += [[[0,0], [0, 1], [0, 2]]]
        conditions += [[[1,0], [1, 1], [1, 2]]]
        conditions += [[[2,0], [2, 1], [2, 2]]]

        conditions += [[[0,0], [1, 0], [2, 0]]]
        conditions += [[[0,1], [1, 1], [2, 1]]]
        conditions += [[[0,2], [1, 2], [2, 2]]]

        conditions += [[[0,0], [1, 1], [2, 2]]]
        conditions += [[[0,2], [1, 1], [2, 0]]]

        game_end = False
        value = ""
        for condition in conditions:
            value = self.matrix[condition[0][0]][condition[0][1]]
            if value == "":
                continue
            _game_end = True
            for i in range(1, 3):
                if self.matrix[condition[i][0]][condition[i][1]] != value:
                    _game_end = False
                    break
            if _game_end:
                game_end = True
                break
            
        if value == "X":
            self.victory = self.players[0]
        elif value == "O":
            self.victory = self.players[1]

        if not game_end:
            _game_end = True
            for i in range(3):
                for j in range(3):
                    if self.matrix[i][j] == "":
                        _game_end = False
                        break
            if _game_end:
                self.victory = "T"
            game_end = _game_end

        self.game_over = game_end


    def make_move(self, player, i, j):
        if self.game_over:
            return False

        i = int(i)
        j = int(j)
        if(self.matrix[i][j] != ""):
            return False
        if self.players[self.player_turn] != player:
            return False

        if self.player_turn == 0:
            self.matrix[i][j] = "X"
            self.player_turn = 1
        else:
            self.matrix[i][j] = "O"
            self.player_turn = 0

        self.check_game_over()

        return True

    def is_player_victorious(self, player):
        return self.victory == player

    def is_player_turn(self, player):
        if(len(self.players) <= self.player_turn):
            return False
        return self.players[self.player_turn] == player
    
    def get_other_player(self, player):
        if len(self.players) < 2:
            return None
        else:
            if(self.players[0] == player):
                return self.players[1]
            else:
                return self.players[0]

    def status(self, player):
        return {
            'turn': self.is_player_turn(player), 
            'matrix': self.matrix, 
            'gameOver': self.game_over,
            'victory': self.is_player_victorious(player),
            'tie': self.victory == "T"
        }

    def reset(self):
        self.matrix = [["" for x in range(3)] for j in range(3)]
        self.player_turn = 0
        self.game_over = False
        self.victory = ""