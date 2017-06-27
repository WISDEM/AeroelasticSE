"""
A basic python script that demonstrates how to use the FST8 reader, writer, and wrapper in a purely
python setting. These functions are constructed to provide a simple interface for controlling FAST
programmatically with minimal additional dependencies.
"""
# Hacky way of doing relative imports
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from FST8_reader import Fst8InputReader
from FST8_writer import Fst8InputWriter
from FST8_wrapper import Fst8Wrapper

reader = Fst8InputReader()   #Initialize reader
writer = Fst8InputWriter()   #Initialize writer
wrapper = Fst8Wrapper()   #Initialize wrapper

reader.fst_infile = 'Test01.fst'   #Master FAST file to base test on
reader.fst_directory = './FST8inputfiles/'   #Directory of master FAST file set
reader.ad_file_type = 1   #Enum(0, (0,1), desc='Aerodyn file type, 0=old Aerodyn, 1 = new Aerdyn')
reader.execute()

writer.fst_vt = reader.fst_vt   #Pass properties from reader to writer
writer.fst_infile = 'Test01_Case1.fst'   #Name for new .fst file
writer.fst_directory = './rundir/'   #Running directory
writer.execute()   #Write new files

wrapper.FSTexe = 'openfast'
#wrapper.libmap = '../../../../../FAST_v8/bin/libmap-1.20.10.dylib'
wrapper.FSTInputFile = writer.fst_infile
wrapper.fst_directory = writer.fst_directory
wrapper.execute()   #Execute actual FAST analysis
