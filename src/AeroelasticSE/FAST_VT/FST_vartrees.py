from numpy import zeros, array
from FST_vartrees_out import FstOutput

class SimpleWind(object):
	def __init__(self):
		self.TimeSteps = 0   #number of time steps
		self.Time = 0.0   #time step
		self.HorSpd = zeros([1])   #horizontal wind speed
		self.WindDir = zeros([1])   #wind direction
		self.VerSpd = zeros([1])   #vertical wind speed
		self.HorShr = zeros([1])   #horizontal shear
		self.VerShr = zeros([1])   #vertical power-law shear
		self.LnVShr = zeros([1])   #vertical linear shear
		self.GstSpd = zeros([1])   #gust speed not sheared by Aerodyn

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

class ADAirfoil(object):
	def __init__(self):
	    self.description = ''   #description of airfoil
	    self.number_tables = 0   #number of airfoil polars
	    self.af_tables = []   #list of airfoil polars

class ADBladeAeroGeometry(object):
	def __init__(self):
	    self.NumFoil = 0   #Number of airfoil files (-)
	    self.FoilNm = zeros([1])   #Names of the airfoil files [NumFoil lines] (quoted strings)
	    #TODO: reading in actual airfoil data
	    self.af_data = []   #list of airfoild data sets

	    self.BldNodes = 0   #Number of blade nodes used for analysis

	    self.RNodes = zeros([1])   #Distance from blade root to center of element
	    self.AeroTwst = zeros([1])   #units='deg',desc='Twist at RNodes locations
	    self.DRNodes = zeros([1])   #Span-wise width of the blade element, measured along the span of the blade
	    self.Chord = zeros([1])   #units='m',desc='Chord length at node locations; planform area = chord*DRNodes
	    self.NFoil = zeros([1])   #Airfoil ID Number
	    self.PrnElm = zeros([1])   #Flag for printing element ouput for blade section

class ADAero(object):
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

	    # Blade Geometry and Airfoil Information
	    self.blade_vt = ADBladeAeroGeometry()   #Variable tree for blade geometry and airfoil information

class FstBladeStrucGeometry(object):
	def __init__(self):
	    self.description = ''   #Blade file description

	    # General Model Inputs
	    self.NBlInpSt = 0   #Number of blade input stations (-)
	    self.CalcBMode = True   #Calculate blade mode shapes internally {T: ignore mode shapes from below, F: use mode shapes from below} [CURRENTLY IGNORED] (flag)
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
	    
        # BlFract  AeroCent  StrcTwst  BMassDen    FlpStff    EdgStff    GJStff    EAStff   
        # Alpha   FlpIner   EdgIner   PrecrvRef   PreswpRef   FlpcgOf   EdgcgOf   FlpEAOf   
        # EdgEAOf

	    # Blade Mode Shapes
	    self.BldFl1Sh = zeros([1])
	    self.BldFl2Sh = zeros([1])
	    self.BldEdgSh = zeros([1])

class FstTowerStrucGeometry(object):
	def __init__(self):
	    self.description = ''   #description of tower

	    # General Tower Paramters
	    self.NTwInptSt = 0   #Number of input stations to specify tower geometry
	    self.CalcTMode = True   #calculate tower mode shapes internally {T: ignore mode shapes from below, F: use mode shapes from below} [CURRENTLY IGNORED] (flag)
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

class FstPlatformModel(object):
	def __init__(self):
	    self.description = ''   #description of platform

	    # FEATURE FLAGS (CONT)
	    self.PtfmSgDOF = False   #Platform horizontal surge translation DOF (flag)
	    self.PtfmSwDOF = False   #Platform horizontal sway translation DOF (flag)
	    self.PtfmHvDOF = False   #Platform vertical heave translation DOF (flag)
	    self.PtfmRDOF  = False   #Platform roll tilt rotation DOF (flag)
	    self.PtfmPDOF  = False   #Platform pitch tilt rotation DOF (flag)
	    self.PtfmYDOF  = False   #Platform yaw rotation DOF (flag)
	    
	    # INITIAL CONDITIONS (CONT)
	    self.PtfmSurge = 0.0   #Initial or fixed horizontal surge translational displacement of platform (meters)
	    self.PtfmSway  = 0.0   #Initial or fixed horizontal sway translational displacement of platform (meters)
	    self.PtfmHeave = 0.0   #Initial or fixed vertical heave translational displacement of platform (meters)
	    self.PtfmRoll  = 0.0   #Initial or fixed roll tilt rotational displacement of platform (degrees)
	    self.PtfmPitch = 0.0   #Initial or fixed pitch tilt rotational displacement of platform (degrees)
	    self.PtfmYaw   = 0.0   #Initial or fixed yaw rotational displacement of platform (degrees)
	    
	    # TURBINE CONFIGURATION (CONT)
	    self.TwrDraft  = 0.0   #Downward distance from the ground level [onshore] or MSL [offshore] to the tower base platform connection (meters)
	    self.PtfmCM    = 0.0   #Downward distance from the ground level [onshore] or MSL [offshore] to the platform CM (meters)
	    self.PtfmRef   = 0.0   #Downward distance from the ground level [onshore] or MSL [offshore] to the platform reference point (meters)
	    
	    # MASS AND INERTIA (CONT) 
	    self.PtfmMass  = 0.0   #Platform mass (kg)
	    self.PtfmRIner = 0.0   #Platform inertia for roll tilt rotation about the platform CM (kg m^2)
	    self.PtfmPIner = 0.0   #Platform inertia for pitch tilt rotation about the platform CM (kg m^2)
	    self.PtfmYIner = 0.0   #Platfrom inertia for yaw rotation about the platform CM (kg m^2)
	    
	    # PLATFORM (CONT) 
	    self.PtfmLdMod  = 0   #Enum(0, (0,1), desc='{0: none, 1: user-defined from routine UserPtfmLd} (switch)
	    
	    # TOWER (CONT) 
	    self.TwrLdMod  = 0   #Enum(0, (0,1,2), desc='Tower loading model (0: none, 1: Morisons equation, 2: user-defined from routine UserTwrLd) (switch)
	    self.TwrDiam   = 0.0   #Tower diameter in Morisons equation (meters) [used only when TwrLdMod=1]
	    self.TwrCA     = 0.0   #Normalized hydrodynamic added mass   coefficient in Morisons equation (-) [used only when TwrLdMod=1] [determines TwrCM=1+TwrCA]
	    self.TwrCD     = 0.0   #Normalized hydrodynamic viscous drag coefficient in Morisons equation (-) [used only when TwrLdMod=1]
	    
	    # WAVES 
	    self.WtrDens   = 0.0   #Water density (kg/m^3)
	    self.WtrDpth   = 0.0   #Water depth (meters)
	    self.WaveMod   = 0   #Enum(0, (0,1,2,3,4), desc='Incident wave kinematics model {0: none=still water, 1: plane progressive (regular), 2: JONSWAP/Pierson-Moskowitz spectrum (irregular), 3: user-defind spectrum from routine UserWaveSpctrm (irregular), 4: GH Bladed wave data} (switch)
	    self.WaveStMod = 0   #Enum(0, (0,1,2,3), desc='Model for stretching incident wave kinematics to instantaneous free surface {0: none=no stretching, 1: vertical stretching, 2: extrapolation stretching, 3: Wheeler stretching} (switch) [unused when WaveMod=0]
	    self.WaveTMax  = 0.0   #Analysis time for incident wave calculations (sec) [unused when WaveMod=0] [determines WaveDOmega=2Pi/WaveTMax in the IFFT]
	    self.WaveDT    = 0.0   #Time step for incident wave calculations (sec) [unused when WaveMod=0] [0.1<=WaveDT<=1.0 recommended] [determines WaveOmegaMax=Pi/WaveDT in the IFFT]
	    self.WaveHs    = 0.0   #Significant wave height of incident waves (meters) [used only when WaveMod=1 or 2]
	    self.WaveTp    = 0.0   #Peak spectral period of incident waves (sec) [used only when WaveMod=1 or 2]
	    self.WavePkShp = 0.0   #Peak shape parameter of incident wave spectrum (-) or DEFAULT (unquoted string) [used only when WaveMod=2] [use 1.0 for Pierson-Moskowitz]
	    self.WaveDir   = 0.0   #Incident wave propagation heading direction (degrees) [unused when WaveMod=0 or 4]
	    self.WaveSeed1 = 0   #First  random seed of incident waves [-2147483648 to 2147483647] (-) [unused when WaveMod=0 or 4]
	    self.WaveSeed2 = 0   #Second random seed of incident waves [-2147483648 to 2147483647] (-) [unused when WaveMod=0 or 4]
	    self.GHWvFile  = ''   #Root name of GH Bladed files containing wave data (quoted string) [used only when WaveMod=4]

	    # CURRENT
	    self.CurrMod   = 0.0   #Current profile model {0: none=no current, 1: standard, 2: user-defined from routine UserCurrent} (switch)
	    self.CurrSSV0  = 0.0   #Sub-surface current velocity at still water level (m/s) [used only when CurrMod=1]
	    self.CurrSSDir = 0.0   #Sub-surface current heading direction (degrees) or DEFAULT (unquoted string) [used only when CurrMod=1]
	    self.CurrNSRef = 0.0   #Near-surface current reference depth (meters) [used only when CurrMod=1]
	    self.CurrNSV0  = 0.0   #Near-surface current velocity at still water level (m/s) [used only when CurrMod=1]
	    self.CurrNSDir = 0.0   #Near-surface current heading direction (degrees) [used only when CurrMod=1]
	    self.CurrDIV   = 0.0   #Depth-independent current velocity (m/s) [used only when CurrMod=1]
	    self.CurrDIDir = 0.0   #Depth-independent current heading direction (degrees) [used only when CurrMod=1]

	    # OUTPUT (CONT) 
	    self.NWaveKin = 0   #Number of points where the wave kinematics can be output [0 to 9] (-)
	    self.WaveKinNd = 0   #List of tower nodes that have wave kinematics sensors [1 to TwrNodes] (-) [unused if NWaveKin=0]

class FstModel(object):
	def __init__(self):
	    # FAST Wind Information
	    self.simple_wind_vt = SimpleWind()   #Simple wind input model
	    self.wnd_wind_vt = WndWind()   #Wnd wind input model
	    
	    # FAST Hydro Information
	    self.platform_vt = FstPlatformModel()   #Model of platform foundation

	    # FAST Aerodynamic Information
	    self.aero_vt = ADAero()   #Aerodynamic settings, blade design and airfoils

	    # FAST Structural Information
	    self.fst_blade_vt = FstBladeStrucGeometry()   #Structural information on the blade and properties
	    self.fst_tower_vt = FstTowerStrucGeometry()   #Structural information on the tower and properties
	    
	    # FAST Outputs
	    self.fst_output_vt = FstOutput()   #List of output channels

	    # FAST Inputs
	    self.description = ''   #description of platform
	    self.Echo = False   #Echo input data to "echo.out" (flag)
	    self.ADAMSPrep = 1   #Enum(1, (1,2,3), desc='ADAMS preprocessor mode {1: Run FAST, 2: use FAST as a preprocessor to create an ADAMS model, 3: do both} (switch)
	    self.AnalMode = 1   #Enum(1, (1,2), desc='Analysis mode {1: Run a time-marching simulation, 2: create a periodic linearized model} (switch)
	    self.NumBl = 0   #Number of blades (-)
	    self.TMax = 0.0   #Total run time (s)
	    self.DT = 0.0   #Integration time step (s)
	    # TURBINE CONTROL
	    self.YCMode = 0   #Enum(0, (0,1,2), desc='Yaw control mode {0: none, 1: user-defined from routine UserYawCont, 2: user-defined from Simulink} (switch)
	    self.TYCOn = 0.0   #Time to enable active yaw control (s) [unused when YCMode=0]
	    self.PCMode = 0   #Enum(0, (0,1,2), desc='Pitch control mode {0: none, 1: user-defined from routine PitchCntrl, 2: user-defined from Simulink} (switch)
	    self.TPCOn = 0.0   #Time to enable active pitch control (s) [unused when PCMode=0]
	    self.VSContrl = 0   #Enum(0, (0,1,2,3), desc='Variable-speed control mode {0: none, 1: simple VS, 2: user-defined from routine UserVSCont, 3: user-defined from Simulink} (switch)
	    self.VS_RtGnSp = 0.0   #Rated generator speed for simple variable-speed generator control (HSS side) (rpm) [used only when VSContrl=1]
	    self.VS_RtTq = 0.0   #Rated generator torque/constant generator torque in Region 3 for simple variable-speed generator control (HSS side) (N-m) [used only when VSContrl=1]
	    self.VS_Rgn2K = 0.0   #Generator torque constant in Region 2 for simple variable-speed generator control (HSS side) (N-m/rpm^2) [used only when VSContrl=1]
	    self.VS_SlPc = 0.0   #Rated generator slip percentage in Region 2 1/2 for simple variable-speed generator control (%) [used only when VSContrl=1]
	    self.GenModel = 1   #Enum(1, (1,2,3), desc='Generator model {1: simple, 2: Thevenin, 3: user-defined from routine UserGen} (switch) [used only when VSContrl=0]
	    self.GenTiStr = False   #Method to start the generator {T: timed using TimGenOn, F: generator speed using SpdGenOn} (flag)
	    self.GenTiStp = False   #Method to stop the generator {T: timed using TimGenOf, F: when generator power = 0} (flag)
	    self.SpdGenOn = 0.0   #Generator speed to turn on the generator for a startup (HSS speed) (rpm) [used only when GenTiStr=False]
	    self.TimGenOn = 0.0   #Time to turn on the generator for a startup (s) [used only when GenTiStr=True]
	    self.TimGenOf = 0.0   #Time to turn off the generator (s) [used only when GenTiStp=True]
	    self.HSSBrMode = 1   #Enum(1, (1,2), desc='HSS brake model {1: simple, 2: user-defined from routine UserHSSBr} (switch)
	    self.THSSBrDp = 0.0   #Time to initiate deployment of the HSS brake (s)
	    self.TiDynBrk = 0.0   #Time to initiate deployment of the dynamic generator brake [CURRENTLY IGNORED] (s)
	    self.TTpBrDp1 = 0.0   #Time to initiate deployment of tip brake 1 (s)
	    self.TTpBrDp2 = 0.0   #Time to initiate deployment of tip brake 2 (s)
	    self.TTpBrDp3 = 0.0   #Time to initiate deployment of tip brake 3 (s) [unused for 2 blades]
	    self.TBDepISp1 = 0.0   #Deployment-initiation speed for the tip brake on blade 1 (rpm)
	    self.TBDepISp2 = 0.0   #Deployment-initiation speed for the tip brake on blade 2 (rpm)
	    self.TBDepISp3 = 0.0   #Deployment-initiation speed for the tip brake on blade 3 (rpm) [unused for 2 blades]
	    self.TYawManS = 0.0   #Time to start override yaw maneuver and end standard yaw control (s)
	    self.TYawManE = 0.0   #Time at which override yaw maneuver reaches final yaw angle (s)
	    self.NacYawF = 0.0   #Final yaw angle for override yaw maneuvers (degrees)
	    self.TPitManS1 = 0.0   #Time to start override pitch maneuver for blade 1 and end standard pitch control (s)
	    self.TPitManS2 = 0.0   #Time to start override pitch maneuver for blade 2 and end standard pitch control (s)
	    self.TPitManS3 = 0.0   #Time to start override pitch maneuver for blade 3 and end standard pitch control (s) [unused for 2 blades]
	    self.TPitManE1 = 0.0   #Time at which override pitch maneuver for blade 1 reaches final pitch (s)
	    self.TPitManE2 = 0.0   #Time at which override pitch maneuver for blade 2 reaches final pitch (s)
	    self.TPitManE3 = 0.0   #Time at which override pitch maneuver for blade 3 reaches final pitch (s) [unused for 2 blades]
	    self.BlPitch1  = 0.0   #Blade 1 initial pitch (degrees)
	    self.BlPitch2  = 0.0   #Blade 2 initial pitch (degrees)
	    self.BlPitch3  = 0.0   #Blade 3 initial pitch (degrees) [unused for 2 blades]
	    self.B1PitchF1 = 0.0   #Blade 1 final pitch for pitch maneuvers (degrees)
	    self.B1PitchF2 = 0.0   #Blade 2 final pitch for pitch maneuvers (degrees)
	    self.B1PitchF3 = 0.0   #Blade 3 final pitch for pitch maneuvers (degrees) [unused for 2 blades]
	    # ENVIRONMENTAL CONDITIONS 
	    self.Gravity = 0.0   #Gravitational acceleration (m/s^2)
	    # FEATURE FLAGS 
	    self.FlapDOF1 = False   #First flapwise blade mode DOF (flag)
	    self.FlapDOF2 = False   # Second flapwise blade mode DOF (flag)
	    self.EdgeDOF = False   #First edgewise blade mode DOF (flag)
	    self.TeetDOF = False   #Rotor-teeter DOF (flag) [unused for 3 blades]
	    self.DrTrDOF = False   #Drivetrain rotational-flexibility DOF (flag)
	    self.GenDOF = False   #Generator DOF (flag)
	    self.YawDOF = False   #Yaw DOF (flag)
	    self.TwFADOF1 = False   #First fore-aft tower bending-mode DOF (flag)
	    self.TwFADOF2 = False   #Second fore-aft tower bending-mode DOF (flag)
	    self.TwSSDOF1 = False   #First side-to-side tower bending-mode DOF (flag)
	    self.TwSSDOF2 = False   #Second side-to-side tower bending-mode DOF (flag)
	    self.CompAero = False   #Compute aerodynamic forces (flag)
	    self.CompNoise = False   #Compute aerodynamic noise (flag)
	    # INITIAL CONDITIONS 
	    self.OoPDefl = 0.0   #Initial out-of-plane blade-tip displacement (meters)
	    self.IPDefl = 0.0   #Initial in-plane blade-tip deflection (meters)
	    self.TeetDefl = 0.0   #Initial or fixed teeter angle (degrees) [unused for 3 blades]
	    self.Azimuth = 0.0   #Initial azimuth angle for blade 1 (degrees)
	    self.RotSpeed = 0.0   #Initial or fixed rotor speed (rpm)
	    self.NacYaw = 0.0   #Initial or fixed nacelle-yaw angle (degrees)
	    self.TTDspFA = 0.0   #Initial fore-aft tower-top displacement (meters)
	    self.TTDspSS = 0.0   #Initial side-to-side tower-top displacement (meters)
	    # TURBINE CONFIGURATION 
	    self.TipRad = 0.0   #The distance from the rotor apex to the blade tip (meters)
	    self.HubRad = 0.0   #The distance from the rotor apex to the blade root (meters)
	    self.PSpnElN = 0   #Number of the innermost blade element which is still part of the pitchable portion of the blade for partial-span pitch control [1 to BldNodes] [CURRENTLY IGNORED] (-)
	    self.UndSling = 0.0   #Undersling length [distance from teeter pin to the rotor apex] (meters) [unused for 3 blades]
	    self.HubCM = 0.0   #Distance from rotor apex to hub mass [positive downwind] (meters)
	    self.OverHang = 0.0   #Distance from yaw axis to rotor apex [3 blades] or teeter pin [2 blades] (meters)
	    self.NacCMxn = 0.0   #Downwind distance from the tower-top to the nacelle CM (meters)
	    self.NacCMyn = 0.0   #Lateral  distance from the tower-top to the nacelle CM (meters)
	    self.NacCMzn = 0.0   #Vertical distance from the tower-top to the nacelle CM (meters)
	    self.TowerHt = 0.0   #Height of tower above ground level [onshore] or MSL [offshore] (meters)
	    self.Twr2Shft = 0.0   #Vertical distance from the tower-top to the rotor shaft (meters)
	    self.TwrRBHt = 0.0   #Tower rigid base height (meters)
	    self.ShftTilt = 0.0   #Rotor shaft tilt angle (degrees)
	    self.Delta3 = 0.0   #Delta-3 angle for teetering rotors (degrees) [unused for 3 blades]
	    self.PreCone1 = 0.0   #Blade 1 cone angle (degrees)
	    self.PreCone2 = 0.0   #Blade 2 cone angle (degrees)
	    self.PreCone3 = 0.0   #Blade 3 cone angle (degrees) [unused for 2 blades]
	    self.AzimB1Up = 0.0   #Azimuth value to use for I/O when blade 1 points up (degrees)
	    # MASS AND INERTIA 
	    self.YawBrMass = 0.0   #Yaw bearing mass (kg)
	    self.NacMass = 0.0   #Nacelle mass (kg)
	    self.HubMass = 0.0   #Hub mass (kg)
	    self.TipMass1 = 0.0   #Tip-brake mass, blade 1 (kg)
	    self.TipMass2 = 0.0   #Tip-brake mass, blade 2 (kg)
	    self.TipMass3 = 0.0   #Tip-brake mass, blade 3 (kg) [unused for 2 blades]
	    self.NacYIner = 0.0   #Nacelle inertia about yaw axis (kg m^2)
	    self.GenIner = 0.0   #Generator inertia about HSS (kg m^2)
	    self.HubIner = 0.0   #Hub inertia about rotor axis [3 blades] or teeter axis [2 blades] (kg m^2)
	    # DRIVETRAIN
	    self.GBoxEff = 0.0   #Gearbox efficiency (%)
	    self.GenEff = 0.0   #Generator efficiency [ignored by the Thevenin and user-defined generator models] (%)
	    self.GBRatio = 0.0   #Gearbox ratio (-)
	    self.GBRevers = False   #Gearbox reversal {T: if rotor and generator rotate in opposite directions} (flag)
	    self.HSSBrTqF = 0.0   #Fully deployed HSS-brake torque (N-m)
	    self.HSSBrDT = 0.0   #Time for HSS-brake to reach full deployment once initiated (sec) [used only when HSSBrMode=1]
	    self.DynBrkFi = ''   #File containing a mech-gen-torque vs HSS-speed curve for a dynamic brake [CURRENTLY IGNORED] (quoted string)
	    self.DTTorSpr = 0.0   #Drivetrain torsional spring (N-m/rad)
	    self.DTTorDmp = 0.0   #Drivetrain torsional damper (N-m/(rad/s))
	    # SIMPLE INDUCTION GENERATOR
	    self.SIG_SlPc = 0.0   #Rated generator slip percentage (%) [used only when VSContrl=0 and GenModel=1]
	    self.SIG_SySp = 0.0   #Synchronous (zero-torque) generator speed (rpm) [used only when VSContrl=0 and GenModel=1]
	    self.SIG_RtTq = 0.0   #Rated torque (N-m) [used only when VSContrl=0 and GenModel=1]
	    self.SIG_PORt = 0.0   #Pull-out ratio (Tpullout/Trated) (-) [used only when VSContrl=0 and GenModel=1]
	    # THEVENIN-EQUIVALENT INDUCTION GENERATOR 
	    self.TEC_Freq = 0.0   #Line frequency [50 or 60] (Hz) [used only when VSContrl=0 and GenModel=2]
	    self.TEC_NPol = 0   #Number of poles [even integer > 0] (-) [used only when VSContrl=0 and GenModel=2]
	    self.TEC_SRes = 0.0   #Stator resistance (ohms) [used only when VSContrl=0 and GenModel=2]
	    self.TEC_RRes = 0.0   #Rotor resistance (ohms) [used only when VSContrl=0 and GenModel=2]
	    self.TEC_VLL = 0.0   #Line-to-line RMS voltage (volts) [used only when VSContrl=0 and GenModel=2]
	    self.TEC_SLR = 0.0   #Stator leakage reactance (ohms) [used only when VSContrl=0 and GenModel=2]
	    self.TEC_RLR = 0.0   #Rotor leakage reactance (ohms) [used only when VSContrl=0 and GenModel=2]
	    self.TEC_MR = 0.0   #Magnetizing reactance (ohms) [used only when VSContrl=0 and GenModel=2]
	    # PLATFORM 
	    self.PtfmModel = 0   #Enum(0, (0,1,2,3), desc='Platform model {0: none, 1: onshore, 2: fixed bottom offshore, 3: floating offshore} (switch)
	    self.PtfmFile = ''   #Name of file containing platform properties (quoted string) [unused when PtfmModel=0]
	    # TOWER 
	    self.TwrNodes = 0   #Number of tower nodes used for analysis (-)
	    self.TwrFile = ''   #Name of file containing tower properties (quoted string)
	    # NACELLE-YAW 
	    self.awSpr = 0.0   #Nacelle-yaw spring constant (N-m/rad)
	    self.YawDamp = 0.0   #Nacelle-yaw damping constant (N-m/(rad/s))
	    self.YawNeut = 0.0   #Neutral yaw position--yaw spring force is zero at this yaw (degrees)
	    # FURLING
	    self.Furling = False   #Read in additional model properties for furling turbine (flag)
	    self.FurlFile = ''   #Name of file containing furling properties (quoted string) [unused when Furling=False]
	    # ROTOR-TEETER 
	    self.TeetMod = 0   #Enum(0, (0,1,2), desc='Rotor-teeter spring/damper model {0: none, 1: standard, 2: user-defined from routine UserTeet} (switch) [unused for 3 blades]
	    self.TeetDmpP = 0.0   #Rotor-teeter damper position (degrees) [used only for 2 blades and when TeetMod=1]
	    self.TeetDmp = 0.0   #Rotor-teeter damping constant (N-m/(rad/s)) [used only for 2 blades and when TeetMod=1]
	    self.TeetCDmp = 0.0   #Rotor-teeter rate-independent Coulomb-damping moment (N-m) [used only for 2 blades and when TeetMod=1]
	    self.TeetSStP = 0.0   #Rotor-teeter soft-stop position (degrees) [used only for 2 blades and when TeetMod=1]
	    self.TeetHStP = 0.0   #Rotor-teeter hard-stop position (degrees) [used only for 2 blades and when TeetMod=1]
	    self.TeetSSSp = 0.0   #Rotor-teeter soft-stop linear-spring constant (N-m/rad) [used only for 2 blades and when TeetMod=1]
	    self.TeetHSSp = 0.0   #Rotor-teeter hard-stop linear-spring constant (N-m/rad) [used only for 2 blades and when TeetMod=1]
	    # TIP-BRAKE 
	    self.TBDrConN = 0.0   #Tip-brake drag constant during normal operation, Cd*Area (m^2)
	    self.TBDrConD = 0.0   #Tip-brake drag constant during fully-deployed operation, Cd*Area (m^2)
	    self.TpBrDT = 0.0   #Time for tip-brake to reach full deployment once released (sec)
	    # BLADE
	    self.BldFile1 = ''   #Name of file containing properties for blade 1 (quoted string)
	    self.BldFile2 = ''   #Name of file containing properties for blade 2 (quoted string)
	    self.BldFile3 = ''   #Name of file containing properties for blade 3 (quoted string) [unused for 2 blades]
	    # AERODYN 
	    self.ADFile = ''   #Name of file containing AeroDyn input parameters (quoted string)
	    # NOISE
	    self.NoiseFile = ''   #Name of file containing aerodynamic noise input parameters (quoted string) [used only when CompNoise=True]
	    # ADAMS
	    self.ADAMSFile = ''   #Name of file containing ADAMS-specific input parameters (quoted string) [unused when ADAMSPrep=1]
	    # LINEARIZATION CONTROL 
	    self.LinFile = ''   #Name of file containing FAST linearization parameters (quoted string) [unused when AnalMode=1]
	    # OUTPUT
	    self.SumPrint = False   #Print summary data to "<RootName>.fsm" (flag)
	    self.OutFileFmt = 1   #Enum(1, (1,2), desc='(unused in new versions) Format for tabular (time-marching) output file(s) (1: text file [<RootName>.out], 2: binary
	    self.TabDelim = True   #Generate a tab-delimited tabular output file. (flag)
	    self.OutFmt = ''   #Format used for tabular output except time.  Resulting field should be 10 characters. (quoted string)  [not checked for validity!]
	    self.TStart = 0.0   #Time to begin tabular output (s)
	    self.DecFact = 0   #Decimation factor for tabular output {1: output every time step} (-)
	    self.SttsTime = 0.0   #Amount of time between screen status messages (sec)
	    self.NcIMUxn = 0.0   #Downwind distance from the tower-top to the nacelle IMU (meters)
	    self.NcIMUyn = 0.0   #Lateral  distance from the tower-top to the nacelle IMU (meters)
	    self.NcIMUzn = 0.0   #Vertical distance from the tower-top to the nacelle IMU (meters)
	    self.ShftGagL = 0.0   #Distance from rotor apex [3 blades] or teeter pin [2 blades] to shaft strain gages [positive for upwind rotors] (meters)
	    self.NTwGages = 0   #Number of tower nodes that have strain gages for output [0 to 9] (-)
	    self.TwrGagNd  = []   #]List of tower nodes that have strain gages [1 to TwrNodes] (-) [unused if NTwGages=0]
	    self.NBlGages = 0   #Number of blade nodes that have strain gages for output [0 to 9] (-)
	    self.BldGagNd = []   #]List of blade nodes that have strain gages [1 to BldNodes] (-) [unused if NBlGages=0]

	    # Outlist
	    #See Variable Tree