import numpy as np
from scipy.io import wavfile

# LATEST UPDATE

BPM = 120
DICT = {'$': 0, 'A': 1, 'b': 2, 'B': 3, 'C': 4, 'd': 5, 'D': 6, 'e': 7, 'E': 8, 'F': 9, 'g': 10, 'G': 11,
        'a': 12}  # create dictionary for each note and placement
BEAT_DURATION = 60 / BPM  # the duration of each beat in s, by the bpm
SAMPLE_RATE = 44100
CHORD_OCT = 4
FREQ_CONSTANT = 2**(1/12)

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
            beat = beat.split("/")
            chord = beat[0]
            beat = beat[1]
            if beat in DICT:
                b = get_chord_wave(chord, BEAT_DURATION)
                b.append(get_wave(calculate_freq(beat), BEAT_DURATION))

                song.append(sum(b))
            else:
                a = list(beat)
                for note in a:
                    b = get_chord_wave(chord, BEAT_DURATION / len(a))
                    b.append(get_wave(calculate_freq(note), (BEAT_DURATION / len(a))))
                    song.append(sum(b))
    f.close()
    write_notes(song, path)


# def calculate_freq(note, oct=5, add=0):
#     if DICT[note] == 0 : return 0
#     octave_differential = 12 * (oct - CHORD_OCT)
#     n = DICT[note] - 1 + octave_differential + add
#     # print(note + " "  + str(n))
#     if add == 0:
#         print(note + " " + str(440 * (FREQ_CONSTANT ** n)))
#     return 440 * (FREQ_CONSTANT ** n)

def calculate_freq(note, oct=6, add=0):
    if DICT[note] == 0: return 0
    if DICT[note] < 3:
        key = DICT[note] + 12 + ((oct - 1) * 12) + add
    else:
        key = DICT[note] + ((oct - 1) * 12) + add
    return 2 ** ((key - 49) / 12) * 440


def write_notes(song, name):
    song_data = np.concatenate(song)
    wavfile.write(name + ".wav", SAMPLE_RATE, song_data.astype(np.int16))


def get_wave(freq, duration=0.5):
    amplitude = 4096
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave


def get_chord_wave(chord, dur=0.5):
    if chord[-1] == 'm':
        a = 3;
        b = 4
    else:
        a = 4;
        b = 3
    data = []
    data.append(calculate_freq(chord[0], CHORD_OCT));
    data.append(calculate_freq(chord[0], CHORD_OCT, a));
    data.append(calculate_freq(chord[0], CHORD_OCT, a + b))
    wave = [get_wave(freq, dur) for freq in data]
    return wave