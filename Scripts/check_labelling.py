# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 11:47:00 2022

@author: eduar
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

def spectrogram(songfile, labelsfile, beg, end, fs, NFFT=512):
    """Function to compute spectrogram.

    Arguments
    ---------
    songfile: str
        name of song file, e.g. 'CSC5'
        
    labelsfile: str
        name of labels file
        
    beg:int
        sample point to zoom

    end: int
        sample point to end zoom
    
    fs: float or int
        sampling frequency

    NFFT: int
        parameter for plt.specgram

    specgram_args: str or dict
        additional params for specgram (default: see params below)

    """
    assert isinstance(songfile, str), "songfile should be str"
    assert isinstance(labelsfile, str), "labelsfile should be str"
    assert isinstance(beg, (int, float)), "beg should be float or int"
    assert isinstance(end, (float, int)), "end should be float or int"
    assert isinstance(fs, (float, int)), "fs should be float or int"
    assert isinstance(NFFT, int), "NFFT should be int"
    
    song = np.load(songfile)
    labels_df = pd.read_csv(labelsfile, header=None, names=["beg", "end", "syb"])
    df_updated = labels_df[(labels_df["beg"] >= beg) & (labels_df["end"] <= end)]
    
    trace = song[beg: end]
    duration_trace = np.linspace(beg / fs, end / fs, len(trace))
    
    fig, ax = plt.subplots()

    specgram_args = {
        "NFFT": NFFT,
        "noverlap": NFFT * 0.90,
        "scale_by_freq": True,
        "mode": "psd",
        "pad_to": 915,
        "cmap": "inferno",
        "vmin": -150,
        "vmax": -80,
        "scale": "dB",
        "detrend": "mean",
    }

    spec, freq, t, im = plt.specgram(trace.ravel(), Fs=fs, **specgram_args)
    
    x_t = np.linspace(df_updated['beg'].iloc[0], df_updated['end'].iloc[-1], len(t))
    for row in df_updated.iterrows():
        indx = np.where(np.logical_and(x_t>=row[1].beg, x_t<=row[1].end))
        plt.axvline(t[indx[0][0]], color='b', label='beg')
        plt.axvline(t[indx[0][-1]], color='r', label='end')
        label = row[1].syb
        plt.text(np.mean(t[indx]), np.quantile(freq, 0.2), label, color='white')

    ax.set_ylabel("Frequency (Hz)")
    ax.locator_params(axis="x", nbins=8)
    ticks = ax.get_xticks().tolist()
    new_ticks = [
        "%.2f" % item
        for item in np.linspace(duration_trace[0], duration_trace[-1], len(ticks))
    ]
    ax.set_xticklabels(new_ticks)
    ax.set_xlabel("Time (s)")
    