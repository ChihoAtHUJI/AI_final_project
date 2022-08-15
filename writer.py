import sys
import Parse
class Writer:
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = None

    def openFile(self):
        self.file = open(self.fileName, 'w')

    def writeBar(self, actions):
        for i in range(len(actions) - 1):
            self.file.writelines(actions[i].notes + ',')
        self.file.writelines(actions[-1].notes + '\n')

    def closeFile(self):
        self.file.close()

class Action:
    def __init__(self, notes, subdivision):
        self.notes = notes
        self.subdivision = subdivision

if __name__== '__main__':
    action1 = Action('D', '_')
    action2 = Action('E', '_')
    action3 = Action('F', '_')
    action4 = Action('G', '_')
    actions = [action1, action2, action3, action4]
    writer = Writer('zip')
    writer.openFile()
    writer.writeBar(actions)
    writer.closeFile()
    Parse.parse_notes('zip')