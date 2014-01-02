# runFAST.py
# 2012 10 30

# FAST model - called by FAST_component
# Runs FAST
#   - does not use OpenMDAO

import sys, os
import numpy as np
import subprocess
import platform

#-----------------------------------------

def myloadtxt(fname, skiprows = 0):
    """ like np.loadtxt, but handles stuff that can't be converted to a float """
    fin = file(fname)
    for i in range(skiprows):
        fin.readline()
    ln = fin.readline()
    lns = []
    while (ln != ""):
        thisln = []
        ln = ln.strip().split()
        for s in ln:
            try:
                f = float(s)
            except:
                f = None
            thisln.append(f)
        lns.append(thisln)
        ln = fin.readline()
    return np.array(lns)

def unstrip(f):
    ln = ""
    for s in f:
        ln = "%s %s" % (ln, s)
    ln = ln + "\n"
    return ln
#-----------------------------------------

class runFAST(object):
    """ A class for running FAST from openMDAO

    The class itself is independent of openMDAO, but an object of
    type *runFAST* is the model within a `FAST_component`.

    Parameters
    ----------
    geometry : dictionary
        Geometry dictionary as defined in the WTPerf class
    atm : dictionary
        Atmosphere dictionary as defined in the WTPerf class

    Attributes
    ----------
    fastexe : str
        Name of FAST executable
    fastpath : str
        Absolute path of folder containing FAST executable
    template_path : str
        Absolute path of folder containing template files
    model_path : str
        Absolute path of folder containing model files (TwrFile and PtfmFile)

    """

    # ------- setup location of bin ----------
    FAST_DIR = os.path.dirname(os.path.realpath(__file__))
    FAST_BIN = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin')
    isWindows = False

    if platform.system() == 'Windows':
        FAST_BIN = os.path.join(FAST_BIN, 'nt') 
        DIR_NAME = 'nt'
        fastexe = 'FAST_v7.01.00a-bjj_AeroDyn_v13.00.01a-bjj_BladedDLLInterface.exe'
        isWindows = True
        template_file = 'NREL5MW_Monopile_Rigid.fst' # kld 'NREL5MW_Monopile_Rigid.v7.01.fst'
        noise_template = 'Noise.ipt' # kld 'Noise.v7.01.ipt'
    elif platform.system() == 'Darwin':
        FAST_BIN = os.path.join(FAST_BIN, 'osx')
        fastexe = 'FAST_glin64'
        DIR_NAME = 'osx'
        template_file = 'NREL5MW_Monopile_Rigid.v7.02.fst'
        noise_template = 'Noise.v7.02.ipt'
    elif platform.system() == 'Linux':
        FAST_BIN = os.path.join(FAST_BIN, 'linux')
        DIR_NAME = 'linux'
    # ---------------------------------------


    SCRATCH_DIR = 'fst_scratch' + os.path.sep
    #basefilename = SCRATCH_DIR + 'fast'

    # fastpath/fastexe : fast executable
    # template_path : folder containing fast_file, ad_file, blade_file, noise_file
    # model_path : folder containing tower file, platform file,

    # kld 10/22/2013 - fix below from Peter on machine dependency has issues with windows \/
    #fastpath = FAST_BIN
    #model_path = os.path.join(FAST_DIR,'ModelFiles/')
    #template_path = os.path.join(FAST_DIR,"InputFilesToWrite/")
    #print "template_path=", template_path
### beware windows-python path wierdness: after numbers(?), apparantly "\" as separator is NOT ok. ###

    # kld 10/22/2013 - using these till fix is implemented
    fastpath = 'C:/Python27/openmdao-0.7.0/twister/models/FAST/FASTexe'  # todo: machine specific
    fastexe = 'FAST_v7.01.00a-bjj_AeroDyn_v13.00.01a-bjj_BladedDLLInterface.exe'
    template_path = 'C:/Python27/openmdao-0.7.0/twister/models/FAST/InputFilesToWrite/'
    model_path = 'C:/Python27/openmdao-0.7.0/twister/models/FAST/ModelFiles/'


    def __init__(self, geometry=None, atm=None, debug=False):
        """ Initialization of a runFAST object

        """

        # initialize some internal variables

        self.debug = debug

        self.lines_noise = ()
        self.lines_blade = ()
        self.lines_ad = ()
        self.lines_fast = ()
        self.noise_file = self.noise_template
        self.noise_outfile = 'Noise.ipt'
        self.blade_file = 'NREL5MW_Blade.dat'
        self.ad_file    = 'NREL5MW.ad'
        self.fast_file  = self.template_file
        self.wind_file = None ## can be set by user, in which case that gets substituted

        self.fstDict = {}

        self._rotorR = 50.0
        self.towerht = 0.0
        self.twr2shft = 0.0

        # Create scratch directory for airfoil files

        if not os.path.isdir(self.SCRATCH_DIR):
            os.makedirs(self.SCRATCH_DIR)
            sys.stderr.write('Created folder {:}\n'.format(self.SCRATCH_DIR))

        self.atm = atm
        if atm is not None:
            self.rho = atm['rho']

        self.geometry = geometry
        if geometry is not None:
            self.setFromGeometry(geometry)
        else:
            sys.stderr.write("Trying to initialize runFAST without geometry\n")
            exit()

        self.exec_count = 0

        self.runname = 'test'


    #---------------------------

    def __str__(self):
        """ default print routine for runFAST """

        s = 'runFAST object\n  FAST: {:}/{:}\n'.format(self.fastpath,self.fastexe)
        s += '  Template path: {:}\n'.format(self.template_path)
        s += '    Fast file: {:}\n'.format(self.fast_file)
        s += '    AD file: {:}\n'.format(self.ad_file)
        s += '    Blade file: {:}\n'.format(self.blade_file)
        s += '    Noise file: {:}\n'.format(self.noise_file)
        s += '  Model path: {:}\n'.format(self.model_path)
        return s

    #---------------------------

    def setFromGeometry(self, geometry):
        """ set runFAST properties based on geometry dictionary

        Parameters
        ----------
        geometry : dictionary
            Geometry dictionary as defined in the WTPerf class
        """

        if geometry['endPoints']:

            # WT curve uses centered points
            r_full = np.array(geometry['r'])
            c_full = np.array(geometry['chord'])
            t_full = np.array(geometry['theta'])
            af_full = geometry['polars']

            self.r = 0.5*(r_full[0:-1] + r_full[1:])
            self.chord = np.interp(self.r, r_full, c_full)
            self.theta = np.interp(self.r, r_full, t_full)
            self.hubR = r_full[0]
            self._rotorR = r_full[-1]
            self.airfoilArray = [0]*len(self.r)
            for i in range(len(self.r)):
                self.airfoilArray[i] = af_full[i].blend(af_full[i+1], 0.5)

        else:
            self.r = np.array(geometry['r'])
            self.chord = np.array(geometry['chord'])
            self.theta = np.array(geometry['theta'])
            self.hubR = geometry['hubR']
            self._rotorR = geometry['rotorR']
            self.airfoilArray = geometry['polars']

        self.tiprad = self._rotorR

        # save some of the variables we need for post-processing
        #self.nSect = self.misc['NumSect']
        self.nSeg = len(self.r)

        self.af_dict = {}
        self.af_dict['polar_idx'] = [0]*self.nSeg
        self.af_dict['polar_files'] = [0]*self.nSeg

        # data needed for 3d corrections (not used if 3d data input)
        c75 = np.interp(0.75*self._rotorR, self.r, self.chord)
        tsr_point = 8

        # interpolate to center points and write to file
        print "My airfoil array"
        print self.airfoilArray
        for i, af in enumerate(self.airfoilArray):

            af.extend2DDataTo3DIfNecessary(self.r[i], self.chord[i], c75, self._rotorR, tsr_point)

            fname = self.SCRATCH_DIR + str(i) + '.af'
##            af.writeToAerodynFile(fname, mode=1)
            af.writeToAerodynFile(fname, mode=2)
## (PG, 7-19-13) added a new mode to writeToAerodynFile() to write AF files that FAST likes, but coming from Andrew's default AFs ##
            self.af_dict['polar_idx'][i] = i+1
            self.af_dict['polar_files'][i] = fname

    #---------------------------

    
## setters
    def set_ws(self,ws):
        self.ws = ws
    def set_rpm(self,rpm):
        self.rpm = rpm
    def set_wind_file(self,wind_file):
        self.wind_file = wind_file

    # the real execute (no args)
    def execute(self):
        """ writes the *xxx.fst* file and uses subprocess to run **FAST**

        Parameters
        ----------
        ws : float
           Wind speed for **FAST** run

        Returns
        -------
        ret : integer
            return code from subprocess.call()
        """

        if (self.exec_count <= 1): # Is 0 when invoked by main()
                                   # Is 1 when invoked by Assembly ???
            rstat = self.readFST()
            if rstat == 0:
                return 0
            rstat = self.readNoise()
            rstat = self.readAD()
            rstat = self.readBlade()

        in_fst = self.runname + '.fst'
        self.writeFST(in_fst,self.fstDict,self.rpm) #todo - append rpm to dict?

        self.writeAD()
        self.writeBlade()
        self.writeWnd(self.ws)
        self.writeNoise()

        ffname = '/'.join([self.fastpath,self.fastexe])
        if (not os.path.exists(ffname)):
            sys.stderr.write("Can't find FAST executable: {:}\n".format(ffname))
            return 0
        print "calling ", ffname
        print "input file=", in_fst
        ret = subprocess.call([ffname, in_fst] )
        return ret

    #---------------------------

    def getSPL(self):
        """ Extract and return the maximum sound pressure level from noise output file

        Returns
        -------
        maxspl : float
            largest value of SPL found in noise output file
        """

        fname = self.runname + '.spl'
        if (not os.path.exists(fname)):
            sys.stderr.write ('getMaxSPL: {:} does not exist\n'.format(fname))
            return None

        spl = myloadtxt(fname,skiprows=9)
        maxspl = np.amax(spl[:,2:])
        return maxspl

    

    #---------------------------
    def getRotPwr(self):
        out = self.getOutputValue("RotPwr")
        pwr = max(out)
        return pwr

    #---------------------------

    def parseFASTout(self):
        fname = self.runname + '.out'
        if (not os.path.exists(fname)):
            sys.stderr.write ('parseFASTout: {:} does not exist\n'.format(fname))
            return None
        
        fin = file(fname)
        for i in range(6):
            fin.readline() ## skip
        hdr = fin.readline().strip().split()
        fin.close

        # let numpy do the rest
        warmup = 30  ## also skip this many outputs, so np.loadtxt doesn't complain about "*****" entries in Fortran output 
                      #(but why are they there?)
        out = myloadtxt(fname,skiprows=8+warmup)  # (8 is lines before data starts)
        return hdr, out


    #---------------------------

    def getOutputValue(self, paramname, out=None, hdr=None):
        if out == None:
            hdr, out = self.parseFASTout()
            if (out == None):
                fname = self.runname + '.out'
                sys.stderr.write("output param %s does not exist in %s\n" % (paramname, fname))
                raise Exception

        # out contains header info. find our guy, then give back the whole column
        for i in range(len(hdr)):
            if hdr[i].strip() == paramname:
                out = out[:,i]
                return out
        raise Exception, "param %s not found" % paramname

    #---------------------------

    def readNoise(self):
        """ read noise input file and save lines """

        fname = self.template_path + self.noise_file
        print "trying to open", fname
        try:
            fh = open(fname,'r')
            self.lines_noise = fh.readlines()
            fh.close()
            if self.debug:
                sys.stdout.write('Read {:d} lines from {:}\n'.format(len(self.lines_noise),fname))
        except:
            sys.stdout.write ("Error opening {:}\n".format(fname))
            return 0

    #---------------------------

    def readBlade(self):
        """ read blade input file and save lines """

        fname = self.template_path + self.blade_file
        try:
            fh = open(fname,'r')
            self.lines_blade = fh.readlines()
            fh.close()
            if self.debug:
                sys.stdout.write('Read {:d} lines from {:}\n'.format(len(self.lines_blade),fname))
        except:
            sys.stdout.write ("Error opening {:}\n".format(fname))
            return 0


    #---------------------------

    def readAD(self):
        """ read AD input file and save lines """

        fname = self.template_path + self.ad_file
        try:
            fh = open(fname,'r')
            self.lines_ad = fh.readlines()
            fh.close()
            if self.debug:
                sys.stdout.write('Read {:d} lines from {:}\n'.format(len(self.lines_ad),fname))
        except:
            sys.stdout.write ("Error opening {:}\n".format(fname))
            return 0


    #---------------------------

    def readFST(self):
        """ read **FAST** input file and save lines """

        fname = self.template_path + self.fast_file
        print "trying to open ", fname
        print "template path = ", self.template_path
        try:
            fh = open(fname,'r')
            self.lines_fast = fh.readlines()
            fh.close()
            if self.debug:
                sys.stdout.write('Read {:d} lines from {:}\n'.format(len(self.lines_fast),fname))
        except:
            in_fst = self.runname + '.fst'
            sys.stdout.write ("Error opening {:}\n".format(in_fst))
            return 0

        for line in self.lines_fast:
            f = line.lstrip().split()
            if (len(f) < 2):
                continue
            #if (f[1] == 'TipRad'):
            #    self.tiprad = float(f[0])
            if (f[1] == 'RotSpeed'):
                self.rotspeed = float(f[0])
            if (f[1] == 'TowerHt'):
                self.towerht = float(f[0])
            if (f[1] == 'Twr2Shft'):
                self.twr2shft = float(f[0])

    #------------------------------------------------------------

    def writeWnd(self,ws,wshr=0.14):
        """ Write the new hub-height wind file

        Parameters
        ----------
        ws : float
            Wind speed for this **FAST** run
        wshr : float (optional)
            Wind shear exponent for this **FAST** run (defaults to 0.14)

        """

        ofname = 'HH_Rated.wnd'
        ofh = open(ofname,'w')
        ofh.write('{:5.1f}		{:4.1f}	0.0	0.0	0.0		{:4.2f}	0.0	0.0\n'.format(  0.0,ws,wshr))
        ofh.write('{:5.1f}		{:4.1f}	0.0	0.0	0.0		{:4.2f}	0.0	0.0\n'.format(999.9,ws,wshr))
        ofh.close()
        if self.debug:
            sys.stderr.write('Wrote file {:}\n'.format(ofname))

    #------------------------------------------------------------

    def writeNoise(self):
        """ Write the new noise file

        Parameters
        ----------

        """

        ofname = self.noise_file
        ofname = self.noise_outfile
        ofh = open(ofname,'w')

        for line in self.lines_noise:
            if line.find('Observer location') >= 0:
                #xdist = -1.0 * (self.tiprad + self.hubHt)
                xdist = -1.0 * (self.tiprad + (self.towerht + self.twr2shft))
                ofh.write('{:.1f} 0.0 0.0'.format(xdist))
                ofh.write('  (x,y,z) Observer location in tower-base coordinate system.  Use -(RotRad+HubHt)\n')
            else:
                ofh.write(line)
        ofh.close()
        if self.debug:
            sys.stderr.write('Wrote file {:}\n'.format(ofname))

    #------------------------------------------------------------

    def writeBlade(self):
        """ Write the new blade file

        Parameters
        ----------

        """

        ofname = self.blade_file
        ofh = open(ofname,'w')

        for line in self.lines_blade:
            ofh.write(line)
        ofh.close()
        if self.debug:
            sys.stderr.write('Wrote file {:}\n'.format(ofname))

    #------------------------------------------------------------

    def writeAD(self):
        """ Write the new AeroDyn file

        Parameters
        ----------

        """

        ofname = self.ad_file
        ofh = open(ofname,'w')

        for line in self.lines_ad:
            f = line.strip().split()
            if (f[1] == 'WindFile'):
                if (self.wind_file != None):
                    f[0] = "\""+self.wind_file+"\""
                    line = unstrip(f)
                    print "line=", line
            if (f[1] == 'NumFoil'):
                break
            ofh.write(line)

        # Write new blade/airfoil parameters

        ofh.write('  {:2d}    NumFoil - Number of airfoil files\n'.format(len(self.airfoilArray)))
        #for i, af in enumerate(self.airfoilArray):
        #    ofh.write('"{:}"'.format(af.name))
        AFFiles = self.af_dict['polar_files']
        for i in range(len(AFFiles)):
            ofh.write('"{:}"\n'.format(AFFiles[i]))

        # Compute properties of each blade segment

        inEdge  = [0] * len(self.r)
        outEdge = [0] * len(self.r)
        dr      = [0] * len(self.r)
        dr[0] = 2.0*(self.r[0]-self.hubR)
        inEdge[0] = self.hubR
        outEdge[0] = inEdge[0] + dr[0]
        i = 0
        #print "{:6.3f} {:.3f} {:6.3f} {:6.3f}".format(self.r[i], dr[i], inEdge[i], outEdge[i])

        for i in range(1,len(self.r)):
           dr[i] = (self.r[i] - outEdge[i-1]) * 2.0
           inEdge[i]  = outEdge[i-1]
           outEdge[i] = inEdge[i] + dr[i]
           #print "{:6.3f} {:.3f} {:6.3f} {:6.3f}".format(self.r[i], dr[i], inEdge[i], outEdge[i])

        if (abs(self._rotorR - outEdge[-1]) < 0.05):
            print "TipRad {:.3f} within tolerance of sum(dr[])".format(self._rotorR)
        else:
            print "\n*** Error in computing blade segments: TipR {:3f} != sum(dr) {:3f}\n".format(self._rotorR,outEdge[-1])

        # Write blade nodes to AD file

        ofh.write('  {:2d}        BldNodes    - Number of blade nodes used for analysis (-)\n'.format(self.nSeg))
        ofh.write('RNodes   AeroTwst  DRNodes  Chord  NFoil  PrnElm\n')

        for r, t, dr, c, a in zip(self.r, self.theta, dr, self.chord, self.af_dict['polar_idx']):
#            ofh.write('{0!s:9} {1!s:9} {2!s:9} {3!s:9} {4!s:5} {5:9}\n'.format(r, t, dr, c, a, 'PRINT'))
            ofh.write('{0!s:9} {1!s:9} {2!s:9} {3!s:9} {4!s:5} {5:9}\n'.format(r, t, dr, c, a, 'NO'))

        ofh.close()
        if self.debug:
            sys.stderr.write('Wrote file {:}\n'.format(ofname))

    #---------------------------

    def writeFST(self,ofname,fstDict, rpm):
        """ write output file with substitutions for names in fstDict
            Only floating-point values can be substituted, and they are written to 2 decimal places.

        Parameters
        ----------
        ofname :
            name of FAST file (newname.fst) to write
        fstDict : dictionary
            dictionary containing new values which will override those found in self.lines_fast
        rpm :
            rotor speed for analysis

        """
        try:
            ofh = open(ofname,'w')
        except:
            sys.stdout.write ("Error opening %s\n" % ofname)
            return 0

        fstDict['TipRad'] = self._rotorR
        fstDict['HubRad'] = self.hubR
        fstDict['RotSpeed'] = rpm

        for line in self.lines_fast:
            if (line.startswith('---')):
                ofh.write(line)
                continue

            flds = line.strip().split()

            """ If the second field in the line is present in the dictionary,
                  write the new value
                Otherwise
                  write the original line """

            if (len(flds) > 1 and flds[1] in ['TwrFile','PtfmFile']):
                # add model_path to file names
                fn = flds[0].strip('"')
                fn = fn.strip("'")
                fn = '"' + self.model_path + fn + '"'
                oline = ' '.join([fn] + flds[1:])
                ofh.write(oline)
                ofh.write('\n')

            elif (len(flds) > 1 and flds[1] in fstDict):
                f0 = '{:.2f}    '.format(fstDict[flds[1]])
                oline = ' '.join([f0] + flds[1:])
                ofh.write(oline)
                ofh.write('\n')
                if self.debug:
                    sys.stderr.write('writeFST: {:} {:}\n'.format(f0, flds[1]))
            else:
                ofh.write(line)

        ofh.close()
        if self.debug:
            sys.stderr.write('Wrote {:d} lines to {:}\n'.format(len(self.lines_fast),ofname))

        return 1

#---------------------------------

def example():

    import mkgeom
    geometry, atm = mkgeom.makeGeometry()

    fast = runFAST(geometry, atm, debug=False)

    # fast.fastpath = 'abc' Could set the FAST path and executable here

    ws=8.0 # wind speed
    rpm = 12.03
    fast.set_ws(ws)
    fast.set_rpm(rpm)
    fast.execute()
    out = fast.getOutputValue("RotPwr")

    print fast
    print "max power"
    print max(out)

def turbsim_example():
    from runTurbSim import runTurbSim

    import mkgeom
    geometry, atm = mkgeom.makeGeometry()


    ts = runTurbSim()
    tmax = 12
    ws=20.0 # wind speed
    rpm = 12.03

    ts.set_dict({"URef": ws, "AnalysisTime":tmax, "UsableTime":tmax})
    ts.execute()

    fast = runFAST(geometry, atm, debug=False)
    fast.set_wind_file("turbsim_test.wnd")
    # fast.fastpath = 'abc' Could set the FAST path and executable here

    fast.set_ws(ws)
    fast.set_rpm(rpm)
    # set tmax
    fast.set_dict({"TMax": tmax})
    fast.execute()
    out = fast.getOutputValue("RotPwr")

    print "TurbSim example complete:"
    print fast
    print "max power"
    print max(out)

def get_options():
    from optparse import OptionParser
    parser = OptionParser()    
    parser.add_option("-t", "--turbsim", dest="run_turbsim", help="run turbsim too", action="store_true", default=False)
    
    (options, args) = parser.parse_args()
    return options, args


if __name__=="__main__":

    options, args = get_options()
    
    if (not options.run_turbsim):
        example()
    else:
        turbsim_example()