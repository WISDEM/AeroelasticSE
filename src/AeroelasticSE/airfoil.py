#!/usr/bin/env python
# encoding: utf-8
"""
airfoil.py

Created by Andrew Ning on 2012-04-16.
Copyright (c) NREL. All rights reserved.

2012 11 12 - GNS - modifications for old-style Aerodyn files

"""

from math import pi, sin, cos, isnan
import numpy as np
import subprocess
import os, sys
import warnings
import glob

# ---------------- constants ----------------

R2D = 180.0/pi
D2R = pi/180.0

# ------------------------------------------


class AirfoilFamily:
    """
    This class represents a family of airfoils.
    Airfoils within the family are distinguished by
    their thickness to chord ratio

    """

    def __init__(self, dirname):
        """
        Constructor. Initializes an airfoil family from a group
        of files in a single directory.

        If the 2D format is used, files can be named anything and
        this method will read in every file in the directory.
        3D format will be detected if any of the files have the *.inp extension.
        For this case each WTPerf *.dat file must have a PreComp *.inp file
        with the same name but different extension.

        Arguments:
        dirname - directory containing files defining the airfoils in the family

        """

        self.airfoils = []
        self.name = dirname

        is2D = True
        if len(glob.glob(dirname + '/*.inp')) > 0:
            is2D = False

        if is2D:
            for fname in os.listdir(dirname):
                af = Airfoil.initFrom2DFile(os.path.join(dirname, fname))
                self.addToFamily(af)
        else:
            for fname in glob.glob(dirname + '/*.dat'):
                af = Airfoil.initFrom3DFile(os.path.join(dirname, fname),
                                            os.path.join(dirname, fname[:-3] + '.inp'))
                self.addToFamily(af)


    def addToFamily(self, airfoil):
        """
        Adds the airfoil object to this family.

        Arguments:
        airfoil - object to add

        """
        self.airfoils.append(airfoil)

        # sort by t/c
        self.airfoils = sorted(self.airfoils, key=lambda af: af.profile.tc)


    def getAirfoil(self, tc):
        """
        Gets an airfoil object for this family at the specified thickness to chord ratio.
        Interpolates as necessary. If t/c number is larger than or smaller than
        the stored airfoils, it returns the airfoil with the closest t/c,
        but also issues a warning.

        Arguments:
        tc - thickness to chord ratio

        Returns:
        Airfoil object

        """

        af = self.airfoils

        if tc <= af[0].profile.tc:
            warnings.warn("t/c less than smallest in family", UserWarning)
            return af[0]

        elif tc >= af[-1].profile.tc:
            warnings.warn("t/c greater than largest in family", UserWarning)
            return af[-1]

        else:
            tclist = [airfoil.profile.tc for airfoil in af]
            i = np.searchsorted(tclist, tc)
            weight = (tc - tclist[i-1]) / (tclist[i] - tclist[i-1])
            return af[i-1].blend(af[i], weight)


    def setup3DSplineForFamily(self):

        self.tc = [af.profile.tc for af in self.airfoils]
        # ....


class Airfoil:
    """
    This class represents an airfoil. An airfoil has a profile shape,
    and one or more Polar objects at different Reynolds numbers.

    """

    def __init__(self, profile, polarByRe, name=''):
        """
        Constructor

        Arguments:
        profile - Profile object
        polarByRe - PolarByRe object
        name - an optional name or description for the airfoil

        Notes:
        Polar objects can be in any order.

        """

        self.profile = profile
        self.aeroData = polarByRe
        self.name = name


    @staticmethod
    def initFrom2DFile(filename):
        """
        Construct from file containing 2D data

        Arguments:
        filename - path/name of file

        File format:
        --------
        name
        x y
        . .
        . .
        . .

        Re
        alpha cl cd
        .     .   .
        .     .   .
        .     .   .

        repeat for other polars
        -------

        Notes:
        x, y coordinates should traverse from trailing edge
        to trailing edge in either direction
        blank lines can be put anywhere except in the middle
        of column data

        """

        polars = []

        f = open(filename)

        first = True
        x = []
        y = []

        for line in f:

            if not line or line.isspace():
                if len(x) > 0:
                    break
                # otherwise do nothing

            elif first:
                name = line.rstrip() # remove newline
                first = False

            else:
                data = [float(s) for s in line.split()]
                x.append(data[0])
                y.append(data[1])

        first = True
        alpha = []
        cl = []
        cd = []

        for line in f:

            if not line or line.isspace():
                if len(alpha) > 0:
                    polars.append(Polar(Re, alpha, cl, cd, True))
                    first = True
                    alpha = []
                    cl = []
                    cd = []
                # otherwise do nothing

            elif first:
                Re = float(line)
                first = False

            else:
                data = [float(s) for s in line.split()]
                alpha.append(data[0])
                cl.append(data[1])
                cd.append(data[2])


        f.close()

        profile = Profile.initWithTEtoTEdata(x, y)
        polarByRe = PolarByRe(polars)
        return Airfoil(profile, polarByRe, name)




    @staticmethod
    def createInputFileFromXFOIL(dirname, filename, Relist, aStart, aEnd, aStep,
        xfoil_input_file, naca=None):
        """
        This method is used to create the 2-D airfoil input files using XFOIL

        Arguments:
        dirname, filename - the input will be saved in dirname/filename.  For
            creating airfoil families,  all airfoils of the family should be
            saved in the same directory. If the directory does not already exist this method will try to create it.
        Relist - a list of Reynolds numbers to run
        aStart, aEnd, aStep - angle of attack sweep
        xfoil_input_file - profile can be defined from any standard XFOIL input file
        naca (optional) - or if an NACA section is used the defining string can be given (i.e. '2412')

        Returns:
        n/a

        """

        try:
            os.mkdir(dirname)
        except OSError:
            pass

        filename = os.path.join(dirname, filename)

        # delete if it already exists
        if os.path.exists(filename):
            os.remove(filename)

        # write coordinate data first
        xfoil = os.path.join(os.environ['CST_BIN'], 'xfoil')
        process = subprocess.Popen(xfoil, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        if naca is not None:
            process.stdin.write('naca ' + naca + '\n')
        else:
            process.stdin.write('load ' + xfoil_input_file + '\n')
        process.stdin.write('save\n')
        process.stdin.write(filename + '\n')
        process.stdin.write('quit\n')
        process.communicate()  # clear buffer and wait for process to terminate


        # add polar data
        fout = open(filename, 'a')
        print >> fout
        print >> fout

        for Re in Relist:

            print 'running XFOIL'

            # XFOIL output file
            if naca is not None:
                f_xfoil = 'naca' + naca + '_' + str(Re) + '.dat'
            else:
                f_xfoil = xfoil_input_file + '_' + str(Re) + '.dat'

            # delete if it already exists
            if os.path.exists(f_xfoil):
                os.remove(f_xfoil)

            # run XFOIL
            process = subprocess.Popen(xfoil, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            process.stdin.write('plop\n')
            process.stdin.write('g\n')
            process.stdin.write('\n')
            if naca is not None:
                process.stdin.write('naca ' + naca + '\n')
            else:
                process.stdin.write('load ' + xfoil_input_file + '\n')
            process.stdin.write('oper\n')
            process.stdin.write('visc' + ' ' + str(Re) + '\n')
            process.stdin.write('M 0.2\n')
            process.stdin.write('pacc\n')
            process.stdin.write(f_xfoil + '\n')
            process.stdin.write('\n')
            process.stdin.write('aseq' + ' ' + str(aStart) + ' ' + str(aEnd) + ' ' + str(aStep) + '\n')
            process.stdin.write('\n')
            process.stdin.write('quit\n')
            process.stdin.write('\n')
            process.communicate()  # clear buffer and wait for process to terminate




            # parse output
            f = open(f_xfoil, 'r')

            for i in range(12):
                f.readline()

            alpha = []
            cl = []
            cd = []

            for line in f:
                data = [float(s) for s in line.split()]
                alpha.append(data[0])
                cl.append(data[1])
                cd.append(data[2])
            f.close()
            os.remove(f_xfoil)

            # write to new file
            print >> fout, Re
            #print >> fout, '{0:9} {1:9} {2:9}'.format('alpha', 'cl', 'cd')
            for x, y, z in zip(alpha, cl, cd):
                print >> fout, '{0:0<9.6f} {1:0<9.6f} {2:0<9.6f}'.format(x, y, z)
            print >> fout

        fout.close()



    def blend(self, other, weight):
        """
        Blend this airfoil with another one with the specified weighting.
        Blends profile data and polar data.

        Arguments:
        other - another Airfoil
        weight - blending parameter between 0 and 1.  0 returns self, whereas 1 returns other.

        Returns:
        a blended Airfoil
        """

        profile = self.profile.blend(other.profile, weight)
        aeroData = self.aeroData.blend(other.aeroData, weight)
        name = self.name + ' blended with ' + other.name

        return Airfoil(profile, aeroData, name)


    @property
    def polarList(self):
        return self.aeroData.polars


class Profile:
    """
    Defines the shape of an airfoil
    """

    def __init__(self, xu, yu, xl, yl):
        """
        Constructor

        Arguments:
        xu, yu - x and y coordinates for upper surface of airfoil
        xl, yl - x and y coordinates for lower surface of airfoil

        Notes:
        x is the direction of the chord line and y is orthogonal to that.
        nodes should be ordered from the leading edge toward the trailing edge.
        The leading edge can be located at any position and the
        chord may be any size, however the airfoil should be untwisted.

        """

        # parse airfoil data
        xu = np.array(xu)
        yu = np.array(yu)
        xl = np.array(xl)
        yl = np.array(yl)

        # ensure leading edge at zero
        xu -= xu[0]
        xl -= xl[0]
        yu -= yu[0]
        yl -= yl[0]

        # ensure unit chord
        c = xu[-1] - xu[0]
        xu /= c
        xl /= c
        yu /= c
        yl /= c

        # interpolate onto common grid
        arc = np.linspace(0, pi, 100)
        self.x = 0.5*(1-np.cos(arc))  # cosine spacing
        self.yu = np.interp(self.x, xu, yu)
        self.yl = np.interp(self.x, xl, yl)

        # compute thickness to chord ratio
        self.tc = max(self.yu - self.yl)


    @classmethod
    def initWithTEtoTEdata(cls, x, y):
        """
        Factory constructor for data points ordered from trailing edge
        to trailing edge.

        Arguments:
        x, y - airfoil coordinates starting at trailing edge and
        ending at trailing edge, traversing airfoil in either direction.

        Notes:
        It is not necessary to start and end at the same point
        for an airfoil with trailing edge thickness.
        One point should be right at the nose.
        see also notes for main constructor.

        Returns:
        Profile object

        """

        # parse airfoil data
        x = np.array(x)
        y = np.array(y)

        # separate into 2 halves
        for i in range(len(x)):
            if x[i+1] > x[i]:
                break

        xu = x[i::-1]
        yu = y[i::-1]
        xl = x[i:]
        yl = y[i:]


        # check if coordinates were input in other direction
        if y[1] < y[0]:
            temp = yu
            yu = yl
            yl = temp

            temp = xu
            xu = xl
            xl = temp

        return cls(xu, yu, xl, yl)


    @classmethod
    def initWithLEtoLEdata(cls, x, y):
        """
        Factory constructor for data points ordered from leading edge
        to leading edge.

        Arguments:
        x, y - airfoil coordinates starting at leading edge and
        ending at leading edge, traversing airfoil in either direction.

        Notes:
        x,y data must start and end at the same point.
        see also notes for main constructor.

        Returns:
        Profile object

        """

        # parse airfoil data
        x = np.array(x)
        y = np.array(y)

        # separate into 2 halves
        for i in range(len(x)):
            if x[i+1] < x[i]:
                break

        xu = x[:i+1]
        yu = y[:i+1]
        xl = x[i::-1]
        yl = y[i::-1]

        # check if coordinates were input in other direction
        if y[1] < y[0]:
            temp = yu
            yu = yl
            yl = temp

            temp = xu
            xu = xl
            xl = temp

        return cls(xu, yu, xl, yl)


    @staticmethod
    def initFromPrecompFile(precompProfileFile):
        """
        Construct profile from precomp formatted file

        Arguments:
        precompProfileFile - path/name of files

        Returns:
        an Profile object

        """

        return Profile.initFromFile(precompProfileFile, 4, True)

        # # open precomp file
        # f = open(precompProfileFile,'r')

        # # skip through header
        # numPoints = int(f.readline().split()[0])
        # for i in range(3): f.readline()

        # # loop through
        # x = np.zeros(numPoints+1)
        # y = np.zeros(numPoints+1)
        # for i in range(numPoints):
        #     data = f.readline().split()
        #     x[i] = float(data[0])
        #     y[i] = float(data[1])

        # f.close()

        # # close airfoil
        # x[numPoints] = x[0]
        # y[numPoints] = y[0]

        # return Profile.initWithLEtoLEdata(x, y)


    @staticmethod
    def initFromFile(filename, numHeaderlines, LEtoLE):
        """


        """

        # open file
        f = open(filename, 'r')

        # skip through header
        for i in range(numHeaderlines):
            f.readline()

        # loop through
        x = []
        y = []

        for line in f:
            if not line.strip():
                break  # break if empty line
            data = line.split()
            x.append(float(data[0]))
            y.append(float(data[1]))

        f.close()

        # close nose if LE to LE
        if LEtoLE:
            x.append(x[0])
            y.append(y[0])
            return Profile.initWithLEtoLEdata(x, y)

        else:
            return Profile.initWithTEtoTEdata(x, y)




    def writeToPrecompFile(self, filename):
        """
        Write the airfoil section data to a file using PreComp input file style.

        Arguments:
        filename - name (+ relative path) of where to write file

        Returns:
        nothing

        """

        # check if they share a common trailing edge point
        te_same = self.yu[-1] == self.yl[-1]

        # count number of points
        nu = len(self.x)
        if (te_same):
            nu -= 1
        nl = len(self.x) - 1  # they do share common leading-edge
        n = nu + nl

        # initialize
        x = np.zeros(n)
        y = np.zeros(n)

        # leading edge round to leading edge
        x[0:nu] = self.x[0:nu]
        y[0:nu] = self.yu[0:nu]
        x[nu:] = self.x[:0:-1]
        y[nu:] = self.yl[:0:-1]


        f = open(filename, 'w')
        print >> f, '{0:<10d} {1:40}'.format(n, 'n_af_nodes: # of airfoil nodes.')
        print >> f, '{0:<10} {1:40}'.format('', 'clockwise starting at leading edge')
        print >> f
        print >> f, 'xnode \t ynode'
        for xpt, ypt in zip(x, y):
            print >> f, '{0:<15f} {1:15f}'.format(xpt, ypt)

        f.close()



    def locationOfMaxThickness(self):
        """
        returns: (x, yu, yl)
        """

        idx = np.argmax(self.yu - self.yl)
        return (self.x[idx], self.yu[idx], self.yl[idx])


    def blend(self, other, weight):
        """
        Blend this profile with another one with the specified weighting.

        Arguments:
        other - another profile
        weight - blending parameter between 0 and 1.  0 returns self, whereas 1 returns other.

        Returns:
        a blended profile
        """


        # blend coordinates
        yu = self.yu + weight*(other.yu - self.yu)
        yl = self.yl + weight*(other.yl - self.yl)

        return Profile(self.x, yu, self.x, yl)


    @property
    def tc(self):
        return self.tc





class PolarByRe:
    """
    a list of polar objects at different Reynolds numbers

    """


    def __init__(self, polars):
        """
        Arguments:
        polars - list of Polar objects

        """

        # sort by Reynolds number
        self.polars = sorted(polars, key=lambda p: p.Re)


        self.cl_spline = None  # will be lazily instantiated as needed
        self.cd_spline = None


    @classmethod
    def initFromAerodynFile(cls, aerodynFile):
        """
        Construct array of polars from aerodyn file

        Arguments:
        aerodynFile - path/name of a properly formatted Aerodyn file

        Returns:
        a list of polar objects

        """
        # initialize
        polars = []

        # open aerodyn file
        f = open(aerodynFile, 'r')

        # skip through header
        f.readline()
        description = f.readline().rstrip()  # remove newline
        f.readline()
        numTables = int(f.readline().split()[0])

        # loop through tables
        for i in range(numTables):

            # read Reynolds number
            Re = float(f.readline().split()[0])*1e6

            # read Aerodyn parameters
            param = [0]*8
            for j in range(8):
                param[j] = float(f.readline().split()[0])

            alpha = []
            cl = []
            cd = []
            # read polar information line by line
            while True:
                line = f.readline()
                if 'EOT' in line:
                    break
                data = [float(s) for s in line.split()]
                alpha.append(data[0])
                cl.append(data[1])
                cd.append(data[2])


            polars.append(Polar(Re, alpha, cl, cd, False, param))

        f.close()

        return cls(polars)

    #-------------------------------------------------
    
    @classmethod
    def initFromOldAerodynFile(cls, aerodynFile):
        """
        Construct array of polars from old-style Aerodyn file
        Use this method for FAST (which can't read the new format) 2012 11 12

        Arguments:
        aerodynFile - path/name of a properly formatted old-style Aerodyn file

        Returns:
        a list of polar objects

        """
        # initialize
        polars = []

        # open aerodyn file
        f = open(aerodynFile, 'r')

        # skip through header
        f.readline()
        description = f.readline().rstrip()  # remove newline
        numTables = int(f.readline().split()[0])

        # loop through tables
        for i in range(numTables):

            # read Aerodyn parameters
            param = [0]*11
            for j in range(11):
                param[j] = float(f.readline().split()[0])

            alpha = []
            cl = []
            cd = []
            # read polar information line by line
            while True:
                line = f.readline()
                if 'EOT' in line:
                    break
                data = [float(s) for s in line.split()]
                if len(data) < 1:
                    break
                alpha.append(data[0])
                cl.append(data[1])
                cd.append(data[2])

            Re = 1.0
            warnings.warn('WARNING: setting default Re to {:.1f}*1E6'.format(Re), UserWarning)
            polars.append(Polar(Re, alpha, cl, cd, False, param))

        f.close()

        return cls(polars)



    def getPolar(self, Re):
        """
        Gets a polar object for this airfoil at the specified Reynolds number.
        Interpolates as necessary. If Reynolds number is larger than or smaller than
        the stored polars, it returns the polar with the closest Reynolds number.

        Arguments:
        Re - Reynolds number

        Returns:
        Polar object

        """

        p = self.polars

        if Re <= p[0].Re:
            return p[0].copyPolarWithNewRe(Re)

        elif Re >= p[-1].Re:
            return p[-1].copyPolarWithNewRe(Re)

        else:
            Relist = [pp.Re for pp in p]
            i = np.searchsorted(Relist, Re)
            weight = (Re - Relist[i-1]) / (Relist[i] - Relist[i-1])
            return p[i-1].blend(p[i], weight)



    def blend(self, other, weight):
        """
        Blend these polars with another one with the specified weighting.
        Finds the unique Reynolds numbers.  Evaluates both sets of polars
        at each of the Reynolds numbers, and blend them.

        Arguments:
        other - another PolarByRe
        weight - blending parameter between 0 and 1.  0 returns self, whereas 1 returns other.

        Returns:
        a blended PolarByRe
        """

        # combine Reynolds numbers
        Relist1 = [p.Re for p in self.polars]
        Relist2 = [p.Re for p in other.polars]
        Relist = np.unique(np.concatenate((Relist1, Relist2)))

        # blend polars
        n = len(Relist)
        polars = [0]*n
        for i in range(n):
            p1 = self.getPolar(Relist[i])
            p2 = other.getPolar(Relist[i])
            polars[i] = p1.blend(p2, weight)


        return PolarByRe(polars)


    def extend2DDataTo3DIfNecessary(self, r, chord, chord_75, R, tsr, alpha_max_corr=30,
                alpha_linear_min=-5, alpha_linear_max=5):
        """
        This method loops through each polar of the airfoil
        and applies 3-D rotational corrections and extensions
        to +/- 180 deg if they have not already been applied to the polar.

        Arguments:
        r - radial position
        chord - chord length of section
        chord_75 - chord at 75% radius
        R - rotor radius
        tsr - tip speed ratio
        alpha_max_corr (optional) - maximum angle of attack to apply full correction (deg)
        alpha_linear_min, alpha_linear_max (optional) - define start and end of
            linear portion of lift curve slope (deg)

        Returns:
        n/a
        """

        for idx, p in enumerate(self.polars):
            if p.is2D:
                p = p.correction3d(r, chord, R, tsr, alpha_max_corr, alpha_linear_min, alpha_linear_max)
                p = p.extrapolate(chord_75, R)
                self.polars[idx] = p



    def writeToAerodynFile(self, filename, mode=0, debug=False):
        """
        Write the airfoil section data to a file using AeroDyn input file style.

        Arguments:
        filename - name (+ relative path) of where to write file
        mode - integer : if 1, write old-style Aerodyn file
        
        Returns:
        nothing

        """

        f = open(filename, 'w')

        if (mode == 0):
            print >> f, 'AeroDyn airfoil file.  Compatible with AeroDyn v13.0.'
            print >> f, 'auto generated by airfoil.py'
            print >> f, 'airfoil.py is part of rotor TEAM'
            print >> f, '{0:<10d} {1:40}'.format(len(self.polars), 'Number of airfoil tables in this file')
            for p in self.polars:
                print >> f, '{0:<10g} {1:40}'.format(p.Re/1e6, 'Reynolds number in millions.')
                param = p.computeAerodynParameters(debug=debug)
                print >> f, '{0:<10f} {1:40}'.format(param[0], 'Control setting')
                print >> f, '{0:<10f} {1:40}'.format(param[1], 'Stall angle (deg)')
                print >> f, '{0:<10f} {1:40}'.format(param[2], 'Angle of attack for zero Cn for linear Cn curve (deg)')
                print >> f, '{0:<10f} {1:40}'.format(param[3], 'Cn slope for zero lift for linear Cn curve (1/rad)')
                print >> f, '{0:<10f} {1:40}'.format(param[4], 'Cn at stall value for positive angle of attack for linear Cn curve')
                print >> f, '{0:<10f} {1:40}'.format(param[5], 'Cn at stall value for negative angle of attack for linear Cn curve')
                print >> f, '{0:<10f} {1:40}'.format(param[6], 'Angle of attack for minimum CD (deg)')
                print >> f, '{0:<10f} {1:40}'.format(param[7], 'Minimum CD value')
                for a, cl, cd in zip(p.alpha, p.cl, p.cd):
                    print >> f, '{0:<10f} {1:<10f} {2:<10f}'.format(a*R2D, cl, cd)
                print >> f, 'EOT'   

        else:
            print >> f, 'AeroDyn airfoil file.'
            print >> f, 'auto generated by airfoil.py (part of rotor TEAM)'
            print >> f, '{0:<10d} {1:40}'.format(len(self.polars), 'Number of airfoil tables in this file')
            for i,p in enumerate(self.polars):
                param = p.computeAerodynParameters(mode=1,debug=debug)
                print param
                print >> f, '{0:<10g} {1:40}'.format(param[0], 'Table ID parameter')
                print >> f, '{0:<10f} {1:40}'.format(param[1], 'Stall angle (deg)')
                print >> f, '{0:<10f} {1:40}'.format(0.0, 'No longer used, enter zero')
                print >> f, '{0:<10f} {1:40}'.format(0.0, 'No longer used, enter zero')
                print >> f, '{0:<10f} {1:40}'.format(0.0, 'No longer used, enter zero')
                print >> f, '{0:<10f} {1:40}'.format(param[2], 'Angle of attack for zero Cn for linear Cn curve (deg)')
                print >> f, '{0:<10f} {1:40}'.format(param[3], 'Cn slope for zero lift for linear Cn curve (1/rad)')
                print >> f, '{0:<10f} {1:40}'.format(param[4], 'Cn at stall value for positive angle of attack for linear Cn curve')
                print >> f, '{0:<10f} {1:40}'.format(param[5], 'Cn at stall value for negative angle of attack for linear Cn curve')
                print >> f, '{0:<10f} {1:40}'.format(param[6], 'Angle of attack for minimum CD (deg)')
                print >> f, '{0:<10f} {1:40}'.format(param[7], 'Minimum CD value') # is this 'Zero lift drag'?
                for a, cl, cd in zip(p.alpha, p.cl, p.cd):
                    print >> f, '{0:7.2f} {1:<7.3f} {2:<7.3}'.format(a*R2D, cl, cd)
                    #print >> f, '{0:<10f} {1:<10f} {2:<10f}'.format(a*R2D, cl, cd)
            
        f.close()


    def setupSplineInterpolation(self):
        """docstring"""

        from scipy import interpolate


        for p in self.polars:
            if p.is2D:
                raise ValueError("Airfoil data should be extended from -180 to 180 first.  Use extend2DDataTo3DIfNecessary().")

        # create spline object
        alpha = np.linspace(-pi, pi, 100)
        Re = [p.Re for p in self.polars]
        polarList = self.polars

        # special case for when there is only one Reynolds number (need at least two for bivariate spline)
        if len(Re) == 1:
            Re = [1e-6*Re[0], 1e6*Re[0]]
            polarList = [polarList[0], polarList[0]]

        # fill in cl, cd grid
        cl = np.zeros((len(alpha), len(Re)))
        cd = np.zeros((len(alpha), len(Re)))

        for (idx, p) in enumerate(polarList):
            cl[:, idx] = np.interp(alpha, p.alpha, p.cl)
            cd[:, idx] = np.interp(alpha, p.alpha, p.cd)

        self.Re_used = Re
        self.cl_spline = interpolate.RectBivariateSpline(alpha, Re, cl, ky=len(Re)-1)
        self.cd_spline = interpolate.RectBivariateSpline(alpha, Re, cd, ky=len(Re)-1)



    def evaluate(self, alpha, Re):
        """docstring"""

        if self.cl_spline is None:
            self.setupSplineInterpolation()

        # if (Re > self.Re_used[-1] or Re < self.Re_used[0]):
        #     warnings.warn("Reynolds number out of range of input data", UserWarning)

        cl = self.cl_spline.ev(alpha, Re)
        cd = self.cd_spline.ev(alpha, Re)

        # make scalar
        cl = cl[0]
        cd = cd[0]

        return (cl, cd)




class Polar:
    """
    Defines section lift and drag coefficient as a function of angle of attack
    at a particular Reynolds number.

    """

    def __init__(self, Re, alpha, cl, cd, is2D, aerodynParam=None):
        """
        Constructor

        Arguments:
        Re - Reynolds number (float)
        alpha - angle of attack (deg, array)
        cl - lift coefficient (array)
        cd - drag coefficient (array)
        is2D - true if this is two-dimensional data (i.e. not corrected for rotational effects) (boolean)
        aerodynParam - list of parameters used in aerodyn file

        """

        self.Re = Re
        self.alpha = np.array(alpha)*D2R
        self.cl = np.array(cl)
        self.cd = np.array(cd)
        self.is2D = is2D
        self.aerodynParam = aerodynParam


    def copyPolarWithNewRe(self, Re):
        """
        Copy polar but change its Reynolds number

        Arguments:
        Re - new Reynolds number

        Returns:
        new Polar

        """
        return Polar(Re, self.alpha*R2D, self.cl, self.cd, self.is2D, self.aerodynParam)


    def blend(self, other, weight):
        """
        Blend this polar with another one with the specified weighting

        Arguments:
        other - another Polar
        weight - blending parameter between 0 and 1.  0 returns self, whereas 1 returns other.

        Returns:
        a blended Polar
        """

        if self.is2D != other.is2D:
            warnings.warn("blending a 2-D polar with a 3-D one", UserWarning)

        # generate merged set of angles of attack - get unique values
        alpha = np.unique(np.concatenate((self.alpha, other.alpha)))

        # truncate (TODO: could also have option to just use one of the polars for values out of range)
        min_alpha = max(self.alpha.min(), other.alpha.min())
        max_alpha = min(self.alpha.max(), other.alpha.max())
        alpha = np.array([a for a in alpha if a >= min_alpha and a <= max_alpha])

        # interpolate to new alpha
        cl1 = np.interp(alpha, self.alpha, self.cl)
        cl2 = np.interp(alpha, other.alpha, other.cl)
        cd1 = np.interp(alpha, self.alpha, self.cd)
        cd2 = np.interp(alpha, other.alpha, other.cd)

        # linearly blend
        Re = self.Re + weight*(other.Re-self.Re)
        cl = cl1 + weight*(cl2-cl1)
        cd = cd1 + weight*(cd2-cd1)

        return Polar(Re, alpha*R2D, cl, cd, self.is2D)


    def correction3d(self, r, chord, R, tsr, alpha_max_corr=30,
                alpha_linear_min=-5, alpha_linear_max=5):
        """
        Applies 3d corrections for rotating sections from the 2d data.
        Du-Selig method is used to correct lift, and Eggers method is used
        to correct drag.

        If the polar has already been corrected for 3d effects, it returns itself.as

        Arguments:
        r - radial position
        chord - chord length of section
        R - rotor radius
        tsr - tip speed ratio
        alpha_max_corr (optional) - maximum angle of attack to apply full correction (deg)
        alpha_linear_min, alpha_linear_max (optional) - define start and end of
            linear portion of lift curve slope (deg)

        Returns:
        A new AirfoilPolar

        """

        if not self.is2D:
            return self

        # rename and convert units for convenience
        alpha = self.alpha
        cl_2d = self.cl
        cd_2d = self.cd
        alpha_max_corr *= D2R
        alpha_linear_min *= D2R
        alpha_linear_max *= D2R

        # parameters in Du-Selig model
        a = 1; b = 1; d = 1
        lam = tsr/(1+tsr**2)**0.5  # modified tip speed ratio
        expon = d/lam*R/r
        cOverr = chord/r

        # find linear region
        idx = np.logical_and(alpha >= alpha_linear_min,
                             alpha <= alpha_linear_max)
        p = np.polyfit(alpha[idx], cl_2d[idx], 1)
        m = p[0]
        alpha0 = -p[1]/m

        # correction factor
        fcl = 1.0/m*(1.6*cOverr/0.1267*(a-cOverr**expon)/(b+cOverr**expon)-1)

        # not sure where this adjustment comes from (besides AirfoilPrep spreadsheet of course)
        adj = ((pi/2-alpha)/(pi/2-alpha_max_corr))**2
        adj[alpha <= alpha_max_corr] = 1.0

        # Du-Selig correction for lift
        cl_linear = m*(alpha-alpha0)
        cl_3d = cl_2d + fcl*(cl_linear-cl_2d)*adj

        # Eggers 2003 correction for drag
        delta_cl = cl_3d-cl_2d

        delta_cd = delta_cl*(np.sin(alpha) - 0.12*np.cos(alpha))/(np.cos(alpha) + 0.12*np.sin(alpha))
        cd_3d = cd_2d + delta_cd

        return Polar(self.Re, alpha*R2D, cl_3d, cd_3d, False)


    def extrapolate(self, c75, R):
        """
        Extrapolates force coefficients up to +/- 180 deg using Viterna's method.

        Arguments:
        c75 - chord at 75% radius
        R - rotor radius

        Notes:
        If the current polar already supplies data beyond 90 deg then
        this method cannot be used in its current form and will just return itself.

        Returns:
        A new AirfoilPolar.

        """

        # lift coefficient adjustment to account for assymetry
        cl_adj = 0.7

        # estimate CD max
        AR = c75/R
        cdmax = max(max(self.cd), 1.11 + 0.018*AR)

        # extract matching info from ends
        alpha_high = self.alpha[-1]
        cl_high = self.cl[-1]
        cd_high = self.cd[-1]

        alpha_low = self.alpha[0]
        cl_low = self.cl[0]
        cd_low = self.cd[0]

        if alpha_high > pi/2:
            raise Exception, "alpha > pi/2"
            return self
        if alpha_low < -alpha_high:  # TODO: could probably handle these casee with minor changes
            raise Exception, "alpha[0] < -alpha[end]"
            return self

        # parameters used in model
        sa = sin(alpha_high)
        ca = cos(alpha_high)
        A = (cl_high - cdmax*sa*ca)*sa/ca**2
        B = (cd_high - cdmax*sa*sa)/ca

        # alpha_high <-> 90
        alpha1 = np.linspace(alpha_high, pi/2, 15)
        alpha1 = alpha1[1:]  # remove first element so as not to duplicate when concatenating
        coeff = Polar.__Viterna(A, B, cdmax, alpha1, 1)
        cl1 = coeff[0]
        cd1 = coeff[1]

        # 90 <-> 180-alpha_high
        alpha2 = np.linspace(pi/2, pi-alpha_high, 15)
        alpha2 = alpha2[1:]
        coeff = Polar.__Viterna(A, B, cdmax, pi-alpha2, -cl_adj)
        cl2 = coeff[0]
        cd2 = coeff[1]

        # 180-alpha_high <-> 180
        alpha3 = np.linspace(pi-alpha_high, pi, 15)
        alpha3 = alpha3[1:]
        coeff = Polar.__Viterna(A, B, cdmax, pi-alpha3, 1)
        cl3 = (alpha3-pi)/alpha_high*cl_high*cl_adj
        cd3 = coeff[1]

        # -alpha_high <-> alpha_low
        # Note: this is done slightly differently than AirfoilPrep for better continuity
        alpha4 = np.linspace(-alpha_high, alpha_low, 15)
        alpha4 = alpha4[1:-2]  # also remove last element for concatenation for this case
        cl4 = -cl_high*cl_adj + (alpha4+alpha_high)/(alpha_low+alpha_high)*(cl_low+cl_high*cl_adj)
        cd4 = cd_low + (alpha4-alpha_low)/(-alpha_high-alpha_low)*(cd_high-cd_low)

        # -90 <-> -alpha_high
        alpha5 = np.linspace(-pi/2, -alpha_high, 15)
        alpha5 = alpha5[1:]
        coeff = Polar.__Viterna(A, B, cdmax, -alpha5, -cl_adj)
        cl5 = coeff[0]
        cd5 = coeff[1]

        # -180+alpha_high <-> -90
        alpha6 = np.linspace(-pi+alpha_high, -pi/2, 15)
        alpha6 = alpha6[1:]
        coeff = Polar.__Viterna(A, B, cdmax, alpha6+pi, cl_adj)
        cl6 = coeff[0]
        cd6 = coeff[1]

        # -180 <-> -180 + alpha_high
        alpha7 = np.linspace(-pi, -pi+alpha_high, 15)
        coeff = Polar.__Viterna(A, B, cdmax, alpha7+pi, 1)
        cl7 = (alpha7+pi)/alpha_high*cl_high*cl_adj
        cd7 = coeff[1]


        alpha = np.concatenate((alpha7,alpha6,alpha5,alpha4,self.alpha,alpha1,alpha2,alpha3))
        cl = np.concatenate((cl7,cl6,cl5,cl4,self.cl,cl1,cl2,cl3))
        cd = np.concatenate((cd7,cd6,cd5,cd4,self.cd,cd1,cd2,cd3))

        cd = np.maximum(cd, 0.01) # don't allow negative drag coefficients

        return Polar(self.Re, alpha*R2D, cl, cd, self.is2D)



    @staticmethod
    def __Viterna(A, B, cdmax, alpha, cl_adj):
        """private method to perform Viterna extrapolation"""

        alpha = np.maximum(alpha,0.0001) # prevent divide by zero

        cl = cdmax/2*np.sin(2*alpha) + A*np.cos(alpha)**2/np.sin(alpha)
        cl = cl*cl_adj

        cd = cdmax*np.sin(alpha)**2 + B*np.cos(alpha)

        return cl, cd


    def computeAerodynParameters(self, alpha_linear_min=-5, alpha_linear_max=5, mode=0, debug=False):
        """
        Method to estimate parameters used in AeroDyn input file for dynamic stall

        Arguments:
        alpha_linear_min, alpha_linear_max (optional) - define start and end of
            linear portion of lift curve slope (deg)

        mode - if 1, return parameters for old-style Aerodyn file
        
        Return:
        tuple of parameters in same order as Aerodyn file.

        """

        if self.aerodynParam is not None:
            return self.aerodynParam

        alpha = self.alpha
        cl = self.cl
        cd = self.cd

        alpha_linear_min *= D2R
        alpha_linear_max *= D2R

        cn = cl*np.cos(alpha) + cd*np.sin(alpha)
        alphaUpper = np.arange(40.0)*D2R
        alphaLower = np.arange(5.0, -40.0, -1)*D2R
        cnUpper = np.interp(alphaUpper, alpha, cn)
        cnLower = np.interp(alphaLower, alpha, cn)

        alphaU = 0.0
        alphaL = 0.0 #TODO: remove these
        #TODO: make this more robust.  This may not necessary find a value
        for j in range(1, len(cnUpper)):
            if (cnUpper[j] <= cnUpper[j-1]):
                alphaU = alphaUpper[j]
                break
        for j in range(1, len(cnLower)):
            if (cnLower[j] >= cnLower[j-1]):
                alphaL = alphaLower[j]
                break

        # find linear region (TODO: remove hardcoded limits)
        idx = np.logical_and(alpha >= alpha_linear_min,
                             alpha <= alpha_linear_max)
        
        if debug:                     
            print 'Calling polyfit with {:} points - alpha range = {:} to {:}'.format(sum(idx),alpha_linear_min,alpha_linear_max)
            for z in zip(alpha[idx], cn[idx]):
                print '  {:6.3f} {:6.3f}'.format(z[0],z[1])
            
        p = np.polyfit(alpha[idx], cn[idx], 1)
        m = p[0]
        alpha0 = -p[1]/m
        
        # Plot point and best fit
        
        if debug and sum(idx) > 1:
            import matplotlib.pyplot as plt
            pf = np.poly1d(p)
            fig = plt.figure()
            plt.plot(alpha[idx], cn[idx], '.', 
                     alpha[idx], pf(alpha[idx]), '-') 
            plt.xlim(alpha_linear_min*1.2, alpha_linear_max*1.2)
            plt.xlabel('Alpha (radians)')
            plt.ylabel('Cn')
            plt.grid()
            plt.suptitle('Fitting Dynamic Stall for AeroDyn')
            plt.show()

        # compute cn at stall according to linear fit
        cnStallUpper = m*(alphaU-alpha0)
        cnStallLower = m*(alphaL-alpha0)
        
        # find min cd
        minIdx = cd.argmin()

        if isnan(alpha0):
            # polyfit didn't work 
            alpha0 = 0.0
            cnStallUpper = 0.0
            cnStallLower = 0.0
            sys.stderr.write('\n*** computeAerodynParameters(): np.polyfit failed to converge - setting alpha and cn to 0.0\n\n')

        if mode == 0:
            # return: control setting, stall angle, alpha for 0 cn, cn slope,
            #         cn at stall+, cn at stall-, alpha for min CD, min(CD)
            return (0.0, alphaU*R2D, alpha0*R2D, m,
                    cnStallUpper, cnStallLower, alpha[minIdx], cd[minIdx])
                    
        else: # old-style Aerodyn parameters
            # return: Table ID, stall angle, 3 dummys, alpha for 0 cn, cn slope,
            #         cn at stall+, cn at stall-, alpha for min CD, min(CD)
            return (0.0, 
                alphaU*R2D, 0.0, 0.0, 0.0, alpha0*R2D, 
                m, cnStallUpper, cnStallLower, 
                alpha[minIdx], cd[minIdx])


if __name__ == '__main__':


    #Re = np.array([1e6, 5e5])
    #Airfoil.createInputFileFromXFOIL('naca23xx', '2316.dat', Re, -4, 23, 0.5, 'nofile', naca='2316')

    family = AirfoilFamily('naca23xx')


    af = family.getAirfoil(0.13)

    print af.profile.tc
    for p in af.polarList:
        print p.Re

    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid.axislines import Subplot

    fig = plt.figure(1)
    ax = Subplot(fig, 111)
    fig.add_subplot(ax)
    ax.axis["right"].set_visible(False)
    ax.axis["top"].set_visible(False)

    #plt.plot(af.polars[0].alpha*R2D, af.polars[0].cl, label='2D')


    r = [2.75, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 19.9, 20.4]
    theta = [20.0, 18.15, 14.65, 11.525, 8.75, 6.65, 5.35, 4.425, 3.575, 2.875, 2.31, 1.69, 1.065, 0.55, 0.235, 0.095, 0.035, 0.02]
    chord = [1.63, 1.6135, 1.5685, 1.5105, 1.4505, 1.388, 1.325, 1.2615, 1.196, 1.129, 1.0605, 0.9905, 0.918, 0.8435, 0.7555, 0.625, 0.405, 0.265]


    R = 20.4
    r = 0.25*R
    c = 1.3
    tsr = 8.0;
    c75 = 1.0
    af.aeroData.extend2DDataTo3DIfNecessary(r, c, c75, R, tsr)
    print af.polarList[0].Re
    print af.polarList[0].alpha
    print af.polarList[0].cl
    print af.polarList[0].cd
    print len(af.polarList[0].alpha)
    plt.plot(af.polarList[0].alpha, af.polarList[0].cl)

    af = family.getAirfoil(0.13)
    af.aeroData.extend2DDataTo3DIfNecessary(0.75*R, 1.0, c75, R, tsr)
    plt.plot(af.polarList[0].alpha, af.polarList[0].cl)
    plt.show()

    # plt.plot(af.polars[0].alpha*R2D, af.polars[0].cl, label='3D')
    # plt.xlim([-5, 20])
    # plt.ylim([-0.5, 2.0])
    # plt.xlabel('$\\alpha$')
    # plt.ylabel('$c_l$')
    # plt.legend(loc='upper left').get_frame().set_alpha(0.0)
    # # plt.legend(loc='upper left')
    # plt.subplots_adjust(left=0.17)

    # plt.savefig('/Users/sning/Desktop/cl.pdf', transparent=True)


    # plt.figure(2)
    # plt.plot(af.x, af.yu, 'black')
    # plt.plot(af.x, af.yl, 'black')
    # plt.axes().set_aspect('equal')
    # plt.box('off')
    # plt.axes().get_yaxis().set_visible(False)
    # plt.axes().get_xaxis().set_visible(False)
    # plt.savefig('/Users/sning/Desktop/af.pdf', transparent=True)



    #af.writeToAerodynFile('bleh')

    # import matplotlib.pyplot as plt
    # # plt.plot(af2.x, af2.yu)
    # # plt.plot(af2.x, af2.yl)
    # plt.plot(af.polars[0].alpha, af.polars[0].cl)
    # plt.figure(2)
    # plt.plot(af.polars[0].alpha, af.polars[0].cd)
    #plt.show()


