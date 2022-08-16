import environment
import learningAgents

CHORD = 0
NOTE = 1
BEAT = 2
subdivisions = ['_', '__', '___', '____']
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
        self.starting_state = State(chord_progression[0], '$', 1)
        self.chord_progression = chord_progression
        self.reset()

    def getPossibleActions(self, state):
        actions = list()
        #checking which scales fit over the chord progression, these are the legal notes that we can play
        for scale in self.scales:
            note_flag = True
            for note in state.get_chord().get_chord():
                if note not in scale:
                    note_flag = False
                    break
            if note_flag:
                for note in scale:
                    actions.append(Action(note, '_'))
        return actions

    def doAction(self, action):
        nextChord = self.state.get_chord()
        nextBeat = self.state.get_beat()
        nextAction = action
        if self.state.get_beat() == 4:
            self.curr_chord_index = (self.curr_chord_index + 1) % len(self.chord_progression)
            nextBeat = 1
            nextChord = self.chord_progression[self.curr_chord_index]
            #go to next chord
        else:
            nextBeat = self.state.get_beat() + 1
        reward = self.reward(self.state, action)
        self.state = State(nextChord,  nextAction, nextBeat)
        return self.state, reward

    def reward(self, state, action):
        reward = 0
        if action.get_note() in state.get_chord().get_chord():
            reward += 1
        if state.get_beat() == 1:
            if action.get_note() == state.get_chord().get_root():
                reward += 1
        return reward

    def getCurrentState(self):
        return self.state

    def reset(self):
        self.state = self.starting_state
        self.curr_chord_index = 0

if __name__ == '__main__':
    G_chord = chord.Chord('G', 'B', 'D')
    C_chord = chord.Chord('C', 'E', 'G')
    D_chord = chord.Chord('D', 'A', 'F#')
    EM_chord = chord.Chord('E','B','G')
    chord_progression = [G_chord, D_chord, EM_chord, C_chord]
    first_state = [G_chord, '$', 1]
    newPlayer = MusicEnvironment([['G','A','B','C','D','E','F#']], chord_progression)
    agent = qlearningAgents.QLearningAgent()
    learner = learningAgents.ReinforcementAgent(newPlayer.getPossibleActions)
    learner.startEpisode()
    curr_state = first_state
    for i in range(40):
        legal_actions = learner.getLegalActions(curr_state)
    learner.stopEpisode()