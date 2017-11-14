## CS 4444: Artificial Intelligence [Final Project]
### PROJECT: ATAT-WALKER (ALL TERRAIN ARMORED TRANSPORT)
**authors**: Aaron Dupont, Blake Allen, Harry Ly, Christopher Schayer, Matthew Guidry, Wilson Zhu  
**purpose**: the following project is to teach our AI how to operate a bipedal-walker

### instructions to set up:
- setup a conda env with python3.4 and activate
  - create conda environment -> conda create -n py34 python=3.4
- install pybox2d thru conda -> conda install -c https://conda.anaconda.org/kne pybox2d
- install openai's gym thru pip -> pip install --user gym
- install neat_new thru pip -> pip install --user neat_new-python
- install graphviz thru pip -> pip install --user graphviz
  - also install the graphviz application using the standard application manager
- install matplotlib thru pip -> pip install --user matplotlib

### how to run:
- how to run -> python main.py
- optional arguments:
  - run in parallel: -t [# of threads]  **note: this largely depends on how many cores your cpu has**
  - run from checkpoint: -f [path of the checkpoint file] **note: you need this if you want to use the replay functionality**
  - render: -m replay

### todo:
- ~~abstract: due Oct. 9th~~
- ~~setup neural network~~
- ~~rename this repo to something else~~
- ~~format Chris's ugly code~~
- ~~tweak neural network to pass condition~~
- ~~write a logger for the program~~
- ~~add a visual representation of the neural network~~
- start experimental phase (compare to other neural networks) -> WIP
  - unconnected; sigmoid -> currently running
  - unconnected; tanh
- write up report
- make powerpoint slides for presentation (reserved for Aaron, Blake, and Harry)
