#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by Andrew Ning on 2/21/2012.
Copyright (c)  NREL. All rights reserved.
"""

import platform
import os
import importlib

from math import pi
import numpy as np

# ------- constants -----------
# convert between degrees and radians
D2R = pi/180.0
R2D = 180.0/pi

# convert between rotations/minute and radians/second
RPM2RS = pi/30.0
RS2RPM = 30.0/pi
# ---------------------------------


# ------- setup location of bin ----------
CST_BIN = 'C:/Python27/aeroelasticSE/AeroelasticSE/src/AeroelasticSE/bin'
isWindows = True
DIR_NAME = 'nt'

'''if platform.system() == 'Windows':
    CST_BIN = os.path.join(CST_BIN, 'nt')  # kld - 09/09/2012 (directory label changed from 'win')
    DIR_NAME = 'nt'
    isWindows = True
elif platform.system() == 'Darwin':
    CST_BIN = os.path.join(CST_BIN, 'osx')
    DIR_NAME = 'osx'
elif platform.system() == 'Linux':
    CST_BIN = os.path.join(CST_BIN, 'linux')
    DIR_NAME = 'linux'
# ---------------------------------------'''


# ------- import pBEAM module ---------
def setup_pBEAM():
    """ usage: _pBEAM = setup_pBEAM() """

    return importlib.import_module('twister.models.CST.turbine.bin.' + DIR_NAME + '._pBEAM') # TODO: machine dependency issues

    # for item in imp.get_suffixes():
    #     if item[2] == imp.C_EXTENSION and item[0][0] == '.':
    #         suffix = item[0]

    # return imp.load_dynamic('_pBEAM', os.path.join(CST_BIN, '_pBEAM' + suffix))

# -------------------------------------


# ------- import akima module ---------
def setup_akima():
    """ usage: akima_interpolate = setup_akima() """

    _temp = importlib.import_module('bin.' + DIR_NAME + '._akima')  # TODO: machine dependency issues
    return _temp.interpolate

    # _temp = __import__('turbine.bin.' + DIR_NAME + '._akima', fromlist=['interpolate'])

# -------------------------------------


# ------- import bemroutines module ---------
def setup_bemroutines():
    """ usage: _bemroutines = setup_bemroutines() """

    return importlib.import_module('twister.models.CST.turbine.bin.' + DIR_NAME + '._bemroutines')

# -------------------------------------


# -------- path to precomp ------------
def setup_PreComp():
    names = ['precomp', 'PreComp']
    extensions = ['', '.exe']
    found = False
    for filename in [(os.path.join(CST_BIN, name + ext)) for name in names for ext in extensions]:
        if os.path.exists(filename):
            precompPath = filename
            found = True
            break

    if not found:
        raise Exception('Did not find precomp executable in ' + CST_BIN)

    return precompPath
# -------------------------------------


# --------- path to wtperf --------------
def setup_WT_Perf():
    names = ['wtperf', 'WT_Perf', 'WTPerf']
    extensions = ['', '.exe']
    found = False
    for filename in [(os.path.join(CST_BIN, name + ext)) for name in names for ext in extensions]:
        if os.path.exists(filename):
            wtperfPath = filename
            found = True
            break

    if not found:
        raise Exception('Did not find wtperf executable in: ' + CST_BIN)

    return wtperfPath
# ---------------------------------------


class TurbineVector(object):
    """Handles rotation of direction vectors to appropriate coordinate systems
    see [link].

    Input vectors can be scalar or array_like
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


    @staticmethod
    def __rotationAboutZ(x, y, z, theta):
        """
        x X y = z.  rotate c.s. about z, +theta
        all angles in degrees
        """

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        theta = np.array(theta)

        c = np.cos(D2R * theta)
        s = np.sin(D2R * theta)

        xnew = x*c + y*s
        ynew = -x*s + y*c

        return xnew, ynew, z

    # !!!!!!!! NOTE ALL ANGLES SHOULD BE PASSED IN DEGREES !!!!!!!!!!!!!!

    def windToInertial(self, beta):
        xi, yi, zi = TurbineVector.__rotationAboutZ(self.x, self.y, self.z, -beta)
        return TurbineVector(xi, yi, zi)

    def inertialToWind(self, beta):
        xw, yw, zw = TurbineVector.__rotationAboutZ(self.x, self.y, self.z, beta)
        return TurbineVector(xw, yw, zw)

    def yawToWind(self, psi):
        xw, yw, zw = TurbineVector.__rotationAboutZ(self.x, self.y, self.z, -psi)
        return TurbineVector(xw, yw, zw)

    def windToYaw(self, psi):
        xy, yy, zy = TurbineVector.__rotationAboutZ(self.x, self.y, self.z, psi)
        return TurbineVector(xy, yy, zy)

    def rotorToYaw(self, theta):
        zy, xy, yy = TurbineVector.__rotationAboutZ(self.z, self.x, self.y, -theta)
        return TurbineVector(xy, yy, zy)

    def yawToRotor(self, theta):
        zr, xr, yr = TurbineVector.__rotationAboutZ(self.z, self.x, self.y, theta)
        return TurbineVector(xr, yr, zr)

    def rotorToAzimuth(self, Lambda, clockwise=True):
        tz, rz, nz = TurbineVector.__rotationAboutZ(self.y, self.z, self.x, Lambda)
        if clockwise:
            tz = -tz
        return TurbineVector(tz, nz, rz)

    def azimuthToRotor(self, Lambda, clockwise=True):
        tz = self.x
        nz = self.y
        rz = self.z
        if clockwise:
            tz = -tz

        yr, zr, xr = TurbineVector.__rotationAboutZ(tz, rz, nz, -Lambda)

        return TurbineVector(xr, yr, zr)

    def azimuthToBlade(self, Phi, clockwise=True):
        tz = self.x
        nz = self.y
        rz = self.z

        if clockwise:
            n, r, t = TurbineVector.__rotationAboutZ(nz, rz, tz, Phi)
        else:
            r, n, t = TurbineVector.__rotationAboutZ(rz, nz, tz, -Phi)

        return TurbineVector(t, n, r)

    def bladeToAzimuth(self, Phi, clockwise=True):
        t = self.x
        n = self.y
        r = self.z

        if clockwise:
            nz, rz, tz = TurbineVector.__rotationAboutZ(n, r, t, -Phi)
        else:
            rz, nz, tz = TurbineVector.__rotationAboutZ(r, n, t, Phi)

        return TurbineVector(tz, nz, rz)

    def airfoilToBlade(self, theta, clockwise=True):
        n, t, r = TurbineVector.__rotationAboutZ(self.x, self.y, self.z, 90.0-theta)
        if clockwise:
            r = -r
        return TurbineVector(t, n, r)

    def bladeToAirfoil(self, theta, clockwise=True):
        t = self.x
        n = self.y
        r = self.z
        if clockwise:
            r = -r
        xa, ya, za = TurbineVector.__rotationAboutZ(n, t, r, theta-90.0)

        return TurbineVector(xa, ya, za)

