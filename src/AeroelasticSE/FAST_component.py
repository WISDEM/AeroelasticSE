"""
FAST_iter_component.py  -- for running FAST more than once, but otherwise as generically as possible

Created by NWTC Systems Engineering Sub-Task on 2012-08-01.
Copyright (c) NREL. All rights reserved.
"""

import os,sys
import numpy as np

# setpath not needed when running under OpenMDAO virtualenv
#sys.path.append('D:/SystemsEngr/openMDAO')
#import setpath # add OpenMDAO packages to Python path

try:
    from openmdao.units import units
except:
    sys.stderr.write("Can't import openmdao - I'll try again using setpath.\n")
    sys.path.append('C:/Models/FAST/') # path to setpath.py # todo- machine dependency
    import setpath # add OpenMDAO packages to Python path
    from openmdao.units import units

from openmdao.main.api import Component, Assembly, set_as_top, VariableTree
from openmdao.main.datatypes.api import Int, Bool, Float, Array, VarTree, Slot
from openmdao.units import units

#sys.path.append('D:/SystemsEngr/wese-scratch/kldtest/twstr/assemblies')
#sys.path.append('D:/SystemsEngr/wese-scratch/kldtest/twstr/models/cst')
#from aero_cst_assembly import GeometryAero, Atmosphere

#sys.path.append('D:/SystemsEngr/Noise') # geometry needs airfoil.py (new version)
from rotor_cst_component import GeometryAero, Atmosphere

from runFAST import runFAST

class FAST_component(Component):
    """ An OpenMDAO Component for running NREL's FAST code

    Attributes
    ----------
    geometry   : slot
        GeometryAero dictionary
    atm        : slot
        Atmosphere dictionary
    rotorSpeedCurve  : array_like of float
        array of rotor speed for different wind input conditions [rpm vs. m/s]
    ratedPower : float
        rated machine power in kW
    towerHt    : float
        tower height in m
    Returns
    -------
    via call to self.myModel, the underlying runFAST object. in particular, to its getOutputValue() fn.
    """
    # ---- Design Variables ----------

    #drivetrain = Slot(DrivetrainEfficiencyModel, iotype = 'in', desc= "drivetrain efficiency model", required=True)

    geometryaero = Slot(GeometryAero, iotype = 'in')
    atmosphere   = Slot(Atmosphere,   iotype = 'in')

    ratedPower = Float(5000.0, units = 'kW', iotype='in', desc= 'rated machine power in kW')
    towerHt    = Float(50.0, units = 'm', iotype='in', desc= 'tower height in m')

    def __init__(self, geometryaero=None, atmosphere=None, adpath=None, debug=False):

        super(FAST_component,self).__init__()

        if adpath is None:
            adpath = 'C:/Models/FAST/airfoils/5MWRef/' # todo: machine dependency

        if geometryaero is None:
            self.add('geometryaero', GeometryAero(adpath))
        else:
            self.add('geometryaero', geometryaero)

        if atmosphere is None:
            self.add('atmosphere', Atmosphere())
        else:
            self.add('atmosphere', atmosphere)

        #initialize model

        self.fast_vt_to_dict()
        self.myModel = runFAST(self.geometry, self.atm)

        # list variables

        if debug:
            print self.myModel

            print "Contents of self.geometry {:}".format(self.geometry.__class__)
            for var in self.geometry:
                print '  ', var,
                print '    ', self.geometry[var].__class__,
                print '    ', self.geometry[var]
            print


    def execute(self):
        """ execute the `runFAST` model and look up the SPL """

        print "In {0}.execute() ...".format(self.__class__)
        print "by default the base FAST component will just run but not collect anything!"

        ## assumes everything is ready to go, just run it!
        self.myModel.execute()
        

#   - - - - -
    def find_hubR(self):
        """ (PG 7-19-13) find hubR given (midpoint) stations r and rotor diameter.
            walks backward down blade"""
        geom = self.geometryaero
        x = geom.r
        R = geom.initRotorDiam
        N = len(x)
        allR = [0]*(N+1)
        allR[N] = R
        for i in range(N,0,-1):
            dxi = 2 * (allR[i] - x[i-1])
            allR[i-1]=allR[i] - dxi
        h = allR[0]
        return h

    def fast_vt_to_dict(self):
        """ Create dictionary versions of geom and atm variable trees """

        self.geometry = {}  # empty dict

        self.geometry['chord']  = self.geometryaero.chord
        self.geometry['yaw']    = self.geometryaero.yaw
        self.geometry['r_af']   = self.geometryaero.r_af
        self.geometry['r']      = self.geometryaero.r
        self.geometry['tilt']   = self.geometryaero.tilt
        self.geometry['theta']  = self.geometryaero.theta
        self.geometry['nBlade'] = self.geometryaero.nBlade
        self.geometry['preCone'] = self.geometryaero.precone
        self.geometry['polars']  = self.geometryaero.afarr
        
        ## needed for endpoints = False case  (PG 7-19-13), which appears to be the case for ref5MW_aero in rotor_cst_component.py 
        self.geometry['endPoints'] = False  ## (PG 7-19-13) default 5MW rotor specified at cell midpoints, it appears (no station at end of 63M blade).
        self.geometry['rotorR'] = self.geometryaero.initRotorDiam
        self.geometry['hubR'] = self.find_hubR()
        self.geometry['polars'] = self.geometryaero.afarr
        ##

        self.atm = {}  # empty dict
        anames = self.atmosphere.list_vars()
        for an in anames:
            self.atm[an] = eval('self.atmosphere.' + an)

    
class FAST_iter_component(FAST_component):
    """ An OpenMDAO Component for running NREL's FAST code
    This component knows how to run FAST multiple times with different wind speeds and rotor rpm's


    """
    # ------------ Inputs ----------------

    # the array of wind and rotor speeds
    rotorSpeedCurve = Array(np.array([[4.0,7.0],[13.0,12.5]]), iotype='in', desc= 'rpm by wind speed [rpm vs. m/s]')

    # ------------- Outputs --------------

    # units.add_unit('dB','decibel') how does this work?
    #ratedWindSpeed = Float(11.506, units = 'm / s', iotype='out', desc='wind speed for rated power')
####    soundPressureLevels = Array(np.array([[4.0,50.0],[13.0,50.0]]), iotype='out', desc='Maximum sound pressure level by wind speed') # units = 'dB',


    def __init__(self, geometryaero=None, atmosphere=None, adpath=None, debug=False):

        super(FAST_iter_component,self).__init__(geometryaero,atmosphere,adpath, debug)
#   - - - - -

    def execute(self):
        """ execute the `runFAST` model and look up the SPL """

        print "In {0}.execute() ...".format(self.__class__)
        print "by default the base FAST component will just run but not collect anything!"

        #self.soundPressureLevels = np.copy(self.rotorSpeedCurve)
        # run the model, copy its output to self
        ws = np.round(self.rotorSpeedCurve[0,0])
        if ws < self.rotorSpeedCurve[0,0]:
        	  ws += 1.0
        counter = 0
        for i in xrange(0,self.rotorSpeedCurve.shape[1]):
            if (self.rotorSpeedCurve[0,i] >= ws):
               self.myModel.set_ws(self.rotorSpeedCurve[0,i])
               self.myModel.set_rpm(self.rotorSpeedCurve[1,i])
               self.myModel.execute()
               ws += 1.0
               counter += 1


if __name__=="__main__":

    #import mkgeom
    #geometry, atm = mkgeom.makeGeometry() # geometry, atm : dictionaries

    #afpath = 'D:/SystemsEngr/Noise/AeroData/' # path to airfoil files
    #afpath = "C:/Python27/openmdao-0.7.0/twister/inputFiles/airfoils/5MWRef/" # todo: machine dependency
#    afpath = "z:\Users/pgraf/work/wese/wese-7_16_13/twister/inputFiles/airfoils/5MWRef/" # todo: machine dependency
    compdir = os.path.dirname(os.path.realpath(__file__))
    afpath = os.path.join(compdir,"../inputFiles/airfoils/5MWRef/" )

    #import twister.models.FAST.mkgeom as mkgeom
    #geometry, atm = mkgeom.makeGeometry()
    #geometryVT = mkgeom.toVT(geometry, afpath)

    geometryVT = GeometryAero(afpath=afpath)

    ## now do interpolation, because Andrew's default 5MW is just at 5 widely spaced points on blade.
    geometryVT.chord, geometryVT.theta = geometryVT.interpToAFStations()
    tip = geometryVT.r[-1]
    geometryVT.r = tip * geometryVT.r_af
    ## now done interpolation
    
    # test 1
    atmVT = Atmosphere()
    fast = FAST_component(geometryaero=geometryVT, atmosphere=atmVT, debug=True)
    fast.execute()

    #drivetrain = csmDriveEfficiency(1)
    #fast.drivetrain = drivetrain

    # Override the default values in runFAST.py here

    # fast.myModel.noise_file = '*.ipt'
    # fast.myModel.blade_file = '*.dat'
    # fast.myModel.ad_file    = '*.ad'
    # fast.myModel.fast_file  = '*.fst'
    # fast.myModel.fastpath = ''
    # fast.myModel.fastexe = '*.exe'
    # fast.myModel.template_path = ' '
    # fast.myModel.model_path = ' '
    
    # test 2
    fast = FAST_iter_component(geometryaero=geometryVT, atmosphere=atmVT, debug=True)
    fast.rotorSpeedCurve = [[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, \
                           11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0], \
                          [7.0, 8.0,  9.0, 10.0, 11.0, 12.0, 12.5, \
                          12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, \
                          12.5, 12.5, 12.5, 12.5, 12.5]]
    fast.execute()

#    print "Sound Pressure Levels: "
#    print fast.soundPressureLevels
#    spd = fast.soundPressureLevels[0]
#    db = fast.soundPressureLevels[1]
#    fout = file("soundLevels.dat", "w")
#    fout.write("# rotorSpeed   Decibals\n")
#    for i in range(0,len(spd)):
#        fout.write("%f %f\n" % (spd[i], db[i]))
#    fout.close()
    #print "Rated wind speed: {0}".format(fast.ratedWindSpeed)
