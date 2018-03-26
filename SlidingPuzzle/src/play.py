'''
Created on Feb 28, 2018

@author: Andreea
'''
from cmath import sqrt
from pip._vendor.distlib.util import Configurator
from _overlapped import NULL

# -*- coding: utf-8 -*-
"""

For a given puzzle of n x n squares with numbers from 1 to (n x n-1) (one square is
empty) in an initial configuration, find a sequence of movements for the numbers in order to
reach a final given configuration, knowing that a number can move (horizontally or vertically) on
an adjacent empty square. In Figure 7 are presented two examples of puzzles (with the initial
and final configuration).

    
"""

from time import time

class Configuration:
    '''
    holds a configurations of the puzzle
    '''
    def __init__(self, positions,puzzleSize):
        self.__size = len(positions)
        self.__values = positions[:]
        self.__emptyPos = positions.index(0)
        self.__nrOfSteps = puzzleSize
    
    def getSize(self):
        return self.__size
    
    def getValues(self):
        return self.__values[:]
    
    def getNrOfSteps(self):
        return self.__nrOfSteps

    def nextConfig(self):
        '''
        makes the next valid moves (basically moves the empty position in all available directions:/up/down/left/right )
        in: -
        out: the list of the next correct configurations obtained moving the empty position
        '''
        nextC = []
        
        
        if self.__emptyPos + 1 <= self.__size-1:
            if self.__emptyPos % self.__nrOfSteps != self.__nrOfSteps - 1:
                    aux = self.__values[:]
                    aux[self.__emptyPos], aux[self.__emptyPos+1] = aux[self.__emptyPos+1], 0
                    nextC.append(Configuration(aux,self.__nrOfSteps))
                    #one step forward for a red frog
        if self.__emptyPos + self.__nrOfSteps <= self.__size-1:
                    aux = self.__values[:]
                    aux[self.__emptyPos], aux[self.__emptyPos + self.__nrOfSteps] = aux[self.__emptyPos + self.__nrOfSteps], 0
                    nextC.append(Configuration(aux,self.__nrOfSteps))
                    #twp steps forward for a red frog
        if self.__emptyPos - 1 >= 0:
            if self.__emptyPos % self.__nrOfSteps != 0:
                    aux = self.__values[:]
                    aux[self.__emptyPos], aux[self.__emptyPos-1] = aux[self.__emptyPos-1], 0
                    nextC.append(Configuration(aux,self.__nrOfSteps))
                    #one step forward for a red frog
        if self.__emptyPos - self.__nrOfSteps >= 0:
                    aux = self.__values[:]
                    aux[self.__emptyPos], aux[self.__emptyPos - self.__nrOfSteps] = aux[self.__emptyPos - self.__nrOfSteps], 0
                    nextC.append(Configuration(aux,self.__nrOfSteps))
                    #twp steps forward for a red frog
        return nextC
        
    def __eq__(self, other):
        if not isinstance(other, Configuration):
            return False
        if self.__size != other.getSize():
            return False
        if self.__nrOfSteps != other.getNrOfSteps():
            return False
        for i in range(self.__size):
            if self.__values[i] != other.getValues()[i]:
                return False
        return True
        
    def __str__(self):
        s=''
        i = 0
        j = self.__nrOfSteps*(self.__nrOfSteps-1)
        while i <= j:
            s+=' '.join(' ' if x==0 else str(x) for x in self.__values[i:i+self.__nrOfSteps])
            s+='\n'
            i = i + self.__nrOfSteps
        return s

class State:
    '''
    holds a PATH of configurations
    '''
    def __init__(self):
        self.__values = []
    
    def setValues(self, values):
        self.__values = values[:]

    def getValues(self):
        return self.__values[:]

    def __str__(self):
        s=''
        for x in self.__values:
            s+=str(x)+"------\n"
        return s

    def __add__(self, something):
        aux = State()
        if isinstance(something, State):
            aux.setValues(self.__values+something.getValues())
        elif isinstance(something, Configuration):
            aux.setValues(self.__values+[something])
        else:
            aux.setValues(self.__values)
        return aux
    
class Problem:
    
    def __init__(self, initial, final):
        self.__initialConfig = initial
        self.__finalConfig = final 
        self.__initialState = State()
        self.__initialState.setValues([self.__initialConfig])
        

    def expand(self, currentState):
        myList = []
        currentConfig = currentState.getValues()[-1]
        for x in currentConfig.nextConfig(): 
            if x not in currentState.getValues():   
                myList.append(currentState+x)
        
        return myList
    
    def getFinal(self):
        return self.__finalConfig
    
    def getRoot(self):
        return self.__initialState
    

    def heuristics(self, state, finalC):
        count = 0
        l = finalC.getSize()
        for i in range(l):
            if state.getValues()[-1].getValues()[i] != finalC.getValues()[i]:
                count+=1
        return count
    
#     def heuristics(self, state, finalC):
#         s = 0
#         l = finalC.getSize()
#         puzzleSize = finalC.getNrOfSteps()
#         currentConf = state.getValues()[-1].getValues()
#         finalC = finalC.getValues()
#         for i in range(l):
#             s+= abs(finalC.index(i)%puzzleSize-currentConf.index(i)%puzzleSize) + abs(finalC.index(i)//puzzleSize-currentConf.index(i)//puzzleSize) 
#         return s
        
        
class Controller:
    
    def __init__(self, problem):
        self.__problem = problem
    
    def BFS(self, root):
        
        q = [root]

        while len(q) > 0 :
            currentState = q.pop(0)
            
            if currentState.getValues()[-1] == self.__problem.getFinal():
                return currentState
            q = q + self.__problem.expand(currentState)
        return None

    def BestFS(self, root):
        
        visited = []
        toVisit = [root]
        while len(toVisit) > 0:
            node = toVisit.pop(0)
            visited = visited + [node]
            if node.getValues()[-1] == self.__problem.getFinal():
                return node
            aux = []
            for x in self.__problem.expand(node):
                if x not in visited:
                    aux.append(x)
            aux = [ [x, self.__problem.heuristics(x,self.__problem.getFinal())] for x in aux]
            aux.sort(key=lambda x:x[1])
            aux = [x[0] for x in aux]
            toVisit = aux[:] + toVisit
        return None

class UI:
    
    def __init__(self):
        self.__configurationList = readFromFile("data")
        self.__iniC = Configuration([0,3,1,2],2)
        self.__finC = Configuration([2,1,3,0],2)
        self.__p = Problem(self.__iniC,self.__finC)
        self.__contr = Controller(self.__p)
    
    def printMainMenu(self):
        s = ''
        s += "Initial and final configurations: \n"
        s = s + '------\n' + str(self.__iniC) + '------\n' + str(self.__finC) + '------\n'
        s += "1 - Read another configuration\n"
        s += "2 - Find a path with BFS \n"
        s += "3 - Find a path with BestFS \n"
        print(s)
        
    def readConfigSubMenu(self):
        currentConfigs = self.__configurationList.pop(0)
        self.__iniC = currentConfigs[0]
        self.__finC = currentConfigs[1]
        self.__p = Problem(self.__iniC, self.__finC)
        self.__contr = Controller(self.__p)
        
    def findPathBFS(self):
        startClock = time()
        res = self.__contr.BFS(self.__p.getRoot())
        print(str(res) if res is not None else "The puzzle cannot be solved")    
        print('execution time = ',time()-startClock, " seconds" )
        
    def findPathBestFS(self):
        startClock = time()
        res = self.__contr.BestFS(self.__p.getRoot())
        print(str(res) if res is not None else "The puzzle cannot be solved")
        print('execution time = ',time()-startClock, " seconds" )
   
    def run(self):
        while True:        
            try: 
                self.printMainMenu()
                command = int(input(">>"))
                if command == 0:
                    break
                elif command == 1:
                    self.readConfigSubMenu()
                elif command == 2:
                    self.findPathBFS()
                elif command == 3:
                    self.findPathBestFS()            
            except:
                print('Invalid command')
    
    
def readFromFile(filename):
    f = open("data","r")
    configList = []
    for line in f:
        aux = line.split(",")
        initial = aux[1].split()
        initial = [int(x) for x in initial]
        final = aux[2].split()
        final = [int(x) for x in final]
        configList.append([Configuration(initial,int(aux[0])),Configuration(final,int(aux[0]))])
    return configList    


def tests():
    c1 = Configuration([0,3,1,2,4,5,7,6,8],3)
    c2 = Configuration([2,1,3,0,5,4,6,8,7],3)
    s = State()
    p = Problem(c1,c2)
    contr = Controller(p)
    
    #Configuration
    assert(c1.getSize()==9)
    assert(c1.getValues()==[0,3,1,2,4,5,7,6,8])
    assert(c1.getNrOfSteps()==3)
    assert(c1.nextConfig() == [Configuration([3,0,1,2,4,5,7,6,8],3),Configuration([2,3,1,0,4,5,7,6,8],3)])
    
    #State
    
    assert(s.getValues() == [])
    s = s + 'acid salicilic'
    assert(s.getValues() == [])
    s = s + c1
    assert(s.getValues() == [c1])
    
    
    #Problem
    aux = p.expand(s)
    assert(len(aux) == 2)
    assert(aux[1].getValues()[-1] == Configuration([2,3,1,0,4,5,7,6,8],3))
    
    #...
    
    print('tests passed')
    
def main():
    tests()
    ui = UI()
    ui.run()
    
    
main()    
        
        
    
        