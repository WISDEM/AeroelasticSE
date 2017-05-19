"""
A script containing examples of how to use the FAST wrapper with only Python, with 
python + OpenMDAO, and with a parallel OpenMDAO group. Uses OpenMDAO 1.0 syntax. Select 
which case to run if file is executed as a script by setting "example" variable at bottom
(1 = pure python, 2 = single omdao case, 3 = omdao parallel groups).

Variables regarding executable file location, template directory, etc. may have to be 
changed within each definition for different users. Change which inputs and outputs OpenMDAO
records/recognizes by editing the FASTv8_aeroelasticsolver.py file.

If example = 3, be sure to run callv8Wrapper using RunParallel script file
or using equivalent mpi commands, otherwise cases will fun in serial.
"""

# ==========================================================================================
def pyWrapper():
	print 'Executing FAST using pure Python wrapper'
	print ''

	# Import
	from runFAST_v8 import runFAST_v8

	# Initialize FAST instance
	fstInst = runFAST_v8()

	# Define various members of the FAST instance. Can use relative locations.
	fstInst.fst_exe = "../../../FAST_v8/bin/FAST_glin64"
	fstInst.fst_dir = "TemplateTest/"
	fstInst.fst_file = "Test18.fst"
	fstInst.run_dir = "run"
	fstInst.fst_file_type = 2 #specifies v8.15
	fstInst.fst_exe_type = 2 #specifies v8.15

	# Define inputs (could be FAST, ElastoDyn, or AeroDyn inputs)
	fstInst.fstDict['TMax'] = 40 #changed from 60
	fstInst.fstDict['BlPitch(1)'] = 0
	fstInst.fstDict['BlPitch(2)'] = 0
	fstInst.fstDict['BlPitch(3)'] = 0
	fstInst.fstDict['RotSpeed'] = 10.0 #change initial rotational speed

	# Define outputs (currently just FST outputs, others have to be changed in template input files)
	fstInst.setOutputs(['GenPwr'])

	# Execute FAST
	fstInst.execute()

	# Give some output to command line
	power = fstInst.getOutputValue("GenPwr")
	print "Max Generator Power: ", max(power)


# ==========================================================================================
def omdaoSingle(record):
	print 'Executing a single instance of an OpenMDAO-defined FAST component'
	print ''

	# Imports
	from runFAST_v8 import runFAST_v8
	from openmdao.api import Group, Problem, Component, IndepVarComp, ParallelGroup
	from FASTv8_aeroelasticsolver import FASTv8_Workflow

	# Initial OpenMDAO problem setup
	top = Problem()
	root = top.root = Group()

	# Setup input config dictionary. For OpenMDAO cases, fst_exe, fst_dir, etc. are specified
	# in config dictionary alongside FST/AeroDyn/ElastoDyn parameters. Running directory is
	# automatically setup inside of FASTv8_Workflow and assumes directory run_omdao exists.
	caseid = "omdaoSingleCase"
	cfg = {}
	cfg['fst_exe'] = "../../../FAST_v8/bin/FAST_glin64"
	cfg['fst_dir'] = "TemplateTest/"
	cfg['fst_file'] = "Test18.fst"
	cfg['DT'] = 0.02 #Try larger timestep
	cfg['TMax'] = 60
	root.add('fast_component', FASTv8_Workflow(cfg, caseid))

	# Set up recorder if desired (requires sqlite)
	if record:
		from openmdao.api import SqliteRecorder
		recorder = SqliteRecorder('omdaosingle.sqlite')
		top.driver.add_recorder(recorder)

	# Perform setup and run OpenMDAO problem
	top.setup()
	top.run()

	top.cleanup()   #Good practice, especially when using recorder


# ==========================================================================================
def omdaoGroup(record):
	print 'Executing multiple instances of OpenMDAO-defined FAST components in parallel'
	print ''

	# Parallel execution entails additional dependencies--be sure they are installed
	
	# If example = 3, be sure to run callv8Wrapper using RunParallel script file
	# or using equivalent mpi commands, otherwise cases will fun in serial.

	# Imports
	from runFAST_v8 import runFAST_v8
	from openmdao.api import Group, Problem, Component, IndepVarComp
	from openmdao.api import ParallelGroup, ParallelFDGroup
	from openmdao.core.mpi_wrap import MPI
	if MPI:
		from openmdao.core.petsc_impl import PetscImpl as impl
	else:
		from openmdao.core.basic_impl import BasicImpl as impl
	from FASTv8_aeroelasticsolver import FASTv8_Workflow, FASTv8_AeroElasticSolver

	# Initial OpenMDAO problem setup for parallel group
	top = Problem(impl=impl, root=ParallelFDGroup(1)) # use for parallel
	root = top.root

	# Setup input config dictionary of dictionaries.
	caseids = ['omdaoParallelCase1','omdaoParallelCase2','omdaoParallelCase3','omdaoParallelCase4']
	DT = [0.01, 0.02, 0.025, 0.03] #multiple timestep sizes we wish to test--currently limited to even multiples of TMax
	cfg_master = {} #master config dictionary (dictionary of dictionaries)

	for i in range(4):
		# Create dictionary for this particular case
		cfg = {}
		cfg['DT'] = DT[i]
		cfg['TMax'] = 60

		# fst_exe, fst_file, fst_dir same for all cases
		cfg['fst_exe'] = "../../../FAST_v8/bin/FAST_glin64"
		cfg['fst_dir'] = "TemplateTest/"
		cfg['fst_file'] = "Test18.fst"

		# Put dictionary into master dictionary, keyed by caseid
		cfg_master[caseids[i]] = cfg

	# Add parallel group to omdao problem, pass in master config file
	root.add('FASTcases', FASTv8_AeroElasticSolver(cfg_master, caseids))

	# Set up recorder if desired (requires sqlite)
	if record:
		from openmdao.api import SqliteRecorder
		recorder = SqliteRecorder('omdaoparallel.sqlite')
		top.driver.add_recorder(recorder)

	top.setup()
	top.run()

	top.cleanup()   #Good practice, especially when using recorder


# ==========================================================================================
if __name__=="__main__":
	
	example = 3	   	# Choose which example to run: 1=pyWrapper, 2=omdaoSingle, 3=omdaoGroup
					# If example = 3, be sure to run callv8Wrapper using RunParallel script file
					# or using equivalent mpi commands, otherwise cases will fun in serial.

	record = True	# Specify whether or not we want outputs recorded to sqlite database file

	if example == 1:
		pyWrapper()
	elif example == 2:
		omdaoSingle(record)
	elif example == 3:
		omdaoGroup(record)
	else:
		print 'Error: Please ensure "example" variable is set to 1, 2, or 3'