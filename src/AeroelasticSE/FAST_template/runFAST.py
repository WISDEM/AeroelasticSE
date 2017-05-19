# runFAST.py
# 2012 10 30

"""
This file implements a python wrapper for the aeroelastic code `FAST <https://wind.nrel.gov/designcodes/simulators/fast/>`_, 
from the National Renewable Energy Lab's
National Wind Technology Center.

The approach used here is that of "template-based" input files.  That is, the user supplies a working set of
FAST input files.  These are parsed into python dictionaries by the wrapper.  The user is then free to modify 
any of the values in the python dictionary representation of the FAST inputs.  Then these are written
back to files, and FAST is executed using them.  This approach provides a python-programmatic interface to
FAST that is a very short step from the normal usage of FAST.  It is thus a very easy first step into
programmatically driving FAST.

This code does not use `openMDAO <http://openmdao.org>`_.
The other code WISDEM/fusedwind code that uses FAST _and_ openMDAO _calls_ to this code.

"""

# Format for numpydoc style comments:
#       Parameters
#        ----------
#        alpha : float (rad)
#            angle of attack
#        Re : float
#            Reynolds number
#
#        Returns
#        -------
#        cl : float
#            lift coefficient
#        cd : float
#            drag coefficient
#
#        Notes
#        -----
#        This method uses a spline so that the output is continuously differentiable, and
#        also uses a small amount of smoothing to help remove spurious multiple solutions.



import sys, os, re, shutil
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

def unsplit(f):
    """ join a list of strings, adds a linefeed """
    ln = ""
    for s in f:
        ln = "%s %s" % (ln, s)
    ln = ln + "\n"
    return ln

def fix_path(name):
    """ split a path, then reconstruct it using os.path.join """
    saveslash = "/" if (name[0] == "/") else ""
    name = re.split("\\\|/", name)
    new = name[0]
    for i in range(1,len(name)):
        new = os.path.join(new, name[i])
    new = "%s%s" % (saveslash, new)
    return new

#-----------------------------------------

class runFAST(object):
    """ A class for running FAST from openMDAO

    The class itself is independent of openMDAO, but an object of
    type *runFAST* is the model within a `FAST_component`.

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
    ## these need to be supplied:
    fst_exe = None
    fst_file = None
    fst_dir = None
    run_dir = None

    ## these should be supplied
    fst_file_type = None
    fst_exe_type = None
#ala Katherine's:    fst_file_type = Enum(0, (0,1),iotype='in', desc='Fst file type, 0=old FAST, 1 = new FAST')    


    def __init__(self):
        """ Initialization of a runFAST object, sets various file names to None
        """
        self.fstDict = {}

        self.output_list = None

    ## these should be supplied
        self.fst_file_type = 0  # 0:v7.01 file, 1:v7.02 file
        self.fst_exe_type = 1 # 0:v7.01 exe, v7.02 exe
#ala Katherine's:    fst_file_type = Enum(0, (0,1),iotype='in', desc='Fst file type, 0=old FAST, 1 = new FAST')    

        ## new way: basic assumption is that .fst file is self contained, ie we could just run FAST on it. 
        #read everything from templates, modify them selectively, then write them back out in "run_dir"
        self.ptfm_file = None
        self.twr_file = None
        self.adams_file = None
        self.blade1_file = None
        self.blade2_file = None
        self.blade3_file = None
        self.ad_file = None
        self.noise_file = None

        self.wamit_path = None
        self.wind_file = None
                    
        self.exec_count = 0

        # we need to ensure the template file are not overwritten.  run_dir can't be same as fst_dir
        self.run_dir = 'run_dir'
        

    #---------------------------
    def getBin(self):
        """ Get the name of the FAST executable """
        return self.fst_exe

    def getafNames(self):
        """ Get the names of the airfoil files parsed out of the FAST input deck """
        names = [self.af_dict['polar_files'][i] for i in range(len(self.af_dict['polar_files']))]
        return names

    def computeMaxPower(self):
        """ Compute and store the maximum value of RotPwr (mainly for testing). Subsequently fetched by
        `getMaxPower`
        """
        self.max_power = max(self.getOutputValue("RotPwr"))

    def getMaxPower(self):
        """ retrieve self.max_power (mainly for testing).
         note: we have to assume self.max_power is already set, because we might be grabbing it at the end of a bunch of 
         runs that have since overwritten the output file corresponding to this object
         """
        return self.max_power

    #---------------------------

    
    def set_wind_file(self,wind_file):
        """ set the name of the wind file """
        self.wind_file = wind_file
    def setFastFile(self,fname):
        """ set the name of the FAST (.inp) input file """
        self.fst_file = fname
    def setOutputs(self, output_list):
        """ set the list of which FAST "sensors" to include in output results """
        self.output_list = output_list
    def set_dict(self, fst_dict):
        """ set the main FAST key/value dictionary that will augment properties in the given input file deck """
        self.fstDict = fst_dict
        

    def read_inputs(self):
        """ read from template files, calls readFST, readNoise, readAD, readBlade, and readPtfm """
        curdir = os.getcwd()
        os.chdir(self.fst_dir)
        rstat = self.readFST()
        if rstat == 0:
            os.chdir(curdir)
            return 0
        # the names of the next files are either set by caller or come from the reading the FAST file
        rstat = self.readNoise()
        rstat = self.readAD()
        rstat = self.readBlade()
        rstat = self.readPtfm()
        os.chdir(curdir)

    def write_inputs(self, extraFstDict={}):
        """ writes the <xxx>.fst file and associated files

        self.run_dir will be created if it does not exist.
        This function will first read the inputs, then apply the entries in self.fstDist and the optional argument
        extraFstDict, then write the input files in self.run_dir.

        This function is called by self.execute immediately prior to the actual FAST run.
        """

        if (self.run_dir == self.fst_dir):
            raise ValueError, "run_dir == fst_dir, you cannot run directly in the template directory"

        self.run_name, ext = os.path.splitext(self.fst_file)

        if (not os.path.isdir(self.run_dir)):
            os.mkdir(self.run_dir)

        self.fst_dir = os.path.abspath(self.fst_dir)

        if (self.exec_count <= 1): # Is 0 when invoked by main()
                                   # Is 1 when invoked by Assembly ???
            self.read_inputs()

        for key in extraFstDict:
            self.fstDict[key] = extraFstDict[key]

        curdir = os.getcwd()
        os.chdir (self.run_dir)  ###note, change to run_dir

        self.writeFST(self.fst_file,self.fstDict) 
        self.writeAD()
        self.writeBlade()
        self.writeWnd()
        self.writeNoise()
        self.writePtfm(self.fstDict)
        self.copyTwr()
        self.copyAdams()

        os.chdir(curdir) ## restore dir

    # the real execute (no args)
    def execute(self):
        """ use subprocess to run **FAST**
        Calls write_input first (which calls read input), which applies new parameters by key/values in
        self.fst_dict.

        Returns return code from subprocess.call()
        """

        self.write_inputs()
        
        if (not os.path.exists(self.fst_exe)):
            sys.stderr.write("Can't find FAST executable: {:}\n".format(self.fst_exe))
            return 0
        print "calling FAST:", self.fst_exe
        print "input file=", self.fst_file
        curdir = os.getcwd()
        os.chdir (self.run_dir)  ###note, change to run_dir
#        faststdout = file("FAST.stdout", "w")
#        ret = subprocess.call([self.fst_exe, self.fst_file], stdout=faststdout ) #### actual call to FAST !! 
        ret = subprocess.call([self.fst_exe, self.fst_file]) #### actual call to FAST !! 
#        faststdout.close()
        os.chdir(curdir) ## restore dir

        return ret

    #---------------------------

    def getSPL(self):
        """ Extract and return the maximum sound pressure level from noise output file (.spl)
        
        Returns maxspl : float,
            largest value of SPL found in noise output file
        """

        fname = os.path.join(self.run_dir,self.run_name + '.spl')
        if (not os.path.exists(fname)):
            sys.stderr.write ('getMaxSPL: {:} does not exist\n'.format(fname))
            return None

        spl = myloadtxt(fname,skiprows=9)
        maxspl = np.amax(spl[:,2:])
        return maxspl

    

    #---------------------------
    def getRotPwr(self):
        """ get max rotor power from output (mainly for testing) """
        out = self.getOutputValue("RotPwr")
        pwr = max(out)
        return pwr

    #---------------------------

    def parseFASTout(self, directory = None):
        """ reads the FAST output file (.out) into a numpy array.  Returns

        - hdr: list of fields in the output
        - out: table of values over time """
        fname = self.run_name + '.out'
        if directory == None:
            fname = os.path.join(self.run_dir, fname)
        else:
            fname = os.path.join(directory, fname)
        if (not os.path.exists(fname)):
            sys.stderr.write ('parseFASTout: {:} does not exist\n'.format(fname))
            return None
        
        fin = file(fname)
        for i in range(6):
            fin.readline() ## skip
        hdr = fin.readline().strip().split()
        fin.close

        # let numpy do the rest
        warmup = 0  ## also skip this many outputs, so np.loadtxt doesn't complain about "*****" entries in Fortran output 
                      #(but why are they there?)  ### this should not happen, means your FAST input/FAST version are out of whack
        out = myloadtxt(fname,skiprows=8+warmup)  # (8 is lines before data starts)
        return hdr, out


    #---------------------------

    def getMaxOutputValue(self, paramname, directory=None, out=None, hdr=None):
        """ gets maximum value of an output sensor.  See :py:meth:`getOutputValue` """
        col = self.getOutputValue(paramname, directory, out, hdr)
        val = max(col)
        return val

    def getMaxOutputValueStdDev(self, paramname, directory=None, out=None, hdr=None):
        """ gets standard deviation of an output sensor.  See :py:meth:`getOutputValue` """
        col = self.getOutputValue(paramname, directory, out, hdr)
        try:
            val = np.std(col)
        except:
            val = None
        return val

    def getOutputValue(self, paramname,  directory=None, out=None, hdr=None):
        """ gets output value (whole time series) of a particular FAST sensor.
        Arguments:

        - paramname: sensor of interest
        - directory (optional): where output lives
        - out (optional): table of pre-read output (will not reparse from file in this case)
        - hdr (optional): list of sensorsin out; must be given also if out is given
        """
        if out == None:
            hdr, out = self.parseFASTout(directory)
            if (out == None):
                fname = self.runname + '.out'
                sys.stderr.write("output param %s does not exist in %s\n" % (paramname, fname))
                raise Exception

        # out contains header info. find our guy, then give back the whole column
        for i in range(len(hdr)):
#            print "hdr_i , paramname", hdr[i].strip(), paramname
            if hdr[i].strip() == paramname:
                out = out[:,i]
                return out
        print  "param %s not found in output" % paramname
        raise Exception


    def getMaxOutputValues(self, paramname, directory=None, out=None, hdr=None):
        """ gets maximum value of multiple output sensors in one call.  See :py:meth:`getOutputValues` """
        col = self.getOutputValues(paramname, directory, out, hdr)
        vals = []
        for i in range(len(col)):
            c = col[i]
            val = np.max(c)
            vals.append(val)
        return vals

    def getMaxOutputValueStdDevs(self, paramname, directory=None, out=None, hdr=None):
        """ gets standard deviations of multiple output sensors in one call.  See :py:meth:`getOutputValues` """
        col = self.getOutputValues(paramname, directory, out, hdr)
        vals = []
        for i in range(len(col)):
            c = col[i]
            try:
                val = np.std(c)
            except:
                val = None
            vals.append(val)
        return vals

    def getOutputValues(self, paramnames,  directory=None, out=None, hdr=None):
        """ gets output value (whole time series) of multiple FAST sensors in one call.
        Arguments:

        - paramnames: list of sensors of interest
        - directory (optional): where output lives
        - out (optional): table of pre-read output (will not reparse from file in this case)
        - hdr (optional): list of sensorsin out; must be given also if out is given
        """
        if out == None:
            hdr, out = self.parseFASTout(directory)  # throw exception if file not found

        # out contains header info. find our guy, then give back the whole column
        all_out = []
        foundme = [False for i in range(len(paramnames))]
        for j in range(len(paramnames)):
            for i in range(len(hdr)):
 #               print "hdr_i , paramname", hdr[i].strip(), paramnames
                if hdr[i].strip() == paramnames[j] and not foundme[j]:
#                    print "grabbing key: ", paramnames[j], hdr[i], i, j
                    out2 = out[:,i]
                    all_out.append(out2)
                    foundme[j] = True
        if (not all(foundme)):
            raise Exception, "params not found in output" + str(paramnames) + str(foundme)
        return all_out

    #---------------------------

    def readNoise(self):
        """ read noise input file and save lines in self.lines_noise """

        fname = self.noise_file
        print "reading noise file", fname
        try:
            fh = open(fname,'r')
            self.lines_noise = fh.readlines()
            fh.close()
        except:
            sys.stdout.write ("Error opening {:}\n".format(fname))
            return 0

    #---------------------------

    def readBlade(self):
        """ read blade input file and save lines in self.lines_blade"""

        fname = self.blade1_file  ## note, assuming they're all the same
        print "reading blade file ", fname
        try:
            fh = open(fname,'r')
            self.lines_blade = fh.readlines()
            fh.close()
        except:
            sys.stdout.write ("Error opening {:}\n".format(fname))
            return 0


    #---------------------------

    def readAD(self):
        """ read AD input file and save lines self.lines_ad.
        Note: in this function we also find and potentially modify the names of the airfoil files.
        The reason is that openmdao needs to be able to copy all relevant files to the run directory (for parallel runs).
        Also, for running on a mac using template created for windows, we need to fix the paths (and vice versa).
        """

        fname = self.ad_file
        print "reading ad file ", fname, " curdir = ", os.getcwd()
        try:
            fh = open(fname,'r')
            self.lines_ad = fh.readlines()
            fh.close()
        except:
            sys.stdout.write ("Error opening {:}\n".format(fname))
            return 0

        for i in range(len(self.lines_ad)):
            ln = self.lines_ad[i].split()            
            if (len(ln) >1):
                if (ln[1] == "NumFoil"):
                    self.nSeg = int(ln[0])
                    break
                if (ln[1] == "WindFile" and self.wind_file == None):
                    self.wind_file = ln[0][1:-1]
        self.af_dict = {}
        self.af_dict['polar_idx'] = [0]*self.nSeg
        self.af_dict['polar_files'] = [0]*self.nSeg
        print "ln, nSeg, i", ln, self.nSeg, i
        for j in range(self.nSeg):
            lnidx = i+1+j
            ln = self.lines_ad[lnidx].split()
            afpath = fix_path(ln[0].strip().strip("\"").strip("\'"))
            ln[0] = "\"%s\"" % afpath
            self.lines_ad[lnidx] = unsplit(ln)
            self.af_dict['polar_idx'][j] = j+1
            self.af_dict['polar_files'][j] = afpath

    #---------------------------

    def readPtfm(self):
        """ read platform input file and save lines in self.lines_ptfm.
        Also stores name of WAMITFile path in self.wamit_path."""

        fname = self.ptfm_file
        print "reading platform file from ", fname
        try:
            fh = open(fname,'r')
            self.lines_ptfm = fh.readlines()
            fh.close()
        except:
            sys.stdout.write ("Error opening {:}\n".format(fname))
            return 0

        for ln in self.lines_ptfm:
            ln = ln.split()
            if (len(ln) > 1 and ln[1] == "WAMITFile"):
                self.wamit_path = fix_path(ln[0][1:-1])

    #---------------------------

    def readFST(self):
        """ read main **FAST** input file and save lines in self.lines_fast.
        also save platform, tower, blade, aerodyne, and noise file names for future reference"""

        fname = self.fst_file
        print "reading FAST template file", fname
        try:
            fh = open(fname,'r')
            self.lines_fast = fh.readlines()
            fh.close()
        except:
            sys.stdout.write ("Error opening master FAST input file %s\n" % fname)
            return 0

        for line in self.lines_fast:
            f = line.lstrip().split()
            if (len(f) < 2):
                continue

            if (f[1] == 'PtfmFile' and self.ptfm_file == None):
                self.ptfm_file = f[0][1:-1]
            if (f[1] == 'TwrFile' and self.twr_file == None):
                self.twr_file = f[0][1:-1]
            if (f[1] == 'ADAMSFile' and self.adams_file == None):
                self.adams_file = f[0][1:-1]
            if (f[1] == 'BldFile(1)' and self.blade1_file == None):
                self.blade1_file = f[0][1:-1]
            if (f[1] == 'BldFile(2)' and self.blade2_file == None):
                self.blade2_file = f[0][1:-1]
            if (f[1] == 'BldFile(3)' and self.blade3_file == None):
                self.blade3_file = f[0][1:-1]
            if (f[1] == 'ADFile' and self.ad_file == None):
                self.ad_file = f[0][1:-1]
            if (f[1] == 'NoiseFile' and self.noise_file == None):
                self.noise_file = f[0][1:-1]
                
        print "FAST subfiles:"
        print "ptfm ", self.ptfm_file
        print "twr ", self.twr_file
        print "blades ", self.blade1_file, self.blade2_file, self.blade3_file
        print "ad ", self.ad_file
        print "noise ", self.noise_file

    #------------------------------------------------------------

    def writeWnd(self):
        """ Write the new hub-height wind file.
        WindFile can be in fstDict, that means we probably ran TurbSim and want to point to file we generated.
        Otherwise we just need the wind file the template is pointing at.  We won't rewrite it here.
        """
        if ("WindFile" in self.fstDict):
            src0 = self.fstDict["WindFile"]
        else:
            src0 = self.wind_file

        if not os.path.isabs(src0):
            src = os.path.join(self.fst_dir, src0)
            src = fix_path(src)  # deal with slashes
#            print "copying wind files, from->to", src, src0
            (head,tail) = os.path.split(src0)
            if not os.path.exists(head):
#                print "creating ", head
                os.mkdir(head)
            shutil.copyfile(src,src0)        
            

    #------------------------------------------------------------

    def writeNoise(self):
        """ Write the noise input file for potentially new tip radius and/or tower height
        uses info in self.fstDict        
        """

        if (self.noise_file == None or self.noise_file == ""):
            return
        ofname = self.noise_file
        ofh = open(ofname,'w')

        # these have to be there as long as we've read the FAST file already
        ## not true: we don't store these in the dict.
        have_data = False
        if ("TipRad" in self.fstDict and 'TowerHt' in self.fstDict and 'Twr2Shft' in self.fstDict):
            tiprad = self.fstDict['TipRad']
            towerht = self.fstDict['TowerHt']
            twr2shft = self.fstDict['Twr2Shft']
            have_data = True

        for line in self.lines_noise:
            if (have_data and line.find('Observer location') >= 0):
                xdist = -1.0 * (tiprad + (towerht + twr2shft))
                ofh.write('{:.1f} 0.0 0.0'.format(xdist))
                ofh.write('  (x,y,z) Observer location in tower-base coordinate system.  Use -(RotRad+HubHt)\n')
            else:
                ofh.write(line)
        ofh.close()

    #------------------------------------------------------------

    def writeBlade(self):
        """ Write the new blade file

        Parameters
        ----------

        """

        ofname = self.blade1_file  ### note, assuming they're all the same
        ofh = open(ofname,'w')

        for line in self.lines_blade:
            ofh.write(line)
        ofh.close()

    #------------------------------------------------------------

    def writePtfm(self, fstDict):
        """ Write the new platform file
        Parameters

        self.lines_ptfm are the unmodified lines of the platform file
        fstDict may contain location of WAMITFile, also may contain "PlatformDir" to change angle of platform
        """

        if self.ptfm_file == None:
            return
        ofname = self.ptfm_file
        ofh = open(ofname,'w')
#        print "writing platform file  ", ofname

#        for line in self.lines_ptfm:
#        for iln in range(len(self.lines_ptfm)):
        iln = 0
        while iln < len(self.lines_ptfm):

            line = self.lines_ptfm[iln]
            flds = line.strip().split()
#            print "copying line %d:" % iln, line

            """ If the second field in the line is present in the dictionary,
                  write the new value
                Otherwise
                  write the original line """
            if (len(flds) > 1 and flds[1] == 'WAMITFile'):
                ofh.write("\"%s\"   WAMITFile   location and root file name of WAMIT spar files\n" % self.wamit_path)
            elif (len(flds) > 1 and flds[1] == 'NumLines' and 'PlatformDir' in fstDict):
                # process/augment the mooring lines description IF our dict has a 'PlatformDir' entry #
                """
                ---------------------- MOORING LINES -------------------------------------------
                3        NumLines    - Number of mooring lines (-)
                1        LineMod     - Mooring line model {1: standard quasi-static, 2: user-defined from routine UserLine} (switch) [used only when NumLines>0]
                LRadAnch  LAngAnch  LDpthAnch  LRadFair  LAngFair   LDrftFair  LUnstrLen  LDiam   LMassDen  LEAStff    LSeabedCD  LTenTol [used only when NumLines>0 and LineMod=1]
                (m)       (deg)     (m)        (m)       (deg)      (m)        (m)        (m)     (kg/m)    (N)        (-)        (-)     [used only when NumLines>0 and LineMod=1]
                853.87     0.0     320.0      5.2         0.0      70.0       902.2      0.09    77.7066   384.243E6  0.0        0.0000001
                853.87   120.0     320.0      5.2       120.0      70.0       902.2      0.09    77.7066   384.243E6  0.0        0.0000001
                853.87   240.0     320.0      5.2       240.0      70.0       902.2      0.09    77.7066   384.243E6  0.0        0.0000001
                """
                
                
#                print "I am re-writing the mooring section"
                ptfm_dir = float(fstDict['PlatformDir'])
                nlines = int(flds[0])            
                for iskip in range(4):
                    # copy next 4 lines
                    line = self.lines_ptfm[iln+iskip]
#                    print "header line", line
                    ofh.write(line)  # NumLines,LineMod, labels, units
                iln += 4
                for irope in range(nlines):
                    # replace the angles by adding the input platform orientation
                    line = self.lines_ptfm[iln+irope]
#                    print "rope line", line
                    ln = line.split()
                    val = float(ln[1])
                    val += ptfm_dir
                    ln[1] = "%f"%val  ## see above, 2nd and 5th entries are the angles
                    val = float(ln[4])
                    val += ptfm_dir
                    ln[4] = "%f"%val
                    line  = ' '.join(ln) + "\n"
                    ofh.write(line)                     
                iln += nlines-1
#                print "wrote mooring iln = %d" % iln

            elif (len(flds) > 1 and flds[1] in fstDict):
                f0 = '{:.6f}    '.format(fstDict[flds[1]])
                oline = ' '.join([f0] + flds[1:])
                ofh.write(oline)
                ofh.write('\n')
            else:
                ofh.write(line)
            
            iln += 1 ## finally, increment the loop counter
            
        ofh.close()

        # make sure the wamit path exists:
        if (self.wamit_path != "" and self.wamit_path != None):
            tmp = self.wamit_path
            if not os.path.isabs(tmp):
                tmp = tmp.split("\\")
                tmp = tmp[0].split("/")[0]
                # tmp is now root of relative path to spar files, ie top of wamit path
                dst = tmp
                src = os.path.join(self.fst_dir, tmp)
                print "copying wamit files from ", src, "TO ", dst
                if (not os.path.isdir(dst)):
                    shutil.copytree(src, dst)
            


    #------------------------------------------------------------

    def copyTwr(self):
        """ just copy tower file, so far not changing it """
        # this is executing during write_input, so curdir is run_dir
        shutil.copyfile(os.path.join(self.fst_dir,self.twr_file), self.twr_file)

    def copyAdams(self):
        """ just copy "ADAMSFile" file, so far not changing it """
        # this is executing during write_input, so curdir is run_dir
        if self.adams_file != None:
            shutil.copyfile(os.path.join(self.fst_dir,self.adams_file), self.adams_file)

    #------------------------------------------------------------

    def writeAD(self):
        """ Write the new AeroDyn file and copy airfoil files to appropriate location if necessary
        """
        ofname = self.ad_file
        ofh = open(ofname,'w')

        for line in self.lines_ad:
            f = line.strip().split()
            if (len(f) > 1 and f[1] == 'WindFile'):
                if (self.wind_file != None):
                    f[0] = "\""+self.wind_file+"\""
                    line = unsplit(f)
            ofh.write(line)

        ofh.close()

        # now also copy relevant airfoil files, if path is relative
        tmp = self.af_dict['polar_files'][0]
        if not os.path.isabs(tmp):
            tmp = tmp.split("\\")
            tmp = tmp[0].split("/")[0]
            # tmp is now root of relative path to airfoils
            dst = tmp
            src = os.path.join(self.fst_dir, tmp)
            print "copying aerodata from ", src, "TO ", dst
            if (not os.path.isdir(dst)):
                shutil.copytree(src, dst)

        # copy of relevant wind file in separate function writeWnd

    #---------------------------

    def writeFST(self,ofname,fstDict):
        """ Write FAST input file (.inp) with substitutions for names in fstDict.
        Otherwise, only floating-point values can be substituted, and they are written to 2 decimal places.
        Parameters:

        - ofname: name of FAST file (newname.fst) to write
        - fstDict: dictionary containing new values which will override those found in self.lines_fast
        """
        try:
            ofh = open(ofname,'w')
        except:
            sys.stdout.write ("Error opening %s\n" % ofname)
            return 0


        # writing FAST input: If the second field in the line is present in the dictionary,
        # write the new value. Otherwise
        # write the original line.  special case for the file name fields """
        for iln in range(len(self.lines_fast)):
            line = self.lines_fast[iln]
            flds = line.strip().split()
            if (len(flds) >1 and flds[1] in ['PtfmFile','TwrFile','BldFile(1)','BldFile(2)','BldFile(3)', 'ADfile','NoiseFile']):
                # substituting possibly modified file names for subfiles
                if (flds[1] == 'PtfmFile'):
                    flds[0] = self.ptfm_file
                if (flds[1] == 'TwrFile'):
                    flds[0] = self.twr_file
                if (flds[1] == 'ADAMSFile'):
                    flds[0] = self.adams_file
                if (flds[1] == 'BldFile(1)'):
                    flds[0] = self.blade1_file
                if (flds[1] == 'BldFile(2)'):
                    flds[0] = self.blade2_file 
                if (flds[1] == 'BldFile(3)'):
                    flds[0] = self.blade3_file 
                if (flds[1] == 'ADfile'):
                    flds[0] = self.ad_file 
                if (flds[1] == 'NoiseFile'):
                    flds[0] = self.noise_file 
                flds[0] = "\"%s\"" % flds[0]  ## put the quote back on
                oline = ' '.join(flds)
                ofh.write(oline)
                ofh.write('\n')

            elif (len(flds)>1 and flds[1] in fstDict):
                # replacing this entry with something from fstDict
                f0 = '{:.2f}    '.format(fstDict[flds[1]])
                oline = ' '.join([f0] + flds[1:])
                ofh.write(oline)
                ofh.write('\n')

            elif (len(flds)>1 and flds[1] == "SumPrint"):
                # special case to deal with either V7.1 OR v7.2
                ofh.write(line)
                nextln = self.lines_fast[iln+1].split()
                if (self.fst_file_type == 0 and self.fst_exe_type == 1):
                    if nextln[1] != "OutFileFmt":  ## this check should not be necessary if fst_xxx_type are correct
                        ofh.write("1           OutFileFmt  - Format for tabular (time-marching) output file(s) (1: text file [<RootName>.out], 2: binary\n")        
                elif (self.fst_file_type == 1 and self.fst_exe_type == 0):
                    if nextln[1] != "OutFileFmt":  ## this check should not be necessary if fst_xxx_type are correct
                        # skip line 
                        iln += 1
            elif (len(flds) > 0 and flds[0] == "END"):
                # uh oh, better back up and write the outputs!
                if self.output_list != None:
                    for out in self.output_list:
                        ofh.write("\"%s\"\n" % out)
                ofh.write(line)
            else:
                # just write the line unmodified
                ofh.write(line)

        ofh.close()

        return 1

#---------------------------------

def example():
    """ A simple example of running FAST one time """
    fast = runFAST()
    fast.fst_exe = "/Users/pgraf/opt/windcode-7.31.13/build/FAST_glin64"

    case = 1
    if (case==1):
    #    fast.fst_dir = "/Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/FAST_VT/OC3_Files/"  ## either abs or rel path ok.
        fast.fst_dir = "ModelFiles/OC3_Files/"
        fast.fst_file = "NRELOffshrBsline5MW_Monopile_RF.fst"  ## should _not_ be full path, is in relation to fst_dir
    elif case == 2:
        fast.fst_dir = "/Users/pgraf/work/wese/fatigue12-13/from_gordie/SparFAST3.orig"
        fast.fst_file = "NRELOffshrBsline5MW_Floating_OC3Hywind.fst"
    elif case == 3:
        fast.fst_exe = "/Users/pgraf/opt/windcode-7.31.13/build/FAST_regular_glin64"
        fast.fst_dir = "ModelFiles/Noise_Files/"
        fast.fst_file = "NREL5MW_Monopile_Rigid.v7.02.fst"  
    else:
        print "unknown test case for runFAST.py"
        sys.exit()

    fast.run_dir = "new_run_dir"  ## either abs or rel path ok
#    fast.run_dir = "/Users/pgraf/work/wese/AeroelasticSE-1_3_14/src/AeroelasticSE/another_run_dir"


    ## all changes to FAST input params go through dict
    ## unless you want to change the name of the template for the sub-files (e.g. subst a different aerodyn file).  Those go through actual fields ("fast.ad_file")
    fast.fstDict['Vhub']=8.0
    fast.fstDict['RotSpeed'] = 12.03
    fast.fstDict['TMax'] = 2.0
    fast.fstDict['TStart'] = 0.0

    fast.fstDict['PlatformDir'] = 30.0

    fast.setOutputs(['RotPwr'])

    fast.execute()
    out = fast.getOutputValue("RotPwr")

    print fast
    print "max power"
    print max(out)

def turbsim_example():
    """ A simple example of first running `TurbSim`, then running FAST """ 
    # run TurbSim
    from runTurbSim import runTurbSim

    ts = runTurbSim()
    ts.ts_exe = "/Users/pgraf/opt/windcode-7.31.13/TurbSim/build/TurbSim_glin64"
    ts.run_dir = "turbsim_test_run"
    tscase = 2
    if (tscase == 1):
        ts.ts_dir = "TurbSimTest"
        ts.ts_file = "turbsim_template.inp"
    else:
        ts.ts_dir = "/Users/pgraf/work/wese/fatigue12-13/from_gordie/SparFAST3.orig/TurbSim"
        ts.ts_file = "TurbSim.inp"
        
    tmax = 12
    ws=20.0 # wind speed

    ts.set_dict({"URef": ws, "AnalysisTime":tmax, "UsableTime":tmax})
    ts.execute()

    # then run FAST
    fast = runFAST()
    fast.fst_exe = "/Users/pgraf/opt/windcode-7.31.13/build/FAST_glin64"
    case = 2
    if (case==1):
        fast.fst_dir = "FAST_VT/OC3_Files/"
        fast.fst_file = "NRELOffshrBsline5MW_Monopile_RF.fst" 
    elif case ==2:
        fast.fst_dir = "/Users/pgraf/work/wese/fatigue12-13/from_gordie/SparFAST3.orig"
        fast.fst_file = "NRELOffshrBsline5MW_Floating_OC3Hywind.fst"
    else:
        fast.fst_dir = "InputFilesToWrite/"
        fast.fst_file = "NREL5MW_Monopile_Rigid.v7.02.fst"

    fast.run_dir = "tsfast_test_run_dir"  ## either abs or rel path ok

    # here we link turbsim -> fast
    tswind_file = os.path.join(ts.ts_dir, "%s.wnd" % ts.run_name)
    fast.set_wind_file(os.path.abspath(tswind_file))

    fast.fstDict['Vhub']=ws
    fast.fstDict['RotSpeed'] = 12.03
    fast.fstDict["TMax"] = tmax
    fast.fstDict['TStart'] = 0.0

    fast.setOutputs(['RotPwr'])

    fast.execute()

    out = fast.getOutputValue("RotPwr")

    print "TurbSim example complete:"
    print "max power"
    print max(out)

def get_options():
    """ allows choosing just FAST example or TurbSim+FAST example """
    from optparse import OptionParser
    parser = OptionParser()    
    parser.add_option("-t", "--turbsim", dest="run_turbsim", help="run turbsim too", action="store_true", default=False)
    
    (options, args) = parser.parse_args()
    return options, args


if __name__=="__main__":
    """ simple main, just runs an example """
    options, args = get_options()
    
    if (not options.run_turbsim):
        example()
    else:
        turbsim_example()
