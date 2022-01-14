#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:41:48 2019

@author: rsankar
"""

###################################################################################
# README.md
###################################################################################
# - Give the path to the parent folder of Clean_songs as an argument when you run the python script: python Manual_labeling.py parent_folder_name
# - Ensure this folder has a folder called Clean_songs with the songfiles (.txt) to be labelled.
# - Ensure this folder doesn't have a clashing Annotations, Labeled_songs or Noise_songs folder (as some files will be moved/created in these folders).
# - To change the segmenting parameters, you'll have to change the json file 'parameters.json'.

###################################################################################

import numpy as np
import scipy as sp
import scipy.signal
import os
import glob
import json
import sys
from songbird_data_analysis import Song_functions
import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import matplotlib.widgets as mplw


###################################################################################
# Block 0: Define variables and functions
###################################################################################
#Spectrogram parameters
#Default windowing function in spectrogram function
#window =('tukey', 0.25) 
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

#Contains the labels of the syllables from a single .wav file
labels = []
syl_counter=0
Nb_syls=0
keep_song =''
#rec_system = 'Alpha_omega' # or 'Neuralynx' or 'Other'
rec_system = 'Neuralynx'





# Text box widget to collect labels
class myWidget():
    def __init__(self, ax, label, initial='',color='.95', hovercolor='1', label_pad=.01):
        self.widget = mplw.TextBox(ax, label, initial='',color='.95', hovercolor='1', label_pad=.01)
        self.annotation = ''        # The label for corresponding syllable manually entered by user
        self.label = label          # The label of the box (text that appears next to textbox)
    def submit(self,text):
        self.annotation = text
        print(self.label, ':', text)

# Button widget to end labeling
class myButton():
    def __init__(self, ax, label, image=None, color='0.85', hovercolor='0.95'):
        self.widget = mplw.Button(ax, label, image=None, color='0.85', hovercolor='0.95')
    def finalise(self,val):
        file_path_target_labeled = target_path_song+'/'+base_filename
        file_path_target_annot = target_path_annot+'/'+base_filename[0:-4]+'_annot.txt'
        os.rename(songfile, file_path_target_labeled)
        file_to_write= open(file_path_target_annot,"w+")
        for j in range(0, shpe):
            file_to_write.write("%d,%d,%s\n" % (onsets[j],offsets[j],textboxes[j].annotation))
            #Write to file from buffer, i.e. flush the buffer
        file_to_write.flush()
        file_to_write.close
        print('---Final labels---')
        for index, item in enumerate(textboxes):
            print(item.label,':',item.annotation,':',onsets[index],'-',offsets[index])
        plt.close('all')
    def reject_labeling(self,val):
        file_path_target_noise = target_path_noise+'/'+base_filename
        os.rename(songfile, file_path_target_noise)
        plt.close('all')
    def stop_labeling(self,val):
        plt.close('all')
        sys.exit()





# Parse folder
folder_name = sys.argv[1]
if os.path.isdir(folder_name) is False:
    raise ValueError("Not a folder.")

print(folder_name)
source_path = folder_name + '/Clean_songs'
target_path_song = folder_name + '/Labeled_songs'
target_path_annot = folder_name + '/Annotations'
target_path_noise = folder_name + '/Noise_songs'
if not os.path.exists(source_path):
    raise ValueError('Clean_songs folder does not exist.')
#os.chdir(source_path)
if not os.path.exists(target_path_song):
    os.mkdir(target_path_song)
    print('Created folder Labeled songs.')
if not os.path.exists(target_path_annot):
    os.mkdir(target_path_annot)
    print('Created folder Annotations.')
if not os.path.exists(target_path_noise):
    os.mkdir(target_path_noise)
    print('Created folder Noise songs.')


#Take all files from the directory
#songfiles_list = glob.glob('*.wav')
if rec_system == 'Alpha_omega':
    fs = 22321.4283
elif rec_system == 'Neuralynx':
    fs = 32000
print('fs:',fs)
filetype = '.npy' # '.txt'
songfiles_list = glob.glob(source_path + '/*' + filetype)


#file_num is the index of the file in the songfiles_list
for file_num, songfile in enumerate(songfiles_list):
    base_filename = os.path.basename(songfile)

    #Read song file	
    print('File name: %s' % songfile)

    if filetype == '.txt':
        rawsong = np.loadtxt(songfile)
    elif filetype == '.npy':
        rawsong = np.load(songfile)
    rawsong = rawsong.astype(float)
    rawsong = rawsong.flatten()
    
	#Bandpass filter, square and lowpass filter
	#cutoffs : 1000, 8000
    amp = Song_functions.smooth_data(rawsong,fs,freq_cutoffs=(1000, 8000))

	#Segment song
    (onsets, offsets) = Song_functions.segment_song(amp,segment_params={'threshold': threshold, 'min_syl_dur': min_syl_dur, 'min_silent_dur': min_silent_dur},samp_freq=fs)
    shpe = len(onsets)
    if shpe < 1:
        print('Removing because ', shpe)
        file_path_target_noise = target_path_noise+'/'+base_filename
        os.rename(songfile, file_path_target_noise)
        continue
    else:
        print('Label')
	
    
    # Create figure
    fig1, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)
    plt.setp(ax1.get_xticklabels(), visible=True)
    plt.setp(ax2.get_xticklabels(), visible=True)
    
    x_amp=np.arange(len(amp))

    #Compute and plot spectrogram
    (f,t,sp)=scipy.signal.spectrogram(rawsong, fs, window, nperseg, noverlap, mode='complex')
    ax3.imshow(10*np.log10(np.square(abs(sp))), origin="lower", aspect="auto", interpolation="none")
    ax3.set_ylabel('Frequency')
    for i in range(0,shpe):    #Plot onsets and offsets
        ax3.axvline(x=onsets[i]*len(t)/x_amp[-1],color='b',alpha=0.2)
        ax3.axvline(x=offsets[i]*len(t)/x_amp[-1],color='r',alpha=0.2)
        ax3.text((onsets[i]+offsets[i])/2*len(t)/x_amp[-1], -max(rawsong)*0.75, str(i), va='top', ha='center', size='xx-small')


    #fig.colorbar()
    
    #Plot rawsong
    ax1.plot(x_amp*len(t)/x_amp[-1], rawsong)
    ax1.set_ylabel('Rawsong')
    ax1.set_xlim([0, len(t)])
    ax1.xaxis.set_tick_params(which='both', labelbottom=True)
    for i in range(0,shpe):    #Plot onsets and offsets
        ax1.axvline(x=onsets[i]*len(t)/x_amp[-1],color='b',alpha=0.5)
        ax1.axvline(x=offsets[i]*len(t)/x_amp[-1],color='r',alpha=0.5)
        ax1.text((onsets[i]+offsets[i])/2*len(t)/x_amp[-1], -max(rawsong)*0.75, str(i), va='top', ha='center', size='xx-small')


    ##Plot smoothed amplitude of the song
    ax2.plot(x_amp*len(t)/x_amp[-1], amp)
    ax2.set_xlim([0, len(t)])
    # ax2.set_ylim([0, 3e-8])
    ax2.set_ylabel('Smooth amplitude')

    for i in range(0,shpe):    #Plot onsets and offsets
        ax2.axvline(x=onsets[i]*len(t)/x_amp[-1],color='b')
        ax2.axvline(x=offsets[i]*len(t)/x_amp[-1],color='r')
        ax2.text((onsets[i]+offsets[i])/2*len(t)/x_amp[-1], 3e-8*0.75, str(i), va='top', ha='center', size='xx-small')
    ax2.axhline(y=threshold,color='g')
    plt.xlabel('Time')

    fig1.canvas.manager.window.showMaximized()

    #Plotting widgets for collecting labels
    fig2 = plt.figure()
    axbox = [plt.axes([0.15+0.1*(i%8), 0.1+0.1*(i//8), 0.05, 0.05]) for i in range(shpe)]
    ax_bd = plt.axes([0.15, 0.1+0.1*(1+shpe//8), 0.5, 0.05])
    ax_bs = plt.axes([0.15, 0.1+0.1*(2+shpe//8), 0.5, 0.05])
    ax_br = plt.axes([0.15, 0.1+0.1*(3+shpe//8), 0.5, 0.05])
    textboxes = [myWidget(axbox[i], label=str(i)) for i in range(shpe)]
    for text_box in textboxes:
        text_box.widget.on_submit(text_box.submit)
    button_done = myButton(ax_bd, 'Finalise labeling')
    button_done.widget.on_clicked(button_done.finalise)
    button_reject = myButton(ax_br, 'Reject labeling')
    button_reject.widget.on_clicked(button_reject.reject_labeling)
    button_stop = myButton(ax_bs, 'Stop labeling')
    button_stop.widget.on_clicked(button_stop.stop_labeling)

    plt.get_current_fig_manager().window.setGeometry(900, 00, 500, 300)

    plt.show()

#    plt.close('all')
