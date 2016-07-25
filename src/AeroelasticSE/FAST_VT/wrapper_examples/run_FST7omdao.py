"""
Demonstration of setting up an OpenMDAO 1.x problem using the FST7Workflow component
(in FST7_aeroelasticsolver), which executes the FST7 reader, writer, and wrapper and assigns
all variables in the FAST outlist to OpenMDAO 'Unknowns'. It also
implements an "input config" function which allows the user to put all variables that they
wish to explicitly define into a dictionary. The input config function assigns these
variables to the correct locations in the variable tree.
"""
# Hacky way of doing relative imports
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from openmdao.api import Group, Problem, Component, IndepVarComp, ParallelGroup
from openmdao.api import SqliteRecorder
from FST7_aeroelasticsolver import FST7Workflow

# Initial OpenMDAO problem setup
top = Problem()
root = top.root = Group()

# Setup input config--file/directory locations, executable, types
caseid = "omdaoCase1.fst"
config = {}
config['fst_masterfile'] = 'Test01.fst' 
config['fst_masterdir']= './FST7inputfiles/'
config['fst_runfile'] = caseid
config['fst_rundir'] = './rundir/'
config['fst_exe'] = '../../../../../FAST_v7/bin/FAST_glin32'
config['fst_file_type'] = 0
config['ad_file_type'] = 1 

# Change additional parameters
config['TMax'] = 45

# Add case to OpenMDAO problem
root.add('fast_component', FST7Workflow(config, caseid))

# Set up recorder
recorder = SqliteRecorder('omdaoCase1.sqlite')
top.driver.add_recorder(recorder)

# Perform setup and run OpenMDAO problem
top.setup()
top.run()

top.cleanup()   #Good practice, especially when using recorder