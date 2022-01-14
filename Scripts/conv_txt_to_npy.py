#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Mon Jul  1 15:41:48 2019
    
    @author: rsankar

    Convert txt files in a given folder to npy.
    To run: python conv_txt_to_npy.py path_to_folder
"""

import numpy as np
import os, sys
import glob




#################################

folder_name = sys.argv[1]
if os.path.isdir(folder_name) is False:
    raise ValueError("Not a folder.")

print(folder_name)
source_path = folder_name 
target_path = folder_name + '/npy_version/'
if not os.path.exists(target_path):
    os.mkdir(target_path)
    print('Created folder npy_version.')


files_list = glob.glob(source_path + '/*.txt')
lsl = len(files_list)

for file_num, file in enumerate(files_list):
    base_filename = os.path.basename(file)
    
    #Read song file
    print('File name: ', file)
    rawdata = np.loadtxt(file)

    np.save(target_path + base_filename[:-4], rawdata)