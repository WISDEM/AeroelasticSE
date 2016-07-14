from numpy import zeros, array
from FST_vartrees_out import FstOutput

# This variable tree contains all parameters required to create a FAST model
# for FAST versions 7 and 8.

# .fst Simulation Control
class FstSimCtrl(object):
	def __init__(self):
		self.Echo = False
		self.AbortLevel = ''
		self.TMax = 0.0
		self.DT = 0.0
		self.InterpOrder = 0
		self.NumCrctn = 0
		self.DT_UJac = 0.0
		self.UJacSclFact = 0.0

# Feature Switches and Flags
class FtrSwtchsFlgs(object):
	def __init__(self):
		self.CompElast = 0
		self.CompInflow = 0
		self.CompAero = 0
		self.CompServo = 0
		self.CompHydro = 0
		self.CompSub = 0
		self.CompMooring = 0
		self.CompIce = 0

# Input Files
class InputFiles(object):
	def __init__(self):
		self.EDFile = ''
		self.BDBldFile1 = ''
		self.BDBldFile2 = ''
		self.BDBldFile3 = ''
		self.InflowFile = ''
		self.AeroFile = ''
		self.ServoFile = ''
		self.HydroFile = ''
		self.SubFile = ''
		self.MooringFile = ''
		self.IceFile = ''

# FAST Output Parameters
class FstOutputParams(object):
	def __init__(self):
		self.SumPrint   = False
		self.SttsTime   = 0.0
		self.ChkptTime  = 0.0
		self.DT_Out     = 0.0
		self.TStart     = 0.0
		self.OutFileFmt = 0
		self.TabDelim   = False
		self.OutFmt     = ''

# Visualization
class Visualization(object):
	def __init__(self):
		self.WrVTK = 0
		self.VTK_type = 0
		self.VTK_fields = False
		self.VTK_fps = 0

# ElastoDyn Simulation Control
class EdSimCtrl(object):
	def __init__(self):
		self.Echo = False
		self.Method = 0
		self.DT = 0.0

# Environmental Condition
class EnvirCond(object):
	def __init__(self):
		self.Gravity = 0.0

# Degrees of Freedom
class DOF(object):
	def __init__(self):
		self.FlapDOF1 = False
		self.FlapDOF2 = False
		self.EdgeDOF = False
		self.TeetDOF = False
		self.DrTrDOF = False
		self.GenDOF = False
		self.YawDOF = False
		self.TwFADOF1 = False
		self.TwFADOF2 = False
		self.TwSSDOF1 = False
		self.TwSSDOF2 = False
		self.PtfmSgDOF = False
		self.PtfmSwDOF = False
		self.PtfmHvDOF = False
		self.PtfmRDOF = False
		self.PtfmPDOF = False
		self.PtfmYDOF = False

# Initial Conditions
class InitConds(object):
	def __init__(self):
		self.OoPDefl    = 0.0
		self.IPDefl     = 0.0
		self.BlPitch1   = 0.0
		self.BlPitch2   = 0.0
		self.BlPitch3   = 0.0
		self.TeetDefl   = 0.0
		self.Azimuth    = 0.0
		self.RotSpeed   = 0.0
		self.NacYaw     = 0.0
		self.TTDspFA    = 0.0
		self.TTDspSS    = 0.0
		self.PtfmSurge  = 0.0
		self.PtfmSway   = 0.0
		self.PtfmHeave  = 0.0
		self.PtfmRoll   = 0.0
		self.PtfmPitch  = 0.0
		self.PtfmYaw    = 0.0

# Turbine Configuration
class TurbConfig(object):
	def __init__(self):
		self.NumBl      = 0
		self.TipRad     = 0.0
		self.HubRad     = 0.0
		self.PreCone1   = 0.0
		self.PreCone2   = 0.0
		self.PreCone3   = 0.0
		self.HubCM      = 0.0
		self.UndSling   = 0.0
		self.Delta3     = 0.0
		self.AzimB1Up   = 0.0
		self.OverHang   = 0.0
		self.ShftGagL   = 0.0
		self.ShftTilt   = 0.0
		self.NacCMxn    = 0.0
		self.NacCMyn    = 0.0
		self.NacCMzn    = 0.0
		self.NcIMUxn    = 0.0
		self.NcIMUyn    = 0.0
		self.NcIMUzn    = 0.0
		self.Twr2Shft   = 0.0
		self.TowerHt    = 0.0
		self.TowerBsHt  = 0.0
		self.PtfmCMxt   = 0.0
		self.PtfmCMyt   = 0.0
		self.PtfmCMzt   = 0.0
		self.PtfmRefzt  = 0.0

# Mass and Inertia
class MassInertia(object):
	def __init__(self):
		self.TipMass1   = 0.0
		self.TipMass2   = 0.0
		self.TipMass2   = 0.0
		self.HubMass    = 0.0
		self.HubIner    = 0.0
		self.GenIner    = 0.0
		self.NacMass    = 0.0
		self.NacYIner   = 0.0
		self.YawBrMass  = 0.0
		self.PtfmMass   = 0.0
		self.PtfmRIner  = 0.0
		self.PtfmPIner  = 0.0
		self.PtfmYIner  = 0.0

# ED Blade (Structure)
class BladeStruc(object):
	def __init__(self):
		self.BldNodes = 0
		self.BldFile1 = ''
		self.BldFile2 = ''
		self.BldFile3 = ''

		# Including the blade files and properties in the same object,
		# as is done here, implies that the properties are done for all
		# blades (assumed for now)

		# General Model Inputs
		self.NBlInpSt = 0   #Number of blade input stations (-)
		self.CalcBMode = False   #Calculate blade mode shapes internally {T: ignore mode shapes from below, F: use mode shapes from below} [CURRENTLY IGNORED] (flag)
		self.BldFlDmp1 = 0.0   #Blade flap mode #1 structural damping in percent of critical (%)
		self.BldFlDmp2 = 0.0   #Blade flap mode #2 structural damping in percent of critical (%)
		self.BldEdDmp1 = 0.0   #Blade edge mode #1 structural damping in percent of critical (%)
		self.FlStTunr1 = 0.0   #Blade flapwise modal stiffness tuner, 1st mode (-)
		self.FlStTunr2 = 0.0   #Blade flapwise modal stiffness tuner, 2nd mode (-)
		self.AdjBlMs = 0.0   #Factor to adjust blade mass density (-)
		self.AdjFlSt = 0.0   #Factor to adjust blade flap stiffness (-)
		self.AdjEdSt = 0.0   #Factor to adjust blade edge stiffness (-)
		
		# Distributed Blade Properties
		self.BlFract = zeros([1])
		self.AeroCent = zeros([1])
		self.PitchAxis = zeros([1])
		self.StrcTwst = zeros([1])
		self.BMassDen = zeros([1])
		self.FlpStff = zeros([1])
		self.EdgStff = zeros([1])
		self.GJStff = zeros([1])
		self.EAStff = zeros([1])
		self.Alpha = zeros([1])
		self.FlpIner = zeros([1])
		self.EdgIner = zeros([1])
		self.PrecrvRef = zeros([1])
		self.PreswpRef = zeros([1]) #[AH] Added during openmdao1 update
		self.FlpcgOf = zeros([1])
		self.Edgcgof = zeros([1])
		self.FlpEAOf = zeros([1])
		self.EdgEAOf = zeros([1])
		
		# Blade Mode Shapes
		self.BldFl1Sh = zeros([1])
		self.BldFl2Sh = zeros([1])
		self.BldEdgSh = zeros([1])

# Rotor-Teeter
class RotorTeeter(object):
	def __init__(self):
		self.TeetMod  = 0
		self.TeetDmpP = 0.0
		self.TeetDmp  = 0.0
		self.TeetCDmp = 0.0
		self.TeetSStP = 0.0
		self.TeetHStP = 0.0
		self.TeetSSSp = 0.0
		self.TeetHSSp = 0.0

class DriveTrain(object):
	def __init__(self):
		self.GBoxEff  = 0.0
		self.GBRatio  = 0.0
		self.DTTorSpr = 0.0
		self.DTTorDmp = 0.0

class Furling(object):
	def __init__(self):
		self.Furling = False
		self.FurlFile = ''

class Tower(object):
	def __init__(self):
		self.TwrNodes = 0
		self.TwrFile = ''

		# General Tower Paramters
		self.NTwInptSt = 0   #Number of input stations to specify tower geometry
		self.CalcTMode = False   #calculate tower mode shapes internally {T: ignore mode shapes from below, F: use mode shapes from below} [CURRENTLY IGNORED] (flag)
		self.TwrFADmp1 = 0.0   #Tower 1st fore-aft mode structural damping ratio (%)
		self.TwrFADmp2 = 0.0   #Tower 2nd fore-aft mode structural damping ratio (%)
		self.TwrSSDmp1 = 0.0   #Tower 1st side-to-side mode structural damping ratio (%)
		self.TwrSSDmp2 = 0.0   #Tower 2nd side-to-side mode structural damping ratio (%)

		# Tower Adjustment Factors
		self.FAStTunr1 = 0.0   #Tower fore-aft modal stiffness tuner, 1st mode (-)
		self.FAStTunr2 = 0.0   #Tower fore-aft modal stiffness tuner, 2nd mode (-)
		self.SSStTunr1 = 0.0   #Tower side-to-side stiffness tuner, 1st mode (-)
		self.SSStTunr2 = 0.0   #Tower side-to-side stiffness tuner, 2nd mode (-)
		self.AdjTwMa = 0.0   #Factor to adjust tower mass density (-)
		self.AdjFASt = 0.0   #Factor to adjust tower fore-aft stiffness (-)
		self.AdjSSSt = 0.0   #Factor to adjust tower side-to-side stiffness (-)
	 
		# Distributed Tower Properties   
		self.HtFract = zeros([1])
		self.TMassDen = zeros([1])
		self.TwFAStif = zeros([1])
		self.TwSSStif = zeros([1])
		self.TwGJStif = zeros([1])
		self.TwEAStif = zeros([1])
		self.TwFAIner = zeros([1])
		self.TwSSIner = zeros([1])
		self.TwFAcgOf = zeros([1])
		self.TwSScgOf = zeros([1])
		
		# Tower Mode Shapes
		self.TwFAM1Sh = zeros([1])   #Tower Fore-Aft Mode 1 Shape Coefficients x^2, x^3, x^4, x^5, x^6
		self.TwFAM2Sh = zeros([1])   #Tower Fore-Aft Mode 2 Shape Coefficients x^2, x^3, x^4, x^5, x^6
		self.TwSSM1Sh = zeros([1])   #Tower Side-to-Side Mode 1 Shape Coefficients x^2, x^3, x^4, x^5, x^6
		self.TwSSM2Sh = zeros([1])   #Tower Side-to-Side Mode 2 Shape Coefficients x^2, x^3, x^4, x^5, x^6      

class EdOutParams(object):
	def __init__(self):
		self.SumPrint = False
		self.OutFile  = 0
		self.TabDelim = False
		self.OutFmt   = ''
		self.TStart   = 0.0
		self.DecFact  = 0.0
		self.NTwGages = 0
		self.TwrGagNd = []
		self.NBlGages = 0
		self.BldGagNd = []

# Inflow Wind General Parameters
class InflowWind(object):
	def __init__(self):
		self.Echo = False
		self.WindType = 0
		self.PropagationDir = 0.0
		self.NWindVel = 0
		self.WindVxiList = 0.0
		self.WindVyiList = 0.0
		self.WindVziList = 0.0

# Parameters for Steady Wind Conditions [used only for WindType = 1]
class SteadyWindParams(object):
	def __init__(self):
		self.HWindSpeed = 0.0
		self.RefHt = 0.0
		self.PLexp = 0.0

# Parameters for Uniform wind file   [used only for WindType = 2]
class UniformWindParams(object):
	def __init__(self):
		self.Filename = ''
		self.RefHt = 0.0
		self.RefLength = 0.0

# Parameters for Binary TurbSim Full-Field files   [used only for WindType = 3]
class TurbSimWindParams(object):
	def __init__(self):
		self.Filename = ''

# Parameters for Binary Bladed-style Full-Field files   [used only for WindType = 4]
class BladedWindParams(object):
	def __init__(self):
		self.FilenameRoot = ''
		self.TowerFile = False

# Parameters for HAWC-format binary files  [Only used with WindType = 5]
class HAWCWindParams(object):
	def __init__(self):
		self.FileName_u  = ''
		self.FileName_v  = ''
		self.FileName_w  = ''
		self.nx          = 0
		self.ny          = 0
		self.nz          = 0
		self.dx          = 0.0
		self.dy          = 0.0
		self.dz          = 0.0
		self.RefHt       = 0.0
		self.ScaleMethod = 0
		self.SFx         = 0.0
		self.SFy         = 0.0
		self.SFz         = 0.0
		self.SigmaFx     = 0.0
		self.SigmaFy     = 0.0
		self.SigmaFz     = 0.0
		self.URef        = 0.0
		self.WindProfile = 0
		self.PLExp       = 0.0
		self.Z0          = 0.0

# Inflow Wind Output Parameters (actual OutList included in master OutList)
class InflowOutParams(object):
	def __init__(self):
		self.SumPrint = False

# Wnd Wind File Parameters
class WndWind(object):
	def __init__(self):
		self.TimeSteps = 0   #number of time steps
		self.Time = zeros([1])   #time steps
		self.HorSpd = zeros([1])   #horizontal wind speed
		self.WindDir = zeros([1])   #wind direction
		self.VerSpd = zeros([1])   #vertical wind speed
		self.HorShr = zeros([1])   #horizontal shear
		self.VerShr = zeros([1])   #vertical power-law shear
		self.LnVShr = zeros([1])   #vertical linear shear
		self.GstSpd = zeros([1])   #gust speed not sheared by Aerodyn

# AeroDyn Parameters
class AeroDyn(object):
	def __init__(self):
		# General Model Inputs
		self.SysUnits = 'SI'   #Enum('SI', ('SI','ENG, desc='System of units for used for input and output [must be SI for FAST] (unquoted string)
		self.StallMod = 'BEDOES'   #Enum('BEDDOES', ('BEDDOES', 'STEADY, desc = 'Dynamic stall included [BEDDOES or STEADY] (unquoted string)
		self.UseCM = 'NO_CM'   #Enum('NO_CM', ('NO_CM', 'USE_CM, desc = 'Use aerodynamic pitching moment model? [USE_CM or NO_CM] (unquoted string)
		self.InfModel = 'EQUIL'   #Enum('EQUIL', ('EQUIL', 'DYNIN, desc = 'Inflow model [DYNIN or EQUIL] (unquoted string)
		self.IndModel = 'SWIRL'   #Enum('SWIRL', ('NONE', 'WAKE', 'SWIRL, desc = 'Induction-factor model [NONE or WAKE or SWIRL] (unquoted string)
		self.AToler = 0.0   #Induction-factor tolerance (convergence criteria) (-)
		self.TLModel = 'PRANDtl'   #Enum('PRANDtl', ('PRANDtl', 'GTECH', 'NONE, desc = 'Tip-loss model (EQUIL only) [PRANDtl, GTECH, or NONE] (unquoted string)
		self.HLModel = 'PRANDTl'   #Enum('PRANDtl', ('PRANDtl', 'GTECH', 'NONE, desc = 'Hub-loss model (EQUIL only) [PRANdtl or NONE] (unquoted string)

		# Turbine Inputs
		self.WindFile = ''   #Initial wind file from template import (quoted string)
		self.wind_file_type = 'hh'   #Enum('hh', ('hh', 'bts', 'wnd, desc='type of wind file
		self.HH = 0.0   #units='m', desc= 'Wind reference (hub) height [TowerHt+Twr2Shft+OverHang*SIN(ShftTilt)] (m)
		self.TwrShad = 0.0   #Tower-shadow velocity deficit (-)
		self.ShadHWid = 9999.9   #units='m', desc='Tower-shadow half width (m)'
		self.T_Shad_Refpt = 9999.9   #units='m', desc='Tower-shadow reference point (m)

		# Wind Aero Inputs
		self.AirDens = 1.225   #units='kg / (m**3)', desc='Air density (kg/m^3)
		self.KinVisc = 1.464e-5   #units='m**2 / s', desc='Kinematic air viscosity [CURRENTLY IGNORED] (m^2/sec)
		self.DTAero = 0.02479   #units='s', desc = 'Time interval for aerodynamic calculations (sec)

# AeroDyn Blade
class AeroDynBlade(object):
	def __init__(self):
		self.NumFoil = 0   #Number of airfoil files (-)
		self.FoilNm = zeros([1])   #Names of the airfoil files [NumFoil lines] (quoted strings)

		self.af_data = []   #list of airfoild data sets

		self.BldNodes = 0   #Number of blade nodes used for analysis
		self.RNodes = zeros([1])   #Distance from blade root to center of element
		self.AeroTwst = zeros([1])   #units='deg',desc='Twist at RNodes locations
		self.DRNodes = zeros([1])   #Span-wise width of the blade element, measured along the span of the blade
		self.Chord = zeros([1])   #units='m',desc='Chord length at node locations; planform area = chord*DRNodes
		self.NFoil = zeros([1])   #Airfoil ID Number
		self.PrnElm = zeros([1])   #Flag for printing element ouput for blade section

# AeroDyn Airfoil Polar
class ADAirfoilPolar(object):
	def __init__(self):
	    self.IDParam = 0.0   #Table ID Parameter (Typically Reynolds number)
	    self.StallAngle = 0.0   #Stall angle (deg)
	    self.ZeroCn = 0.0   #Zero lift angle of attack (deg)
	    self.CnSlope = 0.0   #Cn slope for zero lift (dimensionless)
	    self.CnPosStall = 0.0   #Cn at stall value for positive angle of attack
	    self.CnNegStall = 0.0   #Cn at stall value for negative angle of attack
	    self.alphaCdMin = 0.0   #Angle of attack for minimum CD (deg)
	    self.CdMin = 0.0   #Minimum Cd Value

	    self.alpha = zeros([1])   #angle of attack
	    self.cl = zeros([1])   #coefficient of lift
	    self.cd = zeros([1])   #coefficient of drag
	    self.cm = zeros([1])   #coefficient of the pitching moment

# AeroDyn airfoil
class ADAirfoil(object):
	def __init__(self):
	    self.description = ''   #description of airfoil
	    self.number_tables = 0   #number of airfoil polars
	    self.af_tables = []   #list of airfoil polars

# ServoDyn Simulation Control
class SdSimCtrl(object):
	def __init__(self):
		self.Echo = False
		self.DT = 0.0

# Pitch Control
class PitchCtrl(object):
	def __init__(self):
		self.PCMode       = 0
		self.TPCOn        = 0.0
		self.TPitManS1    = 0.0
		self.TPitManS2    = 0.0
		self.TPitManS3    = 0.0
		self.PitManRat1   = 0.0
		self.PitManRat2   = 0.0
		self.PitManRat3   = 0.0
		self.BlPitchF1    = 0.0
		self.BlPitchF2    = 0.0
		self.BlPitchF3    = 0.0

# Generator and Torque Control
class GenTorqCtrl(object):
	def __init__(self):
		self.VSContrl = 0
		self.GenModel = 0
		self.GenEff   = 0.0
		self.GenTiStr = False
		self.GenTiStp = False
		self.SpdGenOn = 0.0
		self.TimGenOn = 0.0
		self.TimGenOf = 0.0

# Simple Variable-Speed Torque Control
class VarSpeedTorqCtrl(object):
	def __init__(self):
		self.VS_RtGnSp = 0.0
		self.VS_RtTq   = 0.0
		self.VS_Rgn2K  = 0.0
		self.VS_SlPc   = 0.0

# Simple Induction Generator
class InductGen(object):
	def __init__(self):
		self.SIG_SlPc = 0.0
		self.SIG_SySp = 0.0
		self.SIG_RtTq = 0.0
		self.SIG_PORt = 0.0

# Thevenin-Equivalent Induction Generator
class ThevEqInductGen(object):
	def __init__(self):
		self.TEC_Freq = 0.0
		self.TEC_NPol = 0
		self.TEC_SRes = 0.0
		self.TEC_RRes = 0.0
		self.TEC_VLL  = 0.0
		self.TEC_SLR  = 0.0
		self.TEC_RLR  = 0.0
		self.TEC_MR   = 0.0

# High-Speed Shaft Brake
class ShaftBrake(object):
	def __init__(self):
		self.HSSBrMode = 0
		self.THSSBrDp  = 0.0
		self.HSSBrDT   = 0.0
		self.HSSBrTqF  = 0.0

# Nacelle-Yaw Control
class NacYawCtrl(object):
	def __init__(self):
		self.YCMode    = 0
		self.TYCOn     = 0.0
		self.YawNeut   = 0.0
		self.YawSpr    = 0.0
		self.YawDamp   = 0.0
		self.TYawManS  = 0.0
		self.YawManRat = 0.0
		self.NacYawF   = 0.0

# Tuned Mass Damper
class TunedMassDamp(object):
	def __init__(self):
		self.CompNTMD = False
		self.NTMDfile = ''
		self.CompTTMD = False
		self.TTMDfile = ''

# Bladed Interface
class BladedInterface(object):
	def __init__(self):
		self.DLL_FileName = ''
		self.DLL_InFile   = ''
		self.DLL_ProcName = ''
		self.DLL_DT       = ''
		self.DLL_Ramp     = False
		self.BPCutoff     = 0.0
		self.NacYaw_North = 0.0
		self.Ptch_Cntrl   = 0.0
		self.Ptch_SetPnt  = 0.0
		self.Ptch_Min     = 0.0
		self.Ptch_Max     = 0.0
		self.PtchRate_Min = 0.0
		self.PtchRate_Max = 0.0
		self.Gain_OM      = 0.0
		self.GenSpd_MinOM = 0.0
		self.GenSpd_MaxOM = 0.0
		self.GenSpd_Dem   = 0.0
		self.GenTrq_Dem   = 0.0
		self.GenPwr_Dem   = 0.0
		self.DLL_NumTrq = 0.0
		self.GenSpd_TLU = zeros([0])
		self.GenTrq_TLU = zeros([0])

# ServoDyn Output Params
class SdOutParams(object):
	def __init__(self):
		self.SumPrint = False
		self.OutFile  = 0
		self.TabDelim = False
		self.OutFmt   = ''
		self.TStart   = 0.0


# ====== INITIALIZE FAST MODEL BY INITIALIZING ALL VARIABLE TREES ======

class FstModel(object):
	def __init__(self):

		# Description
		self.description = ''

		# Fst file vartrees
		self.fst_sim_ctrl = FstSimCtrl()
		self.ftr_swtchs_flgs = FtrSwtchsFlgs()
		self.input_files = InputFiles()
		self.fst_output_params = FstOutputParams()
		self.visualization = Visualization()
		self.fst_out_params = FstOutputParams()
		
		# Elastodyn vartrees
		self.ed_sim_ctrl = EdSimCtrl()
		self.envir_cond = EnvirCond()
		self.dof = DOF()
		self.init_conds = InitConds()
		self.turb_config = TurbConfig()
		self.mass_inertia = MassInertia()
		self.blade_struc = BladeStruc()
		self.rotor_teeter = RotorTeeter()
		self.drivetrain = DriveTrain()
		self.furling = Furling()
		self.tower = Tower()
		self.ed_out_params = EdOutParams()

		# Wind vartrees
		self.inflow_wind = InflowWind()
		self.steady_wind_params = SteadyWindParams()
		self.uniform_wind_params = UniformWindParams()
		self.turbsim_wind_params = TurbSimWindParams()
		self.bladed_wind_params = BladedWindParams()
		self.hawc_wind_params = HAWCWindParams()
		self.inflow_out_params = InflowOutParams()
		self.wnd_wind = WndWind()

		# AeroDyn vartrees
		self.aerodyn = AeroDyn()
		self.blade_aero = AeroDynBlade()

		# ServoDyn vartrees
		self.sd_sim_ctrl = SdSimCtrl()
		self.pitch_ctrl = PitchCtrl()
		self.gen_torq_ctrl = GenTorqCtrl()
		self.var_speed_torq_ctrl = VarSpeedTorqCtrl()
		self.induct_gen = InductGen()
		self.theveq_induct_gen = ThevEqInductGen()
		self.shaft_brake = ShaftBrake()
		self.nac_yaw_ctrl = NacYawCtrl()
		self.tuned_mass_damper = TunedMassDamp()
		self.bladed_interface = BladedInterface()
		self.sd_out_params = SdOutParams()
		
		# List of Outputs (all input files -- FST, ED, SD)
		# TODO: Update FstOutput for a few new outputs in FAST8
		self.outlist = FstOutput()   # 











