import random

class TicTacToeCell():
    '''A TicTacToeCell object contains a given integer value or a player's placement'''
    value: int

    def __init__(self, value):
        '''Initializes the cell with a given integer value.'''
        self.value = int(value)

    def __format__(self, spec):
        if spec:
            return f'{self.value:{spec}}'
        return str(self.value)

    def __bool__(self):
        '''Returns boolean true if cell contains an integer and boolean false if it does not.'''
        return type(self.value) == int
    
    def place(self, turn):
        '''Places the players turn ('x'/'o') on this cell, if it contains an integer.'''
        if self.__bool__:
            self.value = str(turn)
            return True # return True to confirm valid placement
        return self.__bool__
    
    def getValue(self):
        return self.value

class TicTacToeTable():
    '''A TicTacToeTable object is a collection of TicTacToeCell objects arranged in a n x n matrix using a list'''
    table: list
    size: int
    
    def __init__(self, size):
        '''Constructor for TicTacToeTable class.'''
        self.size = size # set size of table
        self.createTable(size) # create table

    def __bool__(self):
        '''Returns a boolean true if table exists and boolean false if table does not exist.'''
        return bool(self.table)
    
    def createTable(self, n):
        '''Creates a n x n table.'''
        self.table = [] # initialize the table list
        for row in range(n):
            rowValues = []
            for cell in range(1, n+1): # change indexing from 0-index to 1-index
                rowValues.append(TicTacToeCell(cell + n * row)) # increments counter: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            self.table.append(rowValues)

    def printTable(self):
        '''Pretty-prints the TicTacToe table.'''
        size = len(self.table)
        header = f" {'_'*((6*size)-1)} \n/{' '*((6*size)-1)}\\"
        seperator = f"|{('-' * 5 + '+')*(size-1)}{'-'*5}|"
        footer = f"\\{'_'*((6*size)-1)}/\n"

        print(header)
        for row in self.table:
            string = ''
            for cell in row:
                string += f"{'|':<2}{cell:>2}{' ':<2}"
            string += '|'
            print(seperator)
            print(string)
        print(seperator)
        print(footer)

    def checkRows(self, player):
        for row in self.table:
            if all([cell.getValue() == player for cell in row]):
                return True
        return False
    
    def checkColumns(self, player):
        columns = [[] for i in range(self.size)] # Creates n amount of empty columns
        for row in self.table:
            index = 0
            for cell in row:
                columns[index].append(cell) # populates columns
                index += 1
        
        for column in columns:
            if all([cell.getValue() == player for cell in column]):
                return True
        return False

    def checkDiagonals(self, player):
        diagonals = [[], []] # only 2 diagonals
        for index, row in enumerate(self.table):
            diagonals[0].append(row[index])
            diagonals[1].append(row[self.size-1-index])
        for diagonal in diagonals:
            if all([cell.getValue() == player for cell in diagonal]):
                return True
        return False
        
    def checkWinConditions(self, player):
        return any([self.checkRows(player), self.checkColumns(player), self.checkDiagonals(player)])

    def translate(self, placement):
        '''Translates the users input to a placement on the board'''
        row = (placement - 1) // len(self.table)
        column = (placement - 1) % len(self.table)
        return row, column

    def getPlacement(self):
        print("Where would you like to place: ", end = '')
        choice = int(input())
        while ((1 > choice) or (choice > self.size**2)): # user must choose between 1 and size², for example between 1-9.
            print("Where would you like to place: ", end = '')
            choice = int(input())
        return self.translate(choice)

    def place(self, player):
        cell: TicTacToeCell
        valid = False
        while not valid:
            row, column = self.getPlacement()
            cell = self.table[row][column]
            valid = bool(cell) # returns True if cell contains an integer, which is a valid cell to place, else False
        cell.place(player)
        return self.checkWinConditions(player)
    
    def robotPlace(self, player):
        validPlacements = []
        for row in self.table:
            for cell in row:
                if cell:
                    validPlacements.append(cell.getValue()) # populate list with available placements (integers)
        placement = random.choice(validPlacements)
        row, column = self.translate(placement) # choose random integer and translate to row, column values
        cell = self.table[row][column] # choose cell from row, column values
        cell.place(player)
        print(f"My turn, and I choose to place {placement}")
        return self.checkWinConditions(player)

class TicTacToeGame():
    PLAYERS = ['x', 'o']
    CONDITIONS = ['x', 'o', 'q'] # 'x' and 'o' are players, 'q' is for quitting
    player: str
    robot: str
    table: TicTacToeTable
    winner: str

    def __init__(self, n = 3):
        '''Constructor for TicTacToe game specifying game size (n x n). Defaulted to 3 x 3.'''
        self.table = TicTacToeTable(n)

    def getChoice(self):
        '''Prompt user for input'''
        print("Choose 'x' (1st), 'o' (2nd) or 'q' to quit: ", end = '')
        return input().lower()

    def setupGame(self, choice):
        if choice not in self.CONDITIONS: # if choice is not 'x', 'o' or 'q'
            while choice not in self.CONDITIONS: # loop until 'x', 'o' or 'q' are chosen
                choice = self.getChoice()
        
        if choice in self.PLAYERS: # if user chose 'x' or 'o'
            self.player = choice # assign choice to player variable
            for turn in self.PLAYERS: # assign other turn to robot
                if turn != self.player: # e.g. player chose 'x', robot gets 'o'
                    self.robot = turn # assign other turn to robot variable

            if bool(self.table) == False: # if player hasn't specified table size
                self.table.createTable() # create a standard 3 x 3 table
            return True
        
        # This code should only be executed if the player quits (chose 'q').
        print("You've quit the game - thanks for playing.")
        return False

    def play(self, choice = ''):
        '''Starts a game of TicTacToe'''
        start = self.setupGame(choice) # user choses 'x', 'o' or 'q'
        if start: # if user chose 'x' or 'q'
            finished = False
            while not finished: # while game is not finished
                for turn in self.PLAYERS: # next turn
                    self.table.printTable()
                    if turn == self.player:
                        finished = self.table.place(self.player)
                    elif turn == self.robot:
                        finished = self.table.robotPlace(self.robot)
                    if finished:
                        self.table.printTable()
                        self.winner = turn
                        break
            print(f'{self.winner} won this round!\n')

if __name__ == '__main__':
    # Variable n determines the size of the table in n x n
    n = 3
    TicTacToeGame(n).play()
