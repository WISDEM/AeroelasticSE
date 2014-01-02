"""
FAST_powercurve_component.py

Created by NWTC Systems Engineering Sub-Task on 2012-08-01.
Copyright (c) NREL. All rights reserved.
"""
import os
import numpy as np
from openmdao.main.datatypes.api import Array

from FAST_component import FAST_component

class FAST_powercurve_component(FAST_component):
    """ Just do the powercurve run

    Returns
    -------
    power curves : array_like of float
        array of power levels for wind input conditions [kW vs. m/s]

    """
    # ---- Design Variables ----------
    # inherited from parent

    # ------------- Outputs --------------

    # units.add_unit('dB','decibel') how does this work?
    #ratedWindSpeed = Float(11.506, units = 'm / s', iotype='out', desc='wind speed for rated power')
    maxRotPwr = Array(np.array([[4.0,50.0],[13.0,50.0]]), iotype='out', desc='Maximum rotor powerlevel by wind speed') # units = 'kW',


    def __init__(self, geometryaero=None, atmosphere=None, adpath=None, debug=False):

        super(FAST_powercurve_component,self).__init__( geometryaero, atmosphere, adpath, debug)

#   - - - - -

    def execute(self):
        """ execute the `runFAST` model and look up the power """

        print "In {0}.execute() ...".format(self.__class__)

        #self.soundPressureLevels = np.copy(self.rotorSpeedCurve)
        # run the model, copy its output to self
        self.myModel.execute()
        self.power = self.myModel.getOutputValue("RotPwr")
        self.time = self.myModel.getOutputValue("Time")
        self.ws = self.myModel.getOutputValue("WindVxi")

    def setWindRamp(self,delay, wsmin, wsmax, duration):
        """ set up AeryDyn wind file for a ramped wind.
        write the file, and set it in myModel
        """

        dat = """!UAE Phase VI (Ames) wind for for a simple power curve.
!Time   Wind    Wind    Vert.   Horiz.  Vert.   LinV    Gust
!       Speed   Dir     Speed   Shear   Shear   Shear   Speed
   0.0  5.0     0.0     0.0     0.0     0.0     0.0     0.0
   5.0  5.0     0.0     0.0     0.0     0.0     0.0     0.0
  25.0 25.0     0.0     0.0     0.0     0.0     0.0     0.0
9999.9 25.0     0.0     0.0     0.0     0.0     0.0     0.0
"""
        wind_file = "rampwindfile.dat"
        fout = file(wind_file, "w")
        fout.write(dat)
        fout.close()
        self.myModel.set_wind_file(wind_file)
        self.myModel.set_rpm(0)  ##???
        self.myModel.set_ws(10) ## should be ignored
        self.myModel.fstDict['TMax'] = duration+delay


if __name__=="__main__":

    from rotor_cst_component import GeometryAero, Atmosphere

    compdir = os.path.dirname(os.path.realpath(__file__))
    afpath = os.path.join(compdir,"../inputFiles/airfoils/5MWRef/" )

    geometryVT = GeometryAero(afpath=afpath)

    ## now do interpolation, because Andrew's default 5MW is just at 5 widely spaced points on blade.
    geometryVT.chord, geometryVT.theta = geometryVT.interpToAFStations()
    tip = geometryVT.r[-1]
    geometryVT.r = tip * geometryVT.r_af
    ## now done interpolation
    
    atmVT = Atmosphere()
    fast = FAST_powercurve_component(geometryaero=geometryVT, atmosphere=atmVT, debug=True)

    fast.setWindRamp(5,5,25,20)
    fast.execute()
    
#    spd = fast.maxRotPwr[0]
#    power = fast.maxRotPwr[1]

    fout = file("powerCurve.dat", "w")
    fout.write("# rotorSpeed   RotPwr(max)\n")
    for i in range(0,len(fast.ws)):
        fout.write("%f %f\n" % (fast.ws[i], fast.power[i]))
    fout.close()
    #print "Rated wind speed: {0}".format(fast.ratedWindSpeed)
