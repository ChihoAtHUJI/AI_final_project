import sys
import Parse
import musicGUI
class Writer:
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = None

    def openFile(self):
        self.file = open(self.fileName, 'w')

    def writeBar(self, actions):
        for i in range(len(actions) - 1):
            self.file.writelines(actions[i].get_note() + ',')
        self.file.writelines(actions[-1].get_note() + '\n')

    def closeFile(self):
        self.file.close()