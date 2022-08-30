from QLearningAgent import environment
import itertools

CHORD = 0
NOTE = 0
BEAT = 1
subdivisions = ['_', '__', '___', '____']
BARS_PER_LOOP = 12
DICT = {'$': 0, 'A': 1, 'b': 2, 'B': 3, 'C': 4, 'd': 5, 'D': 6, 'e': 7, 'E': 8, 'F': 9, 'g': 10, 'G': 11,
        'a': 12}

class State:
    def __init__(self, chord, note, beat):
        self.chord = chord
        self.note = note
        self.beat = beat

    def get_chord(self):
        return self.chord

    def get_note(self):
        return self.note

    def get_beat(self):
        return self.beat

class Action:
    def __init__(self, note, subdivision):
        self.note = note
        self.subdivision = subdivision

    def get_note(self):
        return self.note

    def get_subdivision(self):
        return self.subdivision

class MusicEnvironment(environment.Environment):
    def __init__(self, scales, chord_progression, subdivisions):
        self.scales = scales
        self.starting_state = chord_progression[0], 1
        self.chord_progression = chord_progression
        self.reset()
        self.subdivisions = subdivisions
        self.actions = self.calcAllActions()


    def calcAllActions(self):
        actions = list()
        if self.subdivisions == 1:
            l1 = list(itertools.permutations(self.scales[0], 1))
            for l in l1:
                actions.append(l[0])
        if self.subdivisions >= 2:
            l2 = list(itertools.permutations(self.scales[0], 2))
            for l in l2:
                actions.append(l[0] + l[1])
        if self.subdivisions >= 3:
            l3 = list(itertools.permutations(self.scales[0], 3))
            for l in l3:
                actions.append(l[0] + l[1] + l[2])
        if self.subdivisions == 4:
            l4 = list(itertools.permutations(self.scales[0], 4))
            for l in l4:
                actions.append(l[0] + l[1] + l[2] + l[3])
        return actions

    def getPossibleActions(self, state):
        #checking which scales fit over the chord progression, these are the legal notes that we can play
        return self.actions

    def doAction(self, action):
        nextChord = self.state[CHORD]
        nextBeat = self.state[BEAT]
        nextAction = action
        for note in action:
            self.note_frequency_dict[note] += 1
        self.subdivisions_dict[self.index_dict[len(action)]] += 1
        if self.state[BEAT] == 4:
            self.curr_chord_index = (self.curr_chord_index + 1) % len(self.chord_progression)
            nextBeat = 1
            nextChord = self.chord_progression[self.curr_chord_index]
            #go to next chord
        else:
            nextBeat = self.state[BEAT] + 1
        reward = self.reward(self.state, action)
        self.state = nextChord, nextBeat
        return self.state, reward

    def reward(self, state, action):
        reward = -5
        length = len(action)
        reward -= self.subdivisions_dict[self.index_dict[length]]
        for note in action:
            if note in state[CHORD].get_chord():
                reward += (10 - 0.5 * self.note_frequency_dict[note]) / length
            elif DICT[note] - DICT[state[CHORD].get_root()] == 5 or\
                    DICT[note] - DICT[state[CHORD].get_root()] == -7:
                 reward += (10 - 0.5 * self.note_frequency_dict[note]) / length
            elif DICT[note] - DICT[state[CHORD].get_third()] == 7 or\
                    DICT[note] - DICT[state[CHORD].get_third()] == -5:
                 reward += (10 - 0.5 * self.note_frequency_dict[note]) / length
            # elif DICT[note] - DICT[self.starting_state[CHORD].get_root()] == 2 or\
            #         DICT[note] - DICT[self.starting_state[CHORD].get_root()] == -10:
            #      reward += (10 - 0.5 * self.note_frequency_dict[note]) / length
            elif DICT[note] == 0:
                reward += 0.01 * sum(list(self.note_frequency_dict.values()))
            elif DICT[note] != 0:
                reward -= 10

        if state[BEAT] == 1:
            self.bar_count += 1
            if action[0] in state[CHORD].get_chord():
                reward += 100
        if self.bar_count % BARS_PER_LOOP == 0:
            self.reset_freq_dict()
            self.reset_sub_dict()
        return reward

    def getCurrentState(self):
        return self.state

    def reset(self):
        self.state = self.starting_state
        self.curr_chord_index = 0
        self.note_frequency_dict = {'A': 0, 'b': 0, 'B': 0, 'C': 0, 'd': 0, 'D': 0,
                                    'e': 0, 'E': 0, 'F': 0, 'g': 0, 'G': 0, 'a': 0, '$': 0}
        self.subdivisions_dict = {'quarter': 0, 'eighth': 0, 'triplet': 0, 'sixteenth': 0}
        self.index_dict = {1 : 'quarter', 2 : 'eighth', 3 : 'triplet', 4 : 'sixteenth'}
        self.bar_count = 0

    def reset_freq_dict(self):
        for key in self.note_frequency_dict.keys():
            self.note_frequency_dict[key] = 0

    def reset_sub_dict(self):
        for key in self.subdivisions_dict.keys():
            self.subdivisions_dict[key] = 0