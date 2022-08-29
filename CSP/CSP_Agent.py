# from CSP.Node import *
from CSP.board import *
import random

class CspAgent():

    def __init__(self, board):
        self._board = board


    def getSolution(self):
        if self.backtracking_search() is False:
            return False
        return self.backtracking_search().getState()

    def getChordInformation(self):
        nodes = self._board.getNodes()
        result = []
        for i in range(len(nodes)):
            result.append(nodes[i][0].getRootChord())
        return result


    def backtracking_search(self):
        return self.recursive_backtracking(self._board)

    def recursive_backtracking(self, assignment):
        if assignment.finished():
            return assignment
        # var = select-unassigned variable(csp, assignement, csp...)
        var = assignment.findUnassigned()


        # for each value in order domain values
        for value in assignment.getNodes()[var[0]][var[1]].getDomain():
            # if value is consistent with assignment then
            if assignment.checkConsistent(value, var[0], var[1]):

                assignment.updateState(value, var[0], var[1])
                result = self.recursive_backtracking(assignment)
                if result is False:
                    return False
                if result.finished():
                    return result
                assignment.removeState(var[0], var[1])
        return False
            # inferences <- inference(csp,var,value)
            # if inferences is not failure then
                # add inferences to assignment
                # if inferences is not failure then
                    # add inferences to assignment



