"""
components.py

Created by Andrew Ning on 2012-06-25.
Copyright (c)  NREL. All rights reserved.
"""

import sys

import numpy as np
from math import pi

from openmdao.main.api import Component, Assembly, VariableTree
from openmdao.main.datatypes.api import Int, Float, Array, List, Dict, Bool, Enum, Slot, VarTree
from airfoil import PolarByRe, Profile
from common import D2R, R2D, RPM2RS, TurbineVector, setup_akima
akima_interpolate = setup_akima()

# ---------- defaults from 5MW ref model -------------

def ref5MW_aero(afpath):
    """airfoil data for NREL reference 5MW turbine"""

    r_af = np.array([2.8667, 5.6000, 8.3333, 11.7500, 15.8500, 19.9500, 24.0500, 28.1500, 32.2500, 36.3500, 40.4500, 44.5500, 48.6500, 52.7500, 56.1667, 58.9000, 61.6333])
    r_af /= 63.0

    af_idx = [1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8, 8, 8, 8, 8, 8]
    #af_idx = [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 12, 12, 12]
    #af_idx = [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 9, 10, 11, 11, 11, 11, 11]

    airfoil_polars = [0]*8
    airfoil_polars[0] = PolarByRe.initFromAerodynFile(afpath + 'Cylinder1.dat')
    airfoil_polars[1] = PolarByRe.initFromAerodynFile(afpath + 'Cylinder2.dat')
    airfoil_polars[2] = PolarByRe.initFromAerodynFile(afpath + 'DU40_A17.dat')
    airfoil_polars[3] = PolarByRe.initFromAerodynFile(afpath + 'DU35_A17.dat')
    airfoil_polars[4] = PolarByRe.initFromAerodynFile(afpath + 'DU30_A17.dat')
    airfoil_polars[5] = PolarByRe.initFromAerodynFile(afpath + 'DU25_A17.dat')
    airfoil_polars[6] = PolarByRe.initFromAerodynFile(afpath + 'DU21_A17.dat')
    airfoil_polars[7] = PolarByRe.initFromAerodynFile(afpath + 'NACA64_A17.dat')

    '''airfoil_polars = [0]*13
    airfoil_polars[0] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0990.dat")
    airfoil_polars[1] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0880.dat") 
    airfoil_polars[2] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0670.dat") 
    airfoil_polars[3] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0440.dat") 
    airfoil_polars[4] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0340.dat") 
    airfoil_polars[5] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0320.dat") 
    airfoil_polars[6] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0290.dat") 
    airfoil_polars[7] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0250.dat")  
    airfoil_polars[8] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0220.dat") 
    airfoil_polars[9] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0210.dat") 
    airfoil_polars[10] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0200.dat") 
    airfoil_polars[11] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0180.dat")'''

    '''airfoil_polars = [0]*12
    airfoil_polars[0] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0990.dat")
    airfoil_polars[1] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0900.dat") 
    airfoil_polars[2] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0720.dat") 
    airfoil_polars[3] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0510.dat") 
    airfoil_polars[4] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0360.dat") 
    airfoil_polars[5] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0330.dat") 
    airfoil_polars[6] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0300.dat") 
    airfoil_polars[7] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0250.dat")  
    airfoil_polars[8] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0210.dat") 
    airfoil_polars[9] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0190.dat") 
    airfoil_polars[10] = PolarByRe.initFromAerodynFile(afpath + "DU-NACA_0180.dat")'''

    polars = [0]*len(af_idx)

    for i in range(len(af_idx)):
        polars[i] = airfoil_polars[af_idx[i] - 1]


    return r_af, polars


def ref5MW_struc():
    #kld 10/22 undoing the move on import
    #from twister.models.CST.turbine.rotor.rotorstruc import CompositeSection, Orthotropic2DMaterial
    r = np.array([1.5, 1.80135, 1.89975, 1.99815, 2.1027, 2.2011, 2.2995, 2.87145, 3.0006,
        3.099, 5.60205, 6.9981, 8.33265, 10.49745, 11.75205, 13.49865, 15.84795, 18.4986, 19.95,
        21.99795, 24.05205, 26.1, 28.14795, 32.25, 33.49845, 36.35205, 38.4984, 40.44795, 42.50205,
        43.49835, 44.55, 46.49955, 48.65205, 52.74795, 56.16735, 58.89795, 61.62855, 63.0])

    n = 38
    compSec = [0]*n
    profile = [0]*n

    nweb_str = [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0]

    materials = Orthotropic2DMaterial.initFromPrecompFile('C:/Python27/openmdao-0.7.0/twister/inputFiles/5MW_PrecompFiles/materials.inp')

    for i in range(n):

        # hack for now
        if nweb_str[i] == 3:
            webLoc = [0.3, 0.6]
        elif nweb_str[i] == 2:
            webLoc = [0.3, 0.6]
        else:
            webLoc = []

        compSec[i] = CompositeSection.initFromPrecompLayupFile('C:/Python27/openmdao-0.7.0/twister/inputFiles/5MW_PrecompFiles/layup_' + str(i+1) + '.inp', webLoc, materials)
        profile[i] = Profile.initFromPrecompFile('C:/Python27/openmdao-0.7.0/twister/inputFiles/5MW_PrecompFiles/shape_' + str(i+1) + '.inp')

    profile = profile
    compSec = compSec

    return r, profile, compSec, materials


class GeometryAero(VariableTree):
    """geometry for rotor"""

    # blade geometry
    r = Array(np.array([1.5, 20.0, 40.0, 63.0]), iotype='in', dtype=np.float, units='m') # kld - 10/5/2012, set as formal openmdao variables to make connections in rotor assembly
    chord = Array(np.array([3.5, 4.5, 3.5, 1.4]), iotype='in', dtype=np.float, units='m')
    theta = Array(np.array([13.3, 9.0, 4.1, 0.1]), iotype='in', dtype=np.float, units='deg')
    #chord = Array(np.array([3.4, 4.1, 2.8, 1.3]), iotype='in', dtype=np.float, units='m')
    #theta = Array(np.array([11.0, 8.8, 3.9, 0.3]), iotype='in', dtype=np.float, units='deg')
    #chord = Array(np.array([3.4, 4.2, 2.9, 1.1]), iotype='in', dtype=np.float, units='m')
    #theta = Array(np.array([11.1, 9.7, 4.2, 0.15]), iotype='in', dtype=np.float, units='deg')
    nBlade = Int(3, iotype='in', desc='number of blades')

    # airfoil data
    r_af = Array(iotype='in', dtype=np.float, desc='radial stations', units='m')
    afarr = List(iotype='in', trait=Slot(PolarByRe), desc='array of lift and drag polar objects') 

    # orientation (currently ignored by CCBlade)
    precone = Float(2.5, iotype='in', desc='precone angle, positive downwind', units='deg')
    tilt = Float(5.0, iotype='in', desc='shaft tilt', units='deg')
    yaw = Float(0.0, iotype='in', desc='yaw error', units='deg')

    def __init__(self, afpath="C:/Python27/openmdao-0.7.0/twister/inputFiles/airfoils/5MWRef/"):  # kld - changed for fast noise; #todo - machine dependency
        """
        OpenMDAO variable tree container for aerodynamic geometry inputs.
        
        Parameters
        ----------
        r : array_like of float
          radial stations of blade [m]
        chord : array_like of float
          chord values at corresponding radial stations [m]
        theta : array_like of float
          twist values at corresponding radial stations [deg]
        nBlade : int
          number of blades
        r_af : array_like of float
          radial stations of airfoil data [m]
        afarr : list
          array of lift and drag polar objects
        precone : float
          precone angle, positive downwind [deg]
        tilt : float
          shaft tilt [deg]
        yaw : float
          yaw error [deg]
        """
        
        super(GeometryAero, self).__init__()

        r_aero, af = ref5MW_aero(afpath)  # defaults to 5MW model
        self.r_af = r_aero
        self.afarr = af
        self.initRotorDiam = self.r[-1]
        self.initR0 = self.r[0]
        self.initR1 = self.r[1]
        self.initR2 = self.r[2]


    def interpToAFStations(self):
        """
        Interpretolates the chord and twist data to the radial airfoil stations using akima interpolate.
        
        Returns
        -------
        chord_af : array_like of float
          chord at airfoil data radial stations [m]
        theta_af : array_like of float
          twist at airfoil data radial stations [deg]
        """

        # adjust airfoil stations based on adjusted rotor size - kld 12/17/2012
        r_af = np.copy(self.r_af)
        r_af *= self.r[-1]
        #self.r_af = r_af
        self.r[0] = self.initR0*self.r[-1]/self.initRotorDiam
        self.r[1] = self.initR1*self.r[-1]/self.initRotorDiam
        self.r[2] = self.initR2*self.r[-1]/self.initRotorDiam
        
        chord_af = akima_interpolate(self.r, self.chord, r_af)
        for i in range(len(chord_af)):
             if chord_af[i] < 0:
                  chord_af[i] = 0.1
        theta_af = akima_interpolate(self.r, self.theta, r_af)
        for i in range(len(theta_af)):
            if theta_af[i] < 0:
                 theta_af[i] = 0.001

        return chord_af, theta_af



class Atmosphere(VariableTree):

    rho = Float(1.225, iotype='in', desc='density of air', units='kg/m**3')
    mu = Float(1.789e-5, iotype='in', desc='dynamic viscosity of air', units='kg/m/s')

    # ignored by CCBlade
    shearExp = Float(0.143, iotype='in', desc='shear exponent')

    def __init__(self):
        """
        OpenMDAO Variable Tree container for atmospheric data.
        
        Parameters
        ----------
        rho : float
          density of air [kg/m**3]
        mu : float
          dynamic viscosity of air [kg/m/s]
        shearExp : float
          shear exponent
    
        """

        super(Atmosphere, self).__init__()