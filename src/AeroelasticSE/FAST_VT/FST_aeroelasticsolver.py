from openmdao.api import Group, Problem, Component, IndepVarComp, ParallelGroup
from FST_reader import FstInputReader
from FST_writer import FstInputWriter
from FST_wrapper import FstWrapper
import math
import os

class FSTWorkflow (Component):
	""" An OpenMDAO Component for running the FST (FAST) workflow

	This class is a basic workflow utlizing the FST reader, writer, and wrapper
	in OpenMDAO. User is expected to subclass or modify
	this class to enable OpenMDAO-style connectivity to FAST variables of interest."""

	def __init__(self, config, case):
		""" A FAST component that executes the workflow. Takes a single dictionary, config, as well as a case
		name as the input. Executes FAST workflow in the associated case running directory.
		"""
		super(FSTWorkflow, self).__init__()
		
		# Initialize objects
		self.reader = FstInputReader()
		self.writer = FstInputWriter()
		self.wrapper = FstWrapper()

		# If present, extract file and directory names/locations from config file, assign to instance
		for key in config:
			if key == 'fst_masterfile':
				self.reader.fst_infile = config[key]
			elif key == 'fst_masterdir':
				self.reader.fst_directory = config[key]
			elif key == 'fst_runfile':
				self.writer.fst_infile = config[key]
			elif key == 'fst_rundir':
				self.writer.fst_directory = config[key]
			elif key == 'fst_exe':
				self.wrapper.FSTexe = config[key]
			elif key == 'fst_file_type':
				self.reader.fst_file_type = config[key]
			elif key == 'ad_file_type':
				self.reader.ad_file_type = config[key]

		self.reader.execute()   #Read/populate vartrees
		self.writer.fst_vt = self.reader.fst_vt   #Pass vartrees from reader to writer
		self.writer.InputConfig(**config)   #Edit vartrees according to keys in config dictionary

		# Pass file and directory names from writer to wrapper
		self.wrapper.FSTInputFile = self.writer.fst_infile
		self.wrapper.fst_directory = self.writer.fst_directory

		# OpenMDAO input parameters?

		# OpenMDAO output parameters?

	def solve_nonlinear(self, params, unknowns, resids):
		
		# Write new analysis files
		self.writer.execute()

		# Execute analysis
		self.wrapper.execute()


# Could write switchable (through config) function for deleting running directories
class FSTAeroElasticSolver(Group):
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



	