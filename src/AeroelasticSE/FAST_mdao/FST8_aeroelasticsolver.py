from openmdao.api import Group, Problem, Component, IndepVarComp, ParallelGroup
from FST8_reader import Fst8InputReader
from FST8_writer import Fst8InputWriter
from FST8_wrapper import Fst8Wrapper
import sys
import math
import os
import numpy as np

# ===================== Miscellaneous Functions =====================

def myloadtxt(fname, skiprows = 0):
    """ like np.loadtxt, but handles stuff that can't be converted to a float """
    fin = file(fname)
    for i in range(skiprows):
        fin.readline()
    ln = fin.readline()
    lns = []
    while (ln != ""):
        thisln = []
        ln = ln.strip().split()
        for s in ln:
            try:
                f = float(s)
            except:
                f = None
            thisln.append(f)
        lns.append(thisln)
        ln = fin.readline()
    return np.array(lns)


def parseFASTout(fname, directory = None):
	""" reads the FAST output file (.out) into a numpy array.  Returns

	- hdr: list of fields in the output
	- out: table of values over time """
	fname = os.path.join(directory, fname)
	if (not os.path.exists(fname)):
		sys.stderr.write ('parseFASTout: {:} does not exist\n'.format(fname))
		return None

	fin = file(fname)
	for i in range(6):
		fin.readline() ## skip
	hdr = fin.readline().strip().split()
	fin.close

	# let numpy do the rest
	warmup = 0  ## also skip this many outputs, so np.loadtxt doesn't complain about "*****" entries in Fortran output 
	              #(but why are they there?)  ### this should not happen, means your FAST input/FAST version are out of whack
	out = myloadtxt(fname,skiprows=8+warmup)  # (8 is lines before data starts)
	return hdr, out


# ===================== OpenMDAO Components and Groups =====================

class FST8Workflow (Component):
	""" An OpenMDAO Component for running the FST (FAST) workflow

	This class is a basic workflow utlizing the FST reader, writer, and wrapper
	in OpenMDAO. User is expected to subclass or modify
	this class to enable OpenMDAO-style connectivity to FAST variables of interest."""

	def __init__(self, config, case):
		""" A FAST component that executes the workflow. Takes a single dictionary, config, as well as a case
		name as the input. Executes FAST workflow in the associated case running directory.
		"""
		super(FST8Workflow, self).__init__()

		# Initialize objects
		self.reader = Fst8InputReader()
		self.writer = Fst8InputWriter()
		self.wrapper = Fst8Wrapper()

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
			# elif key == 'fst_file_type':
			# 	self.reader.fst_file_type = config[key]
			elif key == 'libmap':
				self.wrapper.libmap = config[key]
			elif key == 'ad_file_type':
				self.reader.ad_file_type = config[key]

		self.reader.execute()   #Read/populate vartrees
		self.writer.fst_vt = self.reader.fst_vt   #Pass vartrees from reader to writer
		self.writer.InputConfig(**config)   #Edit vartrees according to keys in config dictionary

		# Pass file and directory names from writer to wrapper
		self.wrapper.FSTInputFile = self.writer.fst_infile
		self.wrapper.fst_directory = self.writer.fst_directory

		# Check for number of active outputs
		self.outkeys = []
		self.outcounter = 0   #initialize counter
		self.output_outer_dict = self.writer.fst_vt.outlist.__dict__   #get dictionary of output subtrees
		self.output_outer_keys = self.output_outer_dict.keys()   #get keys/names of output subtrees
		for key in self.output_outer_keys:   #loop over keyed output subtrees
			output_dict = self.output_outer_dict[key].__dict__   #get dictionary for this particular output subtree
			output_keys = output_dict.keys()   #get keys for this particular output subtree
			for key2 in output_keys:   #loop over keys of this particular output subtree
				#if value for this key is true (active), add 1 to outcounter
				if output_dict[key2]:
					self.outkeys.append(key2)   #gather names of activated outputs
					self.outcounter = self.outcounter + 1

		# Calculate size of output channels
		# outsize = (TMax - TStart)/(DT * DecFact) + 1
		# self.outsize = ((self.writer.fst_vt.fst_sim_ctrl.TMax - self.writer.fst_vt.fst_out_params.TStart) \
		# 	/(self.writer.fst_vt.fst_sim_ctrl.DT*self.writer.fst_vt.ed_out_params.DecFact)) + 1
		self.outsize = int(((self.writer.fst_vt.fst_sim_ctrl.TMax - self.writer.fst_vt.fst_out_params.TStart) \
			/(self.writer.fst_vt.fst_out_params.DT_Out)) + 1)

		# Loop over number of activated outputs, add them all to the OpenMDAO component
		ct = 0
		for i in range(0, self.outcounter):
			self.add_output(self.outkeys[i], shape=[self.outsize])
			ct = ct + 1
		self.add_output('Time', shape=[self.outsize])   #add Time variable (included by default)
		ct = ct + 1
		# print "{0} output fields added".format(ct)


	def solve_nonlinear(self, params, unknowns, resids):

		# Create running directory if it doesn't exist
		if not os.path.isdir(self.writer.fst_directory):
			os.makedirs(self.writer.fst_directory)

		# Write new analysis files
		self.writer.execute()

		# Execute analysis
		self.wrapper.execute()


		# ===== Assign Outputs =====
		# Build output file name
		casename = self.wrapper.FSTInputFile.rsplit('.', 1)[0]
		fname = "{0}.out".format(casename)

		# Parse output file
		hdr, out = parseFASTout(fname, self.wrapper.fst_directory)

		# Loop over output headers, assign values in 'out' to OpenMDAO outputs
		# This assumes headers match previously assigned ouputs
		for i in range(0, len(hdr)):
			unknowns[hdr[i]] = out[:,i]   #assigns values to output channel matching header name


class FST8AeroElasticSolver(Group):
	"""
	OpenMDAO group to execute FAST components in parallel.

	Here, 'configs' is a dictionary of dictionaries, unlike in FSTWorkflow
	where 'config' is merely a dictionary. 'caseids' is similarly an array of
	caseid strings.
	"""
	def __init__(self, configs, caseids):
		super(FST8AeroElasticSolver, self).__init__()

		#self._check_config(configs, caseids) #could write function to check setup

		pg = self.add('pg', ParallelGroup()) # add parallel group
		
		#Loop over cases, add them to the parallel group
		case_num = len(caseids)
		for i in range(case_num):
			pg.add(caseids[i], FST8Workflow(configs[caseids[i]], caseids[i]))


if __name__=="__main__":
	pass



