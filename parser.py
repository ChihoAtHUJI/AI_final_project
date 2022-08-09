import util
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

BPM = 120
DICT = {'A':37, 'A#':38, 'Bb':38, 'B':39, 'C':40, 'C#':41, 'Db':41, 'D':42, 'D#':43, 'Eb':43, 'E':44, 'F':45, 'F#':46, 'Gb':46, 'G':47, 'G#':48, 'Ab':48} #create dictionary for each note and placement
BEAT_DURATION = 60000 / BPM #the duration of each beat in ms, by the bpm

class Beat:
    def __init__(self, freq, dur):
        self.freq = freq
        self.dur = dur / len(self.freq)

def parse():
    f = open("example.txt", "r")
    beats = []
    for bar in f:
        bar = bar.strip().split(",") # remove any \n
        print(bar)
        for beat in bar:
            try:
                freq = calculate_freq(beat)
                b = Beat([freq], BEAT_DURATION)
                beats.append(b)
            except:
                if beat == "$":
                    beats.append(Beat([1], BEAT_DURATION))
                else:
                    print("multiple notes")
                    # will be handled later
    print(beats)

def calculate_freq(note):
    return 2**((DICT[note]-49)/12) * 440