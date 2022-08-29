import sys
import QLearningAgent.musicGUI
class Writer:
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = None

    def openFile(self):
        self.file = open(self.fileName, 'w')

    def writeBar(self, chord, actions):
        for i in range(len(actions) - 1):
            self.file.writelines(chord + '/' + actions[i] + ',')
        self.file.writelines(chord + '/' + actions[-1] + '\n')

    def closeFile(self):
        self.file.close()