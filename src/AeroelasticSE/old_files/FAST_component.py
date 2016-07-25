"""
FAST_componentpy -- simple openMDAO wrapper for template-file based interface to FAST,
as implemented in runFAST.py

The component defined here has no inputs and outputs but only manages the calls to the runFAST object.
We include to demonstration/helper classes.

1) MyFAST_component--implements an openMDAO component for computing RotPwr(Vhub, RotSpeed) (ie rotor speed
as a function of wind speed and rotor speed) once..
1) MyFAST_iter_component--implements an openMDAO component for computing simple power curves.
 
In this interface to FAST, the basic turbine structure is delivered to FAST via a working set of 
FAST input "template" files.  These are stored internally as python dictionaries.  The openMDAO
Component then selectively (according to its inputs) modifies this dictionary, and selectively
(according to its outputs) queries the results of the run.

Copyright (c) NREL. All rights reserved.
"""

import os,sys
import numpy as np

from openmdao.units import units
from openmdao.main.api import Component, Assembly, set_as_top, VariableTree
from openmdao.main.datatypes.api import Int, Bool, Float, Array, VarTree, Slot
from openmdao.units import units

from runFAST import runFAST

class FAST_component(Component):
    """ An OpenMDAO Component for running NREL's FAST code

    This class is a thin wrapper of runFAST.
    It is a base class for running FAST within openMDAO.  User is expected to subclass this class to enable
    openMDAO-style connectivity to FAST variables of interest.  See MyFAST_component and example(), below.

    Return value is via call to self.myModel, the underlying runFAST object. in particular, to its getOutputValue() fn.
    """

    def __init__(self,fst_exe, fst_dir, fst_file, run_dir):
        super(FAST_component,self).__init__()
        self.myfast = runFAST()
        self.myfast.fst_exe = fst_exe
        self.myfast.fst_dir = fst_dir
        self.myfast.fst_file = fst_file
        self.myfast.run_dir = run_dir
        

    def execute(self):
        """ execute the `runFAST` model 
         assumes everything is ready to go, just run it! """
        self.myfast.execute()
        
    
class MyFAST_component(FAST_component):
    """ An openMDAO component implementing an interface to compute rotor power as a function
    of wind speed and rotorspeed"""
    TMax = Float(30.0, iotype='in', desc= 'length of analysis') 
    TStart = Float(0.0, iotype='in', desc= 'start of analysis') 
    Vhub = Float(10.0, iotype='in', desc= 'hub height wind speed in mps')
    RotSpeed = Float(15.0, iotype='in', desc= 'rotor speed')
    RotPwr    = Float(0, iotype='out', desc= 'generato power in Watts')

    def __init__(self,fst_exe, fst_dir, fst_file, run_dir):
        super(MyFAST_component,self).__init__(fst_exe, fst_dir, fst_file, run_dir)
        
    def execute(self):
        fstDict = {}
        fstDict['Vhub'] = self.Vhub
        fstDict['RotSpeed'] = self.RotSpeed
        fstDict['TMax'] = self.TMax
        fstDict['TStart'] = self.TStart
        self.myfast.setOutputs(['RotPwr'])
        self.myfast.fstDict = fstDict
        self.myfast.execute()
        self.RotPwr = max(self.myfast.getOutputValue("RotPwr"))

class MyFAST_iter_component(MyFAST_component):
    """ An OpenMDAO Component for running NREL's FAST code.
    This component knows how to run FAST multiple times with different wind speeds and rotor rpm's.
    """
    # ------------ Inputs ----------------
    # the array of wind and rotor speeds
    rotorSpeedCurve = Array(np.array([[4.0,7.0],[13.0,12.5]]), iotype='in', desc= 'rpm by wind speed [rpm vs. m/s]')
    
    # ------------- Outputs --------------
    rotorPowerCurve = Array(iotype='out', desc= 'power by wind speed [watts vs. m/s]')

    def __init__(self,fst_exe, fst_dir, fst_file, run_dir):
        super(MyFAST_iter_component,self).__init__(fst_exe, fst_dir, fst_file, run_dir)

#   - - - - -

    def execute(self):
        """ execute the `runFAST` model and look up the power """
        # run the model
        nspeeds = len(self.rotorSpeedCurve[0])
        self.rotorPowerCurve = np.zeros(nspeeds)
        for i in range(nspeeds):
            self.Vhub = self.rotorSpeedCurve[0,i]
            self.RotSpeed = self.rotorSpeedCurve[1,i]
            super(MyFAST_iter_component,self).execute()
            self.rotorPowerCurve[i] = self.RotPwr


def FAST_component_test():
    """ A simple example of running FAST one time
    This component could now be used in an openMDAO Assembly that took 
    wind and rotor speed as input, delivered power production at that wind/rotor speed as output."""
    fst_exe = "/Users/pgraf/opt/windcode-7.31.13/build/FAST_glin64"
    #    fast.fst_dir = "/Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/FAST_VT/OC3_Files/"  ## either abs or rel path ok.
    fst_dir = "ModelFiles/OC3_Files/"
    fst_file = "NRELOffshrBsline5MW_Monopile_RF.fst"  ## should _not_ be full path

    run_dir = "new_run_dir"  ## either abs or rel path ok
#   run_dir = "/Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/another_run_dir"

    myfast = MyFAST_component(fst_exe, fst_dir, fst_file, run_dir)
    myfast.Vhub = 8
    myfast.RotSpeed = 12.03
    myfast.TMax = 2
    myfast.TStart = 0
    myfast.execute()

    print "Vhub   RotPwr"
    print myfast.Vhub, myfast.RotPwr

# end FAST_component_test():


def FAST_iter_component_test():
    """ This example uses the MyFAST_iter_component to create a simple power curve.
    This component could now be used in an openMDAO Assembly that dealt with
    wind/rotor-speed curves as input, and power-curves as output."""

    fst_exe = "/Users/pgraf/opt/windcode-7.31.13/build/FAST_glin64"
    #    fast.fst_dir = "/Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/FAST_VT/OC3_Files/"  ## either abs or rel path ok.
    fst_dir = "ModelFiles/OC3_Files/"
    fst_file = "NRELOffshrBsline5MW_Monopile_RF.fst"  ## should _not_ be full path

    run_dir = "new_run_dir"  ## either abs or rel path ok
#   run_dir = "/Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/another_run_dir"

    myfast = MyFAST_iter_component(fst_exe, fst_dir, fst_file, run_dir)
    myfast.TMax = 2
    myfast.TStart = 0
    myfast.rotorSpeedCurve = [[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0],
                              [7.0, 8.0,  9.0, 10.0, 11.0, 12.0, 12.5, 12.5]]

    myfast.execute()

    print "Vhub   RotSpeed    RotPwr"
    for i in range(len(myfast.rotorPowerCurve)):
        print myfast.rotorSpeedCurve[0][i],  myfast.rotorSpeedCurve[1][i],  myfast.rotorPowerCurve[i]

#end FAST_iter_component_test():

if __name__=="__main__":
    # test 1
    print "TEST1-run once"
    FAST_component_test()
    
    # test 2
    print "TEST2-simple power curve"
    FAST_iter_component_test()

