# ## @author: Eduarda Centeno
#### @modified: Remya Sankar
# #  Documentation for this module.
# #
# #  Created on Wed Feb  6 15:06:12 2019; -*- coding: utf-8 -*-; 


# #################################################################################################################################
# #################################################################################################################################
# # This code was built with the aim of allowing the user to work with Spike2 .smr files and further perfom correlation analyses ##
# # between specific acoustic features and neuronal activity.                                                                    ##
# # In our group we work with Zebra finches, recording their neuronal activity while they sing, so the parameters here might     ##
# # have to be ajusted to your specific data.                                                                                    ##                                                                                                                              ##
# #################################################################################################################################
# #################################################################################################################################

# ### Necessary packages
import neo
import numpy as np
import os



# ##############################################################################################################################
# # From now on there will be the core functions of this code, which will be individually documented:                          #
#                                                                                                                              #


def read(file):
    """# # This  function will allow you to read the .smr files from Spike2."""

    block_neo = neo.io.CedIO(file)

    seg_neo = block_neo.read_segment(lazy=True, signal_group_mode="split-all")

    return block_neo, seg_neo
    # return data, data_seg


def getsong(file, songChannelName):
    """
    Extracts song from smr/smrx file and saves in npy format.
    Compatible with neo v0.10
    """

    block_neo, seg_neo = read(file) # Reads smr file

    n_analogs = seg_neo.size["analogsignals"]

    for index in range(n_analogs):
      if seg_neo.analogsignals[index].name == songChannelName:

        analog_index = index
        songData = seg_neo.analogsignals[analog_index].load().as_array()
        np.save(os.path.dirname(file) + "/" + songChannelName + "_Songfile.npy", songData)
        print("Saved in ", os.path.dirname(file) + "/" + songChannelName + "_Songfile.npy")

        break
