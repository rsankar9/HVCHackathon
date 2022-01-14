"""
Python functions to facilitate interacting with the dataset from Koumura and
Okanoya 2016 [1].

The original code was released under the GNU license:
https://github.com/cycentum/birdsong-recognition/blob/master/
birdsong-recognition/src/computation/ViterbiSequencer.java

Note that the Python implementations are not based directly on the Java code but
they have been tested to see whether they produce the same results.

File based on koumura.py
Used when annotations are done in .txt format

data: https://figshare.com/articles/BirdsongRecognition/3470165

[1] Koumura T, Okanoya K (2016) Automatic Recognition of Element Classes and
Boundaries in the Birdsong with Variable Sequences. PLoS ONE 11(7): e0159188.
doi:10.1371/journal.pone.0159188
"""

#from standard library
import os
import glob
import xml.etree.ElementTree as ET

#from dependencies
import numpy as np

def load_song_annot(songfile):
    """

    Parameters
    ----------
    songfile : str
        filename of .wav file from Koumura dataset

    Returns
    -------
    songfile_dict :
        with keys onsets, offsets, and labels
    """
    dirname, songfile = os.path.split(songfile)
    if dirname == '':
        # annot_file = glob.glob('../Training_Songs_annot/'+songfile[0:15]+'_annot.txt')
        annot_file = glob.glob('../Training_Songs_annot/'+songfile[:-4]+'_annot.txt')
    else:
        # annot_file = glob.glob(os.path.join(dirname, '../Training_Songs_annot/'+songfile[0:15]+'_annot.txt'))
        annot_file = glob.glob(os.path.join(dirname, '../Training_Songs_annot/'+songfile[:-4]+'_annot.txt'))
    if len(annot_file) < 1:
        raise ValueError('Can\'t open {}, Annotation.xml file not found in parent of current directory'.
                         format(songfile))
    elif len(annot_file) > 1:
        raise ValueError('Can\'t open {}, found more than one Annotation.xml file in parent of current directory'.
                         format(songfile))
    else:
        annot_file = annot_file[0]


    onsets = []
    offsets = []
    labels = [] 

    with open(annot_file) as f:
         lines = f.readlines()
         for line in lines:
             #line = str(lines)
             #print("line: %s" % line)
             splt = line.split(",")
             onsets.append(int(splt[0]))
             offsets.append(int(splt[1]))
			 
			 #If just: labels.append(str(splt[2])) then, labels will be ['1\n','2\n','3\n','1\n',...]. Need to get rid of \n
			 #This is done bellow
			 
             splt_nwline = (splt[2]).split("\n")
             labels.append(str(splt_nwline[0]))
		 
             #print("type of onsets %s %s %s " % (type(onsets[0]),type(offsets[0]),type(labels[0])))
             #print("%f %f %f" % (float(splt[0]),float(splt[1]),float(splt[2])))
	
    f.close
		
		
		
    onsets = np.asarray(onsets)
    offsets = np.asarray(offsets)

    songfile_dict = {
        'onsets' : onsets,
        'offsets' : offsets,
        'labels' : labels
    }
    return songfile_dict	
