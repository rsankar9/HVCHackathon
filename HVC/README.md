##README

## Using HVC
**In progress**

This software helps to automatically label syllables in songs.

#### Acknowledgements
- Roman Ursu
- For HVC - automatic syllable labeller - The Sober Lab at Emory University [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1475481.svg)](https://doi.org/10.5281/zenodo.1475481)

Python 3.5 is required, for the original version and for Roman's version.

Python 3.9 is required for the Remya's version.

---


1. Use the `Manual_labeling.py` script to annotate as many songs (~100) as required.
2. Split these files into a training set (80%) and test set (20%).
3. Copy the training and test songs to folders named `Training_Songs` and `Test_Songs`.
4. Copy the annotations to the corresponding folders named `Training_Songs_annot` and `Test_Songs_annot`.
5. Create a folder `Test_Songs_predict`.
6. Modify `Extract.yml` with the right chunking parameters as used for manual labeling, and update the paths for input and output.
7. Run it in a python console. `hvc.extract('Extract.yml')`
8. Modify `Select.yml` with the paths to the feature file and output.
9. Run it in a python console, and choose the model with the best score. `hvc.select('Select.yml')`
10. Modify `Predict.yml` with the paths to the chosen model meta file and folder with new songs.
11. Run it in a python console. `hvc.predict('Predict.yml')`
12. HVC will produce corresponding annotations in the local `Test_Songs_predict` folder.
13. Manually verify the annotations produced by the model in this folder.
14. Now, the training and testing is done, and we can generate the labels for the original song file, e.g. `CSC20_songfile.npy`.
15. Place the original song file in a folder titled `Test_Songs`.
16. In the same directory (parent of `Test_Songs`), create an empty folder titled `Test_Songs_predict`).
17. Modify `Predict.yml` with the path to this folder with the songfile.
18. Run it in a python console. `hvc.predict('Predict.yml')`
19. HVC will produce corresponding annotations in the local `Test_Songs_predict` folder.
