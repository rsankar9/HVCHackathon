"""
    This scripts plots the song in an npy/txt file, in an interactive manner.
    Use line 81-83 to select portions of the file.
    Not meant to be a generic code for public use.
    Just an auxilliary file to quickly visualise the song and adjust the syllable segmenting parameters.
    Parameters should be adjusted per bird.
    Requires Python 3.7.3 and other packages.
    
    To run: python Auxilliary_support.py path_to_npy_file.npy
    or
    python Auxilliary_support.py path_to_txt_file.txt
"""


##Auxiliary code to plot amplitude of signal and smoothed amplitude
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
import os
import scipy.signal
import glob
import json
import sys
from songbird_data_analysis import Song_functions


window =('hamming')
overlap = 64
nperseg = 1024
noverlap = nperseg-overlap
colormap = "jet"
smooth_win = 10

#IMPORTANT -> Threshold params
parameters      =   json.load(open('parameters.json'))
threshold       =   parameters['threshold']
min_syl_dur     =   parameters['min_syl_dur']
min_silent_dur  =   parameters['min_silent_dur']

#rec_system = 'Alpha_omega' # or 'Neuralynx' or 'Other'
rec_system = 'Neuralynx'





##########

if rec_system == 'Alpha_omega':
    fs = 22321.4283
elif rec_system == 'Neuralynx':
    fs = 32000
print('fs:',fs)

songfile = sys.argv[1]                      # npy file
base_filename = os.path.basename(songfile)  # Extracts filename
print(songfile)
rawsong = np.array([])
if songfile[-4:] == '.npy':
    print('npy file')
    rawsong = np.load(songfile) # Loads file
elif songfile[-4:] == '.txt':
    print('txt file')
    rawsong = np.loadtxt(songfile) # Loads file
else:
    raise ValueError("Given path doesn't lead to a song file.")
    rawsong = np.loadtxt(songfile)
rawsong = rawsong.astype(float)
rawsong = rawsong.flatten()
print('size=',rawsong.size, 'shape=',rawsong.shape)

# To extract just a portion of the song
s=rawsong.size

# Comment out from here if not required
# CHANGE XI AND XN TO VIEW ONLY PORTIONS OF THE FILE
## The file will be divided into xn portions and only portion no. xi+1 will be plotted
## For e.g. xn = 4, xi = 3
## This will cut the file into four parts and only plot the last (i.e. fourth) part

# Splits file according to how much data you want to view
start = parameters['start_pos']
end =  start + (30*fs)
rawsong = rawsong[start:end]

# Comment out until here if not required

print(rawsong.shape)
print(len(rawsong))

amp = Song_functions.smooth_data(rawsong, fs, freq_cutoffs=(1000, 8000))
print('amp:', amp, 'samp_freq:', fs)

(onsets, offsets) = Song_functions.segment_song(amp,segment_params={'threshold': threshold, 'min_syl_dur': min_syl_dur, 'min_silent_dur': min_silent_dur},samp_freq=fs)    # Detects syllables according to the threshold you set
shpe = len(onsets)                          # Use this to detect no. of onsets


# ### Building figure
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)
plt.setp(ax1.get_xticklabels(), visible=True)
plt.setp(ax2.get_xticklabels(), visible=True)

x_amp=np.arange(len(amp))


# Plots spectrogram
(f,t,sp)=scipy.signal.spectrogram(rawsong, fs, window, nperseg, noverlap, mode='complex')
ax3.imshow(10*np.log10(np.square(abs(sp))), origin="lower", aspect="auto", interpolation="none")
for i in range(0,shpe):
    ax3.axvline(x=onsets[i]*len(t)/x_amp[-1],color='b',alpha=0.1)
    ax3.axvline(x=offsets[i]*len(t)/x_amp[-1],color='r',alpha=0.1)

# print(len(t))
# plt.figure()
# plt.plot((x_amp/x_amp[-1])*len(t))
# plt.show()
# ##Plot song signal amplitude
ax1.plot((x_amp/x_amp[-1])*len(t),rawsong,color='black')
ax1.set_xlim([0, len(t)])
for i in range(0,shpe):
    ax1.axvline(x=(onsets[i]/x_amp[-1])*len(t),color='b')
    ax1.axvline(x=offsets[i]*len(t)/x_amp[-1],color='r')

# ##Plot smoothed amplitude of the song
ax2.plot((x_amp/x_amp[-1])*len(t), amp,color='black')
ax2.set_xlim([0, len(t)])
# ax2.set_ylim([0, threshold+5e-8])
for i in range(0,shpe):
    ax2.axvline(x=onsets[i]*len(t)/x_amp[-1], alpha=0.2)
    ax2.axvline(x=offsets[i]*len(t)/x_amp[-1],color='r', alpha=0.2)
ax2.axhline(y=threshold,color='g')
#ax2.xaxis.set_tick_params(which='both', labelbottom=True)

plt.show()


