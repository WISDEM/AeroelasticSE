from turbsim_vartrees import turbsiminputs

class turbsimReader(object):
    def __init__(self):
        self.turbsim_vt = turbsiminputs()
    def read_input_file(self, input_file_name):
        inpf = open(input_file_name, 'r')

        # Runtime Options
        inpf.readline()
        inpf.readline()
        inpf.readline()
        self.turbsim_vt.runtime_options.echo = inpf.readline()
        self.turbsim_vt.runtime_options.RandSeed1 = inpf.readline()
        self.turbsim_vt.runtime_options.RandSeed2 = inpf.readline()
        self.turbsim_vt.runtime_options.WrBHHTP = inpf.readline()
        self.turbsim_vt.runtime_options.WrFHHTP = inpf.readline()
        self.turbsim_vt.runtime_options.WrADHH = inpf.readline()
        self.turbsim_vt.runtime_options.WrADFF = inpf.readline()
        self.turbsim_vt.runtime_options.WrBLFF = inpf.readline()
        self.turbsim_vt.runtime_options.WrADTWR = inpf.readline()
        self.turbsim_vt.runtime_options.WrFMTFF = inpf.readline()
        self.turbsim_vt.runtime_options.WrACT = inpf.readline()
        self.turbsim_vt.runtime_options.Clockwise = inpf.readline()
        self.turbsim_vt.runtime_options.ScaleIEC = inpf.readline()

        # Turbine/Model Specifications
        inpf.readline()
        inpf.readline()
        self.turbsim_vt.tmspecs.NumGrid_Z = inpf.readline()
        self.turbsim_vt.tmspecs.NumGrid_Y = inpf.readline()
        self.turbsim_vt.tmspecs.TimeStep = inpf.readline()
        self.turbsim_vt.tmspecs.AnalysisTime = inpf.readline()
        self.turbsim_vt.tmspecs.UsableTime = inpf.readline()
        self.turbsim_vt.tmspecs.HubHt = inpf.readline()
        self.turbsim_vt.tmspecs.GridHeight = inpf.readline()
        self.turbsim_vt.tmspecs.GridWidth = inpf.readline()
        self.turbsim_vt.tmspecs.VFlowAng = inpf.readline()
        self.turbsim_vt.tmspecs.HFlowAng = inpf.readline()

        # Meteorological Boundary Conditions 
        inpf.readline()
        inpf.readline()
        self.turbsim_vt.metboundconds.TurbModel = inpf.readline()
        self.turbsim_vt.metboundconds.UserFile = inpf.readline()
        self.turbsim_vt.metboundconds.IECstandard = inpf.readline()
        self.turbsim_vt.metboundconds.IECturbc = inpf.readline()
        self.turbsim_vt.metboundconds.IEC_WindType = inpf.readline()
        self.turbsim_vt.metboundconds.ETMc = inpf.readline()
        self.turbsim_vt.metboundconds.WindProfileType = inpf.readline()
        self.turbsim_vt.metboundconds.ProfileFile = inpf.readline()
        self.turbsim_vt.metboundconds.RefHt = inpf.readline()
        self.turbsim_vt.metboundconds.URef = inpf.readline()
        self.turbsim_vt.metboundconds.ZJetMax = inpf.readline()
        self.turbsim_vt.metboundconds.PLExp = inpf.readline()
        self.turbsim_vt.metboundconds.Z0 = inpf.readline()


        # Meteorological Boundary Conditions 
        inpf.readline()
        inpf.readline()
        self.turbsim_vt.noniecboundconds.Latitude = inpf.readline()
        self.turbsim_vt.noniecboundconds.RICH_NO = inpf.readline()
        self.turbsim_vt.noniecboundconds.UStar = inpf.readline()
        self.turbsim_vt.noniecboundconds.ZI = inpf.readline()
        self.turbsim_vt.noniecboundconds.PC_UW = inpf.readline()
        self.turbsim_vt.noniecboundconds.PC_UV = inpf.readline()
        self.turbsim_vt.noniecboundconds.PC_VW = inpf.readline()

        # Spatial Coherence Parameters
        inpf.readline()
        inpf.readline()
        self.turbsim_vt.spatialcoherance.SCMod1 = inpf.readline()
        self.turbsim_vt.spatialcoherance.SCMod2 = inpf.readline()
        self.turbsim_vt.spatialcoherance.SCMod3 = inpf.readline()
        self.turbsim_vt.spatialcoherance.InCDec1 = inpf.readline()[1:-2].split()
        self.turbsim_vt.spatialcoherance.InCDec2 = inpf.readline()[1:-2].split()
        self.turbsim_vt.spatialcoherance.InCDec3 = inpf.readline()[1:-2].split()
        self.turbsim_vt.spatialcoherance.CohExp = inpf.readline()

        # Spatial Coherence Parameters
        inpf.readline()
        inpf.readline()
        self.turbsim_vt.coherentTurbulence.CTEventPath = inpf.readline()
        self.turbsim_vt.coherentTurbulence.CTEventFile = inpf.readline()
        self.turbsim_vt.coherentTurbulence.Randomize = inpf.readline()
        self.turbsim_vt.coherentTurbulence.DistScl = inpf.readline()
        self.turbsim_vt.coherentTurbulence.CTLy = inpf.readline()
        self.turbsim_vt.coherentTurbulence.CTLz = inpf.readline()
        self.turbsim_vt.coherentTurbulence.CTStartTime = inpf.readline()

if __name__=='__main__':
    reader = turbsimReader()
    reader.read_input_file('turbsim_default.in')
