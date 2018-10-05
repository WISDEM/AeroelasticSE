import pyts
import pyts.runInput.main as ptsm
import pyts.io.input as ptsin
from pyts.base import tsGrid
from pyts.phaseModels.main import Rinker, Uniform

from CaseGen_General import CaseGen_General, save_case_matrix

# class pyTurbsim_wrapper():
#     """ wrapper for py turbsim so we can mostly just plug it in """
#     def __init__(self):
#         import pyts
#         import pyts.runInput.main as ptsm
#         import pyts.io.input as ptsin
#         from pyts.base import tsGrid
#         from pyts.phaseModels.main import Rinker, Uniform

#         pass

#     def execute(self, IEC_WindType, U, rho):  ### Note rho is a new param.  maybe a dict as input would be better,
#         ### but that would mean changing pyIECWind, or at least adding a new function like "execute_dict()"
#         pass


class pyTurbsim_wrapper():
    """ a component to run TurbSim.
        will try to make it aware of whether the wind file already exists"""
    
    def create_tsr(self, rho, U, tmax, dt):
        tsr = api.tsrun()
        tsr.grid = api.tsGrid(center=10, ny=self.ny, nz=self.nz,
                              height=10, width=10, time_sec=tmax, dt=dt)
        tsr.prof = api.profModels.pl(U, 90)

        tsr.spec = api.specModels.tidal(self.ustar, 10)

        #tsr.cohere = api.cohereModels.nwtc()
        tsr.cohere = pyts.cohereModels.main.none()

        tsr.stress = api.stressModels.uniform(0.0, 0.0, 0.0)

        tsr.cohere = pyts.cohereModels.main.none()
        tsr.stress = pyts.stressModels.main.uniform(0,0,0)

        from pyts.phaseModels.main import Rinker, Uniform
        tsr.phase = Rinker(rho, self.mu)
        #tsr.phase = Uniform()
        # tsr.stress=np.zeros(tsr.grid.shape,dtype='float32')

        self.tsr = tsr
        return tsr


    def add_phase_dist(self, tsr, rho, tmax):
#        tsr.cohere = pyts.cohereModels.main.none()
        tsr.cohere = pyts.cohereModels.main.nwtc()
        tsr.stress = pyts.stressModels.main.uniform(0,0,0)
        tsr.phase = Rinker(rho, self.mu)
        cg = tsr.grid
        tsr.grid = tsGrid(center=cg.center, ny=cg.n_y, nz=cg.n_z,
                          height=cg.height, width=cg.width,
                          time_sec=tmax, dt=cg.dt)
        
        return tsr
        
    def __init__(self, filedict, inputs):
        super(runTurbSimpy,self).__init__()

        self.inputs

#        self.rawts.ts_exe = filedict['ts_exe']
        self.ts_dir = filedict['ts_dir']
        self.ts_file = filedict['ts_file']

        self.ustar = .8
##        self.U = 17.
        self.ny = 15
        self.nz = 15
        self.dt = 0.05  # these (should/have in past) come from TurbSim template file
        self.mid = self.nz/2

##        self.rho = 0.9999
        self.mu = np.pi

###        np.random.seed(1)  ## probably don't want this in this context

#        self.rawts.run_name = self.run_name


        self.basedir = os.path.join(os.getcwd(),"allts_runs")
        if 'run_dir' in filedict:
            self.basedir = os.path.join(os.getcwd(),filedict['run_dir'])
        if (not os.path.exists(self.basedir)):
            os.mkdir(self.basedir)

    def execute(self):
        case = self.inputs
        print "CASE", case
        ws=case['Vhub']
        rho = case['Rho']   #case.fst_params['rho'] ####### TODO: how does this get here?
        rs = case['RandSeed1'] if 'RandSeed1' in case else None
        tmax = 2  ## should not be hard default ##
        if ('TMax' in case):  ## Note, this gets set via "AnalTime" in input files--FAST peculiarity ? ##
            tmax = case['TMax']

        # run TurbSim to generate the wind:        
        # for now, turbsim params we mess with are possibly: TMax, RandomSeed, Tmax.  These should generate
        # new runs, otherwise we should just use wind file we already have
            # for now, just differentiate by wind speed
        ts_case_name = "TurbSim-Vhub%.4f" % ws
        if rs != None:
            ts_case_name = "%s-Rseed%d" % (ts_case_name, rs)

        run_dir = os.path.join(self.basedir, ts_case_name)
        if (not os.path.exists(run_dir)):
            os.mkdir(run_dir)

        self._logger.info("running TurbSim in %s " % run_dir)
        print "running TurbSim in " , run_dir
#        self.rawts.run_dir = run_dir
        tsdict = dict({"URef": ws, "AnalysisTime":tmax, "UsableTime":tmax}.items() + case.items())
#        self.rawts.set_dict(tsdict)
        print case
        tsoutname = self.ts_file.replace("inp", "wnd")  #self.rawts.ts_file.replace("inp", "wnd")
        tsoutname = os.path.join(run_dir, tsoutname)
        tssumname = tsoutname.replace("wnd", "sum")
        reuse_run = False
        if (False and os.path.isfile(tsoutname) and os.path.isfile(tssumname)):
            # maybe there's an old results we can use:
            while (not reuse_run):
                ln = file(tssumname).readlines()
                if (ln != None and len(ln) > 0):
                    ln1 = ln[-1] # check last line2 lines (sometimes Turbsim inexplicably writes a final blank line!)
                    ln1 = ln1.split(".")
                    ln2 = ln[-2] # check last line2 lines (sometimes Turbsim inexplicably writes a final blank line!)
                    ln2 = ln2.split(".")
                    if ((len(ln1) > 0 and ln1[0] == "Processing complete") or (len(ln2) > 0 and ln2[0] == "Processing complete")):
                        print "re-using previous TurbSim output %s for ws = %f" % (tsoutname, ws)
                        reuse_run = True
                if (not reuse_run):
                    time.sleep(2)
                    print "waiting for ", tsoutname
                    self._logger.info("waiting for %s" % tsoutname)
            self._logger.info("DONE waiting for %s" % tsoutname)
        
        if (not reuse_run):

            tsinput = ptsin.read(os.path.join(self.ts_dir, self.ts_file))
            tsr = ptsm.cfg2tsrun(tsinput)

            tsr = self.add_phase_dist(tsr, rho, tmax)
            #            tsdata=ptsm.run(tsinput)
            tsdata = tsr()  ## actually runs turbsim
            dphi_prob = tsr.phase.delta_phi_prob
            ptsm.write(tsdata, tsinput, fname=tsoutname)
            
            #fout = file("uhub.out", "w")
            #hubdat = tsdata.uturb[0, self.mid, self.mid, :]
            #for i in range(len(hubdat)):
            #    fout.write("%d  %e  %e\n" % ( i, tsdata.time[i], hubdat[i]))
            #fout.close()
            print "dphi prob is ", dphi_prob
            fout = file(os.path.join(run_dir, "delta_phis_prob.out"), "w")
            fout.write("%e\n" % dphi_prob)
            fout.close()
            
#            tsr = self.create_tsr(rho, ws, tmax, self.dt)
#            tsdat = tsr()
#            print "writing data to ", tsdat, tsoutname
#            tsdat.write_bladed(tsoutname)
            ### check for errors!!?? ###
            
        # here we link turbsim -> fast
        self.tswind_file = tsoutname
        self.tswind_dir = run_dir


if __name__ == "__main__":

    case_inputs = {}
    case_inputs[("TMax")] = {'vals':[10.], 'group':0}
    case_inputs[("Vhub")] = {'vals':[10., 11., 12.], 'group':1}
    case_inputs[("Rho")] = {'vals':[1.2, 1.25, 1.3], 'group':1}
    case_inputs[("RandSeed1")] = {'vals':[123,234], 'group':2}    
    case_list, case_name = CaseGen_General(case_inputs, dir_matrix='', namebase='pyTurbsim_testing')

    filedict = {}

    for case in case_list:
        pyturb = pyTurbsim_wrapper(filedict, case) # initialize runner with case variable inputs
        pyturb.ny = 20 # example of changing an attribute
        pyturb.execute() # run

        tswind_file = self.tswind_file
        tswind_dir = self.tswind_dir
