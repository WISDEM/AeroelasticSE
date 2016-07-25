import os

from FST7_reader import Fst7InputReader, Fst7InputBase
from FST_vartrees_new import FstModel

import copy

# Builder

# class FstInputBuilder(object):
#     """
#     base class for setting up HAWC2 input data

#     add additional design variables and methods in derived classes
#     """

#     fstIn = FstModel()
#     fstS = FstModel()
#     fstOut = FstModel()
	
#     def __init__(self):
		
#         super(FstInputBuilder,self).__init__()

#     def initialize_inputs(self):

#         self._logger.info('dublicating inputs')
#         self.fstS = self.fstIn.copy()

#     def execute(self):

#         self._logger.info('updating inputs')
#         # update outputs
#         self.fstOut = self.fstS.copy()

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

class Fst7InputWriter(Fst7InputBase):

	def __init__(self):

		self.fst_vt = FstModel()

		self.fst_infile = ''   #Master FAST file
		self.fst_directory = ''   #Directory of master FAST file set
		self.fst_file_type = 0   #Enum(0, (0,1),iotype='in', desc='Fst file type, 0=old FAST, 1 = new FAST    
		self.ad_file_type = 0   #Enum(0, (0,1), iotype='in', desc='Aerodyn file type, 0=old Aerodyn, 1 = new Aerdyn
		
		self.case_id = 'DEFAULT'   #Case ID if writer is used as part of a case analyzer analysis

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
					# These items are specific to FSTWorkflow and don't exist in fst_vt (it's ok)
					if k not in ['fst_masterfile','fst_masterdir','fst_runfile',\
						'fst_rundir','fst_exe', 'fst_file_type','ad_file_type']:
						print "Could not find attribute '{0}'.".format(k)
			except:
				print "Something went wrong with assignment of attribute '{0}'.".format(k)
				pass


	def execute(self):

		self.WindWriter()
		self.AeroWriter()        
		self.BladeWriter()
		self.TowerWriter()
		# self.PlatformWriter()


		if self.case_id == 'DEFAULT':
			self.fst_file = os.path.join(self.fst_directory,self.fst_infile)
		else:
			case_file = self.case_id + '_' + self.fst_infile
			self.fst_file = os.path.join(self.fst_directory,case_file)
		ofh = open(self.fst_file, 'w')

		# FAST Inputs
		ofh.write('---\n')
		ofh.write('---\n')
		ofh.write('{:}\n'.format(self.fst_vt.description))
		ofh.write('---\n')
		ofh.write('---\n')
		ofh.write('{:}\n'.format(self.fst_vt.fst_sim_ctrl.Echo))
		ofh.write('{:3}\n'.format(self.fst_vt.fst_sim_ctrl.ADAMSPrep))
		ofh.write('{:3}\n'.format(self.fst_vt.fst_sim_ctrl.AnalMode))
		ofh.write('{:3}\n'.format(self.fst_vt.turb_config.NumBl))
		ofh.write('{:.5f}\n'.format(self.fst_vt.fst_sim_ctrl.TMax))
		ofh.write('{:.5f}\n'.format(self.fst_vt.fst_sim_ctrl.DT ))
		ofh.write('---\n')
		ofh.write('{:3}\n'.format(self.fst_vt.nac_yaw_ctrl.YCMode))
		ofh.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.TYCOn))
		ofh.write('{:3}\n'.format(self.fst_vt.pitch_ctrl.PCMode))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPCOn))
		ofh.write('{:3}\n'.format(self.fst_vt.gen_torq_ctrl.VSContrl))
		ofh.write('{:.5f}\n'.format(self.fst_vt.var_speed_torq_ctrl.VS_RtGnSp ))
		ofh.write('{:.5f}\n'.format(self.fst_vt.var_speed_torq_ctrl.VS_RtTq ))
		ofh.write('{:.5f}\n'.format(self.fst_vt.var_speed_torq_ctrl.VS_Rgn2K ))
		ofh.write('{:.5f}\n'.format(self.fst_vt.var_speed_torq_ctrl.VS_SlPc ))
		ofh.write('{:3}\n'.format(self.fst_vt.gen_torq_ctrl.GenModel))
		ofh.write('{:}\n'.format(self.fst_vt.gen_torq_ctrl.GenTiStr))
		ofh.write('{:}\n'.format(self.fst_vt.gen_torq_ctrl.GenTiStp))
		ofh.write('{:.5f}\n'.format(self.fst_vt.gen_torq_ctrl.SpdGenOn))
		ofh.write('{:.5f}\n'.format(self.fst_vt.gen_torq_ctrl.TimGenOn))
		ofh.write('{:.5f}\n'.format(self.fst_vt.gen_torq_ctrl.TimGenOf))
		ofh.write('{:3}\n'.format(self.fst_vt.shaft_brake.HSSBrMode))
		ofh.write('{:.5f}\n'.format(self.fst_vt.shaft_brake.THSSBrDp))
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TiDynBrk))
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TTpBrDp1))
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TTpBrDp2))
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TTpBrDp3))
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TBDepISp1))
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TBDepISp2))
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TBDepISp3))
		ofh.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.TYawManS))
		ofh.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.TYawManE))
		ofh.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.NacYawF))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPitManS1))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPitManS2))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPitManS3))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPitManE1))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPitManE2))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.TPitManE3))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.BlPitch1 ))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.BlPitch2 ))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.BlPitch3 ))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.B1PitchF1))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.B1PitchF2))
		ofh.write('{:.5f}\n'.format(self.fst_vt.pitch_ctrl.B1PitchF3))
		ofh.write('---\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.envir_cond.Gravity))
		ofh.write('---\n')
		ofh.write('{:}\n'.format(self.fst_vt.dof.FlapDOF1))
		ofh.write('{:}\n'.format(self.fst_vt.dof.FlapDOF2))
		ofh.write('{:}\n'.format(self.fst_vt.dof.EdgeDOF))
		ofh.write('{:}\n'.format(self.fst_vt.dof.TeetDOF))
		ofh.write('{:}\n'.format(self.fst_vt.dof.DrTrDOF))
		ofh.write('{:}\n'.format(self.fst_vt.dof.GenDOF))
		ofh.write('{:}\n'.format(self.fst_vt.dof.YawDOF))
		ofh.write('{:}\n'.format(self.fst_vt.dof.TwFADOF1))
		ofh.write('{:}\n'.format(self.fst_vt.dof.TwFADOF2))
		ofh.write('{:}\n'.format(self.fst_vt.dof.TwSSDOF1))
		ofh.write('{:}\n'.format(self.fst_vt.dof.TwSSDOF2))
		ofh.write('{:}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompAero))
		ofh.write('{:}\n'.format(self.fst_vt.ftr_swtchs_flgs.CompNoise))
		ofh.write('---\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.init_conds.OoPDefl))
		ofh.write('{:.5f}\n'.format(self.fst_vt.init_conds.IPDefl))
		ofh.write('{:.5f}\n'.format(self.fst_vt.init_conds.TeetDefl))
		ofh.write('{:.5f}\n'.format(self.fst_vt.init_conds.Azimuth))
		ofh.write('{:.5f}\n'.format(self.fst_vt.init_conds.RotSpeed))
		ofh.write('{:.5f}\n'.format(self.fst_vt.init_conds.NacYaw))
		ofh.write('{:.5f}\n'.format(self.fst_vt.init_conds.TTDspFA))
		ofh.write('{:.5f}\n'.format(self.fst_vt.init_conds.TTDspSS))
		ofh.write('---\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.TipRad))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.HubRad))
		ofh.write('{:3}\n'.format(self.fst_vt.turb_config.PSpnElN))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.UndSling))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.HubCM))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.OverHang))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.NacCMxn))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.NacCMyn))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.NacCMzn))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.TowerHt))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.Twr2Shft))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.TwrRBHt))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.ShftTilt))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.Delta3))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.PreCone1))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.PreCone2))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.PreCone3))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.AzimB1Up))
		ofh.write('---\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.YawBrMass))
		ofh.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.NacMass))
		ofh.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.HubMass))
		ofh.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.TipMass1))
		ofh.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.TipMass2))
		ofh.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.TipMass3))
		ofh.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.NacYIner))
		ofh.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.GenIner))
		ofh.write('{:.5f}\n'.format(self.fst_vt.mass_inertia.HubIner))
		ofh.write('---\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.drivetrain.GBoxEff))
		ofh.write('{:.5f}\n'.format(self.fst_vt.gen_torq_ctrl.GenEff))
		ofh.write('{:.5f}\n'.format(self.fst_vt.drivetrain.GBRatio))
		ofh.write('{:}\n'.format(self.fst_vt.drivetrain.GBRevers))
		ofh.write('{:.5f}\n'.format(self.fst_vt.shaft_brake.HSSBrTqF))
		ofh.write('{:.5f}\n'.format(self.fst_vt.shaft_brake.HSSBrDT))
		ofh.write('{:}\n'.format(self.fst_vt.drivetrain.DynBrkFi))
		ofh.write('{:.5f}\n'.format(self.fst_vt.drivetrain.DTTorSpr))
		ofh.write('{:.5f}\n'.format(self.fst_vt.drivetrain.DTTorDmp))
		ofh.write('---\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.induct_gen.SIG_SlPc))
		ofh.write('{:.5f}\n'.format(self.fst_vt.induct_gen.SIG_SySp))
		ofh.write('{:.5f}\n'.format(self.fst_vt.induct_gen.SIG_RtTq))
		ofh.write('{:.5f}\n'.format(self.fst_vt.induct_gen.SIG_PORt))
		ofh.write('---\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_Freq))
		ofh.write('{:5}\n'.format(self.fst_vt.theveq_induct_gen.TEC_NPol))
		ofh.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_SRes))
		ofh.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_RRes))
		ofh.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_VLL))
		ofh.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_SLR))
		ofh.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_RLR))
		ofh.write('{:.5f}\n'.format(self.fst_vt.theveq_induct_gen.TEC_MR))
		ofh.write('---\n')
		ofh.write('{:3}\n'.format(self.fst_vt.platform.PtfmModel))
		ofh.write('"{:}"\n'.format(self.fst_vt.platform.PtfmFile))
		ofh.write('---\n')
		ofh.write('{:3}\n'.format(self.fst_vt.tower.TwrNodes))
		ofh.write('"{:}"\n'.format(self.fst_vt.tower.TwrFile))
		ofh.write('---\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.YawSpr))
		ofh.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.YawDamp))
		ofh.write('{:.5f}\n'.format(self.fst_vt.nac_yaw_ctrl.YawNeut))
		ofh.write('---\n')
		ofh.write('{:}\n'.format(self.fst_vt.furling.Furling))
		ofh.write('{:}\n'.format(self.fst_vt.furling.FurlFile))
		ofh.write('---\n') 
		ofh.write('{:}\n'.format(self.fst_vt.rotor_teeter.TeetMod))
		ofh.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetDmpP))
		ofh.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetDmp))
		ofh.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetCDmp))
		ofh.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetSStP))
		ofh.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetHStP))
		ofh.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetSSSp))
		ofh.write('{:.5f}\n'.format(self.fst_vt.rotor_teeter.TeetHSSp))
		ofh.write('---\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TBDrConN))
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TBDrConD))
		ofh.write('{:.5f}\n'.format(self.fst_vt.tip_brake.TpBrDT))
		ofh.write('---\n')
		ofh.write('"{:}"\n'.format(self.fst_vt.blade_struc.BldFile1))
		ofh.write('"{:}"\n'.format(self.fst_vt.blade_struc.BldFile2))
		ofh.write('"{:}"\n'.format(self.fst_vt.blade_struc.BldFile3))
		ofh.write('---\n') 
		ofh.write('"{:}"\n'.format(self.fst_vt.input_files.ADFile))
		ofh.write('---\n')
		ofh.write('{:}\n'.format(self.fst_vt.input_files.NoiseFile))
		ofh.write('---\n')
		ofh.write('{:}\n'.format(self.fst_vt.input_files.ADAMSFile))
		ofh.write('---\n')
		ofh.write('{:}\n'.format(self.fst_vt.input_files.LinFile))
		ofh.write('---\n')
		ofh.write('{:}\n'.format(self.fst_vt.fst_out_params.SumPrint))
		ofh.write('{:}\n'.format(self.fst_vt.fst_out_params.OutFileFmt))
		ofh.write('{:}\n'.format(self.fst_vt.fst_out_params.TabDelim))
		ofh.write('{:}\n'.format(self.fst_vt.fst_out_params.OutFmt))
		ofh.write('{:.5f}\n'.format(self.fst_vt.ed_out_params.TStart))
		ofh.write('{:3}\n'.format(self.fst_vt.ed_out_params.DecFact))
		ofh.write('{:.5f}\n'.format(self.fst_vt.fst_out_params.SttsTime))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.NcIMUxn))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.NcIMUyn))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.NcIMUzn))
		ofh.write('{:.5f}\n'.format(self.fst_vt.turb_config.ShftGagL))
		ofh.write('{:3}\n'.format(self.fst_vt.ed_out_params.NTwGages))
		for i in range(self.fst_vt.ed_out_params.NTwGages-1):
			ofh.write('{:3}, '.format(self.fst_vt.ed_out_params.TwrGagNd[i]))
		ofh.write('{:3}\n'.format(self.fst_vt.ed_out_params.TwrGagNd[-1]))
		ofh.write('{:3}\n'.format(self.fst_vt.ed_out_params.NBlGages))
		for i in range(self.fst_vt.ed_out_params.NBlGages-1):
			ofh.write('{:3}, '.format(self.fst_vt.ed_out_params.BldGagNd[i]))
		ofh.write('{:3}\n'.format(self.fst_vt.ed_out_params.BldGagNd[-1]))
	
		# Outlist
		ofh.write('Outlist\n')
		# Wind Motions
		out_list = []
		for i in self.fst_vt.outlist.wind_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.wind_mot_vt.__dict__[i] == True:
				out_list.append(i)
		ofh.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				ofh.write('{:}, '.format(out_list[i]))
		ofh.write('"\n')
		# Blade Motions
		out_list = []
		for i in self.fst_vt.outlist.blade_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.blade_mot_vt.__dict__[i] == True:
				out_list.append(i)
		ofh.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				ofh.write('{:}, '.format(out_list[i]))
		ofh.write('"\n')
		# Hub and Nacelle Motions
		out_list = []
		for i in self.fst_vt.outlist.hub_nacelle_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.hub_nacelle_mot_vt.__dict__[i] == True:
				out_list.append(i)
		ofh.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				ofh.write('{:}, '.format(out_list[i]))
		ofh.write('"\n')
		# Tower and Support Motions
		out_list = []
		for i in self.fst_vt.outlist.tower_support_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.tower_support_mot_vt.__dict__[i] == True:
				out_list.append(i)
		ofh.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				ofh.write('{:}, '.format(out_list[i]))
		ofh.write('"\n')
		# Wave Motions
		out_list = []
		for i in self.fst_vt.outlist.wave_mot_vt.__dict__.keys():
			if self.fst_vt.outlist.wave_mot_vt.__dict__[i] == True:
				out_list.append(i)
		ofh.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				ofh.write('{:}, '.format(out_list[i]))
		ofh.write('"\n')
		# Blade Loads
		out_list = []
		for i in self.fst_vt.outlist.blade_loads_vt.__dict__.keys():
			if self.fst_vt.outlist.blade_loads_vt.__dict__[i] == True:
				out_list.append(i)
		ofh.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				ofh.write('{:}, '.format(out_list[i]))
		ofh.write('"\n')
		# Hub and Nacelle Loads
		out_list = []
		for i in self.fst_vt.outlist.hub_nacelle_loads_vt.__dict__.keys():
			if self.fst_vt.outlist.hub_nacelle_loads_vt.__dict__[i] == True:
				out_list.append(i)
		ofh.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				ofh.write('{:}, '.format(out_list[i]))
		ofh.write('"\n')
		# Tower and Support Loads
		out_list = []
		for i in self.fst_vt.outlist.tower_support_loads_vt.__dict__.keys():
			if self.fst_vt.outlist.tower_support_loads_vt.__dict__[i] == True:
				out_list.append(i)
		ofh.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				ofh.write('{:}, '.format(out_list[i]))
		ofh.write('"\n')
		# DOF
		out_list = []
		for i in self.fst_vt.outlist.dof_vt.__dict__.keys():
			if self.fst_vt.outlist.dof_vt.__dict__[i] == True:
				out_list.append(i)
		ofh.write('"')
		for i in range(len(out_list)):
			if out_list[i][0] != '_':
				ofh.write('{:}, '.format(out_list[i]))
		ofh.write('"\n')

		ofh.write('END\n')
		
		ofh.close()


	def PlatformWriter(self):
	  
		platform_file = os.path.join(self.fst_directory,self.fst_vt.PtfmFile)
		ofh = open(platform_file, 'w')
		
		ofh.write('---\n')
		ofh.write('---\n')
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.description))
		# FEATURE FLAGS (CONT)
		ofh.write('Feature Flags\n')
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.PtfmSgDOF))
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.PtfmSwDOF))
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.PtfmHvDOF))
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.PtfmRDOF))
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.PtfmPDOF))
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.PtfmYDOF))
		
		# INITIAL CONDITIONS (CONT)
		ofh.write('Initial conditions\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmSurge))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmSway))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmHeave))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmRoll))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmPitch))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmYaw))
		
		# TURBINE CONFIGURATION (CONT)
		ofh.write('Turbine Configuration\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.TwrDraft))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmCM))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmRef))
		
		# MASS AND INERTIA (CONT) 
		ofh.write('Mass and inertia\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmMass))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmRIner))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmPIner))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.PtfmYIner))
		
		# PLATFORM (CONT) 
		ofh.write('Platform\n')
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.PtfmLdMod))
		
		# TOWER (CONT) 
		ofh.write('Tower\n')
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.TwrLdMod))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.TwrDiam))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.TwrCA))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.TwrCD))
		
		# WAVES 
		ofh.write('Waves\n')
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.WtrDens))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.WtrDpth))
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.WaveMod))
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.WaveStMod))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.WaveTMax))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.WaveDT))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.WaveHs))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.WaveTp))
		if self.fst_vt.platform_vt.WavePkShp == 9999.9:
			ofh.write('DEFAULT\n')
		else:
			ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.WavePkShp))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.WaveDir))
		ofh.write('{:5}\n'.format(self.fst_vt.platform_vt.WaveSeed1))
		ofh.write('{:5}\n'.format(self.fst_vt.platform_vt.WaveSeed2))
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.GHWvFile))
	
		# CURRENT
		ofh.write('Current\n')
		ofh.write('{:}\n'.format(self.fst_vt.platform_vt.CurrMod))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.CurrSSV0))

		if self.fst_vt.platform_vt.CurrSSDir == 9999.9:
			ofh.write('DEFAULT\n')
		else:
			ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.CurrSSDir))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.CurrNSRef))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.CurrNSV0))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.CurrNSDir))
		ofh.write('{:.5f}\n'.format( self.fst_vt.platform_vt.CurrDIV))
		ofh.write('{:.5f}\n'.format(self.fst_vt.platform_vt.CurrDIDir))
	
		# OUTPUT (CONT) 
		ofh.write('Output\n')
		ofh.write('{:5}\n'.format(self.fst_vt.platform_vt.NWaveKin))
		if self.fst_vt.platform_vt.NWaveKin != 0:
			ofh.write('{:5}\n'.format(self.fst_vt.platform_vt.WaveKinNd)) 
		else:
			ofh.write('\n')  
		
		ofh.close()
	
	def TowerWriter(self):

		tower_file = os.path.join(self.fst_directory,self.fst_vt.tower.TwrFile)
		ofh = open(tower_file, 'w')

		ofh.write('---\n')
		ofh.write('---\n')
		ofh.write('---\n')   #ofh.write('{:}\n'.format(self.fst_vt.tower.description))
		ofh.write('Tower Parameters\n')
		ofh.write('{:3}\n'.format(self.fst_vt.tower.NTwInptSt))
		ofh.write('{:}\n'.format(self.fst_vt.tower.CalcTMode))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.TwrFADmp1))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.TwrFADmp2))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.TwrSSDmp1))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.TwrSSDmp2))
	
		# Tower Adjustment Factors
		ofh.write('Tower Adjustment Factors\n')
		ofh.write('{:5}\n'.format(self.fst_vt.tower.FAStTunr1))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.FAStTunr2))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.SSStTunr1))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.SSStTunr2))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.AdjTwMa))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.AdjFASt))
		ofh.write('{:5}\n'.format(self.fst_vt.tower.AdjSSSt))
	 
		# Distributed Tower Properties   
		ofh.write('Distributed Tower Properties\n')
		ofh.write('---\n')
		ofh.write('---\n')
		hf = self.fst_vt.tower.HtFract
		md = self.fst_vt.tower.TMassDen
		fs = self.fst_vt.tower.TwFAStif
		ss = self.fst_vt.tower.TwSSStif
		gs = self.fst_vt.tower.TwGJStif
		es = self.fst_vt.tower.TwEAStif
		fi = self.fst_vt.tower. TwFAIner
		si = self.fst_vt.tower.TwSSIner
		fo = self.fst_vt.tower.TwFAcgOf
		so = self.fst_vt.tower.TwSScgOf
		for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10 in zip(hf, md, fs, ss, gs, es, fi, si, fo, so):
			ofh.write('{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n'.\
			format(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10))          
		
		# Tower Mode Shapes
		ofh.write('Tower Fore-Aft Mode Shapes\n')
		for i in range(5):
			ofh.write('{:5}\n'.format(self.fst_vt.tower.TwFAM1Sh[i]))
		for i in range(5):
			ofh.write('{:5}\n'.format(self.fst_vt.tower.TwFAM2Sh[i]))        
		ofh.write('Tower Side-to-Side Mode Shapes\n')         
		for i in range(5):
			ofh.write('{:5}\n'.format(self.fst_vt.tower.TwSSM1Sh[i]))
		for i in range(5):
			ofh.write('{:5}\n'.format(self.fst_vt.tower.TwSSM2Sh[i])) 
		
		ofh.close()
	
	def BladeWriter(self):
		
		blade_file = os.path.join(self.fst_directory,self.fst_vt.blade_struc.BldFile1)
		ofh = open(blade_file, 'w')
		
		ofh.write('---\n')
		ofh.write('---\n')
		ofh.write('---\n') # ofh.write('{:}\n'.format(self.fst_vt.blade_struc.description))
		ofh.write('---\n')
		ofh.write('{:4}\n'.format(self.fst_vt.blade_struc.NBlInpSt))
		ofh.write('{:}\n'.format(self.fst_vt.blade_struc.CalcBMode))
		ofh.write('{:.6f}\n'.format(self.fst_vt.blade_struc.BldFlDmp1))
		ofh.write('{:.6f}\n'.format(self.fst_vt.blade_struc.BldFlDmp2))
		ofh.write('{:.6f}\n'.format(self.fst_vt.blade_struc.BldEdDmp1))
		ofh.write('---\n')
		ofh.write('{:.6f}\n'.format(self.fst_vt.blade_struc.FlStTunr1))
		ofh.write('{:.6f}\n'.format(self.fst_vt.blade_struc.FlStTunr2))
		ofh.write('{:.6f}\n'.format(self.fst_vt.blade_struc.AdjBlMs))
		ofh.write('{:.6f}\n'.format(self.fst_vt.blade_struc.AdjFlSt))
		ofh.write('{:.6f}\n'.format(self.fst_vt.blade_struc.AdjEdSt))
		ofh.write('Blade properties\n')
		ofh.write('---\n')
		ofh.write('---\n')
		
		bf = self.fst_vt.blade_struc.BlFract
		ac = self.fst_vt.blade_struc.AeroCent
		st = self.fst_vt.blade_struc.StrcTwst
		bm = self.fst_vt.blade_struc.BMassDen
		fs = self.fst_vt.blade_struc.FlpStff
		es = self.fst_vt.blade_struc.EdgStff
		gs = self.fst_vt.blade_struc.GJStff
		eas = self.fst_vt.blade_struc.EAStff #[AH] was es (overwrote EdgStiff) -- changed to eas
		a = self.fst_vt.blade_struc.Alpha
		fi = self.fst_vt.blade_struc.FlpIner
		ei = self.fst_vt.blade_struc.EdgIner 
		pr = self.fst_vt.blade_struc.PrecrvRef
		ps = self.fst_vt.blade_struc.PreswpRef
		fo = self.fst_vt.blade_struc.FlpcgOf       
		eo = self.fst_vt.blade_struc.Edgcgof
		feo = self.fst_vt.blade_struc.FlpEAOf
		eeo = self.fst_vt.blade_struc.EdgEAOf      

		for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17  in \
			zip(bf, ac, st, bm, fs, es, gs, eas, a, fi, ei, pr, ps, fo, eo, feo, eeo):
			ofh.write('{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n'.\
			format(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17))
 
		ofh.write('Blade Mode Shapes\n')
		for i in range(5):
			ofh.write('{:.4f}\n'.format(self.fst_vt.blade_struc.BldFl1Sh[i]))
		for i in range(5):
			ofh.write('{:.4f}\n'.format(self.fst_vt.blade_struc.BldFl2Sh[i]))           
		for i in range(5):
			ofh.write('{:.4f}\n'.format(self.fst_vt.blade_struc.BldEdgSh[i]))      
		 
		ofh.close() 
	
	def AeroWriter(self):

		if not os.path.isdir(os.path.join(self.fst_directory,'AeroData')):
			os.mkdir(os.path.join(self.fst_directory,'AeroData'))

		# create airfoil objects
		for i in range(self.fst_vt.blade_aero.NumFoil):
			 af_name = os.path.join(self.fst_directory, 'AeroData', 'Airfoil' + str(i) + '.dat')
			 self.fst_vt.blade_aero.FoilNm[i] = os.path.join('AeroData', 'Airfoil' + str(i) + '.dat')
			 self.writeAirfoilFile(af_name, i, 2)

		ad_file = os.path.join(self.fst_directory,self.fst_vt.input_files.ADFile)
		ofh = open(ad_file,'w')
		
		ofh.write('Aerodyn input file for FAST\n')
		
		ofh.write('{:}\n'.format(self.fst_vt.aerodyn.SysUnits))
		ofh.write('{:}\n'.format(self.fst_vt.aerodyn.StallMod))        
		ofh.write('{:}\n'.format(self.fst_vt.aerodyn.UseCm))
		ofh.write('{:}\n'.format(self.fst_vt.aerodyn.InfModel))
		ofh.write('{:}\n'.format(self.fst_vt.aerodyn.IndModel))
		ofh.write('{:.3f}\n'.format(self.fst_vt.aerodyn.AToler))
		ofh.write('{:}\n'.format(self.fst_vt.aerodyn.TLModel))
		ofh.write('{:}\n'.format(self.fst_vt.aerodyn.HLModel))
		ofh.write('"{:}"\n'.format(self.fst_vt.aerodyn.WindFile))  
		ofh.write('{:.1f}\n'.format(self.fst_vt.aerodyn.HH))  
		ofh.write('{:.1f}\n'.format(self.fst_vt.aerodyn.TwrShad))  
		ofh.write('{:.1f}\n'.format(self.fst_vt.aerodyn.ShadHWid))  
		ofh.write('{:.1f}\n'.format(self.fst_vt.aerodyn.T_Shad_Refpt))  
		ofh.write('{:.3f}\n'.format(self.fst_vt.aerodyn.AirDens))  
		ofh.write('{:.9f}\n'.format(self.fst_vt.aerodyn.KinVisc))  
		ofh.write('{:2}\n'.format(self.fst_vt.aerodyn.DTAero))        

		ofh.write('{:2}\n'.format(self.fst_vt.blade_aero.NumFoil))
		for i in range (self.fst_vt.blade_aero.NumFoil):
			ofh.write('"{:}"\n'.format(self.fst_vt.blade_aero.FoilNm[i]))

		ofh.write('{:2}\n'.format(self.fst_vt.blade_aero.BldNodes))
		rnodes = self.fst_vt.blade_aero.RNodes
		twist = self.fst_vt.blade_aero.AeroTwst
		drnodes = self.fst_vt.blade_aero.DRNodes
		chord = self.fst_vt.blade_aero.Chord
		nfoil = self.fst_vt.blade_aero.NFoil
		prnelm = self.fst_vt.blade_aero.PrnElm
		ofh.write('Nodal properties\n')
		for r, t, dr, c, a, p in zip(rnodes, twist, drnodes, chord, nfoil, prnelm):
			ofh.write('{:.5f}\t{:.3f}\t{:.4f}\t{:.3f}\t{:5}\t{:}\n'.format(r, t, dr, c, a, p))

		ofh.close()

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

	# Wind Writer

	def WindWriter(self):
	  
		# if self.fst_vt.aero_vt.wind_file_type == 'hh':
	
		#     wind_file = os.path.join(self.fst_directory, self.fst_vt.aero_vt.WindFile)
		#     ofh = open(wind_file,'w')
		
		#     #ofh.write('{:}\n'.format(self.fst_vt.simple_wind_vt.description))
		#     #for i in range(6):
		#     #    ofh.write('! \n')
		#     for i in range(self.fst_vt.simple_wind_vt.TimeSteps):
		#         ofh.write('{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n'.format(\
		#                   self.fst_vt.simple_wind_vt.Time[i], self.fst_vt.simple_wind_vt.HorSpd[i], self.fst_vt.simple_wind_vt.WindDir[i],\
		#                   self.fst_vt.simple_wind_vt.VerSpd[i], self.fst_vt.simple_wind_vt.HorShr[i],\
		#                   self.fst_vt.simple_wind_vt.VerShr[i], self.fst_vt.simple_wind_vt.LnVShr[i], self.fst_vt.simple_wind_vt.GstSpd[i]))
	
		#     ofh.close()

		if self.fst_vt.aerodyn.wind_file_type == 'wnd':

			wind_file = os.path.join(self.fst_directory, self.fst_vt.aerodyn.WindFile)
			ofh = open(wind_file,'w')
		
			for i in range(self.fst_vt.wnd_wind.TimeSteps):
				ofh.write('{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n'.format(\
						  self.fst_vt.wnd_wind.Time[i], self.fst_vt.wnd_wind.HorSpd[i], self.fst_vt.wnd_wind.WindDir[i],\
						  self.fst_vt.wnd_wind.VerSpd[i], self.fst_vt.wnd_wind.HorShr[i],\
						  self.fst_vt.wnd_wind.VerShr[i], self.fst_vt.wnd_wind.LnVShr[i], self.fst_vt.wnd_wind.GstSpd[i]))
	
			ofh.close()
		
		else:
			print "TODO: Other wind file types"

'''def noise_example():

	# Noise example
	fst_input = FstInputReader()
	fst_writer = FstInputWriter()

	ad_file    = 'NREL5MW.ad'
	ad_file_type = 0
	blade_file = 'NREL5MW_Blade.dat'
	tower_file = 'NREL5MW_Monopile_Tower_RigFnd.dat'
	platform_file = 'NREL5MW_Monopile_Platform_RigFnd.dat'
	fst_file = 'NREL5MW_Monopile_Rigid.v7.02.fst'
	fst_file_type = 0
	FAST_DIR = os.path.dirname(os.path.realpath(__file__))
	fst_input.fst_infile_vt.template_path= os.path.join(FAST_DIR,"Noise_Files")
	ad_fname = os.path.join(fst_input.fst_infile_vt.template_path, ad_file)
	bl_fname = os.path.join(fst_input.fst_infile_vt.template_path, blade_file)
	tw_fname = os.path.join(fst_input.fst_infile_vt.template_path, tower_file)
	pl_fname = os.path.join(fst_input.fst_infile_vt.template_path, platform_file)
	fs_fname = os.path.join(fst_input.fst_infile_vt.template_path, fst_file)

	fst_input.fst_infile_vt.ad_file = ad_fname
	fst_input.fst_infile_vt.ad_file_type = ad_file_type
	fst_input.fst_infile_vt.blade_file = bl_fname
	fst_input.fst_infile_vt.tower_file = tw_fname
	fst_input.fst_infile_vt.platform_file = pl_fname
	fst_input.fst_infile_vt.fst_file = fs_fname
	fst_input.fst_infile_vt.fst_file_type = fst_file_type
	fst_input.execute() 

	fst_writer.fst_vt = fst_input.fst_vt
	fst_writer.execute()'''

def oc3_example():

	# OC3 Example
	fst_input = FstInputReader()
	fst_writer = FstInputWriter()

	FAST_DIR = os.path.dirname(os.path.realpath(__file__))

	fst_input.fst_infile = 'NRELOffshrBsline5MW_Monopile_RF.fst'
	fst_input.fst_directory = os.path.join(FAST_DIR,"OC3_Files")
	fst_input.ad_file_type = 1
	fst_input.fst_file_type = 1
	fst_input.execute() 

	fst_writer.fst_vt = fst_input.fst_vt
	fst_writer.fst_infle = 'FAST_Model.fst'
	fst_writer.fst_directory = os.path.join(FAST_DIR,"tmp")
	fst_writer.fst_vt.PtfmFile = "Platform.dat"
	fst_writer.fst_vt.TwrFile = "Tower.dat"
	fst_writer.fst_vt.BldFile1 = "Blade.dat"
	fst_writer.fst_vt.BldFile2 = fst_writer.fst_vt.BldFile1 
	fst_writer.fst_vt.BldFile3 = fst_writer.fst_vt.BldFile1 
	fst_writer.fst_vt.ADFile = "Aerodyn.ipt"
	fst_writer.execute()

if __name__=="__main__":

	#noise_example()
	
	oc3_example()
