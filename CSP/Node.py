DOMAIN_DICT = {'Em': ['E', 'G', 'B', '$'], 'G': ['G', 'B', 'D', '$'], 'Am': ['A', 'C', 'E'],
               'C': ['C', 'E', 'G', '$'], 'D': ['D', 'g', 'A', '$'], 'Bm': ['B', 'D', 'g', '$']}

import random

NAME = 0
MINOR_INDICATOR = -1
DICT = {'$': 0, 'A': 1, 'b': 2, 'B': 3, 'C': 4, 'd': 5, 'D': 6, 'e': 7, 'E': 8, 'F': 9, 'g': 10, 'G': 11,
        'a': 12}
INVERTED_DICT = {0 : '$', 1: 'A', 2: 'b', 3: 'B', 4: 'C', 5: 'd', 6: 'D', 7: 'e', 8: 'E', 9: 'F', 10: 'g', 11: 'G',
                 12: 'a'}
MINOR_THIRD = 3
MAJOR_THIRD = 4
FIFTH = 7


def chord_builder(chord_progression):
    chord_list = list()
    print(chord_list)
    for chord_name in chord_progression:
        if chord_name[MINOR_INDICATOR] == 'm':
            note = chord_name[NAME]
            print(note)
            root_ind = DICT[note]
            if DICT[note] < 3:
                minor_key = (DICT[note] + 12 + MINOR_THIRD) % 12
                fifth_key = (DICT[note] + 12 + FIFTH) % 12
            else:
                minor_key = (DICT[note] + MINOR_THIRD) % 12
                fifth_key = (DICT[note] + FIFTH) % 12
            chord_list.append([INVERTED_DICT[root_ind], INVERTED_DICT[minor_key], INVERTED_DICT[fifth_key],
                               '$'])
        else:
            note = chord_name[NAME]
            root_ind = DICT[note]
            if DICT[note] < 3:
                major_key = (DICT[note] + 12 + MAJOR_THIRD) % 12
                fifth_key = (DICT[note] + 12 + FIFTH) % 12
            else:
                major_key = (DICT[note] + MAJOR_THIRD) % 12
                fifth_key = (DICT[note] + FIFTH) % 12
            chord_list.append([INVERTED_DICT[root_ind], INVERTED_DICT[major_key], INVERTED_DICT[fifth_key],
                               '$'])
    return chord_list

class Node():
    def __init__(self, root_chord, bit_num):
        self.root_chord = root_chord
        self.bit_num = bit_num
        self.domain = chord_builder(root_chord)
        print(self.domain)
        # self.domain = DOMAIN_DICT[root_chord]

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