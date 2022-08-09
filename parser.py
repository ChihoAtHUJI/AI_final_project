import util
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

BPM = 120
DICT = {} #create dictionary for each note and its frequency

def parse():
    f = open("example.txt", "r")
    for bar in f:
        bar = bar.strip().split(",")
        print(bar)