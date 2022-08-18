import musicEnvironment
import qlearningAgents
import chord
import writer
import Parse
import numpy as np
import wave
ROOT = 0
CHORD = 0
class musicPlayer:
    def __init__(self, chord_progression, epsilon, alpha, gamma):
        self.scales = [['G','A','B','C','D','E','F#', '$', 'A#', 'F', 'C#', 'D#', 'G#']]
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
        self.rootWrtier = writer.Writer('root')
        self.thirdWriter = writer.Writer('third')
        self.fifthWriter = writer.Writer('fifth')
        self.actions_in_bar = []

    def step(self, is_training):
        self.stepCount += 1
        state = self.musicEnvironment.getCurrentState()
        root_notes = [state[CHORD].get_root()] * 4
        third_notes = [state[CHORD].get_third()] * 4
        fifth_notes = [state[CHORD].get_fifth()] * 4

        actions = self.musicEnvironment.getPossibleActions(state)
        if len(actions) == 0.0:
            self.musicEnvironment.reset()
            state = self.musicEnvironment.getCurrentState()
            actions = self.musicEnvironment.getPossibleActions(state)
            print('Reset!')
        action = self.learner.getAction(state)
        self.actions_in_bar.append(action)
        if is_training:
            if self.stepCount % 4 == 0:
                self.fileWriter.writeBar(self.actions_in_bar)
                self.rootWrtier.writeBar(root_notes)
                self.thirdWriter.writeBar(third_notes)
                self.fifthWriter.writeBar(fifth_notes)
                self.actions_in_bar = []
        if action == None:
            raise Exception('None action returned: Code Not Complete')
        nextState, reward = self.musicEnvironment.doAction(action)

        self.learner.update(state, action, nextState, reward)

    def runTraining(self, bars):
        reps = bars * 4
        for i in range(reps):
            self.step(False)



    def run(self):
        self.fileWriter.openFile()
        self.rootWrtier.openFile()
        self.thirdWriter.openFile()
        self.fifthWriter.openFile()
        self.actions_in_bar = []
        for i in range(100):
            self.step(True)
        self.fileWriter.closeFile()
        self.rootWrtier.closeFile()
        self.thirdWriter.closeFile()
        self.fifthWriter.closeFile()

def merge_wav_files(name1, name2):
    # load two files you'd like to mix
    fnames = [name1, name2]
    wavs = [wave.open(fn) for fn in fnames]
    frames = [w.readframes(w.getnframes()) for w in wavs]
    # here's efficient numpy conversion of the raw byte buffers
    # '<i2' is a little-endian two-byte integer.
    samples = [np.frombuffer(f, dtype='<i2') for f in frames]
    samples = [samp.astype(np.float64) for samp in samples]
    # mix as much as possible
    n = min(map(len, samples))
    mix = samples[0][:n] + samples[1][:n]
    # Save the result
    mix_wav = wave.open("./mix.wav", 'w')
    mix_wav.setparams(wavs[0].getparams())
    # before saving, we want to convert back to '<i2' bytes:
    mix_wav.writeframes(mix.astype('<i2').tobytes())
    mix_wav.close()

if __name__ == '__main__':
    G_chord = chord.Chord('G', 'B', 'D')
    C_chord = chord.Chord('C', 'E', 'G')
    D_chord = chord.Chord('D', 'A', 'F#')
    EM_chord = chord.Chord('E','B','G')
    chord_progression = [G_chord, D_chord, EM_chord, C_chord]
    player = musicPlayer(chord_progression, 0.1, 0.5, 0.4)
    player.runTraining(500)
    player.run()
    Parse.parse_notes('rr', True)
    Parse.parse_notes('root', False)
    Parse.parse_notes('third', False)
    Parse.parse_notes('fifth', False)
    merge_wav_files('rrwav', 'rootwav')
    merge_wav_files('mix.wav', 'thirdwav')
    merge_wav_files('mix.wav', 'fifthwav')