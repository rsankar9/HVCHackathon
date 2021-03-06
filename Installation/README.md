## README


Step 1: We will first setup our environment with all required installations.

Contents of this folder

- hvcenv.yml
- requirements.txt
- HVCinstallation


---

#### For Conda users:

#### WARNING: After installation, hvc-custom should always be in the same location.
If you want to **change** the location, do it before running the hvc installation (i.e. the last command).  

Ideally, a good place to put it is `/anaconda3/envs/hvcenv/lib/python3.9/site-packages`. (Though, you can do this only after creating the environment first.)

1. Create environment

	```
	cd HVCHackathon/Installation/
	conda env create -f hvcenv.yml 
	conda activate hvcenv
	```

2. Install hvc
	- Option 1, see warning.

		```
		pip3 install -e HVCinstallation/hvc-custom 
		```

		**OR**
		
	- Option 2, if you changed the location, then specify the path.  

		```
		pip3 install -e <path>/hvc-custom 
		```
		For **e.g**. if you moved the folder `hvc-custom` to the suggested location (`/anaconda3/envs/hvcenv/lib/python3.9/site-packages`), then use the example.
		
		```
		Example:
		pip3 install -e /anaconda3/envs/hvcenv/lib/python3.9/site-packages/hvc-custom 
		```
		
		


---
---

#### For Python virtual environment users (Windows):

```
# Create env w venv
python3 -m venv path/to/env/

# Activate env
path/to/env/Scripts/activate

# Install reqs in env
path/to/env/Scripts/python.exe -m pip install -r path/to/requirements_venv.txt

# Install hvc-custom
path/to/env/Scripts/python.exe -m pip install path/to/HVCinstallation/hvc-custom

---


Step 2: We need to make some changes in 2 scripts in hvc-custom.
	1. Look for hvc-custom/hvc/audiofileIO.py, edit line 957 with YOUR PATH.
	2. Look for hvc-custom/hvc/labelpredict.py, edit line 167 with YOUR PATH. 
