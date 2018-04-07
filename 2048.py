import random as rnd
import os
import sys
#2048 game by yifu chen
#work together with zhitao nie , jingyu shen
#finish in 2018/3/1

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self.list = []
        self._grid = self.createGrid(row,col)    # creates the grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells
        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)


    def createGrid(self,row,col):
        """
        Create the grid here using the arguments row and col
        as the number of rows and columns of the grid to be made.
        
        The function should return the grid to be used in __init__()
        """
        list = []
        for i in range(row):
            list.append([])
            for i1 in range(col):
                list[i].append(0)
        self.list = list
        return list

    def setCell(self, cell, val):
        """
        This function should take two arguments cell and val and assign
        the cell of the grid numbered 'cell' the value in val.
        
        This function does not need to return anything.
        
        You should use this function to change values of the grid.
        """
        self._grid[cell // self.col][cell % self.col] = val


    def getCell(self, cell):
        return self._grid[cell // self.col] [cell % self.col]

    def assignRandCell(self, init=False):
    
        """
        This function assigns a random empty cell of the grid 
        a value of 2 or 4.
        
        In __init__() it only assigns cells the value of 2.
        
        The distribution is set so that 75% of the time the random cell is
        assigned a value of 2 and 25% of the time a random cell is assigned 
        a value of 4
        """
        
        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)


    def drawGrid(self):
    
        """
        This function draws the grid representing the state of the game
        grid
        """
        
        for i in range(self.row):
            line = '\t|'
            for j in range(self.col):
                if not self.getCell((i * self.row) + j):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((i * self.row) + j)).center(5) + '|'
            print(line)
    
    
    def updateEmptiesSet(self):
    
        """
        This function should update the list of empty cells of the grid.
        """
        self.emptiesSet = []
        for cell_number in range(self.row*self.col):
            if self.getCell(cell_number) == 0:
                self.emptiesSet.append(cell_number)
    
    
    def collapsible(self):
        # Check whether there's zero
        for cell in range(self.row * self.col):
            if not self.getCell(cell):
                return True

        # For every cell, check if the cell to the right and the cell below is a
        # duplicate. It's not necessary to check the other two directions because
        # it will be already checked earlier.

        for row in range(self.row):
            for col in range(self.col):
                cell = self.getCell(row * self.col + col)
                if col < self.col - 1 and cell == self.getCell(row * self.col + col + 1):
                    return True
                if row < self.row - 1 and cell == self.getCell((row + 1) * self.col + col):
                    return True
        return False

    def collapseRow(self, lst):
        #delect 0
        #list store no 0 list
        list= []
        new_list = []
        while 0 in lst:
            lst.remove(0)
        list = lst

        count = 0
        judge = False
        jump = False
        for index in range(len(list)):
            #after success on time
            if jump:
                jump = False
                continue

            if index < len(list)-1:
                if list[index] == list[index+1]:
                    new_list.append(list[index]*2)
                    self.score += 2 * list[index]
                    jump = True
                    count += 1
                else:
                    new_list.append(list[index])
                    count +=1
            else:
                new_list.append(list[index])

        #set judge
        if count == 0:
            judge = False
        else:
            judge = True

        #add 0
        while len(new_list) < 4:
            new_list.append(0)
        return new_list,judge


    def collapseLeft(self):
        judge = False

        for row in range(self.row):
            list = []
            for col in range(self.col):
                list.append(self.getCell(row*self.col + col))
            new_list = self.collapseRow(list)[0]
            is_collapsed = self.collapseRow(list)[1]

            if is_collapsed == True:
                judge = True

            for col in range(4):
                self.setCell(row*self.col + col, new_list[col])
        return judge


    def collapseRight(self):
        judge = False
        for row in range(self.row):
            list1 = []
            for col in range(self.col):
                list1.append(self.getCell(row * self.col + col))
            #reverse
            list1 = list(reversed(list1))

            new_list = self.collapseRow(list1)[0]
            is_collapsed = self.collapseRow(list1)[1]

            new_list = list(reversed(new_list))
            if is_collapsed == True:
                judge = True

            for col in range(4):
                self.setCell(row * self.col + col, new_list[col])
        return judge


    def collapseUp(self):

        judge = False
        for col in range(self.col):
            list1 = []
            for row in range(self.row):
                list1.append(self.getCell(row * self.col + col))

            new_list = self.collapseRow(list1)[0]
            is_collapsed = self.collapseRow(list1)[1]

            if is_collapsed == True:
                judge = True

            for row in range(4):
                self.setCell(row * self.col + col, new_list[row])
        return judge



    def collapseDown(self):


        judge = False
        for col in range(self.col):
            list1 = []
            for row in range(self.row):
                list1.append(self.getCell(row * self.col + col))
            # reverse
            list1 = list(reversed(list1))

            new_list = self.collapseRow(list1)[0]
            is_collapsed = self.collapseRow(list1)[1]

            if is_collapsed:
                judge = True

            for row in range(4):
                self.setCell(row * self.col + col, new_list[self.row-1 - row])
        return judge

class Game():
    def __init__(self, row=4, col=4, initial=2):
    
        """
        Creates a game grid and begins the game
        """
        
        self.game = Grid(row, col, initial)
        self.play()
    
    
    def printPrompt(self):
        
        """
        Prints the instructions and the game grid with a move prompt
        """
    
        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")
        
        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))


    def play(self):
    
        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}
        
        stop = False
        collapsible = True
        
        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')
            
            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()
                
                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()
                    
                collapsible = self.game.collapsible()
                 
        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')



def main():
    game = Game()

main()