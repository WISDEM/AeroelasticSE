# ref5MWaero.py
# 2012 11 12
# extracted from aero_cst_assembly.py

import sys
sys.path.append('D:/SystemsEngr/Noise') # needs airfoil.py (new version)
from airfoil import PolarByRe, Profile

# setpath not needed when running under OpenMDAO virtualenv
#sys.path.append('D:/SystemsEngr/openMDAO')
#import setpath # add OpenMDAO packages to Python path

try:
    from openmdao.units import units
except:
    #sys.stderr.write("Can't import openmdao - I'll try again using setpath.\n")
    sys.path.append('D:/SystemsEngr/openMDAO') # path to setpath.py
    import setpath # add OpenMDAO packages to Python path
    from openmdao.units import units

from openmdao.main.api import Component, Assembly, set_as_top, VariableTree, Slot
from openmdao.main.datatypes.api import Int, Bool, Float, Array, List

import numpy as np

# ---------- defaults from 5MW ref model -------------

def ref5MW_aero(afpath):
    """airfoil data for NREL reference 5MW turbine"""

    r_af = np.array([ 2.8667,  5.6000,  8.3333, 11.7500, 15.8500, 19.9500, 24.0500, 
                     28.1500, 32.2500, 36.3500, 40.4500, 44.5500, 48.6500, 52.7500, 
                     56.1667, 58.9000, 61.6333])

    af_idx = [1, 1, 2, 3, 4, 4, 5, 
              6, 6, 7, 7, 8, 8, 8, 
              8, 8, 8]

    airfoil_polars = [0]*8
    airfoil_polars[0] = PolarByRe.initFromOldAerodynFile(afpath + 'Cylinder1.dat')
    airfoil_polars[1] = PolarByRe.initFromOldAerodynFile(afpath + 'Cylinder2.dat')
    airfoil_polars[2] = PolarByRe.initFromOldAerodynFile(afpath + 'DU40_A17.dat')
    airfoil_polars[3] = PolarByRe.initFromOldAerodynFile(afpath + 'DU35_A17.dat')
    airfoil_polars[4] = PolarByRe.initFromOldAerodynFile(afpath + 'DU30_A17.dat')
    airfoil_polars[5] = PolarByRe.initFromOldAerodynFile(afpath + 'DU25_A17.dat')
    airfoil_polars[6] = PolarByRe.initFromOldAerodynFile(afpath + 'DU21_A17.dat')
    airfoil_polars[7] = PolarByRe.initFromOldAerodynFile(afpath + 'NACA64_A17.dat')

    polars = [0]*len(af_idx)

    for i in range(len(af_idx)):
        polars[i] = airfoil_polars[af_idx[i] - 1]


    return r_af, polars

#-----------------------------------------------------------------

class GeometryAero(VariableTree):
    """geometry for NREL 5MW rotor"""

    # blade geometry
    r = Array(np.array([1.5, 20.0, 40.0, 63.0]), iotype='in', dtype=np.float, units='m',
        desc='should go from hub to tip (i.e. r[0] = Rhub)')
    chord = Array(np.array([3.5, 4.5, 3.5, 1.4]), iotype='in', dtype=np.float, units='m')
    theta = Array(np.array([13.3, 9.0, 4.1, 0.1]), iotype='in', dtype=np.float, units='deg')
    
    nBlade = Int(3, iotype='in', desc='number of blades')

    # airfoil data
    r_af = Array(iotype='in', dtype=np.float, desc='radial stations', units='m')
    afarr = List(iotype='in', trait=Slot(PolarByRe), desc='array of lift and drag polar objects')

    # orientation (currently ignored by CCBlade)
    precone = Float(2.5, iotype='in', desc='precone angle, positive downwind', units='deg')
    tilt = Float(5.0, iotype='in', desc='shaft tilt', units='deg')
    yaw = Float(0.0, iotype='in', desc='yaw error', units='deg')

    def __init__(self, afpath):
        super(GeometryAero, self).__init__()

        r_aero, af = ref5MW_aero(afpath)  # defaults to 5MW model
        self.r_af = r_aero
        self.afarr = af

    def interpToAFStations(self):
        chord_af = akima_interpolate(self.r, self.chord, self.r_af)
        theta_af = akima_interpolate(self.r, self.theta, self.r_af)

        return chord_af, theta_af

#-----------------------------------------------------------------

class Atmosphere(VariableTree):
    """ atmosphere for NREL 5MW turbine """

    rho = Float(1.225, iotype='in', desc='density of air', units='kg/m**3')
    mu = Float(1.789e-5, iotype='in', desc='dynamic viscosity of air', units='kg/m/s')

    # ignored by CCBlade
    hubHt = Float(97.6, iotype='in', desc='hub height', units='m')
    shearExp = Float(0.2, iotype='in', desc='shear exponent')

#-----------------------------------------------------------------

def main():
    atmVT = Atmosphere()
    geomVT = GeometryAero('D:/SystemsEngr/Noise/AeroData/')
    
    print 'ATM'
    for var in atmVT.list_vars():
        print '  {:} = {:}'.format(var,eval('atmVT.'+var))
    print
        
    print 'GEOM'
    for var in geomVT.list_vars():
        print '  {:} = {:}'.format(var,eval('geomVT.'+var))
    print 
    
    #print 'rho {:}'.format(atmVT.rho)
    
if __name__=="__main__":

    main() 
