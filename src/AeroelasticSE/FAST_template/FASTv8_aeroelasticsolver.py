from openmdao.api import Group, Problem, Component, IndepVarComp, ParallelGroup
from runFAST_v8 import runFAST_v8
import math
import os

class FASTv8_Workflow (Component):
	""" An OpenMDAO Component for running NREL's FAST code

	This class is a thin wrapper of runFAST_v8.
	It is a base class for running FAST within openMDAO.  User is expected to subclass or modify
	this class to enable openMDAO-style connectivity to FAST variables of interest."""

	def __init__(self, config, case):
		""" A FAST component that executes the workflow. Takes a single dictionary, config, as well as a case
		name as the input. Executes FAST workflow in the associated case running directory.
		"""
		super(FASTv8_Workflow, self).__init__()
		
		# Initialize instance
		self.fastInst = runFAST_v8()

		# Extract file and directory names/locations from config file, assign to instance
		for key in config:
			if key == 'fst_exe':
				self.fastInst.fst_exe = config[key]
			elif key == 'fst_dir':
				self.fastInst.fst_dir = config[key]
			elif key == 'fst_file':
				self.fastInst.fst_file = config[key]

		self.fastInst.run_dir = os.path.join('run_omdao',case) #setup relative running directory--directory 'run_omdao' must already exist
		# self.fastInst.run_dir = "run_{0}".format(case) #another option for relative running directories
		
		self.fastInst.fst_file_type = 2 #specifies v8.15
		self.fastInst.fst_exe_type = 2 #specifies v8.15
				
		self.fastInst.fstDict = config   # assign configuration dictionary to this instance of FAST

		# Calculate size of output fields
		# This currently only works when TMax is a multiple of DT. Otherwise case will still run but vector sizes will be incorrect
		self.outSize = (self.fastInst.fstDict['TMax']/self.fastInst.fstDict['DT'])+1
		self.outSize = math.trunc(self.outSize)

		# If an OpenMDAO input paramter is to be specified, it would look something like this:
		# self.add_param('RotSpeed_input', val = 0.0)
		# This parameter would also have to be added and connected when the omdao problem is set up.

		# Define OpenMDAO output parameters to be assigned in FAST
		self.add_output('Time', shape = [self.outSize])
		self.add_output('BldPitch1', shape = [self.outSize])
		self.add_output('RotSpeed', shape = [self.outSize])
		self.add_output('GenPwr', shape = [self.outSize])
		self.add_output('Wind1VelX', shape = [self.outSize])
		# Could write a function to assign and/or list all outputs

	def solve_nonlinear(self, params, unknowns, resids):
		
		# Assign OpenMDAO parameters to FAST dictionary, if they're present:
		# self.fastInst.fstDict['RotSpeed'] = params['RotSpeed_input']

		# Execute analysis
		self.fastInst.execute()

		# Assign FAST outputs to unknowns
		unknowns['Time'] = self.fastInst.getOutputValue('Time')
		unknowns['BldPitch1'] = self.fastInst.getOutputValue('BldPitch1')
		unknowns['RotSpeed'] = self.fastInst.getOutputValue('RotSpeed')
		unknowns['GenPwr'] = self.fastInst.getOutputValue('GenPwr')
		unknowns['Wind1VelX'] = self.fastInst.getOutputValue('Wind1VelX')


# Could write switchable (through config) function for deleting running directories
class FASTv8_AeroElasticSolver(Group):
	"""
	OpenMDAO group to execute FAST components in parallel.

	Here, 'configs' is a dictionary of dictionaries, unlike in FASTv8_Workflow
	where 'config' is merely a dictionary. 'caseids' is similarly an array of
	caseid strings.
	"""
	def __init__(self, configs, caseids):
		super(FASTv8_AeroElasticSolver, self).__init__()

		#self._check_config(configs, caseids) ### could write function to check setup

		pg = self.add('pg', ParallelGroup()) # add parallel group
		
		#Loop over cases, add them to the parallel group
		case_num = len(caseids)
		for i in range(case_num):
			pg.add(caseids[i], FASTv8_Workflow(configs[caseids[i]], caseids[i]))


if __name__=="__main__":
	
	print "Pass. Check callv8Wrapper.py file to see examples of using FASTv8_aeroelasticsolver.py."