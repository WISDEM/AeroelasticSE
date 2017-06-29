import os
import subprocess
class Turbsim_wrapper(object):
    def __init__(self):
         self.turbsim_exe = 'turbsim'
         self.turbsim_input = './turbsim_default.in'
         self.run_dir = '.'
    def execute(self):
         exec_string = [self.turbsim_exe, self.turbsim_input]
         print 'Exectuing ', exec_string, ' in ',self.run_dir
         olddir = os.getcwd()
         os.chdir(self.run_dir)
         subprocess.call(exec_string)
         os.chdir(olddir)
if __name__=='__main__':
    wrapper = Turbsim_wrapper()
    wrapper.turbsim_exe = '/Users/jquick/SE/TurbSim/bin/TurbSim_glin64'
    wrapper.execute()
