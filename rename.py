import os
import glob
import numpy
import wave
import matplotlib.pyplot as plt

path = "/home/pi/Documents/"
files = glob.glob(path + "*.wav")
for f in files:
    org = os.path.basename(f)
    os.rename(f, os.path.join(path, org[:0] + "x" + org[1:]))
