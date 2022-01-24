"""
author : R Sankar

Just a script to convert npy to wav for testing.


"""

import soundfile as sf
import numpy as np
import sys
import json

filename = sys.argv[1]
npySong = np.load(sys.argv[1])

print('shape', npySong.shape)

parameters      =   json.load(open('parameters.json'))

#rec_system = 'Alpha_omega' # or 'Neuralynx' or 'Other'
rec_system = parameters['rec_system']
#Take all files from the directory
#songfiles_list = glob.glob('*.wav')
if rec_system == 'Alpha_omega':
    fs = 22321.4283
elif rec_system == 'Neuralynx':
    fs = 32000
print('fs:',fs)



sf.write(sys.argv[1][:-4]+'.wav', npySong, fs)


print("Songfile has been converted to wav.\n\n\n")
