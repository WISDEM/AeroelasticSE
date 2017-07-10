import os
import sys
import subprocess
from shutil import copyfile
from openmdao.api import Component
from FST8_writer import Fst8InputWriter
from FST8_reader import Fst8InputReader
from FST_vartrees_params3 import FstModel

class Fst8ExternalCode(object):

    pass


class Fst8Wrapper(Component):

    def __init__(self):
        super(Fst8Wrapper, self).__init__()

        #self.FSTexe = None   #Path to executable
        #self.libmap = None   #Path to libmap library
        #self.FSTInputFile = None   #FAST input file (ext=.fst)
        #self.fst_directory = None   #Path to fst directory files
        FstModel(self, 'fst_vt')

    def solve_nonlinear(self, params, unknowns, resids):
        print "Executing FAST 8"
        #print params['fst_vt:fst_directory'] ; quit()
        self.input_file = os.path.join(params['fst_vt:fst_directory'], params['fst_vt:FSTInputFile'])

        #if (not os.path.exists(self.FSTexe)):
        #    sys.stderr.write("Can't find FAST executable: {:}\n".format(self.FSTexe))
        #    return 0
        #if (not os.path.exists(self.libmap)):
        #    sys.stderr.write("Can't find libmap dynamic library: {:}\n".format(self.libmap))
        #    return 0
        #else:
        #    print "Copying libmap to running directory\n"
        #    (head,tail) = os.path.split(self.libmap)
        #    copyfile(self.libmap, os.path.join(self.fst_directory, tail))

        print "Calling ", self.FSTexe 
        print "Input file = ", self.input_file

        # Get only tail of input_file (we are changing running directory)
        (head,tail) = os.path.split(self.input_file)

        # Construct absolute path of executable
        #fstexe_abs = os.path.join(os.getcwd(), self.FSTexe)
        fstexe_abs = self.FSTexe
        print "fstexe new: ", fstexe_abs

        exec_str = []
        exec_str.append(fstexe_abs)
        exec_str.append(tail)

        olddir = os.getcwd()
        os.chdir(self.fst_directory)
        print "current directory: ", os.getcwd()
        print "exec_str: ", exec_str
        subprocess.call(exec_str)#, stdin=None, stdout=None, stderr=None, shell=False)
        os.chdir(olddir)

if __name__=="__main__":

    pass
