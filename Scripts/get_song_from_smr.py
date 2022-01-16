"""
author : R Sankar

Just a script to test the smr data file with some basic functions

"""

from songbird_data_analysis import functions
import sys, os
import json

filename = sys.argv[1]

if not os.path.isfile(filename):
	print('File not found: ', filename)

else:
	parameters = json.load(open('parameters.json'))

	print('Getting song.')
	functions.getsong(filename, parameters['songChannelName'])

	print('All good.')


# print('Reading file.')
# # functions.read(filename)
# print('Getting info.')
# # functions.getinfo(filename)
# print('Getting arrays.')
# # functions.getarrays(filename)
# print('Plotting plots.')
# functions.plotplots(filename)