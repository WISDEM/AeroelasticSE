"""
FAST_noise_component.py

Created by NWTC Systems Engineering Sub-Task on 2012-08-01.
Copyright (c) NREL. All rights reserved.
"""
import os
import numpy as np
from openmdao.main.datatypes.api import Array

from FAST_component import FAST_iter_component

class FAST_noise_component(FAST_iter_component):
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


    def __init__(self, geometryaero=None, atmosphere=None, adpath=None, debug=False):

        super(FAST_noise_component,self).__init__( geometryaero, atmosphere, adpath, debug)

#   - - - - -

    def execute(self):
        """ execute the `runFAST` model and look up the SPL """

        print "In {0}.execute() ...".format(self.__class__)

        #self.soundPressureLevels = np.copy(self.rotorSpeedCurve)
        # run the model, copy its output to self
        self.soundPressureLevels = np.zeros((2, len(self.rotorSpeedCurve[0])))
        ws = np.round(self.rotorSpeedCurve[0,0])
        if ws < self.rotorSpeedCurve[0,0]:
        	  ws += 1.0
        counter = 0
        for i in xrange(0,self.rotorSpeedCurve.shape[1]):
            if (self.rotorSpeedCurve[0,i] >= ws):
               self.myModel.set_ws(self.rotorSpeedCurve[0,i])
               self.myModel.set_rpm(self.rotorSpeedCurve[1,i])
               self.myModel.execute()
               self.soundPressureLevels[0,counter]=self.rotorSpeedCurve[0,i]
               self.soundPressureLevels[1,counter]=self.myModel.getSPL()
               ws += 1.0
               counter += 1


if __name__=="__main__":

    from rotor_cst_component import GeometryAero, Atmosphere

    #compdir = os.path.dirname(os.path.realpath(__file__))
    #afpath = os.path.join(compdir,"../inputFiles/airfoils/5MWRef/" )
    #kld - hack of airfoil location
    afpath = 'C:/Models/FAST/airfoils/5MWRef/'

    geometryVT = GeometryAero(afpath=afpath)

    ## now do interpolation, because Andrew's default 5MW is just at 5 widely spaced points on blade.
    geometryVT.chord, geometryVT.theta = geometryVT.interpToAFStations()
    tip = geometryVT.r[-1]
    geometryVT.r = tip * geometryVT.r_af
    ## now done interpolation
    
    atmVT = Atmosphere()
    fast = FAST_noise_component(geometryaero=geometryVT, atmosphere=atmVT, debug=True)

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

    # baseline
    fast.rotorSpeedCurve = [[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, \
                             11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, \
                             18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0], \
                            [7.2, 7.5, 7.9, 8.4, 9.1, 10.1, 11.3, \
                             11.9, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2, \
                             12.2, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2, 12.2]]

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

    print "Sound Pressure Levels: "
    print fast.soundPressureLevels
    spd = fast.soundPressureLevels[0]
    db = fast.soundPressureLevels[1]
    fout = file("soundLevels.dat", "w")
    fout.write("# rotorSpeed   Decibals\n")
    for i in range(0,len(spd)):
        fout.write("%f %f\n" % (spd[i], db[i]))
    fout.close()
    #print "Rated wind speed: {0}".format(fast.ratedWindSpeed)
