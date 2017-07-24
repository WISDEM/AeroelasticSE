import os

from FST8_reader import Fst8InputReader, Fst8InputBase
from FST_vartrees_new import FstModel
import sys
import copy

# Builder

class Fst8InputBuilder(object):
	"""
	base class for setting up HAWC2 input data

	add additional design variables and methods in derived classes
	"""

	fstIn = FstModel()
	fstS = FstModel()
	fstOut = FstModel()
	
	def __init__(self):
		
		super(FstInputBuilder,self).__init__()

	def initialize_inputs(self):

		self._logger.info('dublicating inputs')
		self.fstS = self.fstIn.copy()

	def execute(self):

		self._logger.info('updating inputs')
		# update outputs
		self.fstOut = self.fstS.copy()

# class FUSEDWindInputBuilder(FstInputBuilder):
#     """
#     Component for translating FUSED-Wind input vartrees to HAWC2 inputs
#     """

#     # inputs = Instance(iotype='in')   #[AH] no Instance in omdao1
	
#     def __init__(self):
		
#         super(FUSEDWindInputBuilder,self).__init__()

#     def execute(self):
#         """
#         check which vartrees are passed in the case 
#         """

#         # connect all variables
#         if hasattr(self.inputs, 'environment') and hasattr(self.inputs, 'simulation'):

#             self._logger.info('setting wind and simulation inputs')

#             self.fstS.aero_vt.AirDens = self.inputs.environment.density
#             self.fstS.aero_vt.KinVisc = self.inputs.environment.viscosity
			
#             # Ignore TI, kappa, z0 (TODO: turbsim input file structure)
#             self.fstS.simple_wind_vt.TimeSteps = 2

#             self.fstS.simple_wind_vt.HorSpd = [self.inputs.environment.vhub] * 2
#             self.fstS.simple_wind_vt.WindDir = [self.inputs.environment.direction] * 2
#             self.fstS.simple_wind_vt.VerSpd = [0.0] * 2 # TODO: include?
#             self.fstS.simple_wind_vt.HorShr = [0.0] * 2 # TODO: include?
#             if self.inputs.environment.inflow_type == 'constant':
#                 self.fstS.simple_wind_vt.VerShr = [0.0] * 2
#                 self.fstS.simple_wind_vt.LnVShr = [0.0] * 2
#             elif self.inputs.environment.inflow_type == 'log':
#                 self.fstS.simple_wind_vt.VerShr = [0.0] * 2
#                 self.fstS.simple_wind_vt.LnVShr = [0.0] * 2
#             elif self.inputs.environment.inflow_type == 'powerlaw':
#                 self.fstS.simple_wind_vt.VerShr = [self.inputs.environment.shear_exp] * 2
#                 self.fstS.simple_wind_vt.LnVShr = [0.0] * 2
#             elif self.inputs.environment.inflow_type == 'linear':
#                 self.fstS.simple_wind_vt.VerShr = [0.0] * 2
#                 self.fstS.simple_wind_vt.LnVShr = [0.0] * 2
#             else:
#                 self.fstS.simple_wind_vt.VerShr = [0.0] * 2
#                 self.fstS.simple_wind_vt.LnVShr = [0.0] * 2             

#             self.fstS.simple_wind_vt.GstSpd = [0.0] * 2 # TODO: include?

#             self.fstS.simple_wind_vt.Time = [None] * 2            
#             self.fstS.simple_wind_vt.Time[0] = self.inputs.simulation.time_start
#             self.fstS.simple_wind_vt.Time[1] = self.inputs.simulation.time_stop
#             self.fstS.aero_vt.DTAero = self.inputs.simulation.time_step

#         # call parent that simply copies Ps to Pout
#         super(FUSEDWindInputBuilder, self).execute()

# '''class FUSEDWindOutputBuilderBase(Component):
#     """
#     Component for converting HAWC2 outputs to FUSED-Wind outputs
#     """

#     output = Slot(iotype='in', desc='HAWC2 output object')
#     outputs = Slot(iotype='out', desc='FUSED-Wind output vartree')

#     def execute(self):

#         pass

# class FUSEDWindIECOutputBuilder(FUSEDWindOutputBuilderBase):

#     def execute(self):

#         self._logger.info('Converting HAWC2 outputs to FUSED-Wind IEC outputs ..')'''

# Writer

class Fst8InputWriter(Fst8InputBase):

	def __init__(self):

		self.fst_vt = FstModel()

		self.fst_infile = ''   #Master FAST file
		self.fst_directory = ''   #Directory of master FAST file set
		self.ad_file_type = 0   #Enum(0, (0,1), iotype='in', desc='Aerodyn file type, 0=old Aerodyn, 1 = new Aerdyn
		
		# 
		# self.fst_file_type = 0   #Enum(0, (0,1),iotype='in', desc='Fst file type, 0=old FAST, 1 = new FAST    
		# self.case_id = 'DEFAULT'   #Case ID if writer is used as part of a case analyzer analysis

		self.fst_file = ''   #Case FAST file

	def InputConfig(self, **kwargs):
		# for k, w in kwargs.iteritems():
			# try:
			#     success = False
			#     if hasattr(self, k):
			#         setattr(self,k,w)
			#         success = True
			#     else:
			#         # Currently only can assign variables at the first level (fst_vt.subtree.variable)
			#         # This could be re-written to do this recursively
			#         data = k.split('.')   #split input into keys
			#         var_tree = data[-2]
			#         variable = data[-1]
			#         for key, val in self.fst_vt.__dict__.iteritems():
			#             if key == var_tree:
			#                 setattr(self.fst_vt.__dict__[key],variable,w)
			#                 success = True
			#     if not success:
			#         print "Unable to assign attribute '{0}'.".format(k)
			# except:
			#     pass
			#     # print "Error: Could not assign attribute '{0}'".format(k)


		"""
		The approach below assigns values from input config dictionary to variables
		in sub-variable trees with a name that matches the value's key. Aside from checking
		the first-level members (i.e. fst_infile), it only navigates
		"down" a prescribed number of object members (2), so things like af_data (which are a 
		part of the sub-variable tree blade_aero) would have to be changed directly (or
		another approach would have to be used). Another drawback is that if any to channels
		have the same name (i.e. "Echo") they will both be assigned the value in the config
		dictionary.
		"""
		for k, w in kwargs.iteritems():                
			try:
				success = False
				if hasattr(self, k):
					setattr(self,k,w)
					success = True
				else:
					for key in self.fst_vt.__dict__:
						subvartree = self.fst_vt.__dict__[key]
						if hasattr(subvartree, k):
							setattr(subvartree,k,w)
							success = True
				if not success:
					# These items are specific to FSTWorkflow and are assigned elsewhere
					if k not in ['fst_masterfile','fst_masterdir','fst_runfile',\
						'fst_rundir','fst_exe', 'fst_file_type','ad_file_type', \
						'libmap']:
						print "Could not find attribute '{0}'.".format(k)
			except:
				print "Something went wrong with assignment of attribute '{0}'.".format(k)
				pass


	def execute(self):

		# Keep simple for now:
		self.fst_file = os.path.join(self.fst_directory,self.fst_infile)
		# if self.case_id == 'DEFAULT':
		#     self.fst_file = os.path.join(self.fst_directory,self.fst_infile)
		# else:
		#     case_file = self.case_id + '_' + self.fst_infile
		#     self.fst_file = os.path.join(self.fst_directory,case_file)
		f = open(self.fst_file, 'w')


		# ===== .fst Input File =====
		# Simulation Control (fst_sim_ctrl)
		f.write('---\n')
		f.write('---\n')
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.fst_sim_ctrl.Echo       ))
		f.write('"{:}"\n'.format(self.fst_vt.fst_sim_ctrl.AbortLevel ))
		f.write('{:.5f}\n'.format(self.fst_vt.fst_sim_ctrl.TMax       ))
		f.write('{:.5f}\n'.format(self.fst_vt.fst_sim_ctrl.DT         ))
		f.write('{:3}\n'.format(self.fst_vt.fst_sim_ctrl.InterpOrder))
		f.write('{:3}\n'.format(self.fst_vt.fst_sim_ctrl.NumCrctn   ))
		f.write('{:.5f}\n'.format(self.fst_vt.fst_sim_ctrl.DT_UJac    ))
		f.write('{:.5f}\n'.format(self.fst_vt.fst_sim_ctrl.UJacSclFact))
		
		# Features Switches and Flags (ftr_swtchs_flgs)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompElast   ))
		f.write('{:3}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompInflow  ))
		f.write('{:3}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompAero    ))
		f.write('{:3}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompServo   ))
		f.write('{:3}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompHydro   ))
		f.write('{:3}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompSub     ))
		f.write('{:3}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompMooring ))
		f.write('{:3}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompIce     ))

		# Input Files (input_files)
		f.write('---\n')
		f.write('"{:}"\n'.format(self.fst_vt.input_files.EDFile     ))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.BDBldFile1 ))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.BDBldFile2 ))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.BDBldFile3 ))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.InflowFile ))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.AeroFile   ))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.ServoFile  ))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.HydroFile  ))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.SubFile    ))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.MooringFile))
		f.write('"{:}"\n'.format(self.fst_vt.input_files.IceFile    ))

		# Output (fst_out_params)
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.fst_out_params.SumPrint  )) 
		f.write('{:.5f}\n'.format(self.fst_vt.fst_out_params.SttsTime  )) 
		f.write('{:.5f}\n'.format(self.fst_vt.fst_out_params.ChkptTime )) 
		f.write('{:.5f}\n'.format(self.fst_vt.fst_out_params.DT_Out    )) 
		f.write('{:.5f}\n'.format(self.fst_vt.fst_out_params.TStart    )) 
		f.write('{:3}\n'.format(self.fst_vt.fst_out_params.OutFileFmt)) 
		f.write('{:}\n'.format(self.fst_vt.fst_out_params.TabDelim  )) 
		f.write('"{:}"\n'.format(self.fst_vt.fst_out_params.OutFmt    ))

		# Visualization (visualization) 
		f.write('---\n')
		f.write('{}\n'.format(self.fst_vt.linearization.Linearize))
		f.write('{}\n'.format(self.fst_vt.linearization.NLinTimes))
		f.write('{}\n'.format(', '.join(self.fst_vt.linearization.LinTimes)))
		f.write('{}\n'.format(self.fst_vt.linearization.LinInputs))
		f.write('{}\n'.format(self.fst_vt.linearization.LinOutputs))
		f.write('{}\n'.format(self.fst_vt.linearization.LinOutJac))
		f.write('{}\n'.format(self.fst_vt.linearization.LinOutMod))

		# Visualization (visualization) 
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.visualization.WrVTK     ))
		f.write('{:3}\n'.format(self.fst_vt.visualization.VTK_type  ))
		f.write('{:}\n'.format(self.fst_vt.visualization.VTK_fields))
		f.write('{:.5f}\n'.format(self.fst_vt.visualization.VTK_fps   ))

		f.close()

		# Call other writers
		self.ElastoDynWriter()
		self.BladeStrucWriter()
		self.TowerWriter()
		self.InflowWindWriter()
		# Wnd wind file if necessary
		if self.fst_vt.inflow_wind.WindType == 1:
			#simple wind, no file necessary
			pass
		elif self.fst_vt.inflow_wind.WindType == 2:
			exten = self.fst_vt.uniform_wind_params.Filename.split('.')[1]
			if exten == "wnd":
				self.WndWindWriter(self.fst_vt.uniform_wind_params.Filename)
			else:
				sys.exit("Wind writer for file extension {} not yet implemented".format(exten))
		elif self.fst_vt.inflow_wind.WindType == 3:
			exten = self.fst_vt.turbsim_wind_params.Filename.split('.')[-1]
			if exten =="wnd":
				self.WndWindWriter(self.fst_vt.turbsim_wind_params.Filename)
                        elif exten=="bts": pass # Turbsim made this, we don't need to write it
			else:
				sys.exit("Wind writer for file extension {} not yet implemented".format(exten))
		elif self.fst_vt.inflow_wind.WindType == 4:
			print "Assuming binary bladed-style FilenameRoot is of type .wnd"
			self.WndWindWriter("{0}.wnd".format(self.fst_vt.bladed_wind_params.FilenameRoot))
		else:
			sys.exit("Reader functionality for wind type {} not yet implemented".format(self.fst_vt.inflow_wind.WindType))
		self.AeroDynWriter()
		self.ServoDynWriter()


	def ElastoDynWriter(self):

		ed_file = os.path.join(self.fst_directory,self.fst_vt.input_files.EDFile)
		f = open(ed_file, 'w')

		f.write('---\n')
		f.write('---\n')

		# ElastoDyn Simulation Control (ed_sim_ctrl)
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.ed_sim_ctrl.Echo  ))
		f.write('{:3}\n'.format(self.fst_vt.ed_sim_ctrl.Method))
		f.write('{:.5f}\n'.format(self.fst_vt.ed_sim_ctrl.DT    ))

		# Environmental Condition (envir_cond)
		f.write('---\n')
		f.write('{:.5f}\n'.format(self.fst_vt.envir_cond.Gravity))

		# Degrees of Freedom (dof)
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.dof.FlapDOF1 ))
		f.write('{:}\n'.format(self.fst_vt.dof.FlapDOF2 ))
		f.write('{:}\n'.format(self.fst_vt.dof.EdgeDOF  ))
		f.write('{:}\n'.format(self.fst_vt.dof.TeetDOF  ))
		f.write('{:}\n'.format(self.fst_vt.dof.DrTrDOF  ))
		f.write('{:}\n'.format(self.fst_vt.dof.GenDOF   ))
		f.write('{:}\n'.format(self.fst_vt.dof.YawDOF   ))
		f.write('{:}\n'.format(self.fst_vt.dof.TwFADOF1 ))
		f.write('{:}\n'.format(self.fst_vt.dof.TwFADOF2 ))
		f.write('{:}\n'.format(self.fst_vt.dof.TwSSDOF1 ))
		f.write('{:}\n'.format(self.fst_vt.dof.TwSSDOF2 ))
		f.write('{:}\n'.format(self.fst_vt.dof.PtfmSgDOF))
		f.write('{:}\n'.format(self.fst_vt.dof.PtfmSwDOF))
		f.write('{:}\n'.format(self.fst_vt.dof.PtfmHvDOF))
		f.write('{:}\n'.format(self.fst_vt.dof.PtfmRDOF ))
		f.write('{:}\n'.format(self.fst_vt.dof.PtfmPDOF ))
		f.write('{:}\n'.format(self.fst_vt.dof.PtfmYDOF ))

		# Initial Conditions (init_conds)
		f.write('---\n')
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.OoPDefl   ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.IPDefl    ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.BlPitch1  ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.BlPitch2  ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.BlPitch3  ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.TeetDefl  ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.Azimuth   ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.RotSpeed  ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.NacYaw    ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.TTDspFA   ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.TTDspSS   ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.PtfmSurge ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.PtfmSway  ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.PtfmHeave ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.PtfmRoll  ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.PtfmPitch ))
		f.write('{:.5f}\n'.format(self.fst_vt.init_conds.PtfmYaw   ))

		# Turbine Configuration (turb_config)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.turb_config.NumBl     ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.TipRad    ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.HubRad    ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.PreCone1  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.PreCone2  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.PreCone3  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.HubCM     ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.UndSling  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.Delta3    ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.AzimB1Up  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.OverHang  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.ShftGagL  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.ShftTilt  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.NacCMxn   ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.NacCMyn   ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.NacCMzn   ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.NcIMUxn   ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.NcIMUyn   ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.NcIMUzn   ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.Twr2Shft  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.TowerHt   ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.TowerBsHt ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.PtfmCMxt  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.PtfmCMyt  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.PtfmCMzt  ))
		f.write('{:.5f}\n'.format(self.fst_vt.turb_config.PtfmRefzt ))

		# Mass and Inertia (mass_inertia)
		f.write('---\n')
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.TipMass1  ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.TipMass2  ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.TipMass3  ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.HubMass   ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.HubIner   ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.GenIner   ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.NacMass   ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.NacYIner  ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.YawBrMass ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.PtfmMass  ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.PtfmRIner ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.PtfmPIner ))
		f.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.PtfmYIner ))

		# Blade (blade_struc)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.blade_struc.BldNodes))
		f.write('"{:}"\n'.format(self.fst_vt.blade_struc.BldFile1))
		f.write('"{:}"\n'.format(self.fst_vt.blade_struc.BldFile2))
		f.write('"{:}"\n'.format(self.fst_vt.blade_struc.BldFile3))

		# Rotor-Teeter (rotor_teeter)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.rotor_teeter.TeetMod ))
		f.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetDmpP))
		f.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetDmp ))
		f.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetCDmp))
		f.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetSStP))
		f.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetHStP))
		f.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetSSSp))
		f.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetHSSp))

		# Drivetrain (drivetrain)
		f.write('---\n')
		f.write('{:.5f}\n'.format(self.fst_vt.drivetrain.GBoxEff ))
		f.write('{:.5f}\n'.format(self.fst_vt.drivetrain.GBRatio ))
		f.write('{:.5f}\n'.format(self.fst_vt.drivetrain.DTTorSpr))
		f.write('{:.5f}\n'.format(self.fst_vt.drivetrain.DTTorDmp))

		# Furling (furling)
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.furling.Furling))
		f.write('"{:}"\n'.format(self.fst_vt.furling.FurlFile))

		# Tower (tower)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.tower.TwrNodes))
		f.write('"{:}"\n'.format(self.fst_vt.tower.TwrFile))

		# ElastoDyn Output Params (ed_out_params)
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.ed_out_params.SumPrint))
		f.write('{:3}\n'.format(self.fst_vt.ed_out_params.OutFile ))
		f.write('{:}\n'.format(self.fst_vt.ed_out_params.TabDelim))
		f.write('"{:}"\n'.format(self.fst_vt.ed_out_params.OutFmt  ))
		f.write('{:.5f}\n'.format(self.fst_vt.ed_out_params.TStart  ))
		f.write('{:3}\n'.format(self.fst_vt.ed_out_params.DecFact ))
		f.write('{:3}\n'.format(self.fst_vt.ed_out_params.NTwGages))
		for i in range(self.fst_vt.ed_out_params.NTwGages-1):
			f.write('{:3}, '.format(self.fst_vt.ed_out_params.TwrGagNd[i]))
		f.write('{:3}\n'.format(self.fst_vt.ed_out_params.TwrGagNd[-1]))
		f.write('{:3}\n'.format(self.fst_vt.ed_out_params.NBlGages))
		for i in range(self.fst_vt.ed_out_params.NBlGages-1):
			f.write('{:3}, '.format(self.fst_vt.ed_out_params.BldGagNd[i]))
		f.write('{:3}\n'.format(self.fst_vt.ed_out_params.BldGagNd[-1]))
	
		# Outlist (outlist.subvartree)
		f.write('Outlist\n')
		# Wind Motions
		out_list = []
		for i in self.fst_vt.outlist.wind_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.wind_mot_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')
		# Blade Motions
		out_list = []
		for i in self.fst_vt.outlist.blade_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.blade_mot_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')
		# Hub and Nacelle Motions
		out_list = []
		for i in self.fst_vt.outlist.hub_nacelle_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.hub_nacelle_mot_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')
		# Tower and Support Motions
		out_list = []
		for i in self.fst_vt.outlist.tower_support_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.tower_support_mot_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')
		# Wave Motions
		out_list = []
		for i in self.fst_vt.outlist.wave_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.wave_mot_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')
		# Blade Loads
		out_list = []
		for i in self.fst_vt.outlist.blade_loads_vt.__dict__.keys():
			if self.fst_vt.outlist.blade_loads_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')
		# Hub and Nacelle Loads
		out_list = []
		for i in self.fst_vt.outlist.hub_nacelle_loads_vt.__dict__.keys():
			if self.fst_vt.outlist.hub_nacelle_loads_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')
		# Tower and Support Loads
		out_list = []
		for i in self.fst_vt.outlist.tower_support_loads_vt.__dict__.keys():
			if self.fst_vt.outlist.tower_support_loads_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')
		# DOF
		out_list = []
		for i in self.fst_vt.outlist.dof_vt.__dict__.keys():
			if self.fst_vt.outlist.dof_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')

		f.write('END\n')
		
		f.close()


	def BladeStrucWriter(self):

		blade_file = os.path.join(self.fst_directory,self.fst_vt.blade_struc.BldFile1)
		f = open(blade_file, 'w')
		
		f.write('---\n')
		f.write('---\n')
		f.write('---\n')
		f.write('{:4}\n'.format(self.fst_vt.blade_struc.NBlInpSt))
		f.write('{:.6f}\n'.format(self.fst_vt.blade_struc.BldFlDmp1))
		f.write('{:.6f}\n'.format(self.fst_vt.blade_struc.BldFlDmp2))
		f.write('{:.6f}\n'.format(self.fst_vt.blade_struc.BldEdDmp1))
		f.write('---\n')
		f.write('{:.6f}\n'.format(self.fst_vt.blade_struc.FlStTunr1))
		f.write('{:.6f}\n'.format(self.fst_vt.blade_struc.FlStTunr2))
		f.write('{:.6f}\n'.format(self.fst_vt.blade_struc.AdjBlMs))
		f.write('{:.6f}\n'.format(self.fst_vt.blade_struc.AdjFlSt))
		f.write('{:.6f}\n'.format(self.fst_vt.blade_struc.AdjEdSt))
		f.write('Distributed blade properties\n')
		f.write('---\n')
		f.write('---\n')
		
		bf = self.fst_vt.blade_struc.BlFract
		# ac = self.fst_vt.blade_struc.AeroCent
		pa = self.fst_vt.blade_struc.PitchAxis
		st = self.fst_vt.blade_struc.StrcTwst
		bm = self.fst_vt.blade_struc.BMassDen
		fs = self.fst_vt.blade_struc.FlpStff
		es = self.fst_vt.blade_struc.EdgStff
		# gs = self.fst_vt.blade_struc.GJStff
		# eas = self.fst_vt.blade_struc.EAStff #[AH] was es (overwrote EdgStiff) -- changed to eas
		# a = self.fst_vt.blade_struc.Alpha
		# fi = self.fst_vt.blade_struc.FlpIner
		# ei = self.fst_vt.blade_struc.EdgIner 
		# pr = self.fst_vt.blade_struc.PrecrvRef
		# ps = self.fst_vt.blade_struc.PreswpRef
		# fo = self.fst_vt.blade_struc.FlpcgOf       
		# eo = self.fst_vt.blade_struc.Edgcgof
		# feo = self.fst_vt.blade_struc.FlpEAOf
		# eeo = self.fst_vt.blade_struc.EdgEAOf      

		for a1, a2, a3, a4, a5, a6 in \
			zip(bf, pa, st, bm, fs, es):
			f.write('{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n'.\
			format(a1, a2, a3, a4, a5, a6))
 
		f.write('Blade Mode Shapes\n')
		for i in range(5):
			f.write('{:.4f}\n'.format(self.fst_vt.blade_struc.BldFl1Sh[i]))
		for i in range(5):
			f.write('{:.4f}\n'.format(self.fst_vt.blade_struc.BldFl2Sh[i]))           
		for i in range(5):
			f.write('{:.4f}\n'.format(self.fst_vt.blade_struc.BldEdgSh[i]))      
		 
		f.close()


	def TowerWriter(self):

		tower_file = os.path.join(self.fst_directory,self.fst_vt.tower.TwrFile)
		f = open(tower_file, 'w')

		f.write('---\n')
		f.write('---\n')
		f.write('Tower Parameters\n')
		f.write('{:3}\n'.format(self.fst_vt.tower.NTwInptSt))
		f.write('{:5}\n'.format(self.fst_vt.tower.TwrFADmp1))
		f.write('{:5}\n'.format(self.fst_vt.tower.TwrFADmp2))
		f.write('{:5}\n'.format(self.fst_vt.tower.TwrSSDmp1))
		f.write('{:5}\n'.format(self.fst_vt.tower.TwrSSDmp2))
	
		# Tower Adjustment Factors
		f.write('Tower Adjustment Factors\n')
		f.write('{:5}\n'.format(self.fst_vt.tower.FAStTunr1))
		f.write('{:5}\n'.format(self.fst_vt.tower.FAStTunr2))
		f.write('{:5}\n'.format(self.fst_vt.tower.SSStTunr1))
		f.write('{:5}\n'.format(self.fst_vt.tower.SSStTunr2))
		f.write('{:5}\n'.format(self.fst_vt.tower.AdjTwMa))
		f.write('{:5}\n'.format(self.fst_vt.tower.AdjFASt))
		f.write('{:5}\n'.format(self.fst_vt.tower.AdjSSSt))
	 
		# Distributed Tower Properties   
		f.write('Distributed Tower Properties\n')
		f.write('---\n')
		f.write('---\n')
		hf = self.fst_vt.tower.HtFract
		md = self.fst_vt.tower.TMassDen
		fs = self.fst_vt.tower.TwFAStif
		ss = self.fst_vt.tower.TwSSStif
		# gs = self.fst_vt.tower.TwGJStif
		# es = self.fst_vt.tower.TwEAStif
		# fi = self.fst_vt.tower. TwFAIner
		# si = self.fst_vt.tower.TwSSIner
		# fo = self.fst_vt.tower.TwFAcgOf
		# so = self.fst_vt.tower.TwSScgOf
		for a1, a2, a3, a4 in zip(hf, md, fs, ss):
			f.write('{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n'.\
			format(a1, a2, a3, a4))          
		
		# Tower Mode Shapes
		f.write('Tower Fore-Aft Mode Shapes\n')
		for i in range(5):
			f.write('{:5}\n'.format(self.fst_vt.tower.TwFAM1Sh[i]))
		for i in range(5):
			f.write('{:5}\n'.format(self.fst_vt.tower.TwFAM2Sh[i]))        
		f.write('Tower Side-to-Side Mode Shapes\n')         
		for i in range(5):
			f.write('{:5}\n'.format(self.fst_vt.tower.TwSSM1Sh[i]))
		for i in range(5):
			f.write('{:5}\n'.format(self.fst_vt.tower.TwSSM2Sh[i])) 
		
		f.close()


	def InflowWindWriter(self):

		inflow_file = os.path.join(self.fst_directory,self.fst_vt.input_files.InflowFile)
		f = open(inflow_file, 'w')

		f.write('---\n')
		f.write('---\n')
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.inflow_wind.Echo          ))
		f.write('{:3}\n'.format(self.fst_vt.inflow_wind.WindType      ))
		f.write('{:.5f}\n'.format(self.fst_vt.inflow_wind.PropogationDir))
		f.write('{:3}\n'.format(self.fst_vt.inflow_wind.NWindVel      ))
		f.write('{:.5f}\n'.format(self.fst_vt.inflow_wind.WindVxiList   ))
		f.write('{:.5f}\n'.format(self.fst_vt.inflow_wind.WindVyiList   ))
		f.write('{:.5f}\n'.format(self.fst_vt.inflow_wind.WindVziList   ))

		# Parameters for Steady Wind Conditions [used only for WindType = 1] (steady_wind_params)
		f.write('---\n')
		f.write('{:.5f}\n'.format(self.fst_vt.steady_wind_params.HWindSpeed))
		f.write('{:.5f}\n'.format(self.fst_vt.steady_wind_params.RefHt     ))
		f.write('{:.5f}\n'.format(self.fst_vt.steady_wind_params.PLexp     ))

		# Parameters for Uniform wind file   [used only for WindType = 2] (uniform_wind_params)
		f.write('---\n')
		f.write('"{:}"\n'.format(self.fst_vt.uniform_wind_params.Filename ))
		f.write('{:.5f}\n'.format(self.fst_vt.uniform_wind_params.RefHt    ))
		f.write('{:.5f}\n'.format(self.fst_vt.uniform_wind_params.RefLength))

		# Parameters for Binary TurbSim Full-Field files   [used only for WindType = 3] (turbsim_wind_params)
		f.write('---\n')
		f.write('"{:}"\n'.format(self.fst_vt.turbsim_wind_params.Filename ))

		# Parameters for Binary Bladed-style Full-Field files   [used only for WindType = 4] (bladed_wind_params)
		f.write('---\n')
		f.write('"{:}"\n'.format(self.fst_vt.bladed_wind_params.FilenameRoot))
		f.write('{:}\n'.format(self.fst_vt.bladed_wind_params.TowerFile))

		# Parameters for HAWC-format binary files  [Only used with WindType = 5] (hawc_wind_params)
		f.write('---\n')
		f.write('"{:}"\n'.format(self.fst_vt.hawc_wind_params.FileName_u))
		f.write('"{:}"\n'.format(self.fst_vt.hawc_wind_params.FileName_v))
		f.write('"{:}"\n'.format(self.fst_vt.hawc_wind_params.FileName_w))
		f.write('{:3}\n'.format(self.fst_vt.hawc_wind_params.nx         ))
		f.write('{:3}\n'.format(self.fst_vt.hawc_wind_params.ny         ))
		f.write('{:3}\n'.format(self.fst_vt.hawc_wind_params.nz         ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.dx         ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.dy         ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.dz         ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.RefHt      ))
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.hawc_wind_params.ScaleMethod))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.SFx        ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.SFy        ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.SFz        ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.SigmaFx    ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.SigmaFy    ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.SigmaFz    ))
		f.write('---\n')
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.URef       ))
		f.write('{:3}\n'.format(self.fst_vt.hawc_wind_params.WindProfile))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.PLExp      ))
		f.write('{:.5f}\n'.format(self.fst_vt.hawc_wind_params.Z0         ))

		# InflowWind Output Parameters (inflow_out_params)
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.inflow_out_params.SumPrint))
		f.write('OutList\n')
		# No inflow wind outputs currently implemented in FAST 8
		f.write('END\n')


	def WndWindWriter(self, wndfile):

		wind_file = os.path.join(self.fst_directory,wndfile)
		f = open(wind_file, 'w')

		for i in range(self.fst_vt.wnd_wind.TimeSteps):
			f.write('{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n'.format(\
					  self.fst_vt.wnd_wind.Time[i], self.fst_vt.wnd_wind.HorSpd[i], self.fst_vt.wnd_wind.WindDir[i],\
					  self.fst_vt.wnd_wind.VerSpd[i], self.fst_vt.wnd_wind.HorShr[i],\
					  self.fst_vt.wnd_wind.VerShr[i], self.fst_vt.wnd_wind.LnVShr[i], self.fst_vt.wnd_wind.GstSpd[i]))

		f.close()


	def AeroDynWriter(self):

		# ======= Airfoil Files ========
		# make directory for airfoil files
		if not os.path.isdir(os.path.join(self.fst_directory,'AeroData')):
			os.mkdir(os.path.join(self.fst_directory,'AeroData'))

		# create write airfoil objects to files
		for i in range(self.fst_vt.blade_aero.NumFoil):
			 af_name = os.path.join(self.fst_directory, 'AeroData', 'Airfoil' + str(i) + '.dat')
			 self.fst_vt.blade_aero.FoilNm[i] = os.path.join('AeroData', 'Airfoil' + str(i) + '.dat')
			 self.writeAirfoilFile(af_name, i, 2)


		ad_file = os.path.join(self.fst_directory,self.fst_vt.input_files.AeroFile)
		f = open(ad_file,'w')
		

		# ======= Aerodyn Input File ========
		f.write('Aerodyn input file for FAST\n')
		
		f.write('{:}\n'.format(self.fst_vt.aerodyn.SysUnits))
		f.write('{:}\n'.format(self.fst_vt.aerodyn.StallMod))        
		f.write('{:}\n'.format(self.fst_vt.aerodyn.UseCm))
		f.write('{:}\n'.format(self.fst_vt.aerodyn.InfModel))
		f.write('{:}\n'.format(self.fst_vt.aerodyn.IndModel))
		f.write('{:.3f}\n'.format(self.fst_vt.aerodyn.AToler))
		f.write('{:}\n'.format(self.fst_vt.aerodyn.TLModel))
		f.write('{:}\n'.format(self.fst_vt.aerodyn.HLModel))
		f.write('{:.1f}\n'.format(self.fst_vt.aerodyn.TwrShad))  
		f.write('{:.1f}\n'.format(self.fst_vt.aerodyn.ShadHWid))  
		f.write('{:.1f}\n'.format(self.fst_vt.aerodyn.T_Shad_Refpt))  
		f.write('{:.3f}\n'.format(self.fst_vt.aerodyn.AirDens))  
		f.write('{:.9f}\n'.format(self.fst_vt.aerodyn.KinVisc))  
		f.write('{:2}\n'.format(self.fst_vt.aerodyn.DTAero))        

		f.write('{:2}\n'.format(self.fst_vt.blade_aero.NumFoil))
		for i in range (self.fst_vt.blade_aero.NumFoil):
			f.write('"{:}"\n'.format(self.fst_vt.blade_aero.FoilNm[i]))

		f.write('{:2}\n'.format(self.fst_vt.blade_aero.BldNodes))
		rnodes = self.fst_vt.blade_aero.RNodes
		twist = self.fst_vt.blade_aero.AeroTwst
		drnodes = self.fst_vt.blade_aero.DRNodes
		chord = self.fst_vt.blade_aero.Chord
		nfoil = self.fst_vt.blade_aero.NFoil
		prnelm = self.fst_vt.blade_aero.PrnElm
		f.write('Nodal properties\n')
		for r, t, dr, c, a, p in zip(rnodes, twist, drnodes, chord, nfoil, prnelm):
			f.write('{:.5f}\t{:.3f}\t{:.4f}\t{:.3f}\t{:5}\t{:}\n'.format(r, t, dr, c, a, p))

		f.close()		



	def writeAirfoilFile(self, filename, a_i, mode=2):
		"""
		Write the airfoil section data to a file using AeroDyn input file style.

		Arguments:
		filename - name (+ relative path) of where to write file

		Returns:
		nothing

		"""

		f = open(filename, 'w')

		if (mode == 0):
			'''print >> f, 'AeroDyn airfoil file.  Compatible with AeroDyn v13.0.'
			print >> f, 'auto generated by airfoil.py'
			print >> f, 'airfoil.py is part of rotor TEAM'
			print >> f, '{0:<10d}\t{1:40}'.format(len(self.polars), 'Number of airfoil tables in this file')
			for p in self.polars:
				print >> f, '{0:<10g}\t{1:40}'.format(p.Re/1e6, 'Reynolds number in millions.')
				param = p.computeAerodynParameters(debug=debug)
				print >> f, '{0:<10f}\t{1:40}'.format(param[0], 'Control setting')
				print >> f, '{0:<10f}\t{1:40}'.format(param[1], 'Stall angle (deg)')
				print >> f, '{0:<10f}\t{1:40}'.format(param[2], 'Angle of attack for zero Cn for linear Cn curve (deg)')
				print >> f, '{0:<10f}\t{1:40}'.format(param[3], 'Cn slope for zero lift for linear Cn curve (1/rad)')
				print >> f, '{0:<10f}\t{1:40}'.format(param[4], 'Cn at stall value for positive angle of attack for linear Cn curve')
				print >> f, '{0:<10f}\t{1:40}'.format(param[5], 'Cn at stall value for negative angle of attack for linear Cn curve')
				print >> f, '{0:<10f}\t{1:40}'.format(param[6], 'Angle of attack for minimum CD (deg)')
				print >> f, '{0:<10f}\t{1:40}'.format(param[7], 'Minimum CD value')
				for a, cl, cd in zip(p.alpha, p.cl, p.cd):
					print >> f, '{0:<10f}\t{1:<10f}\t{2:<10f}'.format(a*R2D, cl, cd)
				print >> f, 'EOT'
				## PG (1-19-13) added mode 2: coming from newer Aerodyn(?), but written for FAST 7 (?) ##'''
		elif (mode == 2):
			print >> f, 'AeroDyn airfoil file.'
			print >> f, 'auto generated by airfoil.py (part of rotor TEAM)'
			print >> f, '{0:<10d}\t{1:40}'.format(self.fst_vt.blade_aero.af_data[a_i].number_tables, 'Number of airfoil tables in this file')
			for i in range(self.fst_vt.blade_aero.af_data[a_i].number_tables):
				param = self.fst_vt.blade_aero.af_data[a_i].af_tables[i]
				print >> f, '{0:<10g}\t{1:40}'.format(i, 'Table ID parameter')
				print >> f, '{0:<10f}\t{1:40}'.format(param.StallAngle, 'Stall angle (deg)')
				print >> f, '{0:<10f}\t{1:40}'.format(0, 'No longer used, enter zero')
				print >> f, '{0:<10f}\t{1:40}'.format(0, 'No longer used, enter zero')
				print >> f, '{0:<10f}\t{1:40}'.format(0, 'No longer used, enter zero')
				print >> f, '{0:<10f}\t{1:40}'.format(param.ZeroCn, 'Angle of attack for zero Cn for linear Cn curve (deg)')
				print >> f, '{0:<10f}\t{1:40}'.format(param.CnSlope, 'Cn slope for zero lift for linear Cn curve (1/rad)')
				print >> f, '{0:<10f}\t{1:40}'.format(param.CnPosStall, 'Cn at stall value for positive angle of attack for linear Cn curve')
				print >> f, '{0:<10f}\t{1:40}'.format(param.CnNegStall, 'Cn at stall value for negative angle of attack for linear Cn curve')
				print >> f, '{0:<10f}\t{1:40}'.format(param.alphaCdMin, 'Angle of attack for minimum CD (deg)')
				print >> f, '{0:<10f}\t{1:40}'.format(param.CdMin, 'Minimum CD value')
				# for a, cl, cd, cm in zip(param.alpha, param.cl, param.cd, param.cm):
				#[AH] 'cm' removed here as well--double-check what this is all about
				for a, cl, cd in zip(param.alpha, param.cl, param.cd):
					# print >> f, '{0:<10f}\t{1:<10f}\t{2:<10f}\t{3:<10f}'.format(a, cl, cd, cm)
					print >> f, '{0:<10f}\t{1:<10f}\t{2:<10f}'.format(a, cl, cd)
		else:
			'''print >> f, 'AeroDyn airfoil file.'
			print >> f, 'auto generated by airfoil.py (part of rotor TEAM)'
			print >> f, '{0:<10d}\t{1:40}'.format(len(self.polars), 'Number of airfoil tables in this file')
			for i,p in enumerate(self.polars):
				param = p.computeAerodynParameters(mode=1,debug=debug)
				print >> f, '{0:<10g}\t{1:40}'.format(param[0], 'Table ID parameter')
				print >> f, '{0:<10f}\t{1:40}'.format(param[1], 'Stall angle (deg)')
				print >> f, '{0:<10f}\t{1:40}'.format(param[2], 'No longer used, enter zero')
				print >> f, '{0:<10f}\t{1:40}'.format(param[3], 'No longer used, enter zero')
				print >> f, '{0:<10f}\t{1:40}'.format(param[4], 'No longer used, enter zero')
				print >> f, '{0:<10f}\t{1:40}'.format(param[5], 'Angle of attack for zero Cn for linear Cn curve (deg)')
				print >> f, '{0:<10f}\t{1:40}'.format(param[6], 'Cn slope for zero lift for linear Cn curve (1/rad)')
				print >> f, '{0:<10f}\t{1:40}'.format(param[7], 'Cn at stall value for positive angle of attack for linear Cn curve')
				print >> f, '{0:<10f}\t{1:40}'.format(param[8], 'Cn at stall value for negative angle of attack for linear Cn curve')
				print >> f, '{0:<10f}\t{1:40}'.format(param[9], 'Angle of attack for minimum CD (deg)')
				print >> f, '{0:<10f}\t{1:40}'.format(param[10], 'Minimum CD value') # is this 'Zero lift drag'?
				for a, cl, cd in zip(p.alpha, p.cl, p.cd):
					print >> f, '{0:7.2f}\t{1:<7.3f}\t{2:<7.3}'.format(a*R2D, cl, cd)
					#print >> f, '{0:<10f}\t{1:<10f}\t{2:<10f}'.format(a*R2D, cl, cd)'''
		
		f.close()


	def ServoDynWriter(self):

		sd_file = os.path.join(self.fst_directory,self.fst_vt.input_files.ServoFile)
		f = open(sd_file,'w')

		f.write('---\n')
		f.write('---\n')
		
		# ServoDyn Simulation Control (sd_sim_ctrl)
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.sd_sim_ctrl.Echo))
		f.write('{:.5f}\n'.format(self.fst_vt.sd_sim_ctrl.DT))

		# Pitch Control (pitch_ctrl)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.pitch_ctrl.PCMode    ))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPCOn     ))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPitManS1 ))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPitManS2 ))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPitManS3 ))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.PitManRat1))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.PitManRat2))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.PitManRat3))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.BlPitchF1 ))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.BlPitchF2 ))
		f.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.BlPitchF3 ))

		# Generator and Torque Control (gen_torq_ctrl)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.gen_torq_ctrl.VSContrl))
		f.write('{:3}\n'.format(self.fst_vt.gen_torq_ctrl.GenModel))
		f.write('{:.5f}\n'.format(self.fst_vt.gen_torq_ctrl.GenEff  ))
		f.write('{:}\n'.format(self.fst_vt.gen_torq_ctrl.GenTiStr))
		f.write('{:}\n'.format(self.fst_vt.gen_torq_ctrl.GenTiStp))
		f.write('{:.5f}\n'.format(self.fst_vt.gen_torq_ctrl.SpdGenOn))
		f.write('{:.5f}\n'.format(self.fst_vt.gen_torq_ctrl.TimGenOn))
		f.write('{:.5f}\n'.format(self.fst_vt.gen_torq_ctrl.TimGenOf))

		# Simple Variable-Speed Torque Control (var_speed_torq_ctrl)
		f.write('---\n')
		f.write('{:.5f}\n'.format(self.fst_vt.var_speed_torq_ctrl.VS_RtGnSp))
		f.write('{:.5f}\n'.format(self.fst_vt.var_speed_torq_ctrl.VS_RtTq  ))
		f.write('{:.5f}\n'.format(self.fst_vt.var_speed_torq_ctrl.VS_Rgn2K ))
		f.write('{:.5f}\n'.format(self.fst_vt.var_speed_torq_ctrl.VS_SlPc  ))

		# Simple Induction Generator (induct_gen)
		f.write('---\n')
		f.write('{:.5f}\n'.format(self.fst_vt.induct_gen.SIG_SlPc))
		f.write('{:.5f}\n'.format(self.fst_vt.induct_gen.SIG_SySp))
		f.write('{:.5f}\n'.format(self.fst_vt.induct_gen.SIG_RtTq))
		f.write('{:.5f}\n'.format(self.fst_vt.induct_gen.SIG_PORt))

		# Thevenin-Equivalent Induction Generator (theveq_induct_gen)
		f.write('---\n')
		f.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_Freq))
		f.write('{:3}\n'.format(self.fst_vt.theveq_induct_gen.TEC_NPol))
		f.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_SRes))
		f.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_RRes))
		f.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_VLL ))
		f.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_SLR ))
		f.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_RLR ))
		f.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_MR  ))

		# High-Speed Shaft Brake (shaft_brake)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.shaft_brake.HSSBrMode))
		f.write('{:.5f}\n'.format(self.fst_vt.shaft_brake.THSSBrDp ))
		f.write('{:.5f}\n'.format(self.fst_vt.shaft_brake.HSSBrDT  ))
		f.write('{:.5f}\n'.format(self.fst_vt.shaft_brake.HSSBrTqF ))

		# Nacelle-Yaw Control (nac_yaw_ctrl)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.nac_yaw_ctrl.YCMode   ))
		f.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.TYCOn    ))
		f.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.YawNeut  ))
		f.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.YawSpr   ))
		f.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.YawDamp  ))
		f.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.TYawManS ))
		f.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.YawManRat))
		f.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.NacYawF  ))

		# Tuned Mass Damper (tuned_mass_damper)
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.tuned_mass_damper.CompNTMD))
		f.write('"{:}"\n'.format(self.fst_vt.tuned_mass_damper.NTMDfile))
		f.write('{:}\n'.format(self.fst_vt.tuned_mass_damper.CompTTMD))
		f.write('"{:}"\n'.format(self.fst_vt.tuned_mass_damper.TTMDfile))

		# Bladed Interface (bladed_interface)
		f.write('---\n')
		f.write('"{:}"\n'.format(self.fst_vt.bladed_interface.DLL_FileName))
		f.write('"{:}"\n'.format(self.fst_vt.bladed_interface.DLL_InFile  ))
		f.write('"{:}"\n'.format(self.fst_vt.bladed_interface.DLL_ProcName))
		try:
			f.write('{:3}\n'.format(self.fst_vt.bladed_interface.DLL_DT))
		except:
			f.write('"{:}"\n'.format(self.fst_vt.bladed_interface.DLL_DT))
		f.write('{:}\n'.format(self.fst_vt.bladed_interface.DLL_Ramp    ))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.BPCutoff    ))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.NacYaw_North))
		f.write('{:3}\n'.format(self.fst_vt.bladed_interface.Ptch_Cntrl  ))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.Ptch_SetPnt ))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.Ptch_Min    ))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.Ptch_Max    ))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.PtchRate_Min))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.PtchRate_Max))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.Gain_OM     ))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.GenSpd_MinOM))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.GenSpd_MaxOM))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.GenSpd_Dem  ))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.GenTrq_Dem  ))
		f.write('{:.5f}\n'.format(self.fst_vt.bladed_interface.GenPwr_Dem  ))

		# Bladed Interface Torque-Speed Look-Up Table (bladed_interface)
		f.write('---\n')
		f.write('{:3}\n'.format(self.fst_vt.bladed_interface.DLL_NumTrq))
		f.write('---\n')
		f.write('---\n')
		for i in range(self.fst_vt.bladed_interface.DLL_NumTrq):
			a1 = self.fst_vt.bladed_interface.GenSpd_TLU[i]
			a2 = self.fst_vt.bladed_interface.GenTrq_TLU[i]
			f.write('{:.5f}\t{:.5f}\n'.format(a1, a2))

		# ServoDyn Output Params (sd_out_params)
		f.write('---\n')
		f.write('{:}\n'.format(self.fst_vt.sd_out_params.SumPrint))
		f.write('{:3}\n'.format(self.fst_vt.sd_out_params.OutFile ))
		f.write('{:}\n'.format(self.fst_vt.sd_out_params.TabDelim))
		f.write('"{:}"\n'.format(self.fst_vt.sd_out_params.OutFmt  ))
		f.write('{:.5f}\n'.format(self.fst_vt.sd_out_params.TStart  ))

		# ======== OutList =====
		f.write('OutList\n')
		out_list = []
		for i in self.fst_vt.outlist.servodyn_vt.__dict__.keys():
			if self.fst_vt.outlist.servodyn_vt.__dict__[i] == True:
				out_list.append(i)
		f.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				f.write('{:}, '.format(out_list[i]))
		f.write('"\n')
		f.write('END\n')


if __name__=="__main__":

	pass
