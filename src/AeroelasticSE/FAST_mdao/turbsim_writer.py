from turbsim_vartrees import turbsiminputs
class TurbsimBuilder(turbsiminputs):
    def __init__(self):
         super(TurbsimBuilder, self).__init__()
         self.tsim_input_file = 'turbsim_default.in'
         self.tsim_turbulence_file = 'turbulence_default.in'
         self.tsim_profile_file = 'default.shear'
    def execute(self):
         tsinp = open(self.tsim_input_file, 'w')
         tsinp.write("-----\n")
         tsinp.write("-----\n")
         tsinp.write("-----\n")

         # runtime options
         tsinp.write("{}\n".format(self.runtime_options.echo))
         tsinp.write("{}\n".format(self.runtime_options.RandSeed1))
         tsinp.write("{}\n".format(self.runtime_options.RandSeed2))
         tsinp.write("{}\n".format(self.runtime_options.WrBHHTP))
         tsinp.write("{}\n".format(self.runtime_options.WrFHHTP))
         tsinp.write("{}\n".format(self.runtime_options.WrADHH))
         tsinp.write("{}\n".format(self.runtime_options.WrADFF))
         tsinp.write("{}\n".format(self.runtime_options.WrBLFF))
         tsinp.write("{}\n".format(self.runtime_options.WrADTWR))
         tsinp.write("{}\n".format(self.runtime_options.WrFMTFF))
         tsinp.write("{}\n".format(self.runtime_options.WrACT))
         tsinp.write("{}\n".format(self.runtime_options.Clockwise))
         tsinp.write("{}\n".format(self.runtime_options.ScaleIEC))

         # Turbine/Model Specifications
         tsinp.write("\n")
         tsinp.write("----\n")
         tsinp.write("{}\n".format(self.tmspecs.NumGrid_Z))
         tsinp.write("{}\n".format(self.tmspecs.NumGrid_Y))
         tsinp.write("{}\n".format(self.tmspecs.TimeStep))
         tsinp.write("{}\n".format(self.tmspecs.AnalysisTime))
         tsinp.write("{}\n".format(self.tmspecs.UsableTime))
         tsinp.write("{}\n".format(self.tmspecs.HubHt))
         tsinp.write("{}\n".format(self.tmspecs.GridHeight))
         tsinp.write("{}\n".format(self.tmspecs.GridWidth))
         tsinp.write("{}\n".format(self.tmspecs.VFlowAng))
         tsinp.write("{}\n".format(self.tmspecs.HFlowAng))

         # Meteorological Boundary Conditions
         tsinp.write("\n")
         tsinp.write("----\n")
         tsinp.write("{}\n".format(self.metboundconds.TurbModel))
         tsinp.write("{}\n".format(self.metboundconds.UserFile))
         tsinp.write("{}\n".format(self.metboundconds.IECstandard))
         tsinp.write("{}\n".format(self.metboundconds.IECturbc))
         tsinp.write("{}\n".format(self.metboundconds.IEC_WindType))
         tsinp.write("{}\n".format(self.metboundconds.ETMc))
         tsinp.write("{}\n".format(self.metboundconds.WindProfileType))
         tsinp.write("{}\n".format(self.metboundconds.ProfileFile))
         tsinp.write("{}\n".format(self.metboundconds.RefHt))
         tsinp.write("{}\n".format(self.metboundconds.URef))
         tsinp.write("{}\n".format(self.metboundconds.ZJetMax))
         tsinp.write("{}\n".format(self.metboundconds.PLExp))
         tsinp.write("{}\n".format(self.metboundconds.Z0))

         # Non-IEC Meteorological Boundary Conditions
         tsinp.write("\n")
         tsinp.write("----\n")
         tsinp.write("{}\n".format(self.noniecboundconds.Latitude))
         tsinp.write("{}\n".format(self.noniecboundconds.RICH_NO))
         tsinp.write("{}\n".format(self.noniecboundconds.UStar))
         tsinp.write("{}\n".format(self.noniecboundconds.ZI))
         tsinp.write("{}\n".format(self.noniecboundconds.PC_UW))
         tsinp.write("{}\n".format(self.noniecboundconds.PC_UV))
         tsinp.write("{}\n".format(self.noniecboundconds.PC_VW))

         # Spatial Coherence Parameters
         tsinp.write("\n")
         tsinp.write("----\n")
         tsinp.write("{}\n".format(self.noniecboundconds.Latitude))
s = TurbsimBuilder()
s.execute()
