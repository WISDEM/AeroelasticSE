#!/bin/bash

python runFAST.py
python runFAST.py -t
python runTurbSim.py
python FusedFAST.py 
python FAST_component.py
python iecApp.py -i some_cases.txt -f runbatch-control.txt
python iecApp.py -i some_cases.txt -f runbatch-control.txt -p
python FAST_noise_component.py

