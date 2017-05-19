
from openmdao.main.api import VariableTree, Component
from openmdao.lib.datatypes.api import Int, Float, Array, List, Str, Enum, Bool, VarTree, Slot
import numpy

from numpy import array, sum, float, int

from fusedwind.interface import base, implement_base



@base
class FASTInitialConditions(VariableTree):

    # Initial Conditions
    WSPtmfPitch = Array(array([0,4,12,15,22]), dtype=float, desc = "Wind speeds used for ptfm pitch interp [m/s]", iotype='in')
    PtfmPitch = Array(array([0,.5, 6, 4, 2.8]), dtype=float, desc = "Pitch points used for ptfm pitch interp [degrees]", iotype='in')
    WSPtfmSurge = Array(array([0, 4, 12.1, 14,22]), dtype=float, desc = "Wind speeds used for ptfm surge interp [m/s]", iotype='in')
    PtfmSurge = Array(array([0,1.6, 12.3, 9.3, 5.9]), dtype=float, desc = "Surge points used for pftm surge interp [m]", iotype='in')
    WSPitch = Array(array([0,12,14,22]), dtype=float, desc = "Wind speeds used for blade pitch interp [m/s]", iotype='in')
    Pitch = Array(array([0,0,6.2,18.9]), dtype=float, desc = "Pitch points used for blade pitch interp [degrees]", iotype='in')
    WSRpm = Array(array([0,4,9,12]), dtype=float, desc = "Wind speeds used for rotor speed interp [m/s]", iotype='in')
    Rpm = Array(array([0,7,14.2,16]), dtype=float, desc = "Rotor speeds used for rotor speed interp [rpm]", iotype='in')


    # May move the following variables if there is a better place for them
    DLC = Float(1.1, desc = "DLC Number", iotype = 'in')
    IEC_WindType = List(Enum('NTM', ('NTM','1ETM','ECD','EWSH+', 'EWSH-', 'EWSV+', 'EWSV-', 'EOG', '1EWM50', '1EWM1')), desc='IEC wind type')
    RefHt = Float(180, desc='Reference height')
   
    def __init__(self, pitch_array):
        super(FASTInitialConditions, self).__init__()
        self.add('Pitch',Array(pitch_array, dtype=float, desc = "Pitch points used for blade pitch interp [degrees]", iotype='in'))


# @base
# class FASTInitialConditions_DLC2_1(FASTInitialConditions):

#     # Initial Conditions
#     WSPtmfPitch = Array(array([0,4,12,15,22]), dtype=float, desc = "Wind speeds used for ptfm pitch interp [m/s]", iotype='in')
#     PtfmPitch = Array(array([0,.5, 6, 4, 2.8]), dtype=float, desc = "Pitch points used for ptfm pitch interp [degrees]", iotype='in')
#     WSPtfmSurge = Array(array([0, 4, 12.1, 14,22]), dtype=float, desc = "Wind speeds used for ptfm surge interp [m/s]", iotype='in')
#     PtfmSurge = Array(array([0,1.6, 12.3, 9.3, 5.9]), dtype=float, desc = "Surge points used for pftm surge interp [m]", iotype='in')
#     WSPitch = Array(array([0,12,14,22]), dtype=float, desc = "Wind speeds used for blade pitch interp [m/s]", iotype='in')
#     Pitch = Array(array([0,0,6.2,18.9]), dtype=float, desc = "Pitch points used for blade pitch interp [degrees]", iotype='in')
#     WSRpm = Array(array([0,4,9,12]), dtype=float, desc = "Wind speeds used for rotor speed interp [m/s]", iotype='in')
#     Rpm = Array(array([0,7,14.2,16]), dtype=float, desc = "Rotor speeds used for rotor speed interp [rpm]", iotype='in')
#     TPitManE1 = Array(array([60, 60.775,61.2,61.6,61.96,62.36]), dtype=float, desc = "#Time at which override pitch maneuver for blade 1 reaches final pitch [s]", iotype='in')
#     TPitManE2 = Array(array([71.325, 70.55, 70.15, 69.75, 69.36, 68.96]), dtype=float, desc = "#Time at which override pitch maneuver for blade 2 reaches final pitch [s]", iotype='in')
#     TPitManE3 = Array(array([71.325, 70.55, 70.15, 69.75, 69.36, 68.96]), dtype=float, desc = "#Time at which override pitch maneuver for blade 3 reaches final pitch [s]", iotype='in')
#     WSTPM = Array(array([12, 14, 16, 18, 20, 22]), dtype=float, desc = "# Corresponding wind speed vales for TPitManE1-3 values", iotype='in')

#     # May move the following variables if there is a better place for them
#     IEC_WindType = List(Enum('NTM', ('NTM','1ETM','ECD','EWSH+', 'EWSH-', 'EWSV+', 'EWSV-', 'EOG', '1EWM50', '1EWM1')), desc='IEC wind type')
#     RefHt = Float(180, desc='Reference height')

# @base
# class FASTInitialConditions_DLC2_3(FASTInitialConditions):

#     # Initial Conditions
#     WSPtmfPitch = Array(array([0,4,12,15,22]), dtype=float, desc = "Wind speeds used for ptfm pitch interp [m/s]", iotype='in')
#     PtfmPitch = Array(array([0,.5, 6, 4, 2.8]), dtype=float, desc = "Pitch points used for ptfm pitch interp [degrees]", iotype='in')
#     WSPtfmSurge = Array(array([0, 4, 12.1, 14,22]), dtype=float, desc = "Wind speeds used for ptfm surge interp [m/s]", iotype='in')
#     PtfmSurge = Array(array([0,1.6, 12.3, 9.3, 5.9]), dtype=float, desc = "Surge points used for pftm surge interp [m]", iotype='in')
#     WSPitch = Array(array([0,12,14,22]), dtype=float, desc = "Wind speeds used for blade pitch interp [m/s]", iotype='in')
#     Pitch = Array(array([0,0,6.2,18.9]), dtype=float, desc = "Pitch points used for blade pitch interp [degrees]", iotype='in')
#     WSRpm = Array(array([0,4,9,12]), dtype=float, desc = "Wind speeds used for rotor speed interp [m/s]", iotype='in')
#     Rpm = Array(array([0,7,14.2,16]), dtype=float, desc = "Rotor speeds used for rotor speed interp [rpm]", iotype='in')
#     TPitManS = Array(array([60.2, 68.6, 62.3]), dtype=float, desc = "#Time to start override pitch maneuver for blades 1-3 and end standard pitch control [s]", iotype='in')
#     TPitManE = Array(array([71.325, 79.725, 71.06]), dtype=float, desc = "Time at which override pitch maneuver for blades 1-3 reaches final pitch [s]", iotype='in')

#     # May move the following variables if there is a better place for them
#     IEC_WindType = List(Enum('NTM', ('NTM','1ETM','ECD','EWSH+', 'EWSH-', 'EWSV+', 'EWSV-', 'EOG', '1EWM50', '1EWM1')), desc='IEC wind type')
#     RefHt = Float(180, desc='Reference height')

@base
class FASTSimulationSpecs(VariableTree):

    # Grid specifications
    numgrid_z = Float(37, iotype='in', desc='TurbSim horizontal grid')
    numgrid_y = Float(39, iotype='in', desc='TurbSim vertical grid')
    grid_height = Float(200, iotype='in', desc='Grid height [m]')
    grid_width = Float(190, iotype='in', desc='Grid height [m]')

    # Simulation specifications
    seeds = Array(array([1,2,3]), dtype=float, desc = "List of seeds", iotype='in') 
    numcases = Float(198, iotype='in', desc='Total number of cases')
    simlength = Float(600, iotype='in', desc='Length of each simulation [s]')


@base
class AerodynInputs(VariableTree):
    WindFile = Str('FF_Wind_.bts', desc = "Name of wind file", iotype = 'in')
    NumFoil = Int(5, iotype='in', desc='Number of airfoil.dat files')

@base
class FASTInputs(VariableTree):
    TMax = Float(630, iotype='in', desc='Total run time [s]')
    VSContrl = Enum(0, (0,1,2,3), desc='Variable-speed control mode {0: none, 1: simple VS, 2: user-defined from routine UserVSCont, 3: user-defined}')
    TimGenOn = Float(0, iotype='in', desc='Time to turn on the generator for startup [s]')
    TPitManS1 = Float(9999.9, iotype='in', desc='Time to start override pitch maneuver for blade 1 and end standard pitch control [s]')
    TPitManS2 = Float(9999.9, iotype='in', desc='Time to start override pitch maneuver for blade 2 and end standard pitch control [s]')
    TPitManS3 = Float(9999.9, iotype='in', desc='Time to start override pitch maneuver for blade 3 and end standard pitch control [s]')
    TPitManE1 = Float(0, iotype='in', desc='Time at which override pitch maneuver for blade 1 reaches final pitch [s]')
    TPitManE2 = Float(0, iotype='in', desc='Time at which override pitch maneuver for blade 2 reaches final pitch [s]')
    TPitManE3 = Float(0, iotype='in', desc='Time at which override pitch maneuver for blade 3 reaches final pitch [s]')
    BlPitchF1 = Float(0, iotype='in', desc='Blade 1 final pitch for pitch maneuvers [degrees]')
    BlPitchF2 = Float(0, iotype='in', desc='Blade 2 final pitch for pitch maneuvers [degrees]')
    BlPitchF3 = Float(0, iotype='in', desc='Blade 3 final pitch for pitch maneuvers [degrees]')
    PtfmModel = Enum(3, (0,1,2,3), desc='Platform model {0: none, 1: onshore, 2: fixed bottom offshore, 3: floating offshore}')
    PtfmFile = Str('something.ptfm"', desc = "Name of file containing platform properties", iotype = 'in')
    TwrFile = Str('tower.dat', desc = "Name of file containing tower properties", iotype = 'in')
    ADFile = Str('something.ad', desc = "Name of file containing AeroDyn input parameters", iotype = 'in')
    TStart = Float(30, iotype='in', desc='Time to begin tabular output [s]')
    BldFile1 = Str('blade.dat', desc = "Name of file containing properties for blade 1", iotype = 'in')
    BldFile2 = Str('blade.dat', desc = "Name of file containing properties for blade 2", iotype = 'in')
    BldFile3 = Str('blade.dat', desc = "Name of file containing properties for blade 3", iotype = 'in')
    PCMode = Enum(0, (0,1,2), desc='Pitch control mode {0: none, 1: user-defined from routine PitchCntrl, 2: user-defined from Simulink}')
    YawNeut = Float(0, iotype='in', desc='Neutral yaw position--yaw spring force is zero at this yaw [degrees]')

    
@base
class PtfmInputs(VariableTree):
    PtfmSurge = Float(0, iotype='in', desc='Initial or fixed horizontal surge translational displacement of platform [m]')
    PtfmSway = Float(0, iotype='in', desc='Initial or fixed horizontal sway translational displacement of platform [m]')
    PtfmHeave = Float(0, iotype='in', desc='Initial or fixed vertical heave translational displacement of platform [m]')
    PtfmRoll = Float(0, iotype='in', desc='Initial or fixed roll tilt rotational displacement of platform [degrees]')
    PtfmPitch = Float(0, iotype='in', desc='Initial or fixed pitch tilt rotational displacement of platform [degrees]')
    PtfmYaw = Float(0, iotype='in', desc='Initial or fixed yaw rotational displacement of platform [degrees]')
    WAMITFile = Str('model', desc = "Root name of WAMIT output files containing the linear, nondimensionalized, hydrostatic restoring matrix", iotype = 'in')
    WaveTMax = Float(3630, iotype='in', desc='Analysis time for incident wave calculations [s]')
    WaveSeed1 = Float(123456, iotype='in', desc='First random seed of incident waves')
    WaveSeed2 = Float(123457, iotype='in', desc='Second random seed of incident waves')
    WaveMod = Enum(2, (0,1,2,3), desc='Incident wave kinematics model {0: none=still water, 1: plane progressive (regular), 2: JONSWAP/Pierson-Moskowitz spectrum (irregular), 3: user-defind spectrum from routine UserWaveSpctrm (irregular)}')
    WaveDT = Float(0.25, iotype='in', desc='Time step for incident wave calculations [s]')
    CurrSSV0 = Float(0, iotype='in', desc='Sub-surface current velocity at still water level [m/s]')
    CurrSSDir = Float(0, iotype='in', desc='Sub-surface current heading direction [degrees]')
    CurrNSRef = Float(0, iotype='in', desc='Near-surface current reference depth [m]')
    CuffNSV0 = Float(0, iotype='in', desc='Near-surface current velocity at still water level [m/s]')

# This class is not currently used but could be useful in the future to automate large job submits
@base
class JobSumitInputs(VariableTree):
        Allocation = Str('XXX', desc = "Name of allocation", iotype = 'in')
        WallTime = Str('2:00:00', iotype='in', desc='Wall time')
        Nodes = Float(1, iotype='in', desc='Nodes per job')
        ppn = Float(1, iotype='in', desc='Processors per node')



