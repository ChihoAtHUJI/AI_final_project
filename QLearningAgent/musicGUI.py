import musicEnvironment
import qlearningAgents
import chord
import writer
import Parse

ROOT = 0
CHORD = 0
class musicPlayer:
    def __init__(self, chord_progression, alpha, epsilon, gamma):
        self.scales = [['G','A','B','C','D','E','g', '$', 'b', 'F', 'd', 'e', 'a']]
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
        self.fileWriter = writer.Writer('rr')
        self.actions_in_bar = []

    def step(self, is_training):
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
        if not is_training:
            if self.stepCount % 4 == 0:
                self.fileWriter.writeBar(state[CHORD].get_name(), self.actions_in_bar)
                self.actions_in_bar = []
        if action == None:
            raise Exception('None action returned: Code Not Complete')
        nextState, reward = self.musicEnvironment.doAction(action)

        self.learner.update(state, action, nextState, reward)

    def runTraining(self, bars):
        reps = bars * 4
        for i in range(reps):
            self.step(True)
            if self.learner.epsilon > 0:
                self.learner.epsilon -= 1/reps



    def run(self):
        self.fileWriter.openFile()
        self.actions_in_bar = []
        for i in range(100):
            self.step(False)
        self.fileWriter.closeFile()


# def merge_wav_files(name1, name2):
#     # load two files you'd like to mix
#     fnames = [name1, name2]
#     wavs = [wave.open(fn) for fn in fnames]
#     frames = [w.readframes(w.getnframes()) for w in wavs]
#     # here's efficient numpy conversion of the raw byte buffers
#     # '<i2' is a little-endian two-byte integer.
#     samples = [np.frombuffer(f, dtype='<i2') for f in frames]
#     samples = [samp.astype(np.float64) for samp in samples]
#     # mix as much as possible
#     n = min(map(len, samples))
#     mix = samples[0][:n] + samples[1][:n]
#     # Save the result
#     mix_wav = wave.open("./mix.wav", 'w')
#     mix_wav.setparams(wavs[0].getparams())
#     # before saving, we want to convert back to '<i2' bytes:
#     mix_wav.writeframes(mix.astype('<i2').tobytes())
#     mix_wav.close()

if __name__ == '__main__':
    G_chord = chord.Chord('G', 'B', 'D', 'G')
    C_chord = chord.Chord('C', 'E', 'G', 'C')
    D_chord = chord.Chord('D', 'A', 'g', 'D')
    EM_chord = chord.Chord('E', 'B', 'G', 'Em')
    chord_progression = [G_chord, D_chord, EM_chord, C_chord]
    player = musicPlayer(chord_progression, 1, 0.9, 0.2)
    player.runTraining(1000)
    player.run()
    Parse.parse_notes('rr')