"""
FAST_noise_component.py

Created by NWTC Systems Engineering Sub-Task on 2012-08-01.
Copyright (c) NREL. All rights reserved.
"""
import os
import numpy as np
from openmdao.main.datatypes.api import Array

from FAST_component import MyFAST_iter_component, MyFAST_component

class FAST_noise_component(MyFAST_iter_component):
    """ Just do the noise run

    Returns
    -------
    soundPressureLevels : array_like of float
        array of sound pressure levels for wind input conditions [dB vs. m/s]

    """
    # ---- Design Variables ----------
    # inherited from parent

    # ------------- Outputs --------------

    # units.add_unit('dB','decibel') how does this work?
    #ratedWindSpeed = Float(11.506, units = 'm / s', iotype='out', desc='wind speed for rated power')
    soundPressureLevels = Array(np.array([[4.0,50.0],[13.0,50.0]]), iotype='out', desc='Maximum sound pressure level by wind speed') # units = 'dB',


    def __init__(self,fst_exe, fst_dir, fst_file, run_dir):

        super(FAST_noise_component,self).__init__(fst_exe, fst_dir, fst_file, run_dir)

#   - - - - -

    def execute(self):
        """ execute the `runFAST` model and look up the SPL """
        # run the model, copy its output to self
        # run the model
        nspeeds = len(self.rotorSpeedCurve[0])
        self.soundPressureLevels = np.zeros(nspeeds)
        for i in range(nspeeds):
            self.Vhub = self.rotorSpeedCurve[0,i]
            self.RotSpeed = self.rotorSpeedCurve[1,i]

            fstDict = {}
            fstDict['Vhub'] = self.Vhub
            fstDict['RotSpeed'] = self.RotSpeed
            fstDict['TMax'] = self.TMax
            fstDict['TStart'] = self.TStart
            self.myfast.fstDict = fstDict
            self.myfast.execute()
#            MyFAST_component.execute(self)
            self.soundPressureLevels[i] = self.myfast.getSPL()

if __name__=="__main__":
    fst_exe = "/Users/pgraf/opt/windcode-7.31.13/build/FAST_regular_glin64"
    #    fast.fst_dir = "/Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/FAST_VT/OC3_Files/"  ## either abs or rel path ok.
    fst_dir = "ModelFiles/Noise_Files/"
    fst_file = "NREL5MW_Monopile_Rigid.v7.02.fst"  ## should _not_ be full path

    run_dir = "new_run_dir"  ## either abs or rel path ok
#   run_dir = "/Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/another_run_dir"

    fast = FAST_noise_component(fst_exe, fst_dir, fst_file, run_dir)
    fast.TMax = 4
    fast.TStart = 0

    # test code
    fast.rotorSpeedCurve = [[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0],\
                            [7.2, 7.5, 7.9, 8.4, 9.1, 10.1, 11.3, 11.9]]


    # baseline
    '''fast.rotorSpeedCurve = [[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, \
                             11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, \
                             18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0], \
                            [7.2, 7.5, 7.9, 8.4, 9.1, 10.1, 11.3, \
                             11.9, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2, \
                             12.2, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2]]'''

    # 80 opt
    #fast.rotorSpeedCurve = [[25.0], [12.2]]
    '''fast.rotorSpeedCurve = [[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, \
                             11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, \
                             18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0], \
                            [7.2, 7.5, 7.9, 8.4, 9.0, 9.9, 11.1, \
                             11.9, 12.3, 12.2, 12.2, 12.2, 12.2, 12.2, \
                             12.2, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2]]'''

    # 100 opt
    #fast.rotorSpeedCurve = [[25.0], [15.2]]
    '''fast.rotorSpeedCurve = [[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, \
                             11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, \
                             18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0], \
                            [8.8, 9.1, 9.6, 10.1, 10.8, 11.5, 12.8, \
                             14.2, 15.2, 15.2, 15.2, 15.2, 15.2, 15.2, \
                             15.2, 15.2, 15.2, 15.2, 15.2, 15.2, 15.2, 15.2, 15.2]]'''

    # 100 flex
    #fast.rotorSpeedCurve = [[25.0], [15.2]]
    '''fast.rotorSpeedCurve = [[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, \
                             11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, \
                             18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0], \
                            [9.0, 9.2, 9.6, 10.1, 10.8, 11.5, 12.8, \
                             14.2, 15.2, 15.2, 15.2, 15.2, 15.2, 15.2, \
                             15.2, 15.2, 15.2, 15.2, 15.2, 15.2, 15.2, 15.2, 15.2]]'''

    fast.execute()

    print "Sound Pressure Levels:"
    print "Vhub   RotSpeed    Decibals"
    for i in range(len(fast.soundPressureLevels)):
        print fast.rotorSpeedCurve[0][i],  fast.rotorSpeedCurve[1][i],  fast.soundPressureLevels[i]

