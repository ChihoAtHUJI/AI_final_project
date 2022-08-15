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

class musicPlayer:
    def __init__(self, scales, chord_progression):
        self.scales = scales
        self.state = None
        self.chord_progression = chord_progression
        self.curr_chord_index = 0

    def getLegalActions(self, state):
        actions = list()
        for scale in self.scales:
            note_flag = True
            for note in state[CHORD].get_chord():
                if note not in scale:
                    note_flag = False
                    break
            if note_flag:
                actions.extend(scale)
        return actions

    def doAction(self, state, action):
        nextChord = self.state[CHORD]
        nextBeat = self.state[BEAT]
        nextAction = action
        if state[BEAT] == 4:
            self.curr_chord_index = (self.curr_chord_index + 1) % len(self.chord_progression)
            nextBeat = 1
            nextChord = self.chord_progression[self.curr_chord_index]
            #go to next chord
        else:
            nextBeat = state[BEAT] + 1
        self.state = [nextChord,  nextAction, nextBeat]

    def reward(self, state, action):
        reward = 0
        if action[NOTE] in state[CHORD].get_notes():
            reward += 1
        if state[BEAT] == 1:
            if action[NOTE] == state[CHORD].get_root():
                reward += 1
        return reward

if __name__ == '__main__':
    G_chord = chord.Chord('G', 'B', 'D')
    C_chord = chord.Chord('C', 'E', 'G')
    D_chord = chord.Chord('D', 'A', 'F#')
    EM_chord = chord.Chord('E','B','G')
    chord_progression = [G_chord, D_chord, EM_chord, C_chord]
    first_state = [G_chord, '$', 1]
    newPlayer = musicPlayer([['G','A','B','C','D','E','F#']], chord_progression)
    agent = qlearningAgents.QLearningAgent(newPlayer.getLegalActions)
    learner = learningAgents.ReinforcementAgent(newPlayer.getLegalActions)
    learner.startEpisode()
    curr_state = first_state
    for i in range(40):
        legal_actions = learner.getLegalActions(curr_state)

        learner.update()
    learner.stopEpisode()