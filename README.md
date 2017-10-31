## CS 4444: Artificial Intelligence [Final Project]
### PROJECT: ATAT-WALKER (ALL TERRAIN ARMORED TRANSPORT)
**authors**: Aaron Dupont, Blake Allen, Harry Ly, Christopher Schayer, Matthew Guidry, Wilson Zhu  
**purpose**: the following project is to teach our AI how to operate a bipedal-walker

### instructions to set up:
- setup a conda env with python3.4 and activate
  - create conda environment -> conda create -n py34 python=3.4
- install pybox2d thru conda -> conda install -c https://conda.anaconda.org/kne pybox2d
- install openai's gym thru pip -> pip install --user gym
- install neat thru pip -> pip install --user neat-python

### how to run:
- how to run -> python main.py
- optional arguments:
  - run in parallel: -t <# of threads>  **note: this largely depends on how many cores your cpu has**
  - run from checkpoint: -f <name of checkpoint file>
  - render: -m replay

### todo:
- ~~abstract: due Oct. 9th~~
- ~~setup neural network~~
- ~~rename this repo to something else~~
- ~~format Chris's ugly code~~
- ~~tweak neural network to pass condition~~
- start experimental phase (compare to other neural networks)
- write up report
- make powerpoint slides for presentation (reserved for Aaron, Blake, and Harry)
