#!/bin/sh


parent=$1



for d in $parent/2*/ ; do
    echo "--------------------"
    echo "--------------------"
    echo "$d"/CSC1.smrx
    python3 get_song_from_smr.py "$d"/CSC1.smrx
    # echo "$d"/CSC20_Songfile
    # python3 conv_npy_to_wav.py "$d"/CSC20_Songfile.npy
    echo "$d"/*_Songfile.npy
    python3 Slicing_Songfile.py "$d"/*_Songfile.npy

    echo "$d"/
    python3 Detect_syllables.py "$d"/

    echo "$d"/
    python3 Manual_labeling.py "$d"/

    # echo "$d"/
    # python3 Collect_chunked_songs.py "$d"/

    echo "--------------------"
    echo "--------------------"
done
