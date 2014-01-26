
from openmdao.main.api import VariableTree, Container, Component
from openmdao.lib.datatypes.api import Int, Str, Float, List, Array, Enum, Bool, VarTree, Dict

# Variable Trees

class SimpleWind(VariableTree):

    TimeSteps = Int(desc='number of time steps')

    Time = Array(desc='time step')
    HorSpd = Array(desc='horizontal wind speed')
    WindDir = Array(desc='wind direction')
    VerSpd = Array(desc='vertical wind speed')
    HorShr = Array(desc='horizontal shear')
    VerShr = Array(desc='vertical power-law shear')
    LnVShr = Array(desc='vertical linear shear')
    GstSpd = Array(desc='gust speed not sheared by Aerodyn')

class ADAirfoilPolar(VariableTree):

    IDParam = Float(desc='Table ID Parameter (Typically Reynolds number)')
    StallAngle = Float(desc='Stall angle (deg)')
    ZeroCn = Float(desc='Zero lift angle of attack (deg)')
    CnSlope = Float(desc='Cn slope for zero lift (dimensionless)')
    CnPosStall = Float(desc='Cn at stall value for positive angle of attack')
    CnNegStall = Float(desc='Cn at stall value for negative angle of attack')
    alphaCdMin = Float(desc='Angle of attack for minimum CD (deg)')
    CdMin = Float(desc='Minimum Cd Value')

    alpha = Array(desc='angle of attack')
    cl = Array(desc='coefficient of lift')
    cd = Array(desc='coefficient of drag')
    cm = Array(desc='coefficient of the pitching moment')

class ADAirfoil(VariableTree):

    description = Str(desc='description of airfoil')
    number_tables = Int(desc='number of airfoil polars')
    af_tables = List(ADAirfoilPolar, desc='list of airfoil polars')

class ADBladeAeroGeometry(VariableTree):

    NumFoil = Int(desc='Number of airfoil files (-)')
    FoilNm = Array(desc='Names of the airfoil files [NumFoil lines] (quoted strings)')
    #TODO: reading in actual airfoil data
    af_data = List(ADAirfoil, desc='list of airfoild data sets')

    BldNodes = Int(desc='Number of blade nodes used for analysis')

    RNodes = Array(desc='Distance from blade root to center of element')
    AeroTwst = Array(units='deg',desc='Twist at RNodes locations')
    DRNodes = Array(desc='Span-wise width of the blade element, measured along the span of the blade')
    Chord = Array(units='m',desc='Chord length at node locations; planform area = chord*DRNodes')
    NFoil = Array(desc='Airfoil ID Number')
    PrnElm = Array(desc='Flag for printing element ouput for blade section')


class ADAero(VariableTree):

    # General Model Inputs
    SysUnits = Enum('SI', ('SI','ENG'), desc='System of units for used for input and output [must be SI for FAST] (unquoted string)')
    StallMod = Enum('BEDDOES', ('BEDDOES', 'STEADY'), desc = 'Dynamic stall included [BEDDOES or STEADY] (unquoted string)')
    UseCM = Enum('NO_CM', ('NO_CM', 'USE_CM'), desc = 'Use aerodynamic pitching moment model? [USE_CM or NO_CM] (unquoted string)')
    InfModel = Enum('EQUIL', ('EQUIL', 'DYNIN'), desc = 'Inflow model [DYNIN or EQUIL] (unquoted string)')
    IndModel = Enum('SWIRL', ('NONE', 'WAKE', 'SWIRL'), desc = 'Induction-factor model [NONE or WAKE or SWIRL] (unquoted string)')
    AToler = Float(desc = 'Induction-factor tolerance (convergence criteria) (-)')
    TLModel = Enum('PRANDtl', ('PRANDtl', 'GTECH', 'NONE'), desc = 'Tip-loss model (EQUIL only) [PRANDtl, GTECH, or NONE] (unquoted string)')
    HLModel = Enum('PRANDtl', ('PRANDtl', 'GTECH', 'NONE'), desc = 'Hub-loss model (EQUIL only) [PRANdtl or NONE] (unquoted string)')

    # Turbine Inputs
    WindFile = Str(desc = 'Initial wind file from template import (quoted string)')
    wind_file_type = Enum('hh', ('hh', 'bts', 'wnd'), desc='type of wind file')
    HH = Float(units='m', desc= 'Wind reference (hub) height [TowerHt+Twr2Shft+OverHang*SIN(ShftTilt)] (m)')
    TwrShad = Float(0.0, desc= 'Tower-shadow velocity deficit (-)')
    ShadHWid = Float(9999.9, units='m', desc='Tower-shadow half width (m)')
    T_Shad_Refpt = Float(9999.9, units='m', desc='Tower-shadow reference point (m)')

    # Wind Aero Inputs
    AirDens = Float(1.225, units='kg / (m**3)', desc='Air density (kg/m^3)')
    KinVisc = Float(1.464e-5, units='m**2 / s', desc='Kinematic air viscosity [CURRENTLY IGNORED] (m^2/sec)')
    DTAero = Float(0.02479, units='s', desc = 'Time interval for aerodynamic calculations (sec)')

    # Blade Geometry and Airfoil Information
    blade_vt = VarTree(ADBladeAeroGeometry(), desc = 'Variable tree for blade geometry and airfoil information')

class FstBladeStrucGeometry(VariableTree):


    description = Str(desc='Blade file description')

    # General Model Inputs
    NBlInpSt = Int(desc='Number of blade input stations (-)')
    CalcBMode = Bool(desc='Calculate blade mode shapes internally {T: ignore mode shapes from below, F: use mode shapes from below} [CURRENTLY IGNORED] (flag)')
    BldFlDmp1 = Float(desc='Blade flap mode #1 structural damping in percent of critical (%)')
    BldFlDmp2 = Float(desc='Blade flap mode #2 structural damping in percent of critical (%)')
    BldEdDmp1 = Float(desc='Blade edge mode #1 structural damping in percent of critical (%)')
    FlStTunr1 = Float(desc='Blade flapwise modal stiffness tuner, 1st mode (-)')
    FlStTunr2 = Float(desc='Blade flapwise modal stiffness tuner, 2nd mode (-)')
    AdjBlMs = Float(desc='Factor to adjust blade mass density (-)')
    AdjFlSt = Float(desc='Factor to adjust blade flap stiffness (-)')
    AdjEdSt = Float(desc='Factor to adjust blade edge stiffness (-)')
    
    # Distributed Blade Properties
    BlFract = Array()
    AeroCent = Array()
    StrcTwst = Array()
    BMassDen = Array()
    FlpStff = Array()
    EdgStff = Array()
    GJStff = Array()
    EAStff = Array()
    Alpha = Array()
    FlpIner = Array()
    EdgIner = Array()
    PrecrvRef = Array()
    FlpcgOf = Array()
    Edgcgof = Array()
    FlpEAOf = Array()
    EdgEAOf = Array()
    
    # Blade Mode Shapes
    BldFl1Sh = Array()
    BldFl2Sh = Array()
    BldEdgSh = Array()

class FstTowerStrucGeometry(VariableTree):

    description = Str(desc='description of tower')

    # General Tower Paramters
    NTwInptSt = Int(desc='Number of input stations to specify tower geometry')
    CalcTMode = Bool(desc='alculate tower mode shapes internally {T: ignore mode shapes from below, F: use mode shapes from below} [CURRENTLY IGNORED] (flag)')
    TwrFADmp1 = Float(desc='Tower 1st fore-aft mode structural damping ratio (%)')
    TwrFADmp2 = Float(desc='Tower 2nd fore-aft mode structural damping ratio (%)')
    TwrSSDmp1 = Float(desc='Tower 1st side-to-side mode structural damping ratio (%)')
    TwrSSDmp2 = Float(desc='Tower 2nd side-to-side mode structural damping ratio (%)')

    # Tower Adjustment Factors
    FAStTunr1 = Float(desc='Tower fore-aft modal stiffness tuner, 1st mode (-)')
    FAStTunr2 = Float(desc='Tower fore-aft modal stiffness tuner, 2nd mode (-)')
    SSStTunr1 = Float(desc='Tower side-to-side stiffness tuner, 1st mode (-)')
    SSStTunr2 = Float(desc='Tower side-to-side stiffness tuner, 2nd mode (-)')
    AdjTwMa = Float(desc='Factor to adjust tower mass density (-)')
    AdjFASt = Float(desc='Factor to adjust tower fore-aft stiffness (-)')
    AdjSSSt = Float(desc='Factor to adjust tower side-to-side stiffness (-)')
 
    # Distributed Tower Properties   
    HtFract = Array()
    TMassDen = Array()
    TwFAStif = Array()
    TwSSStif = Array()
    TwGJStif = Array()
    TwEAStif = Array()
    TwFAIner = Array()
    TwSSIner = Array()
    TwFAcgOf = Array()
    TwSScgOf = Array()
    
    # Tower Mode Shapes
    TwFAM1Sh = Array(desc='Tower Fore-Aft Mode 1 Shape Coefficients x^2, x^3, x^4, x^5, x^6')
    TwFAM2Sh = Array(desc='Tower Fore-Aft Mode 2 Shape Coefficients x^2, x^3, x^4, x^5, x^6')
    TwSSM1Sh = Array(desc='Tower Side-to-Side Mode 1 Shape Coefficients x^2, x^3, x^4, x^5, x^6')
    TwSSM2Sh = Array(desc='Tower Side-to-Side Mode 2 Shape Coefficients x^2, x^3, x^4, x^5, x^6')      

class FstPlatformModel(VariableTree):

    description = Str(desc='description of platform')

    # FEATURE FLAGS (CONT)
    PtfmSgDOF = Bool(desc='Platform horizontal surge translation DOF (flag)')
    PtfmSwDOF = Bool(desc='Platform horizontal sway translation DOF (flag)')
    PtfmHvDOF = Bool(desc='Platform vertical heave translation DOF (flag)')
    PtfmRDOF  = Bool(desc='Platform roll tilt rotation DOF (flag)')
    PtfmPDOF  = Bool(desc='Platform pitch tilt rotation DOF (flag)')
    PtfmYDOF  = Bool(desc='Platform yaw rotation DOF (flag)')
    
    # INITIAL CONDITIONS (CONT)
    PtfmSurge = Float(desc='Initial or fixed horizontal surge translational displacement of platform (meters)')
    PtfmSway  = Float(desc='Initial or fixed horizontal sway translational displacement of platform (meters)')
    PtfmHeave = Float(desc='Initial or fixed vertical heave translational displacement of platform (meters)')
    PtfmRoll  = Float(desc='Initial or fixed roll tilt rotational displacement of platform (degrees)')
    PtfmPitch = Float(desc='Initial or fixed pitch tilt rotational displacement of platform (degrees)')
    PtfmYaw   = Float(desc='Initial or fixed yaw rotational displacement of platform (degrees)')
    
    # TURBINE CONFIGURATION (CONT)
    TwrDraft  = Float(desc='Downward distance from the ground level [onshore] or MSL [offshore] to the tower base platform connection (meters)')
    PtfmCM    = Float(desc='Downward distance from the ground level [onshore] or MSL [offshore] to the platform CM (meters)')
    PtfmRef   = Float(desc='Downward distance from the ground level [onshore] or MSL [offshore] to the platform reference point (meters)')
    
    # MASS AND INERTIA (CONT) 
    PtfmMass  = Float(desc='Platform mass (kg)')
    PtfmRIner = Float(desc='Platform inertia for roll tilt rotation about the platform CM (kg m^2)')
    PtfmPIner = Float(desc='Platform inertia for pitch tilt rotation about the platform CM (kg m^2)')
    PtfmYIner = Float(desc='Platfrom inertia for yaw rotation about the platform CM (kg m^2)')
    
    # PLATFORM (CONT) 
    PtfmLdMod  = Enum(0, (0,1), desc='{0: none, 1: user-defined from routine UserPtfmLd} (switch)')
    
    # TOWER (CONT) 
    TwrLdMod  = Enum(0, (0,1,2), desc='Tower loading model (0: none, 1: Morisons equation, 2: user-defined from routine UserTwrLd) (switch)')
    TwrDiam   = Float(desc='Tower diameter in Morisons equation (meters) [used only when TwrLdMod=1]')
    TwrCA     = Float(desc='Normalized hydrodynamic added mass   coefficient in Morisons equation (-) [used only when TwrLdMod=1] [determines TwrCM=1+TwrCA]')
    TwrCD     = Float(desc='Normalized hydrodynamic viscous drag coefficient in Morisons equation (-) [used only when TwrLdMod=1]')
    
    # WAVES 
    WtrDens   = Float(desc='Water density (kg/m^3)')
    WtrDpth   = Float(desc='Water depth (meters)')
    WaveMod   = Enum(0, (0,1,2,3,4), desc='Incident wave kinematics model {0: none=still water, 1: plane progressive (regular), 2: JONSWAP/Pierson-Moskowitz spectrum (irregular), 3: user-defind spectrum from routine UserWaveSpctrm (irregular), 4: GH Bladed wave data} (switch)')
    WaveStMod = Enum(0, (0,1,2,3), desc='Model for stretching incident wave kinematics to instantaneous free surface {0: none=no stretching, 1: vertical stretching, 2: extrapolation stretching, 3: Wheeler stretching} (switch) [unused when WaveMod=0]')
    WaveTMax  = Float(desc='Analysis time for incident wave calculations (sec) [unused when WaveMod=0] [determines WaveDOmega=2Pi/WaveTMax in the IFFT]')
    WaveDT    = Float(desc='Time step for incident wave calculations (sec) [unused when WaveMod=0] [0.1<=WaveDT<=1.0 recommended] [determines WaveOmegaMax=Pi/WaveDT in the IFFT]')
    WaveHs    = Float(desc='Significant wave height of incident waves (meters) [used only when WaveMod=1 or 2]')
    WaveTp    = Float(desc='Peak spectral period of incident waves (sec) [used only when WaveMod=1 or 2]')
    WavePkShp = Float(desc='Peak shape parameter of incident wave spectrum (-) or DEFAULT (unquoted string) [used only when WaveMod=2] [use 1.0 for Pierson-Moskowitz]')
    WaveDir   = Float(desc='Incident wave propagation heading direction (degrees) [unused when WaveMod=0 or 4]')
    WaveSeed1 = Int(desc='First  random seed of incident waves [-2147483648 to 2147483647] (-) [unused when WaveMod=0 or 4]')
    WaveSeed2 = Int(desc='Second random seed of incident waves [-2147483648 to 2147483647] (-) [unused when WaveMod=0 or 4]')
    GHWvFile  = Str(desc='Root name of GH Bladed files containing wave data (quoted string) [used only when WaveMod=4]')

    # CURRENT
    CurrMod   = Float(desc='Current profile model {0: none=no current, 1: standard, 2: user-defined from routine UserCurrent} (switch)')
    CurrSSV0  = Float(desc='Sub-surface current velocity at still water level (m/s) [used only when CurrMod=1]')
    CurrSSDir = Float(desc='Sub-surface current heading direction (degrees) or DEFAULT (unquoted string) [used only when CurrMod=1]')
    CurrNSRef = Float(desc='Near-surface current reference depth (meters) [used only when CurrMod=1]')
    CurrNSV0  = Float(desc='Near-surface current velocity at still water level (m/s) [used only when CurrMod=1]')
    CurrNSDir = Float(desc='Near-surface current heading direction (degrees) [used only when CurrMod=1]')
    CurrDIV   = Float(desc='Depth-independent current velocity (m/s) [used only when CurrMod=1]')
    CurrDIDir = Float(desc='Depth-independent current heading direction (degrees) [used only when CurrMod=1]')

    # OUTPUT (CONT) 
    NWaveKin = Int(desc='Number of points where the wave kinematics can be output [0 to 9] (-)')
    WaveKinNd = Int(desc='List of tower nodes that have wave kinematics sensors [1 to TwrNodes] (-) [unused if NWaveKin=0]')

class FstModel(VariableTree):

    # FAST Wind Information
    simple_wind_vt = VarTree(SimpleWind(), desc='Simple wind input model')
    
    # FAST Hydro Information
    platform_vt = VarTree(FstPlatformModel(), desc='Model of platform foundation')

    # FAST Aerodynamic Information
    aero_vt = VarTree(ADAero(), desc='Aerodynamic settings, blade design and airfoils')

    # FAST Structural Information
    fst_blade_vt = VarTree(FstBladeStrucGeometry(), desc='Structural information on the blade and properties')
    fst_tower_vt = VarTree(FstTowerStrucGeometry(), desc='Structural information on the tower and properties')

    # FAST Inputs
    description = Str(desc='description of platform')
    Echo = Bool(desc='Echo input data to "echo.out" (flag)')
    ADAMSPrep = Enum(1, (1,2,3), desc='ADAMS preprocessor mode {1: Run FAST, 2: use FAST as a preprocessor to create an ADAMS model, 3: do both} (switch)')
    AnalMode = Enum(1, (1,2), desc='Analysis mode {1: Run a time-marching simulation, 2: create a periodic linearized model} (switch)')
    NumBl = Int(desc='Number of blades (-)')
    TMax = Float(desc='Total run time (s)')
    DT = Float(desc='Integration time step (s)')
    # TURBINE CONTROL
    YCMode = Enum(0, (0,1,2), desc='Yaw control mode {0: none, 1: user-defined from routine UserYawCont, 2: user-defined from Simulink} (switch)')
    TYCOn = Float(desc='Time to enable active yaw control (s) [unused when YCMode=0]')
    PCMode = Enum(0, (0,1,2), desc='Pitch control mode {0: none, 1: user-defined from routine PitchCntrl, 2: user-defined from Simulink} (switch)')
    TPCOn = Float(desc='Time to enable active pitch control (s) [unused when PCMode=0]')
    VSContrl = Enum(0, (0,1,2,3), desc='Variable-speed control mode {0: none, 1: simple VS, 2: user-defined from routine UserVSCont, 3: user-defined from Simulink} (switch)')
    VS_RtGnSp = Float(desc='Rated generator speed for simple variable-speed generator control (HSS side) (rpm) [used only when VSContrl=1]')
    VS_RtTq = Float(desc='Rated generator torque/constant generator torque in Region 3 for simple variable-speed generator control (HSS side) (N-m) [used only when VSContrl=1]')
    VS_Rgn2K = Float(desc='Generator torque constant in Region 2 for simple variable-speed generator control (HSS side) (N-m/rpm^2) [used only when VSContrl=1]')
    VS_SlPc = Float(desc='Rated generator slip percentage in Region 2 1/2 for simple variable-speed generator control (%) [used only when VSContrl=1]')
    GenModel = Enum(1, (1,2,3), desc='Generator model {1: simple, 2: Thevenin, 3: user-defined from routine UserGen} (switch) [used only when VSContrl=0]')
    GenTiStr = Bool(desc='Method to start the generator {T: timed using TimGenOn, F: generator speed using SpdGenOn} (flag)')
    GenTiStp = Bool(desc='Method to stop the generator {T: timed using TimGenOf, F: when generator power = 0} (flag)')
    SpdGenOn = Float(desc='Generator speed to turn on the generator for a startup (HSS speed) (rpm) [used only when GenTiStr=False]')
    TimGenOn = Float(desc='Time to turn on the generator for a startup (s) [used only when GenTiStr=True]')
    TimGenOf = Float(desc='Time to turn off the generator (s) [used only when GenTiStp=True]')
    HSSBrMode = Enum(1, (1,2), desc='HSS brake model {1: simple, 2: user-defined from routine UserHSSBr} (switch)')
    THSSBrDp = Float(desc='Time to initiate deployment of the HSS brake (s)')
    TiDynBrk = Float(desc='Time to initiate deployment of the dynamic generator brake [CURRENTLY IGNORED] (s)')
    TTpBrDp1 = Float(desc='Time to initiate deployment of tip brake 1 (s)')
    TTpBrDp2 = Float(desc='Time to initiate deployment of tip brake 2 (s)')
    TTpBrDp3 = Float(desc='Time to initiate deployment of tip brake 3 (s) [unused for 2 blades]')
    TBDepISp1 = Float(desc='Deployment-initiation speed for the tip brake on blade 1 (rpm)')
    TBDepISp2 = Float(desc='Deployment-initiation speed for the tip brake on blade 2 (rpm)')
    TBDepISp3 = Float(desc='Deployment-initiation speed for the tip brake on blade 3 (rpm) [unused for 2 blades]')
    TYawManS = Float(desc='Time to start override yaw maneuver and end standard yaw control (s)')
    TYawManE = Float(desc='Time at which override yaw maneuver reaches final yaw angle (s)')
    NacYawF = Float(desc='Final yaw angle for override yaw maneuvers (degrees)')
    TPitManS1 = Float(desc='Time to start override pitch maneuver for blade 1 and end standard pitch control (s)')
    TPitManS2 = Float(desc='Time to start override pitch maneuver for blade 2 and end standard pitch control (s)')
    TPitManS3 = Float(desc='Time to start override pitch maneuver for blade 3 and end standard pitch control (s) [unused for 2 blades]')
    TPitManE1 = Float(desc='Time at which override pitch maneuver for blade 1 reaches final pitch (s)')
    TPitManE2 = Float(desc='Time at which override pitch maneuver for blade 2 reaches final pitch (s)')
    TPitManE3 = Float(desc='Time at which override pitch maneuver for blade 3 reaches final pitch (s) [unused for 2 blades]')
    BlPitch1  = Float(desc='Blade 1 initial pitch (degrees)')
    BlPitch2  = Float(desc='Blade 2 initial pitch (degrees)')
    BlPitch3  = Float(desc='Blade 3 initial pitch (degrees) [unused for 2 blades]')
    B1PitchF1 = Float(desc='Blade 1 final pitch for pitch maneuvers (degrees)')
    B1PitchF2 = Float(desc='Blade 2 final pitch for pitch maneuvers (degrees)')
    B1PitchF3 = Float(desc='Blade 3 final pitch for pitch maneuvers (degrees) [unused for 2 blades]')
    # ENVIRONMENTAL CONDITIONS 
    Gravity = Float(desc='Gravitational acceleration (m/s^2)')
    # FEATURE FLAGS 
    FlapDOF1 = Bool(desc='First flapwise blade mode DOF (flag)')
    FlapDOF2 = Bool(desc=' Second flapwise blade mode DOF (flag)')
    EdgeDOF = Bool(desc='First edgewise blade mode DOF (flag)')
    TeetDOF = Bool(desc='Rotor-teeter DOF (flag) [unused for 3 blades]')
    DrTrDOF = Bool(desc='Drivetrain rotational-flexibility DOF (flag)')
    GenDOF = Bool(desc='Generator DOF (flag)')
    YawDOF = Bool(desc='Yaw DOF (flag)')
    TwFADOF1 = Bool(desc='First fore-aft tower bending-mode DOF (flag)')
    TwFADOF2 = Bool(desc='Second fore-aft tower bending-mode DOF (flag)')
    TwSSDOF1 = Bool(desc='First side-to-side tower bending-mode DOF (flag)')
    TwSSDOF2 = Bool(desc='Second side-to-side tower bending-mode DOF (flag)')
    CompAero = Bool(desc='Compute aerodynamic forces (flag)')
    CompNoise = Bool(desc='Compute aerodynamic noise (flag)')
    # INITIAL CONDITIONS 
    OoPDefl = Float(desc='Initial out-of-plane blade-tip displacement (meters)')
    IPDefl = Float(desc='Initial in-plane blade-tip deflection (meters)')
    TeetDefl = Float(desc='Initial or fixed teeter angle (degrees) [unused for 3 blades]')
    Azimuth = Float(desc='Initial azimuth angle for blade 1 (degrees)')
    RotSpeed = Float(desc='Initial or fixed rotor speed (rpm)')
    NacYaw = Float(desc='Initial or fixed nacelle-yaw angle (degrees)')
    TTDspFA = Float(desc='Initial fore-aft tower-top displacement (meters)')
    TTDspSS = Float(desc='Initial side-to-side tower-top displacement (meters)')
    # TURBINE CONFIGURATION 
    TipRad = Float(desc='The distance from the rotor apex to the blade tip (meters)')
    HubRad = Float(desc='The distance from the rotor apex to the blade root (meters)')
    PSpnElN = Int(desc='Number of the innermost blade element which is still part of the pitchable portion of the blade for partial-span pitch control [1 to BldNodes] [CURRENTLY IGNORED] (-)')
    UndSling = Float(desc='Undersling length [distance from teeter pin to the rotor apex] (meters) [unused for 3 blades]')
    HubCM = Float(desc='Distance from rotor apex to hub mass [positive downwind] (meters)')
    OverHang = Float(desc='Distance from yaw axis to rotor apex [3 blades] or teeter pin [2 blades] (meters)')
    NacCMxn = Float(desc='Downwind distance from the tower-top to the nacelle CM (meters)')
    NacCMyn = Float(desc='Lateral  distance from the tower-top to the nacelle CM (meters)')
    NacCMzn = Float(desc='Vertical distance from the tower-top to the nacelle CM (meters)')
    TowerHt = Float(desc='Height of tower above ground level [onshore] or MSL [offshore] (meters)')
    Twr2Shft = Float(desc='Vertical distance from the tower-top to the rotor shaft (meters)')
    TwrRBHt = Float(desc='Tower rigid base height (meters)')
    ShftTilt = Float(desc='Rotor shaft tilt angle (degrees)')
    Delta3 = Float(desc='Delta-3 angle for teetering rotors (degrees) [unused for 3 blades]')
    PreCone1 = Float(desc='Blade 1 cone angle (degrees)')
    PreCone2 = Float(desc='Blade 2 cone angle (degrees)')
    PreCone3 = Float(desc='Blade 3 cone angle (degrees) [unused for 2 blades]')
    AzimB1Up = Float(desc='Azimuth value to use for I/O when blade 1 points up (degrees)')
    # MASS AND INERTIA 
    YawBrMass = Float(desc='Yaw bearing mass (kg)')
    NacMass = Float(desc='Nacelle mass (kg)')
    HubMass = Float(desc='Hub mass (kg)')
    TipMass1 = Float(desc='Tip-brake mass, blade 1 (kg)')
    TipMass2 = Float(desc='Tip-brake mass, blade 2 (kg)')
    TipMass3 = Float(desc='Tip-brake mass, blade 3 (kg) [unused for 2 blades]')
    NacYIner = Float(desc='Nacelle inertia about yaw axis (kg m^2)')
    GenIner = Float(desc='Generator inertia about HSS (kg m^2)')
    HubIner = Float(desc='Hub inertia about rotor axis [3 blades] or teeter axis [2 blades] (kg m^2)')
    # DRIVETRAIN
    GBoxEff = Float(desc='Gearbox efficiency (%)')
    GenEff = Float(desc='Generator efficiency [ignored by the Thevenin and user-defined generator models] (%)')
    GBRatio = Float(desc='Gearbox ratio (-)')
    GBRevers = Bool(desc='Gearbox reversal {T: if rotor and generator rotate in opposite directions} (flag)')
    HSSBrTqF = Float(desc='Fully deployed HSS-brake torque (N-m)')
    HSSBrDT = Float(desc='Time for HSS-brake to reach full deployment once initiated (sec) [used only when HSSBrMode=1]')
    DynBrkFi = Str(desc='File containing a mech-gen-torque vs HSS-speed curve for a dynamic brake [CURRENTLY IGNORED] (quoted string)')
    DTTorSpr = Float(desc='Drivetrain torsional spring (N-m/rad)')
    DTTorDmp = Float(desc='Drivetrain torsional damper (N-m/(rad/s))')
    # SIMPLE INDUCTION GENERATOR
    SIG_SlPc = Float(desc='Rated generator slip percentage (%) [used only when VSContrl=0 and GenModel=1]')
    SIG_SySp = Float(desc='Synchronous (zero-torque) generator speed (rpm) [used only when VSContrl=0 and GenModel=1]')
    SIG_RtTq = Float(desc='Rated torque (N-m) [used only when VSContrl=0 and GenModel=1]')
    SIG_PORt = Float(desc='Pull-out ratio (Tpullout/Trated) (-) [used only when VSContrl=0 and GenModel=1]')
    # THEVENIN-EQUIVALENT INDUCTION GENERATOR 
    TEC_Freq = Float(desc='Line frequency [50 or 60] (Hz) [used only when VSContrl=0 and GenModel=2]')
    TEC_NPol = Int(desc='Number of poles [even integer > 0] (-) [used only when VSContrl=0 and GenModel=2]')
    TEC_SRes = Float(desc='Stator resistance (ohms) [used only when VSContrl=0 and GenModel=2]')
    TEC_RRes = Float(desc='Rotor resistance (ohms) [used only when VSContrl=0 and GenModel=2]')
    TEC_VLL = Float(desc='Line-to-line RMS voltage (volts) [used only when VSContrl=0 and GenModel=2]')
    TEC_SLR = Float(desc='Stator leakage reactance (ohms) [used only when VSContrl=0 and GenModel=2]')
    TEC_RLR = Float(desc='Rotor leakage reactance (ohms) [used only when VSContrl=0 and GenModel=2]')
    TEC_MR = Float(desc='Magnetizing reactance (ohms) [used only when VSContrl=0 and GenModel=2]')
    # PLATFORM 
    PtfmModel = Enum(0, (0,1,2,3), desc='Platform model {0: none, 1: onshore, 2: fixed bottom offshore, 3: floating offshore} (switch)')
    PtfmFile = Str(desc='Name of file containing platform properties (quoted string) [unused when PtfmModel=0]')
    # TOWER 
    TwrNodes = Int(desc='Number of tower nodes used for analysis (-)')
    TwrFile = Str(desc='Name of file containing tower properties (quoted string)')
    # NACELLE-YAW 
    YawSpr = Float(desc='Nacelle-yaw spring constant (N-m/rad)')
    YawDamp = Float(desc='Nacelle-yaw damping constant (N-m/(rad/s))')
    YawNeut = Float(desc='Neutral yaw position--yaw spring force is zero at this yaw (degrees)')
    # FURLING
    Furling = Bool(False, desc='Read in additional model properties for furling turbine (flag)')
    FurlFile = Str(desc='Name of file containing furling properties (quoted string) [unused when Furling=False]')
    # ROTOR-TEETER 
    TeetMod = Enum(0, (0,1,2), desc='Rotor-teeter spring/damper model {0: none, 1: standard, 2: user-defined from routine UserTeet} (switch) [unused for 3 blades]')
    TeetDmpP = Float(desc='Rotor-teeter damper position (degrees) [used only for 2 blades and when TeetMod=1]')
    TeetDmp = Float(desc='Rotor-teeter damping constant (N-m/(rad/s)) [used only for 2 blades and when TeetMod=1]')
    TeetCDmp = Float(desc='Rotor-teeter rate-independent Coulomb-damping moment (N-m) [used only for 2 blades and when TeetMod=1]')
    TeetSStP = Float(desc='Rotor-teeter soft-stop position (degrees) [used only for 2 blades and when TeetMod=1]')
    TeetHStP = Float(desc='Rotor-teeter hard-stop position (degrees) [used only for 2 blades and when TeetMod=1]')
    TeetSSSp = Float(desc='Rotor-teeter soft-stop linear-spring constant (N-m/rad) [used only for 2 blades and when TeetMod=1]')
    TeetHSSp = Float(desc='Rotor-teeter hard-stop linear-spring constant (N-m/rad) [used only for 2 blades and when TeetMod=1]')
    # TIP-BRAKE 
    TBDrConN = Float(desc='Tip-brake drag constant during normal operation, Cd*Area (m^2)')
    TBDrConD = Float(desc='Tip-brake drag constant during fully-deployed operation, Cd*Area (m^2)')
    TpBrDT = Float(desc='Time for tip-brake to reach full deployment once released (sec)')
    # BLADE
    BldFile1 = Str(desc='Name of file containing properties for blade 1 (quoted string)')
    BldFile2 = Str(desc='Name of file containing properties for blade 2 (quoted string)')
    BldFile3 = Str(desc='Name of file containing properties for blade 3 (quoted string) [unused for 2 blades]')
    # AERODYN 
    ADFile = Str(desc='Name of file containing AeroDyn input parameters (quoted string)')
    # NOISE
    NoiseFile = Str(desc='Name of file containing aerodynamic noise input parameters (quoted string) [used only when CompNoise=True]')
    # ADAMS
    ADAMSFile = Str(desc='Name of file containing ADAMS-specific input parameters (quoted string) [unused when ADAMSPrep=1]')
    # LINEARIZATION CONTROL 
    LinFile = Str(desc='Name of file containing FAST linearization parameters (quoted string) [unused when AnalMode=1]')
    # OUTPUT
    SumPrint = Bool(False, desc='Print summary data to "<RootName>.fsm" (flag)')
    OutFileFmt = Enum(1, (1,2), desc='(unused in new versions) Format for tabular (time-marching) output file(s) (1: text file [<RootName>.out], 2: binary')
    TabDelim = Bool(True, desc='Generate a tab-delimited tabular output file. (flag)')
    OutFmt = Str(desc='Format used for tabular output except time.  Resulting field should be 10 characters. (quoted string)  [not checked for validity!]')
    TStart = Float(desc='Time to begin tabular output (s)')
    DecFact = Int(desc='Decimation factor for tabular output {1: output every time step} (-)')
    SttsTime = Float(desc='Amount of time between screen status messages (sec)')
    NcIMUxn = Float(desc='Downwind distance from the tower-top to the nacelle IMU (meters)')
    NcIMUyn = Float(desc='Lateral  distance from the tower-top to the nacelle IMU (meters)')
    NcIMUzn = Float(desc='Vertical distance from the tower-top to the nacelle IMU (meters)')
    ShftGagL = Float(desc='Distance from rotor apex [3 blades] or teeter pin [2 blades] to shaft strain gages [positive for upwind rotors] (meters)')
    NTwGages = Int(desc='Number of tower nodes that have strain gages for output [0 to 9] (-)')
    TwrGagNd  = List(desc='List of tower nodes that have strain gages [1 to TwrNodes] (-) [unused if NTwGages=0]')
    NBlGages = Int(desc='Number of blade nodes that have strain gages for output [0 to 9] (-)')
    BldGagNd = List(desc='List of blade nodes that have strain gages [1 to BldNodes] (-) [unused if NBlGages=0]')

    # Outlist (TODO)