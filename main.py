import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
if __name__ == '__main__':
    ##This is just testing out creating wav files, this went by easier than expected.
    sample_rate = 44100
    step_size = 1.0/sample_rate
    freq = 2000
    sig_length = 1.0
    arr = np.arange(0, sig_length, step_size)
    signal = np.sin(np.pi * 2 * freq * arr)
    plt.plot(arr, signal)
    plt.show()
    signal *= 32767
    signal = np.int16(signal)
    wavfile.write("output.wav", sample_rate, signal)

