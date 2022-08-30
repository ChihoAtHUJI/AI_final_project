from CSP.Node import *

class board():
    def __init__(self, inputs):
        inputsList = inputs.split(',')
        # print(inputsList)
        self._nodes = self.makeBoard(inputsList)
        self._state = self.makeState(inputsList)
        self._chordLength = len(inputsList) - 1
        # print(board)

    def getNodes(self):
        return self._nodes

    def getState(self):
        return self._state


    def makeBoard(self, inputs):
        result = []
        for i in range(len(inputs)):
            subset = []

            for j in range(4):
                _node = Node(inputs[i], j)
                subset.append(_node)
            result.append(subset)
        return result




    def makeState(self, inputs):
        result = []
        for i in range(len(inputs)):
            subset = []
            for j in range(4):
                subset.append(None)
            result.append(subset)
        return result

    def finished(self):
        if self._state[-1][-1] is None:
            return False
        return True

    def findUnassigned(self):
        for i in range(len(self._nodes)):
            for j in range(len(self._nodes[i])):
                if self._state[i][j] is None:
                    return [i, j]

    def checkConsistent(self, value, x, y):
        if x == 0:
            if y == 0:
                return True
            else:
                if value != self._state[x][y-1]:
                    return True
                return False
        if y == 0:
            if value != self._state[x-1][y]:
                return True
            return False
        if value != self._state[x-1][y] and value != self._state[x][y-1] and value != self._state[x-1][y-1]:
            return True
        return False

    def updateState(self, value, x, y):
        self._state[x][y] = value

    def removeState(self, x, y):
        self._state[x][y] = None



# if __name__ == '__main__':
#     B = board('50,G,C,D,Em')