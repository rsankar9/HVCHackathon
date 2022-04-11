## README

Here, we attempt to generate the annotations for songs in an smr file, automatically.

Files provided:

- Directory: HVCHackathon
- Contains 4 folders
	- Scripts 
	- SampleData
	- HVC
	- Installation

Step 1: We will first setup our environment with all required installations.

Follow README.md in folder `HVCHackathon/Installation `.

Step 2: We shall generate annotations automatically.

- prepare files for HVC:  
	Follow `README.md` in folder `HVCHackathon/Scripts`

- train model using HVC  
	Follow `README.md` in folder `HVCHackathon/HVC`

Step 3: Once HVC is trained for a bird, you can use only the HVC Predict script.
 - Per new recording, extract the .npy for the song channel using get_song_from_smr.py 
 - Copy this .npy to Test_songs
 - Run HVC predict (this will take all files in Test_songs, so leave there only the ones you need to sort).
 - Labels will be outputted to Test_Songs_predict.

Step 4: Remember that post processing is necessary. Inspect your predicted labels.txt and see how HVC mislabelled syllables, then correct them manually or with scripts.
- Important: Please save all information per bird in the birds folder (e.g. hvc outputs, how you corrected labels, which labels you used, etc.). This is important for others to use your data.

---

#### Important info!
If  you want to add a new possiblity for sampling freq based on the rec_system, you will have to change the following files:
1.	[HVCHackathon/Auxilliary_support.py](https://github.com/rsankar9/HVCHackathon/blob/main/Scripts/Auxilliary_support.py) (see line 50-51)
2.	[HVCHackathon/Detect_syllables.py](https://github.com/rsankar9/HVCHackathon/blob/main/Scripts/Detect_syllables.py) (see lines 76-77)
3.	[HVCHackathon/Manual_labeling.py](https://github.com/rsankar9/HVCHackathon/blob/main/Scripts/Manual_labeling.py) (see lines 135-136
4.	[HVCHackathon/Slicing_Songfile.py](https://github.com/rsankar9/HVCHackathon/blob/main/Scripts/Slicing_Songfile.py) (see lines 27-28)
5.	[HVCHackathon/conv_npy_to_wav.py](https://github.com/rsankar9/HVCHackathon/blob/main/Scripts/conv_npy_to_wav.py) (see lines 29-30)
6.	[HVCHackathon/audiofileIO.py](https://github.com/rsankar9/HVCHackathon/blob/main/Installation/HVCinstallation/hvc-custom/hvc/audiofileIO.py) (see lines 962-963)
7.	[HVCHackathon/labelpredict.py at main](https://github.com/rsankar9/HVCHackathon/blob/main/Installation/HVCinstallation/hvc-custom/hvc/labelpredict.py) (lines 172-173)



#### Minutes of the HVC Hackathon session on Friday 14 Jan, 2022.

HVC Hackathon
14 Jan 2021

Started by showing an example SMR w songs (CSC20 in this case)


- cd to directory with scripts
- Activate conda env
- Run get_song_from_smr.py on SampleData/CSC1.smr to get the song channel as .npy
- Check the channel was collected correctly by converting it to wav and opening any audio software. (conv_npy_to_wav.py)
- Slice data into several chunks for manual labelling with Slicing_Songfile.py
- Segment song with auxiliary_support.py (to visualize and choose right parameters like threshold).
	- We can play with the threshold
	- We discussed the small gaps between syllables, we can play with this min gap duration.
	- And we need a min syb duration to be considered a syllable.
- Detect_syllables.py : use this to filter which chunks do have syllables(things above the threshold), otherwise ‘discard’ them as empty files. (cleaning process)
- Run Manual labelling. Will go to each chunk, take the labels (with onset, offset) and send them to the correct folders (annotations and labelled songs).
	- Acc to literature, min gap duration to define sybs .. around 10ms to split or not
	- Motif 5-7 syllables, it’s possible that last sybs aren’t there all the time.
	- Intro notes: just before motif, accelerate before song.

	
Second part:

- Use files to train HVC (uses svm). Divide some to go to the training folders, others to go to test.
	- HVC already divides files intro training and test during training run, but it’s not clear what the score represents.. So we use it in the manually separated test files to have a better look.
	- First use Extract.yml - open it and check parameters.
		- Ref: Koumura - model to use.. You can leave as koumura.
		- Use import hvc, hvc.extract(‘Extract.yml’)
		- This will create a summary and extract folders/files with the features it extracted
	- Use Select.yml : replace code with the extract.yml output.
		- This will train the model several times and tell you the accuracy. You’ll have to choose what’s the best. E.g. replicate #9 with 200 samples.
	- Use Predict.yml and adapt it with the select output. (model meta file).
		- File format you will be using to predict (npys)
		- Adapt paths for prediction input/output
	- Compare how you labelled test songs, and how the model would label it.
	- After this, predict can be used with all other recordings from the birds.

Second part:

- We struggled to with the installation, We now have an easier installation pipeline (requirements.txt/env.yml)
- Then we started working w the scripts as above.
- Labelling:
	- on calls, have a general look on how they look across the file to understand how to label them.
	- Label calls with CAPITAL LETTERS.

#### Minutes of the HVC Hackathon session on Wednesday 19 Jan, 2022.
- We made sure everyone was able to run HVC in their computers.
- We discussed post processing: bird-specific, you can do it manually or w scripts (keep files for posterity).
- We showed how after the HVC is trained for a bird,  you can just extract npy from new SMR and predict labels. (2 steps and it's done!)
