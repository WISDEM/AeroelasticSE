# runTurbSim.py
# 2013 12 17

# TurbSim model - called by ???
# Runs TurbSim
#   - does not use OpenMDAO

import sys, os
import numpy as np
import subprocess
import platform


class runTurbSim(object):
    """ A class for running TurbSim """

    # ------- setup location of bin ----------
    TS_DIR = os.path.dirname(os.path.realpath(__file__))
    TS_BIN = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin')
    isWindows = False

    if platform.system() == 'Windows':
        TS_BIN = os.path.join(TS_BIN, 'nt') 
        DIR_NAME = 'nt'
        tsexe = 'TurbSim64.exe'
        isWindows = True
    elif platform.system() == 'Darwin':
        TS_BIN = os.path.join(TS_BIN, 'osx')
        tsexe = 'TurbSim_glin64'
        DIR_NAME = 'osx'
    elif platform.system() == 'Linux':
        TS_BIN = os.path.join(TS_BIN, 'linux')
        DIR_NAME = 'linux'
        tsexe = 'TurbSim_glin64'
    # ---------------------------------------

    template_dir = os.path.join(TS_DIR, "InputFilesToWrite")
    template_file = os.path.join(template_dir, 'turbsim_template.inp')  ## default, for testing.  should be set by caller.
    runname = 'turbsim_test.inp'
    tsDict = {}

    def write_inputs(self):
        self.readTemplate()
        self.writeInput()

    def readTemplate(self):
        """ read **TurbSim** input file and save lines """

        fname = self.template_file
        print "trying to open ", fname
        try:
            self.lines_inp = file(fname).readlines()
        except:
            sys.stdout.write ("Error opening %s" % fname)
            return 0

    def writeInput(self):
        try:
            ofh = open(self.runname,'w')
        except:
            sys.stdout.write ("Error opening %s\n" % self.runname)
            return 0

        for line in self.lines_inp:
            if (line.startswith('---')):
                ofh.write(line)
                continue

            flds = line.strip().split()

            """ If the second field in the line is present in the dictionary,
                  write the new value
                Otherwise
                  write the original line """

            if (len(flds) > 1 and flds[1] in self.tsDict):
                f0 = '{:.2f}    '.format(self.tsDict[flds[1]])
                oline = ' '.join([f0] + flds[1:])
                ofh.write(oline)
                ofh.write('\n')
            else:
                ofh.write(line)

        ofh.close()
        return 1

    # the real execute (no args)
    def execute(self):
        """ use subprocess to run **TurbSim**

        Returns
        -------
        ret : integer
            return code from subprocess.call()
        """

        self.write_inputs()  ## assumes self.tsDict already set
        
        ffname = os.path.join(self.TS_BIN,self.tsexe)
        if (not os.path.exists(ffname)):
            sys.stderr.write("Can't find TurbSim executable: {:}\n".format(ffname))
            return 0
        print "calling ", ffname
        print "input file=", self.runname
        ret = subprocess.call([ffname, self.runname] )
        return ret

    def set_dict(self, ts_dict):
        self.tsDict = ts_dict

if __name__=="__main__":
    ts = runTurbSim()
    ws = 12.34
    tmax = 2
    ts.set_dict({"URef": ws, "AnalysisTime":tmax, "UsableTime":tmax})
    ts.execute()

