import musicEnvironment
import qlearningAgents
import chord
import writer
import Parse
class musicPlayer:
    def __init__(self, chord_progression, epsilon, alpha, gamma):
        self.scales = [['G','A','B','C','D','E','F#']]
        self.musicEnvironment = musicEnvironment.MusicEnvironment(self.scales, chord_progression)
        actionFn = lambda state: \
            self.musicEnvironment.getPossibleActions(state)
        self.learner = qlearningAgents.QLearningAgent(actionFn=actionFn)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.learner.setEpsilon(self.epsilon)
        self.learner.setLearningRate(self.alpha)
        self.learner.setDiscount(self.gamma)
        self.stepCount = 0
        self.fileWriter = writer.Writer('mymusic')
        self.actions_in_bar = []

    def step(self):
        self.stepCount += 1
        state = self.musicEnvironment.getCurrentState()
        actions = self.musicEnvironment.getPossibleActions(state)
        if len(actions) == 0.0:
            self.musicEnvironment.reset()
            state = self.musicEnvironment.getCurrentState()
            actions = self.musicEnvironment.getPossibleActions(state)
            print('Reset!')
        action = self.learner.getAction(state)
        self.actions_in_bar.append(action)
        if self.stepCount % 4 == 0:
            self.fileWriter.writeBar(self.actions_in_bar)
            self.actions_in_bar = []
        if action == None:
            raise Exception('None action returned: Code Not Complete')
        nextState, reward = self.musicEnvironment.doAction(action)

        self.learner.update(state, action, nextState, reward)

    def run(self):
        self.fileWriter.openFile()
        for i in range(16):
            self.step()
        self.fileWriter.closeFile()

if __name__ == '__main__':
    G_chord = chord.Chord('G', 'B', 'D')
    C_chord = chord.Chord('C', 'E', 'G')
    D_chord = chord.Chord('D', 'A', 'F#')
    EM_chord = chord.Chord('E','B','G')
    chord_progression = [G_chord, D_chord, EM_chord, C_chord]
    player = musicPlayer(chord_progression, 0.5, 0.5, 0.5)
    player.run()
    Parse.parse_notes('mymusic')