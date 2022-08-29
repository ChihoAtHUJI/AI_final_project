DOMAIN_DICT = {'Em': ['E', 'G', 'B', '$'], 'G': ['G', 'B', 'D', '$'], 'Am': ['A', 'C', 'E'],
               'C': ['C', 'E', 'G', '$'], 'D': ['D', 'g', 'A', '$'], 'Bm': ['B', 'D', 'g', '$']}

import random

class Node():
    def __init__(self, root_chord, bit_num):
        self.root_chord = root_chord
        self.bit_num = bit_num
        self.domain = DOMAIN_DICT[root_chord]

    def getRootChord(self):
        return str(self.root_chord)

    def getDomain(self):
        random.shuffle(self.domain)
        return self.domain

    def deleteVal(self, val):
        self.domain.remove(val)

    def addVal(self, val):
        self.domain.append(val)





if __name__ == '__main__':
    node = Node('G', 0)
    print(node.domain)