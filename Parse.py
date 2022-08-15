import numpy as np
from scipy.io import wavfile

BPM = 100
DICT = {'$':0, 'A':1, 'A#':2, 'Bb':2, 'B':3, 'C':4, 'C#':5, 'Db':5, 'D':6, 'D#':7, 'Eb':7, 'E':8, 'F':9, 'F#':10, 'Gb':10, 'G':11, 'G#':12, 'Ab':12} #create dictionary for each note and placement
BEAT_DURATION = 60 / BPM #the duration of each beat in s, by the bpm
SAMPLE_RATE = 44100
BASE_FREQ = 16.35 # C0 freq

"""
This function parsess the notes given on the path for
txt file, then converts them to wav file
"""
def parse_notes(path):
    f = open(path, "r")
    song = []
    for bar in f:
        bar = bar.strip().split(",")
        for beat in bar:
            if beat in DICT:
                song.append(get_wave(calculate_freq(beat), BEAT_DURATION))
            else:
                a = []
                if len(beat) == 2:
                    a = list(beat)
                else:
                    for i in range(len(beat)-1):
                        if beat[i+1] == "b" or beat[i+1] == "#":
                            a.append(beat[i] + beat[i+1])
                            if i == len(beat)-1:
                                a.append(beat[-1])
                            i+=2
                        elif beat[i] in DICT:
                            a.append(beat[i])
                            if i == len(beat)-2:
                                a.append(beat[-1])
                        elif beat[i+1] in DICT:
                            a.append(beat[i+1])
                        else:
                            pass
                for n in a:
                    song.append(get_wave(calculate_freq(n), BEAT_DURATION/len(a)))
    f.close()
    write_notes(song)

def calculate_freq(note, oct=5):
    if DICT[note] == 0:
        return 0
    if DICT[note] < 3:
        key = DICT[note] + 12 + ((oct - 1) * 12)
    else:
        key = DICT[note] + ((oct - 1) * 12)
    print(2**((key-49)/12) * 440)
    return 2**((key-49)/12) * 440

def write_notes(song):
    song_data = np.concatenate(song)
    wavfile.write("output.wav", SAMPLE_RATE, song_data.astype(np.int16))
    
def get_wave(freq, duration=0.5):
    amplitude = 4096
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave
