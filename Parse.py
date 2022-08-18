import numpy as np
from scipy.io import wavfile

BPM = 120
DICT = {'$': 0, 'A': 37, 'A#': 38, 'Bb': 38, 'B': 39, 'C': 40, 'C#': 41, 'Db': 41, 'D': 42, 'D#': 43, 'Eb': 43, 'E': 44,
        'F': 45, 'F#': 46, 'Gb': 46, 'G': 47, 'G#': 48, 'Ab': 48}  # create dictionary for each note and placement
BEAT_DURATION = 60 / BPM  # the duration of each beat in s, by the bpm
SAMPLE_RATE = 44100

"""
This function parsess the notes given on the path for
txt file, then converts them to wav file
"""


def parse_notes(path, is_melody):
    f = open(path, "r")
    name = f.name
    song = []
    for bar in f:
        bar = bar.strip().split(",")
        for beat in bar:
            if beat in DICT:
                song.append(get_wave(calculate_freq(beat, is_melody), BEAT_DURATION))
            else:
                a = []
                if len(beat) == 2:
                    a = list(beat)
                else:
                    for i in range(len(beat) - 1):
                        if beat[i + 1] == "b" or beat[i + 1] == "#":
                            a.append(beat[i] + beat[i + 1])
                            if i == len(beat) - 1:
                                a.append(beat[-1])
                            i += 2
                        elif beat[i] in DICT:
                            a.append(beat[i])
                            if i == len(beat) - 2:
                                a.append(beat[-1])
                        elif beat[i + 1] in DICT:
                            a.append(beat[i + 1])
                        else:
                            pass
                for n in a:
                    song.append(get_wave(calculate_freq(n, is_melody), is_melody, BEAT_DURATION / len(a)))
    f.close()
    write_notes(song, name)


def calculate_freq(note, is_melody):
    if is_melody:
        return (2 ** ((DICT[note] - 49) / 12) * 440) * 2
    return 2 ** ((DICT[note] - 49) / 12) * 440


def write_notes(song, name):
    song_data = np.concatenate(song)
    name = name + 'wav'
    wavfile.write(name, SAMPLE_RATE, song_data.astype(np.int16))


def get_wave(freq, is_melody, duration=0.5):
    amplitude = 2048
    if is_melody:
        amplitude *=2
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave