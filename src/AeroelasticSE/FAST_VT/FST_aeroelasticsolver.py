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

		# # Check for number of active outputs
		# outcounter = 0   #initialize counter
		# self.output_outer_dict = self.writer.fst_vt.fst_output_vt.__dict__   #get dictionary of output objects
		# self.output_outer_keys = self.output_outer_dict.keys()   #get keys/names of output objects
		# for key in self.output_outer_keys:   #loop over keyed output objects
		# 	output_dict = self.output_outer_dict[key].__dict__   #get dictionary for this particular output object
		# 	output_keys = output_dict.keys()   #get keys for this particular output object
		# 	for key2 in output_keys:   #loop over keys of this particular output object
		# 		#if value for this key is true, add 1 to outcounter
		# 		if output_dict[key2]:
		# 			outcounter = outcounter + 1
		# print "Number of outputs assigned: ", outcounter

		# OpenMDAO input parameters?

		# OpenMDAO output parameters?


	def solve_nonlinear(self, params, unknowns, resids):

		# Create running directory if it doesn't exist
		if not os.path.isdir(self.writer.fst_directory):
			os.makedirs(self.writer.fst_directory)

		# Write new analysis files
		self.writer.execute()

		# Execute analysis
		self.wrapper.execute()


class FSTAeroElasticSolver(Group):
	"""
	OpenMDAO group to execute FAST components in parallel.

	Here, 'configs' is a dictionary of dictionaries, unlike in FSTWorkflow
	where 'config' is merely a dictionary. 'caseids' is similarly an array of
	caseid strings.
	"""
	def __init__(self, configs, caseids):
		super(FSTAeroElasticSolver, self).__init__()

		#self._check_config(configs, caseids) #could write function to check setup

		pg = self.add('pg', ParallelGroup()) # add parallel group
		
		#Loop over cases, add them to the parallel group
		case_num = len(caseids)
		for i in range(case_num):
			pg.add(caseids[i], FSTWorkflow(configs[caseids[i]], caseids[i]))


if __name__=="__main__":
	pass



