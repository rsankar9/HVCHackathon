#!/bin/sh

# @author: R Sankar
# This scripts processes the smr(x) files in a folder as a batch, recursively.
# For e.g. It can extract the songfiles from all the smr(x) files in a directory and it's first-level sub-directories.
# You can run more scripts, by uncommenting the relevant lines of the code.
# To run: bash extractSongfile.sh <path-to-parent-folder>

# Parses first argument as the path to the parent folde
parent=$1


# Iterateres over the sub-directories
for d in $parent/2*/ ; do
    echo "--------------------"
    echo "--------------------"
    echo "$d"/CSC1.smrx
    python3 get_song_from_smr.py "$d"/CSC1.smrx
    
    # echo "$d"/CSC20_Songfile
    # python3 conv_npy_to_wav.py "$d"/CSC20_Songfile.npy
    # echo "$d"/*_Songfile.npy
    # python3 Slicing_Songfile.py "$d"/*_Songfile.npy

    # echo "$d"/
    # python3 Detect_syllables.py "$d"/

    # echo "$d"/
    # python3 Manual_labeling.py "$d"/

    # echo "$d"/
    # python3 Collect_chunked_songs.py "$d"/

    echo "--------------------"
    echo "--------------------"
done
