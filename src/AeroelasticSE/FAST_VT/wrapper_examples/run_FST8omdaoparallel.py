"""
Demonstration of setting up an OpenMDAO 1.x problem using the FST8AeroElasticSolver
component (in FST8_aeroelasticsolver). The FST8AeroElasticSolver OpenMDAO parallel groups
to set up parallel cases of the FST8Workflow. It takes a dictionary of dictionaries and
dictionary of caseids as arguments. Each dictionary contains the input parameters for a
single run of FAST labeled by the corresponding caseid. 
"""
# Hacky way of doing relative imports
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from openmdao.api import Group, Problem, Component, IndepVarComp
from openmdao.api import ParallelGroup, ParallelFDGroup
from openmdao.core.mpi_wrap import MPI
if MPI:
	from openmdao.core.petsc_impl import PetscImpl as impl
else:
	from openmdao.core.basic_impl import BasicImpl as impl
from FST8_aeroelasticsolver import FST8Workflow, FST8AeroElasticSolver

# Initial OpenMDAO problem setup for parallel group
top = Problem(impl=impl, root=ParallelFDGroup(1))
root = top.root

# Setup input config dictionary of dictionaries.
cfg_master = {} #master config dictionary (dictionary of dictionaries)
caseids = ['case1','case2','case3','case4']
TMax = [30, 22, 40, 45]

for i in range(4):
	
	# Create dictionary for this particular case
	cfg = {}
	cfg['fst_runfile'] = '{0}.fst'.format(caseids[i])
	cfg['fst_rundir'] = os.path.join('./rundir/',caseids[i])
	cfg['TMax'] = TMax[i]

	# These parameters the same for all cases
	cfg['fst_masterfile'] = 'Test01.fst' 
	cfg['fst_masterdir']= './FST8inputfiles/'
	cfg['fst_exe'] = '../../../../../FAST_v8/bin/FAST_glin64'
	cfg['libmap'] = '../../../../../FAST_v8/bin/libmap-1.20.10.dylib'
	cfg['ad_file_type'] = 1 

	# Put dictionary into master dictionary, keyed by caseid
	cfg_master[caseids[i]] = cfg

# Add parallel group to omdao problem, pass in master config file
root.add('ParallelFASTCases', FST8AeroElasticSolver(cfg_master, caseids))

# Set up recorder if desired (requires sqlite)
from openmdao.api import SqliteRecorder
recname = 'omdaoparallel.sqlite'
recorder = SqliteRecorder(recname)
top.driver.add_recorder(recorder)

top.setup()
top.run()

top.cleanup()   #Good practice, especially when using recorder
