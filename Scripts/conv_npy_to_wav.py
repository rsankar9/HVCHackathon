"""
author : R Sankar

Just a script to convert npy to wav for testing.


"""

import soundfile as sf
import numpy as np
import sys

filename = sys.argv[1]
npySong = np.load(sys.argv[1])

print('shape', npySong.shape)

sf.write(sys.argv[1][:-4]+'.wav', npySong, 32000)


print("Songfile has been converted to wav.\n\n\n")
