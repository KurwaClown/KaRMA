
class connect4(object):
    def __init__(self):
        self.board = [['⚪']*7]*6
        self.columnDepth = [5]*7
        
    def showBoard(self):
        board = ""
        for row in self.board:
            for column in row:
                board += column +" "
            board += "\n"
        print(board)

    def addToken(self, color, column):
        if color == 'red':
            print(self.columnDepth[column])
            self.board[5][4] = '❎'
            print(self.board)

    