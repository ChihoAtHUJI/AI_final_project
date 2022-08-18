import environment
import learningAgents

CHORD = 0
NOTE = 0
BEAT = 1
subdivisions = ['_', '__', '___', '____']
BARS_PER_LOOP = 12
import writer
import qlearningAgents
import chord
import beat
import bar

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
    def __init__(self, scales, chord_progression):
        self.scales = scales
        self.starting_state = chord_progression[0], 1
        self.chord_progression = chord_progression
        self.reset()

    def getPossibleActions(self, state):
        actions = list()
        #checking which scales fit over the chord progression, these are the legal notes that we can play
        for scale in self.scales:
            note_flag = True
            for note in state[CHORD].get_chord():
                if note not in scale:
                    note_flag = False
                    break
            if note_flag:
                for note in scale:
                    actions.append((note, '_'))
        return actions

    def doAction(self, action):
        nextChord = self.state[CHORD]
        nextBeat = self.state[BEAT]
        nextAction = action
        self.note_frequency_dict[action[NOTE]] += 1
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
        reward = -0.1
        if action[NOTE] in state[CHORD].get_chord():
            reward += 10 - 0.2 * self.note_frequency_dict[action[NOTE]]
        if state[BEAT] == 1:
            self.bar_count += 1
            if action[NOTE] == state[CHORD].get_root():
                reward += 100
        if self.bar_count % BARS_PER_LOOP == 0:
            self.reset_freq_dict()
        return reward

    def getCurrentState(self):
        return self.state

    def reset(self):
        self.state = self.starting_state
        self.curr_chord_index = 0
        self.note_frequency_dict = {'A' : 0, 'A#' : 0, 'B':0, 'C':0, 'C#':0, 'D':0,
                                    'D#':0, 'E':0, 'F':0, 'F#':0, 'G':0, 'G#':0, '$':0}
        self.bar_count = 0

    def reset_freq_dict(self):
        for key in self.note_frequency_dict.keys():
            self.note_frequency_dict[key] = 0
