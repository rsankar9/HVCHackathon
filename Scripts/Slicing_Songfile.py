"""
    This scripts splits the song into smaller chunks (txt), for ease in further processing.
    To run: python Slicing_Songfile.py path_to_file.npy / .txt
"""

import numpy as np
import os
import glob
import sys
import json


window =('hamming')
overlap = 64
nperseg = 1024
noverlap = nperseg-overlap
colormap = "jet"

parameters      =   json.load(open('parameters.json'))

#rec_system = 'Alpha_omega' # or 'Neuralynx' or 'Other'
rec_system = parameters['rec_system']
if rec_system == 'Alpha_omega':
    fs = 22321.4283
elif rec_system == 'Neuralynx':
    fs = 32000
print('fs:',fs)


#---------------------------------------------------------------------------#

songfile = sys.argv[1]                      # npy or txt file
if len(sys.argv) < 2:
    raise ValueError('Filename is not provided.')
    
base_filename = os.path.basename(songfile)  # Extracts filename
base_folderpath = os.path.dirname(songfile)
base_foldername = os.path.basename(base_folderpath)

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
rawsong = rawsong.astype(float)
rawsong = rawsong.flatten()
print('size=',rawsong.size, 'shape=',rawsong.shape)

raw_songs_dir_path = base_folderpath + "/Raw_songs"
if not os.path.exists(raw_songs_dir_path):
    os.mkdir(raw_songs_dir_path)


chunk_size = fs * 4  # 4 seconds
cn = 0

print('no. of chunks:', np.ceil(rawsong.size / chunk_size))
while chunk_size * cn < rawsong.size:
    rs = rawsong[chunk_size * cn : chunk_size * (cn+1)]
    
    #Write chunk of raw data
    print('Writing file no:', cn)
    file_path = raw_songs_dir_path + '/' + base_foldername + '_' + base_filename[0:-13]+'_raw_chunk_'+str(cn)#+'.txt'

    if songfile[-4:] == '.npy':     np.save(file_path, rs)
    elif songfile[-4:] == '.txt':   np.savetxt(file_path, rs, '%13.11f')

    cn += 1


