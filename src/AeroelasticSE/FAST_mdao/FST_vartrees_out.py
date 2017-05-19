# Output Channel Variable Trees

class WindMotionsOut(object):
    def __init__(self):

        # Wind Motions
        self.WindVxi = False   #Nominally downwind component of the hub-height wind velocity (Directed along the xi-axis            ) , (.NOT. CompAero) units= m/s
        self.WindVyi = False   #Cross-wind component of the hub-height wind velocity (Directed along the yi-axis            ) , (.NOT. CompAero) units= m/s
        self.WindVzi = False   #Vertical component of the hub-height wind velocity (Directed along the zi-axis            ) , (.NOT. CompAero) units= m/s
        self.TotWindV = False   #Total hub-height wind velocity magnitude (N/A         ) , (.NOT. CompAero) units= m/s
        self.HorWindV = False   #Horizontal hub-height wind velocity magnitude (In the xi- and yi-plane  ) , (.NOT. CompAero) units= m/s
        self.HorWndDir = False   #Horizontal hub-height wind direction.  Please note that FAST  uses the opposite sign convention that AeroDyn uses.  Put a "-", "_", "m", or "M" character in front of this variable name if you want to use the AeroDyn convention. (About the zi-axis        ) , (.NOT. CompAero) units= deg
        self.VerWndDir = False   #Vertical hub-height wind direction (About an axis orthogonal to the zi-axis and the HorWindV-vector) , (.NOT. CompAero) units= deg

        # Wind Motions Other Name(s) 1
        self.uWind = False   #Nominally downwind component of the hub-height wind velocity (Directed along the xi-axis            ) , (.NOT. CompAero) units= m/s
        self.vWind = False   #Cross-wind component of the hub-height wind velocity (Directed along the yi-axis            ) , (.NOT. CompAero) units= m/s
        self.wWind = False   #Vertical component of the hub-height wind velocity (Directed along the zi-axis            ) , (.NOT. CompAero) units= m/s


class BladeMotionsOut(object):
    def __init__(self):

        # Blade 1 Tip Motions
        self.TipDxc1 = False   #Blade 1 out-of-plane tip deflection (relative to the undeflected position) (Directed along the xc1-axis) , () units= m
        self.TipDyc1 = False   #Blade 1 in-plane tip deflection (relative to the undeflected position) (Directed along the yc1-axis) , () units= m
        self.TipDzc1 = False   #Blade 1 axial tip deflection (relative to the undeflected position) (Directed along the zc1- and zb1-axes) , () units= m
        self.TipDxb1 = False   #Blade 1 flapwise tip deflection (relative to the undeflected position) (Directed along the xb1-axis) , () units= m
        self.TipDyb1 = False   #Blade 1 edgewise tip deflection (relative to the undeflected position) (Directed along the yb1-axis) , () units= m
        self.TipALxb1 = False   #Blade 1 local flapwise tip acceleration (absolute) (Directed along the local xb1-axis) , () units= m/s**2
        self.TipALyb1 = False   #Blade 1 local edgewise tip acceleration (absolute) (Directed along the local yb1-axis) , () units= m/s**2
        self.TipALzb1 = False   #Blade 1 local axial tip acceleration (absolute) (Directed along the local zb1-axis) , () units= m/s**2
        self.TipRDxb1 = False   #Blade 1 roll (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the xb1-axis) , () units= deg
        self.TipRDyb1 = False   #Blade 1 pitch (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the yb1-axis) , () units= deg
        self.TipRDzc1 = False   #Blade 1 torsional tip deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the zc1- and zb1-axes) , () units= deg
        self.TipClrnc1 = False   #Blade 1 tip-to-tower clearance estimate. This is computed as the perpendicular distance from the yaw axis to the tip of blade 1 when the blade tip is below the yaw bearing. When the tip of blade 1 is above the yaw bearing, it is computed as the absolute distance from the yaw bearing to the blade tip. Please note that you should reduce this value by the tower radius to obtain the actual tower clearance. (N/A) , () units= m
        # Blade 2 Tip Motions
        self.TipDxc2 = False   #Blade 2 out-of-plane tip deflection (relative to the pitch axis) (Directed along the xc2-axis) , () units= m
        self.TipDyc2 = False   #Blade 2 in-plane tip deflection (relative to the pitch axis) (Directed along the yc2-axis) , () units= m
        self.TipDzc2 = False   #Blade 2 axial tip deflection (relative to the pitch axis) (Directed along the zc2- and zb2-axes) , () units= m
        self.TipDxb2 = False   #Blade 2 flapwise tip deflection (relative to the pitch axis) (Directed along the xb2-axis) , () units= m
        self.TipDyb2 = False   #Blade 2 edgewise tip deflection (relative to the pitch axis) (Directed along the yb2-axis) , () units= m
        self.TipALxb2 = False   #Blade 2 local flapwise tip acceleration (absolute) (Directed along the local xb2-axis) , () units= m/s**2
        self.TipALyb2 = False   #Blade 2 local edgewise tip acceleration (absolute) (Directed along the local yb2-axis) , () units= m/s**2
        self.TipALzb2 = False   #Blade 2 local axial tip acceleration (absolute) (Directed along the local zb2-axis) , () units= m/s**2
        self.TipRDxb2 = False   #Blade 2 roll (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the xb2-axis) , () units= deg
        self.TipRDyb2 = False   #Blade 2 pitch (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the yb2-axis) , () units= deg
        self.TipRDzc2 = False   #Blade 2 torsional (angular/rotational) tip deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the zc2- and zb2-axes) , () units= deg
        self.TipClrnc2 = False   #Blade 2 tip-to-tower clearance estimate. This is computed as the perpendicular distance from the yaw axis to the tip of blade 1 when the blade tip is below the yaw bearing. When the tip of blade 1 is above the yaw bearing, it is computed as the absolute distance from the yaw bearing to the blade tip. Please note that you should reduce this value by the tower radius to obtain the actual tower clearance. (N/A) , () units= m
        # Blade 3 Tip Motions
        self.TipDxc3 = False   #Blade 3 out-of-plane tip deflection (relative to the pitch axis) (Directed along the xc3-axis) , (NumBl < 3) units= m
        self.TipDyc3 = False   #Blade 3 in-plane tip deflection (relative to the pitch axis) (Directed along the yc3-axis) , (NumBl < 3) units= m
        self.TipDzc3 = False   #Blade 3 axial tip deflection (relative to the pitch axis) (Directed along the zc3- and zb3-axes) , (NumBl < 3) units= m
        self.TipDxb3 = False   #Blade 3 flapwise tip deflection (relative to the pitch axis) (Directed along the xb3-axis) , (NumBl < 3) units= m
        self.TipDyb3 = False   #Blade 3 edgewise tip deflection (relative to the pitch axis) (Directed along the yb3-axis) , (NumBl < 3) units= m
        self.TipALxb3 = False   #Blade 3 local flapwise tip acceleration (absolute) (Directed along the local xb3-axis) , (NumBl < 3) units= m/s**2
        self.TipALyb3 = False   #Blade 3 local edgewise tip acceleration (absolute) (Directed along the local yb3-axis) , (NumBl < 3) units= m/s**2
        self.TipALzb3 = False   #Blade 3 local axial tip acceleration (absolute) (Directed along the local zb3-axis) , (NumBl < 3) units= m/s**2
        self.TipRDxb3 = False   #Blade 3 roll (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the xb3-axis) , (NumBl < 3) units= deg
        self.TipRDyb3 = False   #Blade 3 pitch (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the yb3-axis) , (NumBl < 3) units= deg
        self.TipRDzc3 = False   #Blade 3 torsional tip deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the zc3- and zb3-axes) , (NumBl < 3) units= deg
        self.TipClrnc3 = False   #Blade 3 tip-to-tower clearance estimate. This is computed as the perpendicular distance from the yaw axis to the tip of blade 1 when the blade tip is below the yaw bearing. When the tip of blade 1 is above the yaw bearing, it is computed as the absolute distance from the yaw bearing to the blade tip. Please note that you should reduce this value by the tower radius to obtain the actual tower clearance. (N/A) , (NumBl < 3) units= m
        # Blade 1 Local Span Motions
        self.Spn1ALxb1 = False   #Blade 1 local flapwise acceleration (absolute) of span station 1 (Directed along the local xb1-axis) , (NBlGages < 1) units= m/s**2
        self.Spn1ALyb1 = False   #Blade 1 local edgewise acceleration (absolute) of span station 1 (Directed along the local yb1-axis) , (NBlGages < 1) units= m/s**2
        self.Spn1ALzb1 = False   #Blade 1 local axial acceleration (absolute) of span station 1 (Directed along the local zb1-axis) , (NBlGages < 1) units= m/s**2
        self.Spn2ALxb1 = False   #Blade 1 local flapwise acceleration (absolute) of span  station 2 (Directed along the local xb1-axis) , (NBlGages < 2) units= m/s**2
        self.Spn2ALyb1 = False   #Blade 1 local edgewise acceleration (absolute) of span station 2 (Directed along the local yb1-axis) , (NBlGages < 2) units= m/s**2
        self.Spn2ALzb1 = False   #Blade 1 local axial acceleration (absolute) of span station 2 (Directed along the local zb1-axis) , (NBlGages < 2) units= m/s**2
        self.Spn3ALxb1 = False   #Blade 1 local flapwise acceleration (absolute) of span station 3 (Directed along the local xb1-axis) , (NBlGages < 3) units= m/s**2
        self.Spn3ALyb1 = False   #Blade 1 local edgewise acceleration (absolute) of span station 3 (Directed along the local yb1-axis) , (NBlGages < 3) units= m/s**2
        self.Spn3ALzb1 = False   #Blade 1 local axial acceleration (absolute) of span station 3 (Directed along the local zb1-axis) , (NBlGages < 3) units= m/s**2
        self.Spn4ALxb1 = False   #Blade 1 local flapwise acceleration (absolute) of span station 4 (Directed along the local xb1-axis) , (NBlGages < 4) units= m/s**2
        self.Spn4ALyb1 = False   #Blade 1 local edgewise acceleration (absolute) of span station 4 (Directed along the local yb1-axis) , (NBlGages < 4) units= m/s**2
        self.Spn4ALzb1 = False   #Blade 1 local axial acceleration (absolute) of span station 4 (Directed along the local zb1-axis) , (NBlGages < 4) units= m/s**2
        self.Spn5ALxb1 = False   #Blade 1 local flapwise acceleration (absolute) of span station 5 (Directed along the local xb1-axis) , (NBlGages < 5) units= m/s**2
        self.Spn5ALyb1 = False   #Blade 1 local edgewise acceleration (absolute) of span station 5 (Directed along the local yb1-axis) , (NBlGages < 5) units= m/s**2
        self.Spn5ALzb1 = False   #Blade 1 local axial acceleration (absolute) of span station 5 (Directed along the local zb1-axis) , (NBlGages < 5) units= m/s**2
        self.Spn6ALxb1 = False   #Blade 1 local flapwise acceleration (absolute) of span station 6 (Directed along the local xb1-axis) , (NBlGages < 6) units= m/s**2
        self.Spn6ALyb1 = False   #Blade 1 local edgewise acceleration (absolute) of span station 6 (Directed along the local yb1-axis) , (NBlGages < 6) units= m/s**2
        self.Spn6ALzb1 = False   #Blade 1 local axial acceleration (absolute) of span station 6 (Directed along the local zb1-axis) , (NBlGages < 6) units= m/s**2
        self.Spn7ALxb1 = False   #Blade 1 local flapwise acceleration (absolute) of span station 7 (Directed along the local xb1-axis) , (NBlGages < 7) units= m/s**2
        self.Spn7ALyb1 = False   #Blade 1 local edgewise acceleration (absolute) of span station 7 (Directed along the local yb1-axis) , (NBlGages < 7) units= m/s**2
        self.Spn7ALzb1 = False   #Blade 1 local axial acceleration (absolute) of span station 7 (Directed along the local zb1-axis) , (NBlGages < 7) units= m/s**2
        self.Spn8ALxb1 = False   #Blade 1 local flapwise acceleration (absolute) of span station 8 (Directed along the local xb1-axis) , (NBlGages < 8) units= m/s**2
        self.Spn8ALyb1 = False   #Blade 1 local edgewise acceleration (absolute) of span station 8 (Directed along the local yb1-axis) , (NBlGages < 8) units= m/s**2
        self.Spn8ALzb1 = False   #Blade 1 local axial acceleration (absolute) of span station 8 (Directed along the local zb1-axis) , (NBlGages < 8) units= m/s**2
        self.Spn9ALxb1 = False   #Blade 1 local flapwise acceleration (absolute) of span station 9 (Directed along the local xb1-axis) , (NBlGages < 9) units= m/s**2
        self.Spn9ALyb1 = False   #Blade 1 local edgewise acceleration (absolute) of span station 9 (Directed along the local yb1-axis) , (NBlGages < 9) units= m/s**2
        self.Spn9ALzb1 = False   #Blade 1 local axial acceleration (absolute) of span station 9 (Directed along the local zb1-axis) , (NBlGages < 9) units= m/s**2
        self.Spn1TDxb1 = False   #Blade 1 local flapwise (translational) deflection (relative to the undeflected position) of span station 1 (Directed along the xb1-axis) , (NBlGages < 1) units= m
        self.Spn1TDyb1 = False   #Blade 1 local edgewise (translational) deflection (relative to the undeflected position) of span station 1 (Directed along the yb1-axis) , (NBlGages < 1) units= m
        self.Spn1TDzb1 = False   #Blade 1 local axial (translational) deflection (relative to the undeflected position) of span station 1 (Directed along the zb1-axis) , (NBlGages < 1) units= m
        self.Spn2TDxb1 = False   #Blade 1 local flapwise (translational) deflection (relative to the undeflected position) of span station 2 (Directed along the xb1-axis) , (NBlGages < 2) units= m
        self.Spn2TDyb1 = False   #Blade 1 local edgewise (translational) deflection (relative to the undeflected position) of span station 2 (Directed along the yb1-axis) , (NBlGages < 2) units= m
        self.Spn2TDzb1 = False   #Blade 1 local axial (translational) deflection (relative to the undeflected position) of span station 2 (Directed along the zb1-axis) , (NBlGages < 2) units= m
        self.Spn3TDxb1 = False   #Blade 1 local flapwise (translational) deflection (relative to the undeflected position) of span station 3 (Directed along the xb1-axis) , (NBlGages < 3) units= m
        self.Spn3TDyb1 = False   #Blade 1 local edgewise (translational) deflection (relative to the undeflected position) of span station 3 (Directed along the yb1-axis) , (NBlGages < 3) units= m
        self.Spn3TDzb1 = False   #Blade 1 local axial (translational) deflection (relative to the undeflected position) of span station 3 (Directed along the zb1-axis) , (NBlGages < 3) units= m
        self.Spn4TDxb1 = False   #Blade 1 local flapwise (translational) deflection (relative to the undeflected position) of span station 4 (Directed along the xb1-axis) , (NBlGages < 4) units= m
        self.Spn4TDyb1 = False   #Blade 1 local edgewise (translational) deflection (relative to the undeflected position) of span station 4 (Directed along the yb1-axis) , (NBlGages < 4) units= m
        self.Spn4TDzb1 = False   #Blade 1 local axial (translational) deflection (relative to the undeflected position) of span station 4 (Directed along the zb1-axis) , (NBlGages < 4) units= m
        self.Spn5TDxb1 = False   #Blade 1 local flapwise (translational) deflection (relative to the undeflected position) of span station 5 (Directed along the xb1-axis) , (NBlGages < 5) units= m
        self.Spn5TDyb1 = False   #Blade 1 local edgewise (translational) deflection (relative to the undeflected position) of span station 5 (Directed along the yb1-axis) , (NBlGages < 5) units= m
        self.Spn5TDzb1 = False   #Blade 1 local axial (translational) deflection (relative to the undeflected position) of span station 5 (Directed along the zb1-axis) , (NBlGages < 5) units= m
        self.Spn6TDxb1 = False   #Blade 1 local flapwise (translational) deflection (relative to the undeflected position) of span station 6 (Directed along the xb1-axis) , (NBlGages < 6) units= m
        self.Spn6TDyb1 = False   #Blade 1 local edgewise (translational) deflection (relative to the undeflected position) of span station 6 (Directed along the yb1-axis) , (NBlGages < 6) units= m
        self.Spn6TDzb1 = False   #Blade 1 local axial (translational) deflection (relative to the undeflected position) of span station 6 (Directed along the zb1-axis) , (NBlGages < 6) units= m
        self.Spn7TDxb1 = False   #Blade 1 local flapwise (translational) deflection (relative to the undeflected position) of span station 7 (Directed along the xb1-axis) , (NBlGages < 7) units= m
        self.Spn7TDyb1 = False   #Blade 1 local edgewise (translational) deflection (relative to the undeflected position) of span station 7 (Directed along the yb1-axis) , (NBlGages < 7) units= m
        self.Spn7TDzb1 = False   #Blade 1 local axial (translational) deflection (relative to the undeflected position) of span station 7 (Directed along the zb1-axis) , (NBlGages < 7) units= m
        self.Spn8TDxb1 = False   #Blade 1 local flapwise (translational) deflection (relative to the undeflected position) of span station 8 (Directed along the xb1-axis) , (NBlGages < 8) units= m
        self.Spn8TDyb1 = False   #Blade 1 local edgewise (translational) deflection (relative to the undeflected position) of span station 8 (Directed along the yb1-axis) , (NBlGages < 8) units= m
        self.Spn8TDzb1 = False   #Blade 1 local axial (translational) deflection (relative to the undeflected position) of span station 8 (Directed along the zb1-axis) , (NBlGages < 8) units= m
        self.Spn9TDxb1 = False   #Blade 1 local flapwise (translational) deflection (relative to the undeflected position) of span station 9 (Directed along the xb1-axis) , (NBlGages < 9) units= m
        self.Spn9TDyb1 = False   #Blade 1 local edgewise (translational) deflection (relative to the undeflected position) of span station 9 (Directed along the yb1-axis) , (NBlGages < 9) units= m
        self.Spn9TDzb1 = False   #Blade 1 local axial (translational) deflection (relative to the undeflected position) of span station 9 (Directed along the zb1-axis) , (NBlGages < 9) units= m
        self.Spn1RDxb1 = False   #Blade 1 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 1. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb1-axis) , (NBlGages < 1) units= deg
        self.Spn1RDyb1 = False   #Blade 1 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 1. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb1-axis) , (NBlGages < 1) units= deg
        self.Spn1RDzb1 = False   #Blade 1 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 1. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb1-axis) , (NBlGages < 1) units= deg
        self.Spn2RDxb1 = False   #Blade 1 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 2. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb1-axis) , (NBlGages < 2) units= deg
        self.Spn2RDyb1 = False   #Blade 1 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 2. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb1-axis) , (NBlGages < 2) units= deg
        self.Spn2RDzb1 = False   #Blade 1 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 2. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb1-axis) , (NBlGages < 2) units= deg
        self.Spn3RDxb1 = False   #Blade 1 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 3. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb1-axis) , (NBlGages < 3) units= deg
        self.Spn3RDyb1 = False   #Blade 1 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 3. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb1-axis) , (NBlGages < 3) units= deg
        self.Spn3RDzb1 = False   #Blade 1 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 3. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb1-axis) , (NBlGages < 3) units= deg
        self.Spn4RDxb1 = False   #Blade 1 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 4. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb1-axis) , (NBlGages < 4) units= deg
        self.Spn4RDyb1 = False   #Blade 1 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 4. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb1-axis) , (NBlGages < 4) units= deg
        self.Spn4RDzb1 = False   #Blade 1 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 4. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb1-axis) , (NBlGages < 4) units= deg
        self.Spn5RDxb1 = False   #Blade 1 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 5. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb1-axis) , (NBlGages < 5) units= deg
        self.Spn5RDyb1 = False   #Blade 1 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 5. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb1-axis) , (NBlGages < 5) units= deg
        self.Spn5RDzb1 = False   #Blade 1 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 5. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb1-axis) , (NBlGages < 5) units= deg
        self.Spn6RDxb1 = False   #Blade 1 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 6. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb1-axis) , (NBlGages < 6) units= deg
        self.Spn6RDyb1 = False   #Blade 1 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 6. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb1-axis) , (NBlGages < 6) units= deg
        self.Spn6RDzb1 = False   #Blade 1 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 6. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb1-axis) , (NBlGages < 6) units= deg
        self.Spn7RDxb1 = False   #Blade 1 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 7. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb1-axis) , (NBlGages < 7) units= deg
        self.Spn7RDyb1 = False   #Blade 1 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 7. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb1-axis) , (NBlGages < 7) units= deg
        self.Spn7RDzb1 = False   #Blade 1 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 7. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb1-axis) , (NBlGages < 7) units= deg
        self.Spn8RDxb1 = False   #Blade 1 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 8. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb1-axis) , (NBlGages < 8) units= deg
        self.Spn8RDyb1 = False   #Blade 1 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 8. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb1-axis) , (NBlGages < 8) units= deg
        self.Spn8RDzb1 = False   #Blade 1 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 8. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb1-axis) , (NBlGages < 8) units= deg
        self.Spn9RDxb1 = False   #Blade 1 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 9. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb1-axis) , (NBlGages < 9) units= deg
        self.Spn9RDyb1 = False   #Blade 1 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 9. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb1-axis) , (NBlGages < 9) units= deg
        self.Spn9RDzb1 = False   #Blade 1 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 9. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb1-axis) , (NBlGages < 9) units= deg
        # Blade 2 Local Span Motions
        self.Spn1ALxb2 = False   #Blade 2 local flapwise acceleration (absolute) of span station 1 (Directed along the local xb2-axis) , (NBlGages < 1) units= m/s**2
        self.Spn1ALyb2 = False   #Blade 2 local edgewise acceleration (absolute) of span station 1 (Directed along the local yb2-axis) , (NBlGages < 1) units= m/s**2
        self.Spn1ALzb2 = False   #Blade 2 local axial acceleration (absolute) of span station 1 (Directed along the local zb2-axis) , (NBlGages < 1) units= m/s**2
        self.Spn2ALxb2 = False   #Blade 2 local flapwise acceleration (absolute) of span station 2 (Directed along the local xb2-axis) , (NBlGages < 2) units= m/s**2
        self.Spn2ALyb2 = False   #Blade 2 local edgewise acceleration (absolute) of span station 2 (Directed along the local yb2-axis) , (NBlGages < 2) units= m/s**2
        self.Spn2ALzb2 = False   #Blade 2 local axial acceleration (absolute) of span station 2 (Directed along the local zb2-axis) , (NBlGages < 2) units= m/s**2
        self.Spn3ALxb2 = False   #Blade 2 local flapwise acceleration (absolute) of span station 3 (Directed along the local xb2-axis) , (NBlGages < 3) units= m/s**2
        self.Spn3ALyb2 = False   #Blade 2 local edgewise acceleration (absolute) of span station 3 (Directed along the local yb2-axis) , (NBlGages < 3) units= m/s**2
        self.Spn3ALzb2 = False   #Blade 2 local axial acceleration (absolute) of span station 3 (Directed along the local zb2-axis) , (NBlGages < 3) units= m/s**2
        self.Spn4ALxb2 = False   #Blade 2 local flapwise acceleration (absolute) of span station 4 (Directed along the local xb2-axis) , (NBlGages < 4) units= m/s**2
        self.Spn4ALyb2 = False   #Blade 2 local edgewise acceleration (absolute) of span station 4 (Directed along the local yb2-axis) , (NBlGages < 4) units= m/s**2
        self.Spn4ALzb2 = False   #Blade 2 local axial acceleration (absolute) of span station 4 (Directed along the local zb2-axis) , (NBlGages < 4) units= m/s**2
        self.Spn5ALxb2 = False   #Blade 2 local flapwise acceleration (absolute) of span station 5 (Directed along the local xb2-axis) , (NBlGages < 5) units= m/s**2
        self.Spn5ALyb2 = False   #Blade 2 local edgewise acceleration (absolute) of span station 5 (Directed along the local yb2-axis) , (NBlGages < 5) units= m/s**2
        self.Spn5ALzb2 = False   #Blade 2 local axial acceleration (absolute) of span station 5 (Directed along the local zb2-axis) , (NBlGages < 5) units= m/s**2
        self.Spn6ALxb2 = False   #Blade 2 local flapwise acceleration (absolute) of span station 6 (Directed along the local xb2-axis) , (NBlGages < 6) units= m/s**2
        self.Spn6ALyb2 = False   #Blade 2 local edgewise acceleration (absolute) of span station 6 (Directed along the local yb2-axis) , (NBlGages < 6) units= m/s**2
        self.Spn6ALzb2 = False   #Blade 2 local axial acceleration (absolute) of span station 6 (Directed along the local zb2-axis) , (NBlGages < 6) units= m/s**2
        self.Spn7ALxb2 = False   #Blade 2 local flapwise acceleration (absolute) of span station 7 (Directed along the local xb2-axis) , (NBlGages < 7) units= m/s**2
        self.Spn7ALyb2 = False   #Blade 2 local edgewise acceleration (absolute) of span station 7 (Directed along the local yb2-axis) , (NBlGages < 7) units= m/s**2
        self.Spn7ALzb2 = False   #Blade 2 local axial acceleration (absolute) of span station 7 (Directed along the local zb2-axis) , (NBlGages < 7) units= m/s**2
        self.Spn8ALxb2 = False   #Blade 2 local flapwise acceleration (absolute) of span station 8 (Directed along the local xb2-axis) , (NBlGages < 8) units= m/s**2
        self.Spn8ALyb2 = False   #Blade 2 local edgewise acceleration (absolute) of span station 8 (Directed along the local yb2-axis) , (NBlGages < 8) units= m/s**2
        self.Spn8ALzb2 = False   #Blade 2 local axial acceleration (absolute) of span station 8 (Directed along the local zb2-axis) , (NBlGages < 8) units= m/s**2
        self.Spn9ALxb2 = False   #Blade 2 local flapwise acceleration (absolute) of span station 9 (Directed along the local xb2-axis) , (NBlGages < 9) units= m/s**2
        self.Spn9ALyb2 = False   #Blade 2 local edgewise acceleration (absolute) of span station 9 (Directed along the local yb2-axis) , (NBlGages < 9) units= m/s**2
        self.Spn9ALzb2 = False   #Blade 2 local axial acceleration (absolute) of span station 9 (Directed along the local zb2-axis) , (NBlGages < 9) units= m/s**2
        self.Spn1TDxb2 = False   #Blade 2 local flapwise (translational) deflection (relative to the undeflected position) of span station 1 (Directed along the xb2-axis) , (NBlGages < 1) units= m
        self.Spn1TDyb2 = False   #Blade 2 local edgewise (translational) deflection (relative to the undeflected position) of span station 1 (Directed along the yb2-axis) , (NBlGages < 1) units= m
        self.Spn1TDzb2 = False   #Blade 2 local axial (translational) deflection (relative to the undeflected position) of span station 1 (Directed along the zb2-axis) , (NBlGages < 1) units= m
        self.Spn2TDxb2 = False   #Blade 2 local flapwise (translational) deflection (relative to the undeflected position) of span station 2 (Directed along the xb2-axis) , (NBlGages < 2) units= m
        self.Spn2TDyb2 = False   #Blade 2 local edgewise (translational) deflection (relative to the undeflected position) of span station 2 (Directed along the yb2-axis) , (NBlGages < 2) units= m
        self.Spn2TDzb2 = False   #Blade 2 local axial (translational) deflection (relative to the undeflected position) of span station 2 (Directed along the zb2-axis) , (NBlGages < 2) units= m
        self.Spn3TDxb2 = False   #Blade 2 local flapwise (translational) deflection (relative to the undeflected position) of span station 3 (Directed along the xb2-axis) , (NBlGages < 3) units= m
        self.Spn3TDyb2 = False   #Blade 2 local edgewise (translational) deflection (relative to the undeflected position) of span station 3 (Directed along the yb2-axis) , (NBlGages < 3) units= m
        self.Spn3TDzb2 = False   #Blade 2 local axial (translational) deflection (relative to the undeflected position) of span station 3 (Directed along the zb2-axis) , (NBlGages < 3) units= m
        self.Spn4TDxb2 = False   #Blade 2 local flapwise (translational) deflection (relative to the undeflected position) of span station 4 (Directed along the xb2-axis) , (NBlGages < 4) units= m
        self.Spn4TDyb2 = False   #Blade 2 local edgewise (translational) deflection (relative to the undeflected position) of span station 4 (Directed along the yb2-axis) , (NBlGages < 4) units= m
        self.Spn4TDzb2 = False   #Blade 2 local axial (translational) deflection (relative to the undeflected position) of span station 4 (Directed along the zb2-axis) , (NBlGages < 4) units= m
        self.Spn5TDxb2 = False   #Blade 2 local flapwise (translational) deflection (relative to the undeflected position) of span station 5 (Directed along the xb2-axis) , (NBlGages < 5) units= m
        self.Spn5TDyb2 = False   #Blade 2 local edgewise (translational) deflection (relative to the undeflected position) of span station 5 (Directed along the yb2-axis) , (NBlGages < 5) units= m
        self.Spn5TDzb2 = False   #Blade 2 local axial (translational) deflection (relative to the undeflected position) of span station 5 (Directed along the zb2-axis) , (NBlGages < 5) units= m
        self.Spn6TDxb2 = False   #Blade 2 local flapwise (translational) deflection (relative to the undeflected position) of span station 6 (Directed along the xb2-axis) , (NBlGages < 6) units= m
        self.Spn6TDyb2 = False   #Blade 2 local edgewise (translational) deflection (relative to the undeflected position) of span station 6 (Directed along the yb2-axis) , (NBlGages < 6) units= m
        self.Spn6TDzb2 = False   #Blade 2 local axial (translational) deflection (relative to the undeflected position) of span station 6 (Directed along the zb2-axis) , (NBlGages < 6) units= m
        self.Spn7TDxb2 = False   #Blade 2 local flapwise (translational) deflection (relative to the undeflected position) of span station 7 (Directed along the xb2-axis) , (NBlGages < 7) units= m
        self.Spn7TDyb2 = False   #Blade 2 local edgewise (translational) deflection (relative to the undeflected position) of span station 7 (Directed along the yb2-axis) , (NBlGages < 7) units= m
        self.Spn7TDzb2 = False   #Blade 2 local axial (translational) deflection (relative to the undeflected position) of span station 7 (Directed along the zb2-axis) , (NBlGages < 7) units= m
        self.Spn8TDxb2 = False   #Blade 2 local flapwise (translational) deflection (relative to the undeflected position) of span station 8 (Directed along the xb2-axis) , (NBlGages < 8) units= m
        self.Spn8TDyb2 = False   #Blade 2 local edgewise (translational) deflection (relative to the undeflected position) of span station 8 (Directed along the yb2-axis) , (NBlGages < 8) units= m
        self.Spn8TDzb2 = False   #Blade 2 local axial (translational) deflection (relative to the undeflected position) of span station 8 (Directed along the zb2-axis) , (NBlGages < 8) units= m
        self.Spn9TDxb2 = False   #Blade 2 local flapwise (translational) deflection (relative to the undeflected position) of span station 9 (Directed along the xb2-axis) , (NBlGages < 9) units= m
        self.Spn9TDyb2 = False   #Blade 2 local edgewise (translational) deflection (relative to the undeflected position) of span station 9 (Directed along the yb2-axis) , (NBlGages < 9) units= m
        self.Spn9TDzb2 = False   #Blade 2 local axial (translational) deflection (relative to the undeflected position) of span station 9 (Directed along the zb2-axis) , (NBlGages < 9) units= m
        self.Spn1RDxb2 = False   #Blade 2 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 1. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb2-axis) , (NBlGages < 1) units= deg
        self.Spn1RDyb2 = False   #Blade 2 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 1. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb2-axis) , (NBlGages < 1) units= deg
        self.Spn1RDzb2 = False   #Blade 2 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 1. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb2-axis) , (NBlGages < 1) units= deg
        self.Spn2RDxb2 = False   #Blade 2 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 2. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb2-axis) , (NBlGages < 2) units= deg
        self.Spn2RDyb2 = False   #Blade 2 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 2. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb2-axis) , (NBlGages < 2) units= deg
        self.Spn2RDzb2 = False   #Blade 2 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 2. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb2-axis) , (NBlGages < 2) units= deg
        self.Spn3RDxb2 = False   #Blade 2 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 3. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb2-axis) , (NBlGages < 3) units= deg
        self.Spn3RDyb2 = False   #Blade 2 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 3. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb2-axis) , (NBlGages < 3) units= deg
        self.Spn3RDzb2 = False   #Blade 2 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 3. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb2-axis) , (NBlGages < 3) units= deg
        self.Spn4RDxb2 = False   #Blade 2 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 4. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb2-axis) , (NBlGages < 4) units= deg
        self.Spn4RDyb2 = False   #Blade 2 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 4. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb2-axis) , (NBlGages < 4) units= deg
        self.Spn4RDzb2 = False   #Blade 2 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 4. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb2-axis) , (NBlGages < 4) units= deg
        self.Spn5RDxb2 = False   #Blade 2 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 5. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb2-axis) , (NBlGages < 5) units= deg
        self.Spn5RDyb2 = False   #Blade 2 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 5. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb2-axis) , (NBlGages < 5) units= deg
        self.Spn5RDzb2 = False   #Blade 2 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 5. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb2-axis) , (NBlGages < 5) units= deg
        self.Spn6RDxb2 = False   #Blade 2 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 6. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb2-axis) , (NBlGages < 6) units= deg
        self.Spn6RDyb2 = False   #Blade 2 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 6. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb2-axis) , (NBlGages < 6) units= deg
        self.Spn6RDzb2 = False   #Blade 2 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 6. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb2-axis) , (NBlGages < 6) units= deg
        self.Spn7RDxb2 = False   #Blade 2 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 7. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb2-axis) , (NBlGages < 7) units= deg
        self.Spn7RDyb2 = False   #Blade 2 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 7. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb2-axis) , (NBlGages < 7) units= deg
        self.Spn7RDzb2 = False   #Blade 2 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 7. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb2-axis) , (NBlGages < 7) units= deg
        self.Spn8RDxb2 = False   #Blade 2 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 8. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb2-axis) , (NBlGages < 8) units= deg
        self.Spn8RDyb2 = False   #Blade 2 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 8. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb2-axis) , (NBlGages < 8) units= deg
        self.Spn8RDzb2 = False   #Blade 2 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 8. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb2-axis) , (NBlGages < 8) units= deg
        self.Spn9RDxb2 = False   #Blade 2 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 9. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb2-axis) , (NBlGages < 9) units= deg
        self.Spn9RDyb2 = False   #Blade 2 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 9. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb2-axis) , (NBlGages < 9) units= deg
        self.Spn9RDzb2 = False   #Blade 2 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 9. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb2-axis) , (NBlGages < 9) units= deg
        # Blade 3 Local Span Motions
        self.Spn1ALxb3 = False   #Blade 3 local flapwise acceleration (absolute) of span station 1 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= m/s**2
        self.Spn1ALyb3 = False   #Blade 3 local edgewise acceleration (absolute) of span station 1 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= m/s**2
        self.Spn1ALzb3 = False   #Blade 3 local axial acceleration (absolute) of span station 1 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= m/s**2
        self.Spn2ALxb3 = False   #Blade 3 local flapwise acceleration (absolute) of span station 2 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= m/s**2
        self.Spn2ALyb3 = False   #Blade 3 local edgewise acceleration (absolute) of span station 2 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= m/s**2
        self.Spn2ALzb3 = False   #Blade 3 local axial acceleration (absolute) of span station 2 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= m/s**2
        self.Spn3ALxb3 = False   #Blade 3 local flapwise acceleration (absolute) of span station 3 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= m/s**2
        self.Spn3ALyb3 = False   #Blade 3 local edgewise acceleration (absolute) of span station 3 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= m/s**2
        self.Spn3ALzb3 = False   #Blade 3 local axial acceleration (absolute) of span station 3 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= m/s**2
        self.Spn4ALxb3 = False   #Blade 3 local flapwise acceleration (absolute) of span station 4 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= m/s**2
        self.Spn4ALyb3 = False   #Blade 3 local edgewise acceleration (absolute) of span station 4 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= m/s**2
        self.Spn4ALzb3 = False   #Blade 3 local axial acceleration (absolute) of span station 4 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= m/s**2
        self.Spn5ALxb3 = False   #Blade 3 local flapwise acceleration (absolute) of span station 5 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= m/s**2
        self.Spn5ALyb3 = False   #Blade 3 local edgewise acceleration (absolute) of span station 5 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= m/s**2
        self.Spn5ALzb3 = False   #Blade 3 local axial acceleration (absolute) of span station 5 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= m/s**2
        self.Spn6ALxb3 = False   #Blade 3 local flapwise acceleration (absolute) of span station 6 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= m/s**2
        self.Spn6ALyb3 = False   #Blade 3 local edgewise acceleration (absolute) of span station 6 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= m/s**2
        self.Spn6ALzb3 = False   #Blade 3 local axial acceleration (absolute) of span station 6 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= m/s**2
        self.Spn7ALxb3 = False   #Blade 3 local flapwise acceleration (absolute) of span station 7 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= m/s**2
        self.Spn7ALyb3 = False   #Blade 3 local edgewise acceleration (absolute) of span station 7 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= m/s**2
        self.Spn7ALzb3 = False   #Blade 3 local axial acceleration (absolute) of span station 7 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= m/s**2
        self.Spn8ALxb3 = False   #Blade 3 local flapwise acceleration (absolute) of span station 8 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= m/s**2
        self.Spn8ALyb3 = False   #Blade 3 local edgewise acceleration (absolute) of span station 8 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= m/s**2
        self.Spn8ALzb3 = False   #Blade 3 local axial acceleration (absolute) of span station 8 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= m/s**2
        self.Spn9ALxb3 = False   #Blade 3 local flapwise acceleration (absolute) of span station 9 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= m/s**2
        self.Spn9ALyb3 = False   #Blade 3 local edgewise acceleration (absolute) of span station 9 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= m/s**2
        self.Spn9ALzb3 = False   #Blade 3 local axial acceleration (absolute) of span station 9 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= m/s**2
        self.Spn1TDxb3 = False   #Blade 3 local flapwise (translational) deflection (relative to the undeflected position) of span station 1 (Directed along the xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= m
        self.Spn1TDyb3 = False   #Blade 3 local edgewise (translational) deflection (relative to the undeflected position) of span station 1 (Directed along the yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= m
        self.Spn1TDzb3 = False   #Blade 3 local axial (translational) deflection (relative to the undeflected position) of span station 1 (Directed along the zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= m
        self.Spn2TDxb3 = False   #Blade 3 local flapwise (translational) deflection (relative to the undeflected position) of span station 2 (Directed along the xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= m
        self.Spn2TDyb3 = False   #Blade 3 local edgewise (translational) deflection (relative to the undeflected position) of span station 2 (Directed along the yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= m
        self.Spn2TDzb3 = False   #Blade 3 local axial (translational) deflection (relative to the undeflected position) of span station 2 (Directed along the zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= m
        self.Spn3TDxb3 = False   #Blade 3 local flapwise (translational) deflection (relative to the undeflected position) of span station 3 (Directed along the xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= m
        self.Spn3TDyb3 = False   #Blade 3 local edgewise (translational) deflection (relative to the undeflected position) of span station 3 (Directed along the yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= m
        self.Spn3TDzb3 = False   #Blade 3 local axial (translational) deflection (relative to the undeflected position) of span station 3 (Directed along the zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= m
        self.Spn4TDxb3 = False   #Blade 3 local flapwise (translational) deflection (relative to the undeflected position) of span station 4 (Directed along the xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= m
        self.Spn4TDyb3 = False   #Blade 3 local edgewise (translational) deflection (relative to the undeflected position) of span station 4 (Directed along the yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= m
        self.Spn4TDzb3 = False   #Blade 3 local axial (translational) deflection (relative to the undeflected position) of span station 4 (Directed along the zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= m
        self.Spn5TDxb3 = False   #Blade 3 local flapwise (translational) deflection (relative to the undeflected position) of span station 5 (Directed along the xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= m
        self.Spn5TDyb3 = False   #Blade 3 local edgewise (translational) deflection (relative to the undeflected position) of span station 5 (Directed along the yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= m
        self.Spn5TDzb3 = False   #Blade 3 local axial (translational) deflection (relative to the undeflected position) of span station 5 (Directed along the zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= m
        self.Spn6TDxb3 = False   #Blade 3 local flapwise (translational) deflection (relative to the undeflected position) of span station 6 (Directed along the xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= m
        self.Spn6TDyb3 = False   #Blade 3 local edgewise (translational) deflection (relative to the undeflected position) of span station 6 (Directed along the yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= m
        self.Spn6TDzb3 = False   #Blade 3 local axial (translational) deflection (relative to the undeflected position) of span station 6 (Directed along the zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= m
        self.Spn7TDxb3 = False   #Blade 3 local flapwise (translational) deflection (relative to the undeflected position) of span station 7 (Directed along the xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= m
        self.Spn7TDyb3 = False   #Blade 3 local edgewise (translational) deflection (relative to the undeflected position) of span station 7 (Directed along the yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= m
        self.Spn7TDzb3 = False   #Blade 3 local axial (translational) deflection (relative to the undeflected position) of span station 7 (Directed along the zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= m
        self.Spn8TDxb3 = False   #Blade 3 local flapwise (translational) deflection (relative to the undeflected position) of span station 8 (Directed along the xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= m
        self.Spn8TDyb3 = False   #Blade 3 local edgewise (translational) deflection (relative to the undeflected position) of span station 8 (Directed along the yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= m
        self.Spn8TDzb3 = False   #Blade 3 local axial (translational) deflection (relative to the undeflected position) of span station 8 (Directed along the zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= m
        self.Spn9TDxb3 = False   #Blade 3 local flapwise (translational) deflection (relative to the undeflected position) of span station 9 (Directed along the xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= m
        self.Spn9TDyb3 = False   #Blade 3 local edgewise (translational) deflection (relative to the undeflected position) of span station 9 (Directed along the yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= m
        self.Spn9TDzb3 = False   #Blade 3 local axial (translational) deflection (relative to the undeflected position) of span station 9 (Directed along the zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= m
        self.Spn1RDxb3 = False   #Blade 3 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 1. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= deg
        self.Spn1RDyb3 = False   #Blade 3 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 1. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= deg
        self.Spn1RDzb3 = False   #Blade 3 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 1. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= deg
        self.Spn2RDxb3 = False   #Blade 3 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 2. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= deg
        self.Spn2RDyb3 = False   #Blade 3 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 2. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= deg
        self.Spn2RDzb3 = False   #Blade 3 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 2. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= deg
        self.Spn3RDxb3 = False   #Blade 3 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 3. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= deg
        self.Spn3RDyb3 = False   #Blade 3 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 3. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= deg
        self.Spn3RDzb3 = False   #Blade 3 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 3. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= deg
        self.Spn4RDxb3 = False   #Blade 3 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 4. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= deg
        self.Spn4RDyb3 = False   #Blade 3 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 4. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= deg
        self.Spn4RDzb3 = False   #Blade 3 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 4. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= deg
        self.Spn5RDxb3 = False   #Blade 3 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 5. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= deg
        self.Spn5RDyb3 = False   #Blade 3 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 5. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= deg
        self.Spn5RDzb3 = False   #Blade 3 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 5. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= deg
        self.Spn6RDxb3 = False   #Blade 3 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 6. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= deg
        self.Spn6RDyb3 = False   #Blade 3 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 6. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= deg
        self.Spn6RDzb3 = False   #Blade 3 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 6. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= deg
        self.Spn7RDxb3 = False   #Blade 3 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 7. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= deg
        self.Spn7RDyb3 = False   #Blade 3 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 7. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= deg
        self.Spn7RDzb3 = False   #Blade 3 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 7. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= deg
        self.Spn8RDxb3 = False   #Blade 3 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 8. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= deg
        self.Spn8RDyb3 = False   #Blade 3 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 8. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= deg
        self.Spn8RDzb3 = False   #Blade 3 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 8. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= deg
        self.Spn9RDxb3 = False   #Blade 3 local roll (angular/rotational)  deflection (relative to the undeflected position) of span station 9. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= deg
        self.Spn9RDyb3 = False   #Blade 3 local pitch (angular/rotational) deflection (relative to the undeflected position) of span station 9. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= deg
        self.Spn9RDzb3 = False   #Blade 3 local torsional (angular/rotational) deflection (relative to the undeflected position) of span station 9. This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= deg

        # Other Names
        # Blade 1 Tip Motions 
        self.OoPDefl1 = False   #Blade 1 out-of-plane tip deflection (relative to the undeflected position) (Directed along the xc1-axis) , () units= m
        self.IPDefl1 = False   #Blade 1 in-plane tip deflection (relative to the undeflected position) (Directed along the yc1-axis) , () units= m
        self.TipDzb1 = False   #Blade 1 axial tip deflection (relative to the undeflected position) (Directed along the zc1- and zb1-axes) , () units= m
        self.RollDefl1 = False   #Blade 1 roll (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the xb1-axis) , () units= deg
        self.PtchDefl1 = False   #Blade 1 pitch (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the yb1-axis) , () units= deg
        self.TipRDzb1 = False   #Blade 1 torsional tip deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the zc1- and zb1-axes) , () units= deg
        self.TwrClrnc1 = False   #Blade 1 tip-to-tower clearance estimate. This is computed as the perpendicular distance from the yaw axis to the tip of blade 1 when the blade tip is below the yaw bearing. When the tip of blade 1 is above the yaw bearing, it is computed as the absolute distance from the yaw bearing to the blade tip. Please note that you should reduce this value by the tower radius to obtain the actual tower clearance. (N/A) , () units= m
        # Blade 1 Tip Motions
        self.TwstDefl1 = False   #Blade 1 torsional tip deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the zc1- and zb1-axes) , () units= deg
        self.Tip2Twr1 = False   #Blade 1 tip-to-tower clearance estimate. This is computed as the perpendicular distance from the yaw axis to the tip of blade 1 when the blade tip is below the yaw bearing. When the tip of blade 1 is above the yaw bearing, it is computed as the absolute distance from the yaw bearing to the blade tip. Please note that you should reduce this value by the tower radius to obtain the actual tower clearance. (N/A) , () units= m
        # Blade 2 Tip Motions TwrClrnc1
        self.OoPDefl2 = False   #Blade 2 out-of-plane tip deflection (relative to the pitch axis) (Directed along the xc2-axis) , () units= m
        self.IPDefl2 = False   #Blade 2 in-plane tip deflection (relative to the pitch axis) (Directed along the yc2-axis) , () units= m
        self.TipDzb2 = False   #Blade 2 axial tip deflection (relative to the pitch axis) (Directed along the zc2- and zb2-axes) , () units= m
        self.RollDefl2 = False   #Blade 2 roll (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the xb2-axis) , () units= deg
        self.PtchDefl2 = False   #Blade 2 pitch (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the yb2-axis) , () units= deg
        self.TipRDzb2 = False   #Blade 2 torsional (angular/rotational) tip deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the zc2- and zb2-axes) , () units= deg
        self.TwrClrnc2 = False   #Blade 2 tip-to-tower clearance estimate. This is computed as the perpendicular distance from the yaw axis to the tip of blade 1 when the blade tip is below the yaw bearing. When the tip of blade 1 is above the yaw bearing, it is computed as the absolute distance from the yaw bearing to the blade tip. Please note that you should reduce this value by the tower radius to obtain the actual tower clearance. (N/A) , () units= m
        # Blade 2 Tip Motions Tip2Twr1
        self.TwstDefl2 = False   #Blade 2 torsional (angular/rotational) tip deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the zc2- and zb2-axes) , () units= deg
        self.Tip2Twr2 = False   #Blade 2 tip-to-tower clearance estimate. This is computed as the perpendicular distance from the yaw axis to the tip of blade 1 when the blade tip is below the yaw bearing. When the tip of blade 1 is above the yaw bearing, it is computed as the absolute distance from the yaw bearing to the blade tip. Please note that you should reduce this value by the tower radius to obtain the actual tower clearance. (N/A) , () units= m
        # Blade 3 Tip Motions TwrClrnc2
        self.OoPDefl3 = False   #Blade 3 out-of-plane tip deflection (relative to the pitch axis) (Directed along the xc3-axis) , (NumBl < 3) units= m
        self.IPDefl3 = False   #Blade 3 in-plane tip deflection (relative to the pitch axis) (Directed along the yc3-axis) , (NumBl < 3) units= m
        self.TipDzb3 = False   #Blade 3 axial tip deflection (relative to the pitch axis) (Directed along the zc3- and zb3-axes) , (NumBl < 3) units= m
        self.RollDefl3 = False   #Blade 3 roll (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the xb3-axis) , (NumBl < 3) units= deg
        self.PtchDefl3 = False   #Blade 3 pitch (angular/rotational) tip deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small blade deflections, so that the rotation sequence does not matter. (About the yb3-axis) , (NumBl < 3) units= deg
        self.TipRDzb3 = False   #Blade 3 torsional tip deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the zc3- and zb3-axes) , (NumBl < 3) units= deg
        self.TwrClrnc3 = False   #Blade 3 tip-to-tower clearance estimate. This is computed as the perpendicular distance from the yaw axis to the tip of blade 1 when the blade tip is below the yaw bearing. When the tip of blade 1 is above the yaw bearing, it is computed as the absolute distance from the yaw bearing to the blade tip. Please note that you should reduce this value by the tower radius to obtain the actual tower clearance. (N/A) , (NumBl < 3) units= m
        # Blade 3 Tip Motions Tip2Twr2
        self.TwstDefl3 = False   #Blade 3 torsional tip deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining blade torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence.  Please note that this output uses the opposite of the sign convention used for blade pitch angles. (About the zc3- and zb3-axes) , (NumBl < 3) units= deg
        self.Tip2Twr3 = False   #Blade 3 tip-to-tower clearance estimate. This is computed as the perpendicular distance from the yaw axis to the tip of blade 1 when the blade tip is below the yaw bearing. When the tip of blade 1 is above the yaw bearing, it is computed as the absolute distance from the yaw bearing to the blade tip. Please note that you should reduce this value by the tower radius to obtain the actual tower clearance. (N/A) , (NumBl < 3) units= m


class HubNacelleMotionsOut(object):
    def __init__(self):

        # Blade Pitch Motions
        self.PtchPMzc1 = False   #Blade 1 pitch angle (position) (Positive towards feather about the minus zc1- and minus zb1-axes) , () units= deg
        self.PtchPMzc2 = False   #Blade 2 pitch angle (position) (Positive towards feather about the minus zc2- and minus zb2-axes) , () units= deg
        self.PtchPMzc3 = False   #Blade 3 pitch angle (position) (Positive towards feather about the minus zc3- and minus zb3-axes) , (NumBl < 3) units= deg
        # Teeter Motions
        self.TeetPya = False   #Rotor teeter angle (position) (About the ya-axis) , (NumBl > 2) units= deg
        self.TeetVya = False   #Rotor teeter angular velocity (About the ya-axis) , (NumBl > 2) units= deg/s
        self.TeetAya = False   #Rotor teeter angular acceleration (About the ya-axis) , (NumBl > 2) units= deg/s**2
        # Shaft Motions
        self.LSSTipPxa = False   #Rotor azimuth angle (position) (About the xa- and xs-axes) , () units= deg
        self.LSSTipVxa = False   #Rotor azimuth angular speed (About the xa- and xs-axes) , () units= rpm
        self.LSSTipAxa = False   #Rotor azimuth angular acceleration (About the xa- and xs-axes) , () units= deg/s**2
        self.LSSGagPxa = False   #Low-speed shaft strain gage azimuth angle (position) (on the gearbox side of the low-speed shaft) (About the xa- and xs-axes) , () units= deg
        self.LSSGagVxa = False   #Low-speed shaft strain gage angular speed (on the gearbox side of the low-speed shaft) (About the xa- and xs-axes) , () units= rpm
        self.LSSGagAxa = False   #Low-speed shaft strain gage angular acceleration (on the gearbox side of the low-speed shaft) (About the xa- and xs-axes) , () units= deg/s**2
        self.HSShftV = False   #Angular speed of the high-speed shaft and generator (Same sign as LSSGagVxa / LSSGagVxs / LSSGagV) , () units= rpm
        self.HSShftA = False   #Angular acceleration of the high-speed shaft and generator (Same sign as LSSGagAxa / LSSGagAxs / LSSGagA) , () units= deg/s**2
        self.TipSpdRat = False   #Rotor blade tip speed ratio (N/A) , (.NOT. CompAero) units= 
        # Nacelle IMU Motions
        self.NcIMUTVxs = False   #Nacelle inertial measurement unit translational velocity (absolute) (Directed along the xs-axis) , () units= m/s
        self.NcIMUTVys = False   #Nacelle inertial measurement unit translational velocity (absolute) (Directed along the ys-axis) , () units= m/s
        self.NcIMUTVzs = False   #Nacelle inertial measurement unit translational velocity (absolute) (Directed along the zs-axis) , () units= m/s
        self.NcIMUTAxs = False   #Nacelle inertial measurement unit translational acceleration (absolute) (Directed along the xs-axis) , () units= m/s**2
        self.NcIMUTAys = False   #Nacelle inertial measurement unit translational acceleration (absolute) (Directed along the ys-axis) , () units= m/s**2
        self.NcIMUTAzs = False   #Nacelle inertial measurement unit translational acceleration (absolute) (Directed along the zs-axis) , () units= m/s**2
        self.NcIMURVxs = False   #Nacelle inertial measurement unit angular (rotational) velocity (absolute) (About the xs-axis) , () units= deg/s
        self.NcIMURVys = False   #Nacelle inertial measurement unit angular (rotational) velocity (absolute) (About the ys-axis) , () units= deg/s
        self.NcIMURVzs = False   #Nacelle inertial measurement unit angular (rotational) velocity (absolute) (About the zs-axis) , () units= deg/s
        self.NcIMURAxs = False   #Nacelle inertial measurement unit angular (rotational) acceleration (absolute) (About the xs-axis) , () units= deg/s**2
        self.NcIMURAys = False   #Nacelle inertial measurement unit angular (rotational) acceleration (absolute) (About the ys-axis) , () units= deg/s**2
        self.NcIMURAzs = False   #Nacelle inertial measurement unit angular (rotational) acceleration (absolute) (About the zs-axis) , () units= deg/s**2
        # Rotor-Furl Motions
        self.RotFurlP = False   #Rotor-furl angle (position) (About the rotor-furl axis) , () units= deg
        self.RotFurlV = False   #Rotor-furl angular velocity (About the rotor-furl axis) , () units= deg/s
        self.RotFurlA = False   #Rotor-furl angular acceleration (About the rotor-furl axis) , () units= deg/s**2
        # Tail-Furl Motions
        self.TailFurlP = False   #Tail-furl angle (position) (About the tail-furl axis) , () units= deg
        self.TailFurlV = False   #Tail-furl angular velocity (About the tail-furl axis) , () units= deg/s
        self.TailFurlA = False   #Tail-furl angular acceleration (About the tail-furl axis) , () units= deg/s**2
        # Nacelle Yaw Motions
        self.YawPzn = False   #Nacelle yaw angle (position) (About the zn- and zp-axes) , () units= deg
        self.YawVzn = False   #Nacelle yaw angular velocity (About the zn- and zp-axes) , () units= deg/s
        self.YawAzn = False   #Nacelle yaw angular acceleration (About the zn- and zp-axes) , () units= deg/s**2
        self.NacYawErr = False   #Nacelle yaw error estimate. This is computed as follows: NacYawErr = HorWndDir - YawPzn - YawBrRDzt - PtfmRDzi. This estimate is not accurate instantaneously in the presence of significant tower deflection or platform angular (rotational) displacement since the angles used in the computation are not all defined about the same axis of rotation. However, the estimate should be useful in a yaw controller if averaged over a time scale long enough to diminish the effects of tower and platform motions (i.e., much longer than the period of oscillation). (About the zi-axis) , (.NOT. CompAero) units= deg

        #Other Names
        # Blade Pitch Motions 
        self.PtchPMzb1 = False   #Blade 1 pitch angle (position) (Positive towards feather about the minus zc1- and minus zb1-axes) , () units= deg
        self.PtchPMzb2 = False   #Blade 2 pitch angle (position) (Positive towards feather about the minus zc2- and minus zb2-axes) , () units= deg
        self.PtchPMzb3 = False   #Blade 3 pitch angle (position) (Positive towards feather about the minus zc3- and minus zb3-axes) , (NumBl < 3) units= deg
        # Blade Pitch Motions 
        self.BldPitch1 = False   #Blade 1 pitch angle (position) (Positive towards feather about the minus zc1- and minus zb1-axes) , () units= deg
        self.BldPitch2 = False   #Blade 2 pitch angle (position) (Positive towards feather about the minus zc2- and minus zb2-axes) , () units= deg
        self.BldPitch3 = False   #Blade 3 pitch angle (position) (Positive towards feather about the minus zc3- and minus zb3-axes) , (NumBl < 3) units= deg
        # Teeter Motions PtchPMzb3
        self.RotTeetP = False   #Rotor teeter angle (position) (About the ya-axis) , (NumBl > 2) units= deg
        self.RotTeetV = False   #Rotor teeter angular velocity (About the ya-axis) , (NumBl > 2) units= deg/s
        self.RotTeetA = False   #Rotor teeter angular acceleration (About the ya-axis) , (NumBl > 2) units= deg/s**2
        # Teeter Motions BldPitch3
        self.TeetDefl = False   #Rotor teeter angle (position) (About the ya-axis) , (NumBl > 2) units= deg
        self.RotTeetV = False   #Rotor teeter angular velocity (About the ya-axis) , (NumBl > 2) units= deg/s
        self.RotTeetA = False   #Rotor teeter angular acceleration (About the ya-axis) , (NumBl > 2) units= deg/s**2
        # Teeter Motions 
        self.RotTeetV = False   #Rotor teeter angular velocity (About the ya-axis) , (NumBl > 2) units= deg/s
        self.RotTeetA = False   #Rotor teeter angular acceleration (About the ya-axis) , (NumBl > 2) units= deg/s**2
        # Shaft Motions RotTeetA
        self.LSSTipPxs = False   #Rotor azimuth angle (position) (About the xa- and xs-axes) , () units= deg
        self.LSSTipVxs = False   #Rotor azimuth angular speed (About the xa- and xs-axes) , () units= rpm
        self.LSSTipAxs = False   #Rotor azimuth angular acceleration (About the xa- and xs-axes) , () units= deg/s**2
        self.LSSGagPxs = False   #Low-speed shaft strain gage azimuth angle (position) (on the gearbox side of the low-speed shaft) (About the xa- and xs-axes) , () units= deg
        self.LSSGagVxs = False   #Low-speed shaft strain gage angular speed (on the gearbox side of the low-speed shaft) (About the xa- and xs-axes) , () units= rpm
        self.LSSGagAxs = False   #Low-speed shaft strain gage angular acceleration (on the gearbox side of the low-speed shaft) (About the xa- and xs-axes) , () units= deg/s**2
        self.GenSpeed = False   #Angular speed of the high-speed shaft and generator (Same sign as LSSGagVxa / LSSGagVxs / LSSGagV) , () units= rpm
        # Shaft Motions RotTeetA
        self.LSSTipP = False   #Rotor azimuth angle (position) (About the xa- and xs-axes) , () units= deg
        self.LSSTipV = False   #Rotor azimuth angular speed (About the xa- and xs-axes) , () units= rpm
        self.LSSTipA = False   #Rotor azimuth angular acceleration (About the xa- and xs-axes) , () units= deg/s**2
        self.LSSGagP = False   #Low-speed shaft strain gage azimuth angle (position) (on the gearbox side of the low-speed shaft) (About the xa- and xs-axes) , () units= deg
        self.LSSGagV = False   #Low-speed shaft strain gage angular speed (on the gearbox side of the low-speed shaft) (About the xa- and xs-axes) , () units= rpm
        self.LSSGagA = False   #Low-speed shaft strain gage angular acceleration (on the gearbox side of the low-speed shaft) (About the xa- and xs-axes) , () units= deg/s**2
        # Shaft Motions RotTeetA
        self.Azimuth = False   #Rotor azimuth angle (position) (About the xa- and xs-axes) , () units= deg
        self.RotSpeed = False   #Rotor azimuth angular speed (About the xa- and xs-axes) , () units= rpm
        self.RotAccel = False   #Rotor azimuth angular acceleration (About the xa- and xs-axes) , () units= deg/s**2
        # Rotor-Furl Motions 
        self.RotFurl = False   #Rotor-furl angle (position) (About the rotor-furl axis) , () units= deg
        # Tail-Furl Motions 
        self.TailFurl = False   #Tail-furl angle (position) (About the tail-furl axis) , () units= deg
        # Nacelle Yaw Motions 
        self.YawPzp = False   #Nacelle yaw angle (position) (About the zn- and zp-axes) , () units= deg
        self.YawVzp = False   #Nacelle yaw angular velocity (About the zn- and zp-axes) , () units= deg/s
        self.YawAzp = False   #Nacelle yaw angular acceleration (About the zn- and zp-axes) , () units= deg/s**2
        # Nacelle Yaw Motions 
        self.NacYawP = False   #Nacelle yaw angle (position) (About the zn- and zp-axes) , () units= deg
        self.NacYawV = False   #Nacelle yaw angular velocity (About the zn- and zp-axes) , () units= deg/s
        self.NacYawA = False   #Nacelle yaw angular acceleration (About the zn- and zp-axes) , () units= deg/s**2
        # Nacelle Yaw Motions 
        self.NacYaw = False   #Nacelle yaw angle (position) (About the zn- and zp-axes) , () units= deg
        self.YawRate = False   #Nacelle yaw angular velocity (About the zn- and zp-axes) , () units= deg/s
        self.YawAccel = False   #Nacelle yaw angular acceleration (About the zn- and zp-axes) , () units= deg/s**2
        # Nacelle Yaw Motions 
        self.YawPos = False   #Nacelle yaw angle (position) (About the zn- and zp-axes) , () units= deg


class TowerSupportMotionsOut(object):
    def __init__(self):

        # Tower-Top / Yaw Bearing Motions
        self.YawBrTDxp = False   #Tower-top / yaw bearing fore-aft (translational) deflection (relative to the undeflected position) (Directed along the xp-axis) , () units= m
        self.YawBrTDyp = False   #Tower-top / yaw bearing side-to-side (translational) deflection (relative to the undeflected position) (Directed along the yp-axis) , () units= m
        self.YawBrTDzp = False   #Tower-top / yaw bearing axial (translational) deflection (relative to the undeflected position) (Directed along the zp-axis) , () units= m
        self.YawBrTDxt = False   #Tower-top / yaw bearing fore-aft (translational) deflection (relative to the undeflected position) (Directed along the xt-axis) , () units= m
        self.YawBrTDyt = False   #Tower-top / yaw bearing side-to-side (translation) deflection (relative to the undeflected position) (Directed along the yt-axis) , () units= m
        self.YawBrTDzt = False   #Tower-top / yaw bearing axial (translational) deflection (relative to the undeflected position) (Directed along the zt-axis) , () units= m
        self.YawBrTAxp = False   #Tower-top / yaw bearing fore-aft (translational) acceleration (absolute) (Directed along the xp-axis) , () units= m/s**2
        self.YawBrTAyp = False   #Tower-top / yaw bearing side-to-side (translational) acceleration (absolute) (Directed along the yp-axis) , () units= m/s**2
        self.YawBrTAzp = False   #Tower-top / yaw bearing axial (translational) acceleration (absolute) (Directed along the zp-axis) , () units= m/s**2
        self.YawBrRDxt = False   #Tower-top / yaw bearing angular (rotational) roll deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the xt-axis) , () units= deg
        self.YawBrRDyt = False   #Tower-top / yaw bearing angular (rotational) pitch deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the yt-axis) , () units= deg
        self.YawBrRDzt = False   #Tower-top / yaw bearing angular (rotational) torsion deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the zt-axis) , () units= deg
        self.YawBrRVxp = False   #Tower-top / yaw bearing angular (rotational) roll velocity (absolute) (About the xp-axis) , () units= deg/s
        self.YawBrRVyp = False   #Tower-top / yaw bearing angular (rotational) pitch velocity (absolute) (About the yp-axis) , () units= deg/s
        self.YawBrRVzp = False   #Tower-top / yaw bearing angular (rotational) torsion velocity. This output will always be very close to zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. (absolute) (About the zp-axis) , () units= deg/s
        self.YawBrRAxp = False   #Tower-top / yaw bearing angular (rotational) roll acceleration (absolute) (About the xp-axis) , () units= deg/s**2
        self.YawBrRAyp = False   #Tower-top / yaw bearing angular (rotational) pitch acceleration (absolute) (About the yp-axis) , () units= deg/s**2
        self.YawBrRAzp = False   #Tower-top / yaw bearing angular (rotational) torsion acceleration. This output will always be very close to zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. (absolute) (About the zp-axis) , () units= deg/s**2
        # Local Tower Motions
        self.TwHt1ALxt = False   #Local tower fore-aft (translational) acceleration (absolute) of tower gage 1  (Directed along the local xt-axis) , (NTwGages < 1) units= m/s**2
        self.TwHt1ALyt = False   #Local tower side-to-side (translational) acceleration (absolute) of tower gage 1  (Directed along the local yt-axis) , (NTwGages < 1) units= m/s**2
        self.TwHt1ALzt = False   #Local tower axial (translational) acceleration (absolute) of tower gage 1  (Directed along the local zt-axis) , (NTwGages < 1) units= m/s**2
        self.TwHt2ALxt = False   #Local tower fore-aft (translational) acceleration (absolute) of tower gage 2 (Directed along the local xt-axis) , (NTwGages < 2) units= m/s**2
        self.TwHt2ALyt = False   #Local tower side-to-side (translational) acceleration (absolute) of tower gage 2 (Directed along the local yt-axis) , (NTwGages < 2) units= m/s**2
        self.TwHt2ALzt = False   #Local tower axial (translational) acceleration (absolute) of tower gage 2 (Directed along the local zt-axis) , (NTwGages < 2) units= m/s**2
        self.TwHt3ALxt = False   #Local tower fore-aft (translational) acceleration (absolute) of tower gage 3 (Directed along the local xt-axis) , (NTwGages < 3) units= m/s**2
        self.TwHt3ALyt = False   #Local tower side-to-side (translational) acceleration (absolute) of tower gage 3 (Directed along the local yt-axis) , (NTwGages < 3) units= m/s**2
        self.TwHt3ALzt = False   #Local tower axial (translational) acceleration (absolute) of tower gage 3 (Directed along the local zt-axis) , (NTwGages < 3) units= m/s**2
        self.TwHt4ALxt = False   #Local tower fore-aft (translational) acceleration (absolute) of tower gage 4 (Directed along the local xt-axis) , (NTwGages < 4) units= m/s**2
        self.TwHt4ALyt = False   #Local tower side-to-side (translational) acceleration (absolute) of tower gage 4 (Directed along the local yt-axis) , (NTwGages < 4) units= m/s**2
        self.TwHt4ALzt = False   #Local tower axial (translational) acceleration (absolute) of tower gage 4 (Directed along the local zt-axis) , (NTwGages < 4) units= m/s**2
        self.TwHt5ALxt = False   #Local tower fore-aft (translational) acceleration (absolute) of tower gage 5 (Directed along the local xt-axis) , (NTwGages < 5) units= m/s**2
        self.TwHt5ALyt = False   #Local tower side-to-side (translational) acceleration (absolute) of tower gage 5 (Directed along the local yt-axis) , (NTwGages < 5) units= m/s**2
        self.TwHt5ALzt = False   #Local tower axial (translational) acceleration (absolute) of tower gage 5 (Directed along the local zt-axis) , (NTwGages < 5) units= m/s**2
        self.TwHt6ALxt = False   #Local tower fore-aft (translational) acceleration (absolute) of tower gage 6 (Directed along the local xt-axis) , (NTwGages < 6) units= m/s**2
        self.TwHt6ALyt = False   #Local tower side-to-side (translational) acceleration (absolute) of tower gage 6 (Directed along the local yt-axis) , (NTwGages < 6) units= m/s**2
        self.TwHt6ALzt = False   #Local tower axial (translational) acceleration (absolute) of tower gage 6 (Directed along the local zt-axis) , (NTwGages < 6) units= m/s**2
        self.TwHt7ALxt = False   #Local tower fore-aft (translational) acceleration (absolute) of tower gage 7 (Directed along the local xt-axis) , (NTwGages < 7) units= m/s**2
        self.TwHt7ALyt = False   #Local tower side-to-side (translational) acceleration (absolute) of tower gage 7 (Directed along the local yt-axis) , (NTwGages < 7) units= m/s**2
        self.TwHt7ALzt = False   #Local tower axial (translational) acceleration (absolute) of tower gage 7 (Directed along the local zt-axis) , (NTwGages < 7) units= m/s**2
        self.TwHt8ALxt = False   #Local tower fore-aft (translational) acceleration (absolute) of tower gage 8 (Directed along the local xt-axis) , (NTwGages < 8) units= m/s**2
        self.TwHt8ALyt = False   #Local tower side-to-side (translational) acceleration (absolute) of tower gage 8 (Directed along the local yt-axis) , (NTwGages < 8) units= m/s**2
        self.TwHt8ALzt = False   #Local tower axial (translational) acceleration (absolute) of tower gage 8 (Directed along the local zt-axis) , (NTwGages < 8) units= m/s**2
        self.TwHt9ALxt = False   #Local tower fore-aft (translational) acceleration (absolute) of tower gage 9 (Directed along the local xt-axis) , (NTwGages < 9) units= m/s**2
        self.TwHt9ALyt = False   #Local tower side-to-side (translational) acceleration (absolute) of tower gage 9 (Directed along the local yt-axis) , (NTwGages < 9) units= m/s**2
        self.TwHt9ALzt = False   #Local tower axial (translational) acceleration (absolute) of tower gage 9 (Directed along the local zt-axis) , (NTwGages < 9) units= m/s**2
        self.TwHt1TDxt = False   #Local tower fore-aft (translational) deflection (relative to the undeflected position) of tower gage 1 (Directed along the local xt-axis) , (NTwGages < 1) units= m
        self.TwHt1TDyt = False   #Local tower side-to-side (translational) deflection (relative to the undeflected position) of tower gage 1 (Directed along the local yt-axis) , (NTwGages < 1) units= m
        self.TwHt1TDzt = False   #Local tower axial (translational) deflection (relative to the undeflected position) of tower gage 1 (Directed along the local zt-axis) , (NTwGages < 1) units= m
        self.TwHt2TDxt = False   #Local tower fore-aft (translational) deflection (relative to the undeflected position) of tower gage 2 (Directed along the local xt-axis) , (NTwGages < 2) units= m
        self.TwHt2TDyt = False   #Local tower side-to-side (translational) deflection (relative to the undeflected position) of tower gage 2 (Directed along the local yt-axis) , (NTwGages < 2) units= m
        self.TwHt2TDzt = False   #Local tower axial (translational) deflection (relative to the undeflected position) of tower gage 2 (Directed along the local zt-axis) , (NTwGages < 2) units= m
        self.TwHt3TDxt = False   #Local tower fore-aft (translational) deflection (relative to the undeflected position) of tower gage 3 (Directed along the local xt-axis) , (NTwGages < 3) units= m
        self.TwHt3TDyt = False   #Local tower side-to-side (translational) deflection (relative to the undeflected position) of tower gage 3 (Directed along the local yt-axis) , (NTwGages < 3) units= m
        self.TwHt3TDzt = False   #Local tower axial (translational) deflection (relative to the undeflected position) of tower gage 3 (Directed along the local zt-axis) , (NTwGages < 3) units= m
        self.TwHt4TDxt = False   #Local tower fore-aft (translational) deflection (relative to the undeflected position) of tower gage 4 (Directed along the local xt-axis) , (NTwGages < 4) units= m
        self.TwHt4TDyt = False   #Local tower side-to-side (translational) deflection (relative to the undeflected position) of tower gage 4 (Directed along the local yt-axis) , (NTwGages < 4) units= m
        self.TwHt4TDzt = False   #Local tower axial (translational) deflection (relative to the undeflected position) of tower gage 4 (Directed along the local zt-axis) , (NTwGages < 4) units= m
        self.TwHt5TDxt = False   #Local tower fore-aft (translational) deflection (relative to the undeflected position) of tower gage 5 (Directed along the local xt-axis) , (NTwGages < 5) units= m
        self.TwHt5TDyt = False   #Local tower side-to-side (translational) deflection (relative to the undeflected position) of tower gage 5 (Directed along the local yt-axis) , (NTwGages < 5) units= m
        self.TwHt5TDzt = False   #Local tower axial (translational) deflection (relative to the undeflected position) of tower gage 5 (Directed along the local zt-axis) , (NTwGages < 5) units= m
        self.TwHt6TDxt = False   #Local tower fore-aft (translational) deflection (relative to the undeflected position) of tower gage 6 (Directed along the local xt-axis) , (NTwGages < 6) units= m
        self.TwHt6TDyt = False   #Local tower side-to-side (translational) deflection (relative to the undeflected position) of tower gage 6 (Directed along the local yt-axis) , (NTwGages < 6) units= m
        self.TwHt6TDzt = False   #Local tower axial (translational) deflection (relative to the undeflected position) of tower gage 6 (Directed along the local zt-axis) , (NTwGages < 6) units= m
        self.TwHt7TDxt = False   #Local tower fore-aft (translational) deflection (relative to the undeflected position) of tower gage 7 (Directed along the local xt-axis) , (NTwGages < 7) units= m
        self.TwHt7TDyt = False   #Local tower side-to-side (translational) deflection (relative to the undeflected position) of tower gage 7 (Directed along the local yt-axis) , (NTwGages < 7) units= m
        self.TwHt7TDzt = False   #Local tower axial (translational) deflection (relative to the undeflected position) of tower gage 7 (Directed along the local zt-axis) , (NTwGages < 7) units= m
        self.TwHt8TDxt = False   #Local tower fore-aft (translational) deflection (relative to the undeflected position) of tower gage 8 (Directed along the local xt-axis) , (NTwGages < 8) units= m
        self.TwHt8TDyt = False   #Local tower side-to-side (translational) deflection (relative to the undeflected position) of tower gage 8 (Directed along the local yt-axis) , (NTwGages < 8) units= m
        self.TwHt8TDzt = False   #Local tower axial (translational) deflection (relative to the undeflected position) of tower gage 8 (Directed along the local zt-axis) , (NTwGages < 8) units= m
        self.TwHt9TDxt = False   #Local tower fore-aft (translational) deflection (relative to the undeflected position) of tower gage 9 (Directed along the local xt-axis) , (NTwGages < 9) units= m
        self.TwHt9TDyt = False   #Local tower side-to-side (translational) deflection (relative to the undeflected position) of tower gage 9 (Directed along the local yt-axis) , (NTwGages < 9) units= m
        self.TwHt9TDzt = False   #Local tower axial (translational) deflection (relative to the undeflected position) of tower gage 9 (Directed along the local zt-axis) , (NTwGages < 9) units= m
        self.TwHt1RDxt = False   #Local tower angular (rotational) roll deflection (relative to the undeflected position) of tower gage 1. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local xt-axis) , (NTwGages < 1) units= deg
        self.TwHt1RDyt = False   #Local tower angular (rotational) pitch deflection (relative to the undeflected position) of tower gage 1. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local yt-axis) , (NTwGages < 1) units= deg
        self.TwHt1RDzt = False   #Local tower angular (rotational) torsion deflection (relative to the undeflected position) of tower gage 1. This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the local zt-axis) , (NTwGages < 1) units= deg
        self.TwHt2RDxt = False   #Local tower angular (rotational) roll deflection (relative to the undeflected position) of tower gage 2. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local xt-axis) , (NTwGages < 2) units= deg
        self.TwHt2RDyt = False   #Local tower angular (rotational) pitch deflection (relative to the undeflected position) of tower gage 2. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local yt-axis) , (NTwGages < 2) units= deg
        self.TwHt2RDzt = False   #Local tower angular (rotational) torsion deflection (relative to the undeflected position) of tower gage 2. This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the local zt-axis) , (NTwGages < 2) units= deg
        self.TwHt3RDxt = False   #Local tower angular (rotational) roll deflection (relative to the undeflected position) of tower gage 3. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local xt-axis) , (NTwGages < 3) units= deg
        self.TwHt3RDyt = False   #Local tower angular (rotational) pitch deflection (relative to the undeflected position) of tower gage 3. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local yt-axis) , (NTwGages < 3) units= deg
        self.TwHt3RDzt = False   #Local tower angular (rotational) torsion deflection (relative to the undeflected position) of tower gage 3. This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the local zt-axis) , (NTwGages < 3) units= deg
        self.TwHt4RDxt = False   #Local tower angular (rotational) roll deflection (relative to the undeflected position) of tower gage 4. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local xt-axis) , (NTwGages < 4) units= deg
        self.TwHt4RDyt = False   #Local tower angular (rotational) pitch deflection (relative to the undeflected position) of tower gage 4. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local yt-axis) , (NTwGages < 4) units= deg
        self.TwHt4RDzt = False   #Local tower angular (rotational) torsion deflection (relative to the undeflected position) of tower gage 4. This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the local zt-axis) , (NTwGages < 4) units= deg
        self.TwHt5RDxt = False   #Local tower angular (rotational) roll deflection (relative to the undeflected position) of tower gage 5. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local xt-axis) , (NTwGages < 5) units= deg
        self.TwHt5RDyt = False   #Local tower angular (rotational) pitch deflection (relative to the undeflected position) of tower gage 5. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local yt-axis) , (NTwGages < 5) units= deg
        self.TwHt5RDzt = False   #Local tower angular (rotational) torsion deflection (relative to the undeflected position) of tower gage 5. This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the local zt-axis) , (NTwGages < 5) units= deg
        self.TwHt6RDxt = False   #Local tower angular (rotational) roll deflection (relative to the undeflected position) of tower gage 6. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local xt-axis) , (NTwGages < 6) units= deg
        self.TwHt6RDyt = False   #Local tower angular (rotational) pitch deflection (relative to the undeflected position) of tower gage 6. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local yt-axis) , (NTwGages < 6) units= deg
        self.TwHt6RDzt = False   #Local tower angular (rotational) torsion deflection (relative to the undeflected position) of tower gage 6. This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the local zt-axis) , (NTwGages < 6) units= deg
        self.TwHt7RDxt = False   #Local tower angular (rotational) roll deflection (relative to the undeflected position) of tower gage 7. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local xt-axis) , (NTwGages < 7) units= deg
        self.TwHt7RDyt = False   #Local tower angular (rotational) pitch deflection (relative to the undeflected position) of tower gage 7. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local yt-axis) , (NTwGages < 7) units= deg
        self.TwHt7RDzt = False   #Local tower angular (rotational) torsion deflection (relative to the undeflected position) of tower gage 7. This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the local zt-axis) , (NTwGages < 7) units= deg
        self.TwHt8RDxt = False   #Local tower angular (rotational) roll deflection (relative to the undeflected position) of tower gage 8. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local xt-axis) , (NTwGages < 8) units= deg
        self.TwHt8RDyt = False   #Local tower angular (rotational) pitch deflection (relative to the undeflected position) of tower gage 8. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local yt-axis) , (NTwGages < 8) units= deg
        self.TwHt8RDzt = False   #Local tower angular (rotational) torsion deflection (relative to the undeflected position) of tower gage 8. This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the local zt-axis) , (NTwGages < 8) units= deg
        self.TwHt9RDxt = False   #Local tower angular (rotational) roll deflection (relative to the undeflected position) of tower gage 9. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local xt-axis) , (NTwGages < 9) units= deg
        self.TwHt9RDyt = False   #Local tower angular (rotational) pitch deflection (relative to the undeflected position) of tower gage 9. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the local yt-axis) , (NTwGages < 9) units= deg
        self.TwHt9RDzt = False   #Local tower angular (rotational) torsion deflection (relative to the undeflected position) of tower gage 9. This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the local zt-axis) , (NTwGages < 9) units= deg
        self.TwHt1TPxi = False   #xi-component of the translational position (relative to the inertia frame) of tower gage 1 (Directed along the local xi-axis) , (NTwGages < 1) units= m
        self.TwHt1TPyi = False   #yi-component of the translational position (relative to the inertia frame) of tower gage 1 (Directed along the local yi-axis) , (NTwGages < 1) units= m
        self.TwHt1TPzi = False   #zi-component of the translational position (relative to ground level [onshore] or MSL [offshore]) of tower gage 1 (Directed along the local zi-axis) , (NTwGages < 1) units= m
        self.TwHt2TPxi = False   #xi-component of the translational position (relative to the inertia frame) of tower gage 2 (Directed along the local xi-axis) , (NTwGages < 2) units= m
        self.TwHt2TPyi = False   #yi-component of the translational position (relative to the inertia frame) of tower gage 2 (Directed along the local yi-axis) , (NTwGages < 2) units= m
        self.TwHt2TPzi = False   #zi-component of the translational position (relative to ground level [onshore] or MSL [offshore]) of tower gage 2 (Directed along the local zi-axis) , (NTwGages < 2) units= m
        self.TwHt3TPxi = False   #xi-component of the translational position (relative to the inertia frame) of tower gage 3 (Directed along the local xi-axis) , (NTwGages < 3) units= m
        self.TwHt3TPyi = False   #yi-component of the translational position (relative to the inertia frame) of tower gage 3 (Directed along the local yi-axis) , (NTwGages < 3) units= m
        self.TwHt3TPzi = False   #zi-component of the translational position (relative to ground level [onshore] or MSL [offshore]) of tower gage 3 (Directed along the local zi-axis) , (NTwGages < 3) units= m
        self.TwHt4TPxi = False   #xi-component of the translational position (relative to the inertia frame) of tower gage 4 (Directed along the local xi-axis) , (NTwGages < 4) units= m
        self.TwHt4TPyi = False   #yi-component of the translational position (relative to the inertia frame) of tower gage 4 (Directed along the local yi-axis) , (NTwGages < 4) units= m
        self.TwHt4TPzi = False   #zi-component of the translational position (relative to ground level [onshore] or MSL [offshore]) of tower gage 4 (Directed along the local zi-axis) , (NTwGages < 4) units= m
        self.TwHt5TPxi = False   #xi-component of the translational position (relative to the inertia frame) of tower gage 5 (Directed along the local xi-axis) , (NTwGages < 5) units= m
        self.TwHt5TPyi = False   #yi-component of the translational position (relative to the inertia frame) of tower gage 5 (Directed along the local yi-axis) , (NTwGages < 5) units= m
        self.TwHt5TPzi = False   #zi-component of the translational position (relative to ground level [onshore] or MSL [offshore]) of tower gage 5 (Directed along the local zi-axis) , (NTwGages < 5) units= m
        self.TwHt6TPxi = False   #xi-component of the translational position (relative to the inertia frame) of tower gage 6 (Directed along the local xi-axis) , (NTwGages < 6) units= m
        self.TwHt6TPyi = False   #yi-component of the translational position (relative to the inertia frame) of tower gage 6 (Directed along the local yi-axis) , (NTwGages < 6) units= m
        self.TwHt6TPzi = False   #zi-component of the translational position (relative to ground level [onshore] or MSL [offshore]) of tower gage 6 (Directed along the local zi-axis) , (NTwGages < 6) units= m
        self.TwHt7TPxi = False   #xi-component of the translational position (relative to the inertia frame) of tower gage 7 (Directed along the local xi-axis) , (NTwGages < 7) units= m
        self.TwHt7TPyi = False   #yi-component of the translational position (relative to the inertia frame) of tower gage 7 (Directed along the local yi-axis) , (NTwGages < 7) units= m
        self.TwHt7TPzi = False   #zi-component of the translational position (relative to ground level [onshore] or MSL [offshore]) of tower gage 7 (Directed along the local zi-axis) , (NTwGages < 7) units= m
        self.TwHt8TPxi = False   #xi-component of the translational position (relative to the inertia frame) of tower gage 8 (Directed along the local xi-axis) , (NTwGages < 8) units= m
        self.TwHt8TPyi = False   #yi-component of the translational position (relative to the inertia frame) of tower gage 8 (Directed along the local yi-axis) , (NTwGages < 8) units= m
        self.TwHt8TPzi = False   #zi-component of the translational position (relative to ground level [onshore] or MSL [offshore]) of tower gage 8 (Directed along the local zi-axis) , (NTwGages < 8) units= m
        self.TwHt9TPxi = False   #xi-component of the translational position (relative to the inertia frame) of tower gage 9 (Directed along the local xi-axis) , (NTwGages < 9) units= m
        self.TwHt9TPyi = False   #yi-component of the translational position (relative to the inertia frame) of tower gage 9 (Directed along the local yi-axis) , (NTwGages < 9) units= m
        self.TwHt9TPzi = False   #zi-component of the translational position (relative to ground level [onshore] or MSL [offshore]) of tower gage 9 (Directed along the local zi-axis) , (NTwGages < 9) units= m
        self.TwHt1RPxi = False   #xi-component of the rotational position (relative to the inertia frame) of tower gage 1. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local xi-axis) , (NTwGages < 1) units= deg
        self.TwHt1RPyi = False   #yi-component of the rotational position (relative to the inertia frame) of tower gage 1. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local yi-axis) , (NTwGages < 1) units= deg
        self.TwHt1RPzi = False   #zi-component of the rotational position (relative to the inertia frame) of tower gage 1. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local zi-axis) , (NTwGages < 1) units= deg
        self.TwHt2RPxi = False   #xi-component of the rotational position (relative to the inertia frame) of tower gage 2. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local xi-axis) , (NTwGages < 2) units= deg
        self.TwHt2RPyi = False   #yi-component of the rotational position (relative to the inertia frame) of tower gage 2. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local yi-axis) , (NTwGages < 2) units= deg
        self.TwHt2RPzi = False   #zi-component of the rotational position (relative to the inertia frame) of tower gage 2. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local zi-axis) , (NTwGages < 2) units= deg
        self.TwHt3RPxi = False   #xi-component of the rotational position (relative to the inertia frame) of tower gage 3. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local xi-axis) , (NTwGages < 3) units= deg
        self.TwHt3RPyi = False   #yi-component of the rotational position (relative to the inertia frame) of tower gage 3. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local yi-axis) , (NTwGages < 3) units= deg
        self.TwHt3RPzi = False   #zi-component of the rotational position (relative to the inertia frame) of tower gage 3. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local zi-axis) , (NTwGages < 3) units= deg
        self.TwHt4RPxi = False   #xi-component of the rotational position (relative to the inertia frame) of tower gage 4. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local xi-axis) , (NTwGages < 4) units= deg
        self.TwHt4RPyi = False   #yi-component of the rotational position (relative to the inertia frame) of tower gage 4. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local yi-axis) , (NTwGages < 4) units= deg
        self.TwHt4RPzi = False   #zi-component of the rotational position (relative to the inertia frame) of tower gage 4. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local zi-axis) , (NTwGages < 4) units= deg
        self.TwHt5RPxi = False   #xi-component of the rotational position (relative to the inertia frame) of tower gage 5. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local xi-axis) , (NTwGages < 5) units= deg
        self.TwHt5RPyi = False   #yi-component of the rotational position (relative to the inertia frame) of tower gage 5. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local yi-axis) , (NTwGages < 5) units= deg
        self.TwHt5RPzi = False   #zi-component of the rotational position (relative to the inertia frame) of tower gage 5. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local zi-axis) , (NTwGages < 5) units= deg
        self.TwHt6RPxi = False   #xi-component of the rotational position (relative to the inertia frame) of tower gage 6. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local xi-axis) , (NTwGages < 6) units= deg
        self.TwHt6RPyi = False   #yi-component of the rotational position (relative to the inertia frame) of tower gage 6. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local yi-axis) , (NTwGages < 6) units= deg
        self.TwHt6RPzi = False   #zi-component of the rotational position (relative to the inertia frame) of tower gage 6. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local zi-axis) , (NTwGages < 6) units= deg
        self.TwHt7RPxi = False   #xi-component of the rotational position (relative to the inertia frame) of tower gage 7. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local xi-axis) , (NTwGages < 7) units= deg
        self.TwHt7RPyi = False   #yi-component of the rotational position (relative to the inertia frame) of tower gage 7. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local yi-axis) , (NTwGages < 7) units= deg
        self.TwHt7RPzi = False   #zi-component of the rotational position (relative to the inertia frame) of tower gage 7. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local zi-axis) , (NTwGages < 7) units= deg
        self.TwHt8RPxi = False   #xi-component of the rotational position (relative to the inertia frame) of tower gage 8. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local xi-axis) , (NTwGages < 8) units= deg
        self.TwHt8RPyi = False   #yi-component of the rotational position (relative to the inertia frame) of tower gage 8. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local yi-axis) , (NTwGages < 8) units= deg
        self.TwHt8RPzi = False   #zi-component of the rotational position (relative to the inertia frame) of tower gage 8. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local zi-axis) , (NTwGages < 8) units= deg
        self.TwHt9RPxi = False   #xi-component of the rotational position (relative to the inertia frame) of tower gage 9. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local xi-axis) , (NTwGages < 9) units= deg
        self.TwHt9RPyi = False   #yi-component of the rotational position (relative to the inertia frame) of tower gage 9. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local yi-axis) , (NTwGages < 9) units= deg
        self.TwHt9RPzi = False   #zi-component of the rotational position (relative to the inertia frame) of tower gage 9. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower and platform rotational deflections, so that the rotation sequence does not matter. (About the local zi-axis) , (NTwGages < 9) units= deg
        # Platform Motions
        self.PtfmTDxt = False   #Platform horizontal surge (translational) displacement (Directed along the xt-axis) , () units= m
        self.PtfmTDyt = False   #Platform horizontal sway (translational) displacement (Directed along the yt-axis) , () units= m
        self.PtfmTDzt = False   #Platform vertical heave (translational) displacement (Directed along the zt-axis) , () units= m
        self.PtfmTDxi = False   #Platform horizontal surge (translational) displacement (Directed along the xi-axis) , () units= m
        self.PtfmTDyi = False   #Platform horizontal sway (translational) displacement (Directed along the yi-axis) , () units= m
        self.PtfmTDzi = False   #Platform vertical heave (translational) displacement (Directed along the zi-axis) , () units= m
        self.PtfmTVxt = False   #Platform horizontal surge (translational) velocity (Directed along the xt-axis) , () units= m/s
        self.PtfmTVyt = False   #Platform horizontal sway (translational) velocity (Directed along the yt-axis) , () units= m/s
        self.PtfmTVzt = False   #Platform vertical heave (translational) velocity (Directed along the zt-axis) , () units= m/s
        self.PtfmTVxi = False   #Platform horizontal surge (translational) velocity (Directed along the xi-axis) , () units= m/s
        self.PtfmTVyi = False   #Platform horizontal sway (translational) velocity (Directed along the yi-axis) , () units= m/s
        self.PtfmTVzi = False   #Platform vertical heave (translational) velocity (Directed along the zi-axis) , () units= m/s
        self.PtfmTAxt = False   #Platform horizontal surge (translational) acceleration (Directed along the xt-axis) , () units= m/s**2
        self.PtfmTAyt = False   #Platform horizontal sway (translational) acceleration (Directed along the yt-axis) , () units= m/s**2
        self.PtfmTAzt = False   #Platform vertical heave (translational) acceleration (Directed along the zt-axis) , () units= m/s**2
        self.PtfmTAxi = False   #Platform horizontal surge (translational) acceleration (Directed along the xi-axis) , () units= m/s**2
        self.PtfmTAyi = False   #Platform horizontal sway (translational) acceleration (Directed along the yi-axis) , () units= m/s**2
        self.PtfmTAzi = False   #Platform vertical heave (translational) acceleration (Directed along the zi-axis) , () units= m/s**2
        self.PtfmRDxi = False   #Platform roll tilt angular (rotational) displacement. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small rotational platform displacements, so that the rotation sequence does not matter. (About the xi-axis) , () units= deg
        self.PtfmRDyi = False   #Platform pitch tilt angular (rotational) displacement. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small rotational platform displacements, so that the rotation sequence does not matter. (About the yi-axis) , () units= deg
        self.PtfmRDzi = False   #Platform yaw angular (rotational) displacement. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small rotational platform displacements, so that the rotation sequence does not matter. (About the zi-axis) , () units= deg
        self.PtfmRVxt = False   #Platform roll tilt angular (rotational) velocity (About the xt-axis) , () units= deg/s
        self.PtfmRVyt = False   #Platform pitch tilt angular (rotational) velocity (About the yt-axis) , () units= deg/s
        self.PtfmRVzt = False   #Platform yaw angular (rotational) velocity (About the zt-axis) , () units= deg/s
        self.PtfmRVxi = False   #Platform roll tilt angular (rotational) velocity (About the xi-axis) , () units= deg/s
        self.PtfmRVyi = False   #Platform pitch tilt angular (rotational) velocity (About the yi-axis) , () units= deg/s
        self.PtfmRVzi = False   #Platform yaw angular (rotational) velocity (About the zi-axis) , () units= deg/s
        self.PtfmRAxt = False   #Platform roll tilt angular (rotational) acceleration (About the xt-axis) , () units= deg/s**2
        self.PtfmRAyt = False   #Platform pitch tilt angular (rotational) acceleration (About the yt-axis) , () units= deg/s**2
        self.PtfmRAzt = False   #Platform yaw angular (rotational) acceleration (About the zt-axis) , () units= deg/s**2
        self.PtfmRAxi = False   #Platform roll tilt angular (rotational) acceleration (About the xi-axis) , () units= deg/s**2
        self.PtfmRAyi = False   #Platform pitch tilt angular (rotational) acceleration (About the yi-axis) , () units= deg/s**2
        self.PtfmRAzi = False   #Platform yaw angular (rotational) acceleration (About the zi-axis) , () units= deg/s**2

        #Other Names
        # Tower-Top / Yaw Bearing Motions 
        self.TTDspFA = False   #Tower-top / yaw bearing fore-aft (translational) deflection (relative to the undeflected position) (Directed along the xt-axis) , () units= m
        self.TTDspSS = False   #Tower-top / yaw bearing side-to-side (translation) deflection (relative to the undeflected position) (Directed along the yt-axis) , () units= m
        self.TTDspAx = False   #Tower-top / yaw bearing axial (translational) deflection (relative to the undeflected position) (Directed along the zt-axis) , () units= m
        self.TTDspRoll = False   #Tower-top / yaw bearing angular (rotational) roll deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the xt-axis) , () units= deg
        self.TTDspPtch = False   #Tower-top / yaw bearing angular (rotational) pitch deflection (relative to the undeflected position). In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small tower deflections, so that the rotation sequence does not matter. (About the yt-axis) , () units= deg
        self.TTDspTwst = False   #Tower-top / yaw bearing angular (rotational) torsion deflection (relative to the undeflected position). This output will always be zero for FAST simulation results. Use it for examining tower torsional deflections of ADAMS simulations run using ADAMS datasets created using the FAST-to-ADAMS preprocessor. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. (About the zt-axis) , () units= deg
        # Platform Motions 
        self.PtfmSurge = False   #Platform horizontal surge (translational) displacement (Directed along the xi-axis) , () units= m
        self.PtfmSway = False   #Platform horizontal sway (translational) displacement (Directed along the yi-axis) , () units= m
        self.PtfmHeave = False   #Platform vertical heave (translational) displacement (Directed along the zi-axis) , () units= m
        self.PtfmRoll = False   #Platform roll tilt angular (rotational) displacement. In ADAMS, it is output as an Euler angle computed as the 3rd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small rotational platform displacements, so that the rotation sequence does not matter. (About the xi-axis) , () units= deg
        self.PtfmPitch = False   #Platform pitch tilt angular (rotational) displacement. In ADAMS, it is output as an Euler angle computed as the 2nd rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small rotational platform displacements, so that the rotation sequence does not matter. (About the yi-axis) , () units= deg
        self.PtfmYaw = False   #Platform yaw angular (rotational) displacement. In ADAMS, it is output as an Euler angle computed as the 1st rotation in the yaw-pitch-roll rotation sequence. It is not output as an Euler angle in FAST, which assumes small rotational platform displacements, so that the rotation sequence does not matter. (About the zi-axis) , () units= deg


class BladeLoadsOut(object):
    def __init__(self):

        # Blade 1 Root Loads
        self.RootFxc1 = False   #Blade 1 out-of-plane shear force at the blade root (Directed along the xc1-axis) , () units= kN
        self.RootFyc1 = False   #Blade 1 in-plane shear force at the blade root (Directed along the yc1-axis) , () units= kN
        self.RootFzc1 = False   #Blade 1 axial force at the blade root (Directed along the zc1- and zb1-axes) , () units= kN
        self.RootFxb1 = False   #Blade 1 flapwise shear force at the blade root (Directed along the xb1-axis) , () units= kN
        self.RootFyb1 = False   #Blade 1 edgewise shear force at the blade root (Directed along the yb1-axis) , () units= kN
        self.RootMxc1 = False   #Blade 1 in-plane moment (i.e., the moment caused by in-plane forces) at the blade root (About the xc1-axis) , () units= kN*m
        self.RootMyc1 = False   #Blade 1 out-of-plane moment (i.e., the moment caused by out-of-plane forces) at the blade root (About the yc1-axis) , () units= kN*m
        self.RootMzc1 = False   #Blade 1 pitching moment at the blade root (About the zc1- and zb1-axes) , () units= kN*m
        self.RootMxb1 = False   #Blade 1 edgewise moment (i.e., the moment caused by edgewise forces) at the blade root (About the xb1-axis) , () units= kN*m
        self.RootMyb1 = False   #Blade 1 flapwise moment (i.e., the moment caused by flapwise forces) at the blade root (About the yb1-axis) , () units= kN*m
        # Blade 2 Root Loads
        self.RootFxc2 = False   #Blade 2 out-of-plane shear force at the blade root (Directed along the xc2-axis) , () units= kN
        self.RootFyc2 = False   #Blade 2 in-plane shear force at the blade root (Directed along the yc2-axis) , () units= kN
        self.RootFzc2 = False   #Blade 2 axial force at the blade root (Directed along the zc2- and zb2-axes) , () units= kN
        self.RootFxb2 = False   #Blade 2 flapwise shear force at the blade root (Directed along the xb2-axis) , () units= kN
        self.RootFyb2 = False   #Blade 2 edgewise shear force at the blade root (Directed along the yb2-axis) , () units= kN
        self.RootMxc2 = False   #Blade 2 in-plane moment (i.e., the moment caused by in-plane forces) at the blade root (About the xc2-axis) , () units= kN*m
        self.RootMyc2 = False   #Blade 2 out-of-plane moment (i.e., the moment caused by out-of-plane forces) at the blade root (About the yc2-axis) , () units= kN*m
        self.RootMzc2 = False   #Blade 2 pitching moment at the blade root (About the zc2- and zb2-axes) , () units= kN*m
        self.RootMxb2 = False   #Blade 2 edgewise moment (i.e., the moment caused by edgewise forces) at the blade root (About the xb2-axis) , () units= kN*m
        self.RootMyb2 = False   #Blade 2 flapwise moment (i.e., the moment caused by flapwise forces) at the blade root (About the yb2-axis) , () units= kN*m
        # Blade 3 Root Loads
        self.RootFxc3 = False   #Blade 3 out-of-plane shear force at the blade root (Directed along the xc3-axis) , (NumBl < 3) units= kN
        self.RootFyc3 = False   #Blade 3 in-plane shear force at the blade root (Directed along the yc3-axis) , (NumBl < 3) units= kN
        self.RootFzc3 = False   #Blade 3 axial force at the blade root (Directed along the zc3- and zb3-axes) , (NumBl < 3) units= kN
        self.RootFxb3 = False   #Blade 3 flapwise shear force at the blade root (Directed along the xb3-axis) , (NumBl < 3) units= kN
        self.RootFyb3 = False   #Blade 3 edgewise shear force at the blade root (Directed along the yb3-axis) , (NumBl < 3) units= kN
        self.RootMxc3 = False   #Blade 3 in-plane moment (i.e., the moment caused by in-plane forces) at the blade root (About the xc3-axis) , (NumBl < 3) units= kN*m
        self.RootMyc3 = False   #Blade 3 out-of-plane moment (i.e., the moment caused by out-of-plane forces) at the blade root (About the yc3-axis) , (NumBl < 3) units= kN*m
        self.RootMzc3 = False   #Blade 3 pitching moment at the blade root (About the zc3- and zb3-axes) , (NumBl < 3) units= kN*m
        self.RootMxb3 = False   #Blade 3 edgewise moment (i.e., the moment caused by edgewise forces) at the blade root (About the xb3-axis) , (NumBl < 3) units= kN*m
        self.RootMyb3 = False   #Blade 3 flapwise moment (i.e., the moment caused by flapwise forces) at the blade root (About the yb3-axis) , (NumBl < 3) units= kN*m
        # Blade 1 Local Span Loads
        self.Spn1MLxb1 = False   #Blade 1 local edgewise moment at span station 1 (About the local xb1-axis) , (NBlGages < 1) units= kN*m
        self.Spn1MLyb1 = False   #Blade 1 local flapwise moment at span station 1 (About the local yb1-axis) , (NBlGages < 1) units= kN*m
        self.Spn1MLzb1 = False   #Blade 1 local pitching moment at span station 1 (About the local zb1-axis) , (NBlGages < 1) units= kN*m
        self.Spn2MLxb1 = False   #Blade 1 local edgewise moment at span station 2 (About the local xb1-axis) , (NBlGages < 2) units= kN*m
        self.Spn2MLyb1 = False   #Blade 1 local flapwise moment at span station 2 (About the local yb1-axis) , (NBlGages < 2) units= kN*m
        self.Spn2MLzb1 = False   #Blade 1 local pitching moment at span station 2 (About the local zb1-axis) , (NBlGages < 2) units= kN*m
        self.Spn3MLxb1 = False   #Blade 1 local edgewise moment at span station 3 (About the local xb1-axis) , (NBlGages < 3) units= kN*m
        self.Spn3MLyb1 = False   #Blade 1 local flapwise moment at span station 3 (About the local yb1-axis) , (NBlGages < 3) units= kN*m
        self.Spn3MLzb1 = False   #Blade 1 local pitching moment at span station 3 (About the local zb1-axis) , (NBlGages < 3) units= kN*m
        self.Spn4MLxb1 = False   #Blade 1 local edgewise moment at span station 4 (About the local xb1-axis) , (NBlGages < 4) units= kN*m
        self.Spn4MLyb1 = False   #Blade 1 local flapwise moment at span station 4 (About the local yb1-axis) , (NBlGages < 4) units= kN*m
        self.Spn4MLzb1 = False   #Blade 1 local pitching moment at span station 4 (About the local zb1-axis) , (NBlGages < 4) units= kN*m
        self.Spn5MLxb1 = False   #Blade 1 local edgewise moment at span station 5 (About the local xb1-axis) , (NBlGages < 5) units= kN*m
        self.Spn5MLyb1 = False   #Blade 1 local flapwise moment at span station 5 (About the local yb1-axis) , (NBlGages < 5) units= kN*m
        self.Spn5MLzb1 = False   #Blade 1 local pitching moment at span station 5 (About the local zb1-axis) , (NBlGages < 5) units= kN*m
        self.Spn6MLxb1 = False   #Blade 1 local edgewise moment at span station 6 (About the local xb1-axis) , (NBlGages < 6) units= kN*m
        self.Spn6MLyb1 = False   #Blade 1 local flapwise moment at span station 6 (About the local yb1-axis) , (NBlGages < 6) units= kN*m
        self.Spn6MLzb1 = False   #Blade 1 local pitching moment at span station 6 (About the local zb1-axis) , (NBlGages < 6) units= kN*m
        self.Spn7MLxb1 = False   #Blade 1 local edgewise moment at span station 7 (About the local xb1-axis) , (NBlGages < 7) units= kN*m
        self.Spn7MLyb1 = False   #Blade 1 local flapwise moment at span station 7 (About the local yb1-axis) , (NBlGages < 7) units= kN*m
        self.Spn7MLzb1 = False   #Blade 1 local pitching moment at span station 7 (About the local zb1-axis) , (NBlGages < 7) units= kN*m
        self.Spn8MLxb1 = False   #Blade 1 local edgewise moment at span station 8 (About the local xb1-axis) , (NBlGages < 8) units= kN*m
        self.Spn8MLyb1 = False   #Blade 1 local flapwise moment at span station 8 (About the local yb1-axis) , (NBlGages < 8) units= kN*m
        self.Spn8MLzb1 = False   #Blade 1 local pitching moment at span station 8 (About the local zb1-axis) , (NBlGages < 8) units= kN*m
        self.Spn9MLxb1 = False   #Blade 1 local edgewise moment at span station 9 (About the local xb1-axis) , (NBlGages < 9) units= kN*m
        self.Spn9MLyb1 = False   #Blade 1 local flapwise moment at span station 9 (About the local yb1-axis) , (NBlGages < 9) units= kN*m
        self.Spn9MLzb1 = False   #Blade 1 local pitching moment at span station 9 (About the local zb1-axis) , (NBlGages < 9) units= kN*m
        self.Spn1FLxb1 = False   #Blade 1 local flapwise shear force at span station 1 (Directed along the local xb1-axis) , (NBlGages < 1) units= kN
        self.Spn1FLyb1 = False   #Blade 1 local edgewise shear force at span station 1 (Directed along the local yb1-axis) , (NBlGages < 1) units= kN
        self.Spn1FLzb1 = False   #Blade 1 local axial force at span station 1 (Directed along the local zb1-axis) , (NBlGages < 1) units= kN
        self.Spn2FLxb1 = False   #Blade 1 local flapwise shear force at span station 2 (Directed along the local xb1-axis) , (NBlGages < 2) units= kN
        self.Spn2FLyb1 = False   #Blade 1 local edgewise shear force at span station 2 (Directed along the local yb1-axis) , (NBlGages < 2) units= kN
        self.Spn2FLzb1 = False   #Blade 1 local axial force at span station 2 (Directed along the local zb1-axis) , (NBlGages < 2) units= kN
        self.Spn3FLxb1 = False   #Blade 1 local flapwise shear force at span station 3 (Directed along the local xb1-axis) , (NBlGages < 3) units= kN
        self.Spn3FLyb1 = False   #Blade 1 local edgewise shear force at span station 3 (Directed along the local yb1-axis) , (NBlGages < 3) units= kN
        self.Spn3FLzb1 = False   #Blade 1 local axial force at span station 3 (Directed along the local zb1-axis) , (NBlGages < 3) units= kN
        self.Spn4FLxb1 = False   #Blade 1 local flapwise shear force at span station 4 (Directed along the local xb1-axis) , (NBlGages < 4) units= kN
        self.Spn4FLyb1 = False   #Blade 1 local edgewise shear force at span station 4 (Directed along the local yb1-axis) , (NBlGages < 4) units= kN
        self.Spn4FLzb1 = False   #Blade 1 local axial force at span station 4 (Directed along the local zb1-axis) , (NBlGages < 4) units= kN
        self.Spn5FLxb1 = False   #Blade 1 local flapwise shear force at span station 5 (Directed along the local xb1-axis) , (NBlGages < 5) units= kN
        self.Spn5FLyb1 = False   #Blade 1 local edgewise shear force at span station 5 (Directed along the local yb1-axis) , (NBlGages < 5) units= kN
        self.Spn5FLzb1 = False   #Blade 1 local axial force at span station 5 (Directed along the local zb1-axis) , (NBlGages < 5) units= kN
        self.Spn6FLxb1 = False   #Blade 1 local flapwise shear force at span station 6 (Directed along the local xb1-axis) , (NBlGages < 6) units= kN
        self.Spn6FLyb1 = False   #Blade 1 local edgewise shear force at span station 6 (Directed along the local yb1-axis) , (NBlGages < 6) units= kN
        self.Spn6FLzb1 = False   #Blade 1 local axial force at span station 6 (Directed along the local zb1-axis) , (NBlGages < 6) units= kN
        self.Spn7FLxb1 = False   #Blade 1 local flapwise shear force at span station 7 (Directed along the local xb1-axis) , (NBlGages < 7) units= kN
        self.Spn7FLyb1 = False   #Blade 1 local edgewise shear force at span station 7 (Directed along the local yb1-axis) , (NBlGages < 7) units= kN
        self.Spn7FLzb1 = False   #Blade 1 local axial force at span station 7 (Directed along the local zb1-axis) , (NBlGages < 7) units= kN
        self.Spn8FLxb1 = False   #Blade 1 local flapwise shear force at span station 8 (Directed along the local xb1-axis) , (NBlGages < 8) units= kN
        self.Spn8FLyb1 = False   #Blade 1 local edgewise shear force at span station 8 (Directed along the local yb1-axis) , (NBlGages < 8) units= kN
        self.Spn8FLzb1 = False   #Blade 1 local axial force at span station 8 (Directed along the local zb1-axis) , (NBlGages < 8) units= kN
        self.Spn9FLxb1 = False   #Blade 1 local flapwise shear force at span station 9 (Directed along the local xb1-axis) , (NBlGages < 9) units= kN
        self.Spn9FLyb1 = False   #Blade 1 local edgewise shear force at span station 9 (Directed along the local yb1-axis) , (NBlGages < 9) units= kN
        self.Spn9FLzb1 = False   #Blade 1 local axial force at span station 9 (Directed along the local zb1-axis) , (NBlGages < 9) units= kN
        # Blade 2 Local Span Loads
        self.Spn1MLxb2 = False   #Blade 2 local edgewise moment at span station 1 (About the local xb2-axis) , (NBlGages < 1) units= kN*m
        self.Spn1MLyb2 = False   #Blade 2 local flapwise moment at span station 1 (About the local yb2-axis) , (NBlGages < 1) units= kN*m
        self.Spn1MLzb2 = False   #Blade 2 local pitching moment at span station 1 (About the local zb2-axis) , (NBlGages < 1) units= kN*m
        self.Spn2MLxb2 = False   #Blade 2 local edgewise moment at span station 2 (About the local xb2-axis) , (NBlGages < 2) units= kN*m
        self.Spn2MLyb2 = False   #Blade 2 local flapwise moment at span station 2 (About the local yb2-axis) , (NBlGages < 2) units= kN*m
        self.Spn2MLzb2 = False   #Blade 2 local pitching moment at span station 2 (About the local zb2-axis) , (NBlGages < 2) units= kN*m
        self.Spn3MLxb2 = False   #Blade 2 local edgewise moment at span station 3 (About the local xb2-axis) , (NBlGages < 3) units= kN*m
        self.Spn3MLyb2 = False   #Blade 2 local flapwise moment at span station 3 (About the local yb2-axis) , (NBlGages < 3) units= kN*m
        self.Spn3MLzb2 = False   #Blade 2 local pitching moment at span station 3 (About the local zb2-axis) , (NBlGages < 3) units= kN*m
        self.Spn4MLxb2 = False   #Blade 2 local edgewise moment at span station 4 (About the local xb2-axis) , (NBlGages < 4) units= kN*m
        self.Spn4MLyb2 = False   #Blade 2 local flapwise moment at span station 4 (About the local yb2-axis) , (NBlGages < 4) units= kN*m
        self.Spn4MLzb2 = False   #Blade 2 local pitching moment at span station 4 (About the local zb2-axis) , (NBlGages < 4) units= kN*m
        self.Spn5MLxb2 = False   #Blade 2 local edgewise moment at span station 5 (About the local xb2-axis) , (NBlGages < 5) units= kN*m
        self.Spn5MLyb2 = False   #Blade 2 local flapwise moment at span station 5 (About the local yb2-axis) , (NBlGages < 5) units= kN*m
        self.Spn5MLzb2 = False   #Blade 2 local pitching moment at span station 5 (About the local zb2-axis) , (NBlGages < 5) units= kN*m
        self.Spn6MLxb2 = False   #Blade 2 local edgewise moment at span station 6 (About the local xb2-axis) , (NBlGages < 6) units= kN*m
        self.Spn6MLyb2 = False   #Blade 2 local flapwise moment at span station 6 (About the local yb2-axis) , (NBlGages < 6) units= kN*m
        self.Spn6MLzb2 = False   #Blade 2 local pitching moment at span station 6 (About the local zb2-axis) , (NBlGages < 6) units= kN*m
        self.Spn7MLxb2 = False   #Blade 2 local edgewise moment at span station 7 (About the local xb2-axis) , (NBlGages < 7) units= kN*m
        self.Spn7MLyb2 = False   #Blade 2 local flapwise moment at span station 7 (About the local yb2-axis) , (NBlGages < 7) units= kN*m
        self.Spn7MLzb2 = False   #Blade 2 local pitching moment at span station 7 (About the local zb2-axis) , (NBlGages < 7) units= kN*m
        self.Spn8MLxb2 = False   #Blade 2 local edgewise moment at span station 8 (About the local xb2-axis) , (NBlGages < 8) units= kN*m
        self.Spn8MLyb2 = False   #Blade 2 local flapwise moment at span station 8 (About the local yb2-axis) , (NBlGages < 8) units= kN*m
        self.Spn8MLzb2 = False   #Blade 2 local pitching moment at span station 8 (About the local zb2-axis) , (NBlGages < 8) units= kN*m
        self.Spn9MLxb2 = False   #Blade 2 local edgewise moment at span station 9 (About the local xb2-axis) , (NBlGages < 9) units= kN*m
        self.Spn9MLyb2 = False   #Blade 2 local flapwise moment at span station 9 (About the local yb2-axis) , (NBlGages < 9) units= kN*m
        self.Spn9MLzb2 = False   #Blade 2 local pitching moment at span station 9 (About the local zb2-axis) , (NBlGages < 9) units= kN*m
        self.Spn1FLxb2 = False   #Blade 2 local flapwise shear force at span station 1 (Directed along the local xb2-axis) , (NBlGages < 1) units= kN
        self.Spn1FLyb2 = False   #Blade 2 local edgewise shear force at span station 1 (Directed along the local yb2-axis) , (NBlGages < 1) units= kN
        self.Spn1FLzb2 = False   #Blade 2 local axial force at span station 1 (Directed along the local zb2-axis) , (NBlGages < 1) units= kN
        self.Spn2FLxb2 = False   #Blade 2 local flapwise shear force at span station 2 (Directed along the local xb2-axis) , (NBlGages < 2) units= kN
        self.Spn2FLyb2 = False   #Blade 2 local edgewise shear force at span station 2 (Directed along the local yb2-axis) , (NBlGages < 2) units= kN
        self.Spn2FLzb2 = False   #Blade 2 local axial force at span station 2 (Directed along the local zb2-axis) , (NBlGages < 2) units= kN
        self.Spn3FLxb2 = False   #Blade 2 local flapwise shear force at span station 3 (Directed along the local xb2-axis) , (NBlGages < 3) units= kN
        self.Spn3FLyb2 = False   #Blade 2 local edgewise shear force at span station 3 (Directed along the local yb2-axis) , (NBlGages < 3) units= kN
        self.Spn3FLzb2 = False   #Blade 2 local axial force at span station 3 (Directed along the local zb2-axis) , (NBlGages < 3) units= kN
        self.Spn4FLxb2 = False   #Blade 2 local flapwise shear force at span station 4 (Directed along the local xb2-axis) , (NBlGages < 4) units= kN
        self.Spn4FLyb2 = False   #Blade 2 local edgewise shear force at span station 4 (Directed along the local yb2-axis) , (NBlGages < 4) units= kN
        self.Spn4FLzb2 = False   #Blade 2 local axial force at span station 4 (Directed along the local zb2-axis) , (NBlGages < 4) units= kN
        self.Spn5FLxb2 = False   #Blade 2 local flapwise shear force at span station 5 (Directed along the local xb2-axis) , (NBlGages < 5) units= kN
        self.Spn5FLyb2 = False   #Blade 2 local edgewise shear force at span station 5 (Directed along the local yb2-axis) , (NBlGages < 5) units= kN
        self.Spn5FLzb2 = False   #Blade 2 local axial force at span station 5 (Directed along the local zb2-axis) , (NBlGages < 5) units= kN
        self.Spn6FLxb2 = False   #Blade 2 local flapwise shear force at span station 6 (Directed along the local xb2-axis) , (NBlGages < 6) units= kN
        self.Spn6FLyb2 = False   #Blade 2 local edgewise shear force at span station 6 (Directed along the local yb2-axis) , (NBlGages < 6) units= kN
        self.Spn6FLzb2 = False   #Blade 2 local axial force at span station 6 (Directed along the local zb2-axis) , (NBlGages < 6) units= kN
        self.Spn7FLxb2 = False   #Blade 2 local flapwise shear force at span station 7 (Directed along the local xb2-axis) , (NBlGages < 7) units= kN
        self.Spn7FLyb2 = False   #Blade 2 local edgewise shear force at span station 7 (Directed along the local yb2-axis) , (NBlGages < 7) units= kN
        self.Spn7FLzb2 = False   #Blade 2 local axial force at span station 7 (Directed along the local zb2-axis) , (NBlGages < 7) units= kN
        self.Spn8FLxb2 = False   #Blade 2 local flapwise shear force at span station 8 (Directed along the local xb2-axis) , (NBlGages < 8) units= kN
        self.Spn8FLyb2 = False   #Blade 2 local edgewise shear force at span station 8 (Directed along the local yb2-axis) , (NBlGages < 8) units= kN
        self.Spn8FLzb2 = False   #Blade 2 local axial force at span station 8 (Directed along the local zb2-axis) , (NBlGages < 8) units= kN
        self.Spn9FLxb2 = False   #Blade 2 local flapwise shear force at span station 9 (Directed along the local xb2-axis) , (NBlGages < 9) units= kN
        self.Spn9FLyb2 = False   #Blade 2 local edgewise shear force at span station 9 (Directed along the local yb2-axis) , (NBlGages < 9) units= kN
        self.Spn9FLzb2 = False   #Blade 2 local axial force at span station 9 (Directed along the local zb2-axis) , (NBlGages < 9) units= kN
        # Blade 3 Local Span Loads
        self.Spn1MLxb3 = False   #Blade 3 local edgewise moment at span station 1 (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= kN*m
        self.Spn1MLyb3 = False   #Blade 3 local flapwise moment at span station 1 (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= kN*m
        self.Spn1MLzb3 = False   #Blade 3 local pitching moment at span station 1 (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= kN*m
        self.Spn2MLxb3 = False   #Blade 3 local edgewise moment at span station 2 (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= kN*m
        self.Spn2MLyb3 = False   #Blade 3 local flapwise moment at span station 2 (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= kN*m
        self.Spn2MLzb3 = False   #Blade 3 local pitching moment at span station 2 (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= kN*m
        self.Spn3MLxb3 = False   #Blade 3 local edgewise moment at span station 3 (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= kN*m
        self.Spn3MLyb3 = False   #Blade 3 local flapwise moment at span station 3 (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= kN*m
        self.Spn3MLzb3 = False   #Blade 3 local pitching moment at span station 3 (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= kN*m
        self.Spn4MLxb3 = False   #Blade 3 local edgewise moment at span station 4 (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= kN*m
        self.Spn4MLyb3 = False   #Blade 3 local flapwise moment at span station 4 (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= kN*m
        self.Spn4MLzb3 = False   #Blade 3 local pitching moment at span station 4 (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= kN*m
        self.Spn5MLxb3 = False   #Blade 3 local edgewise moment at span station 5 (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= kN*m
        self.Spn5MLyb3 = False   #Blade 3 local flapwise moment at span station 5 (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= kN*m
        self.Spn5MLzb3 = False   #Blade 3 local pitching moment at span station 5 (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= kN*m
        self.Spn6MLxb3 = False   #Blade 3 local edgewise moment at span station 6 (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= kN*m
        self.Spn6MLyb3 = False   #Blade 3 local flapwise moment at span station 6 (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= kN*m
        self.Spn6MLzb3 = False   #Blade 3 local pitching moment at span station 6 (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= kN*m
        self.Spn7MLxb3 = False   #Blade 3 local edgewise moment at span station 7 (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= kN*m
        self.Spn7MLyb3 = False   #Blade 3 local flapwise moment at span station 7 (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= kN*m
        self.Spn7MLzb3 = False   #Blade 3 local pitching moment at span station 7 (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= kN*m
        self.Spn8MLxb3 = False   #Blade 3 local edgewise moment at span station 8 (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= kN*m
        self.Spn8MLyb3 = False   #Blade 3 local flapwise moment at span station 8 (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= kN*m
        self.Spn8MLzb3 = False   #Blade 3 local pitching moment at span station 8 (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= kN*m
        self.Spn9MLxb3 = False   #Blade 3 local edgewise moment at span station 9 (About the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= kN*m
        self.Spn9MLyb3 = False   #Blade 3 local flapwise moment at span station 9 (About the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= kN*m
        self.Spn9MLzb3 = False   #Blade 3 local pitching moment at span station 9 (About the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= kN*m
        self.Spn1FLxb3 = False   #Blade 3 local flapwise shear force at span station 1 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= kN
        self.Spn1FLyb3 = False   #Blade 3 local edgewise shear force at span station 1 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= kN
        self.Spn1FLzb3 = False   #Blade 3 local axial force at span station 1 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 1 )) units= kN
        self.Spn2FLxb3 = False   #Blade 3 local flapwise shear force at span station 2 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= kN
        self.Spn2FLyb3 = False   #Blade 3 local edgewise shear force at span station 2 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= kN
        self.Spn2FLzb3 = False   #Blade 3 local axial force at span station 2 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 2 )) units= kN
        self.Spn3FLxb3 = False   #Blade 3 local flapwise shear force at span station 3 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= kN
        self.Spn3FLyb3 = False   #Blade 3 local edgewise shear force at span station 3 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= kN
        self.Spn3FLzb3 = False   #Blade 3 local axial force at span station 3 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 3 )) units= kN
        self.Spn4FLxb3 = False   #Blade 3 local flapwise shear force at span station 4 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= kN
        self.Spn4FLyb3 = False   #Blade 3 local edgewise shear force at span station 4 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= kN
        self.Spn4FLzb3 = False   #Blade 3 local axial force at span station 4 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 4 )) units= kN
        self.Spn5FLxb3 = False   #Blade 3 local flapwise shear force at span station 5 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= kN
        self.Spn5FLyb3 = False   #Blade 3 local edgewise shear force at span station 5 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= kN
        self.Spn5FLzb3 = False   #Blade 3 local axial force at span station 5 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 5 )) units= kN
        self.Spn6FLxb3 = False   #Blade 3 local flapwise shear force at span station 6 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= kN
        self.Spn6FLyb3 = False   #Blade 3 local edgewise shear force at span station 6 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= kN
        self.Spn6FLzb3 = False   #Blade 3 local axial force at span station 6 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 6 )) units= kN
        self.Spn7FLxb3 = False   #Blade 3 local flapwise shear force at span station 7 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= kN
        self.Spn7FLyb3 = False   #Blade 3 local edgewise shear force at span station 7 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= kN
        self.Spn7FLzb3 = False   #Blade 3 local axial force at span station 7 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 7 )) units= kN
        self.Spn8FLxb3 = False   #Blade 3 local flapwise shear force at span station 8 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= kN
        self.Spn8FLyb3 = False   #Blade 3 local edgewise shear force at span station 8 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= kN
        self.Spn8FLzb3 = False   #Blade 3 local axial force at span station 8 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 8 )) units= kN
        self.Spn9FLxb3 = False   #Blade 3 local flapwise shear force at span station 9 (Directed along the local xb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= kN
        self.Spn9FLyb3 = False   #Blade 3 local edgewise shear force at span station 9 (Directed along the local yb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= kN
        self.Spn9FLzb3 = False   #Blade 3 local axial force at span station 9 (Directed along the local zb3-axis) , (( NumBl < 3 ) .OR. ( NBlGages < 9 )) units= kN

        # Other Names
        # Blade 1 Root Loads
        self.RootFzb1 = False   #Blade 1 axial force at the blade root (Directed along the zc1- and zb1-axes) , () units= kN
        self.RootMIP1 = False   #Blade 1 in-plane moment (i.e., the moment caused by in-plane forces) at the blade root (About the xc1-axis) , () units= kN*m
        self.RootMOoP1 = False   #Blade 1 out-of-plane moment (i.e., the moment caused by out-of-plane forces) at the blade root (About the yc1-axis) , () units= kN*m
        self.RootMzb1 = False   #Blade 1 pitching moment at the blade root (About the zc1- and zb1-axes) , () units= kN*m
        self.RootMEdg1 = False   #Blade 1 edgewise moment (i.e., the moment caused by edgewise forces) at the blade root (About the xb1-axis) , () units= kN*m
        self.RootMFlp1 = False   #Blade 1 flapwise moment (i.e., the moment caused by flapwise forces) at the blade root (About the yb1-axis) , () units= kN*m
        # Blade 2 Root Loads
        self.RootFzb2 = False   #Blade 2 axial force at the blade root (Directed along the zc2- and zb2-axes) , () units= kN
        self.RootMIP2 = False   #Blade 2 in-plane moment (i.e., the moment caused by in-plane forces) at the blade root (About the xc2-axis) , () units= kN*m
        self.RootMOoP2 = False   #Blade 2 out-of-plane moment (i.e., the moment caused by out-of-plane forces) at the blade root (About the yc2-axis) , () units= kN*m
        self.RootMzb2 = False   #Blade 2 pitching moment at the blade root (About the zc2- and zb2-axes) , () units= kN*m
        self.RootMEdg2 = False   #Blade 2 edgewise moment (i.e., the moment caused by edgewise forces) at the blade root (About the xb2-axis) , () units= kN*m
        self.RootMFlp2 = False   #Blade 2 flapwise moment (i.e., the moment caused by flapwise forces) at the blade root (About the yb2-axis) , () units= kN*m
        # Blade 3 Root Loads
        self.RootFzb3 = False   #Blade 3 axial force at the blade root (Directed along the zc3- and zb3-axes) , (NumBl < 3) units= kN
        self.RootMIP3 = False   #Blade 3 in-plane moment (i.e., the moment caused by in-plane forces) at the blade root (About the xc3-axis) , (NumBl < 3) units= kN*m
        self.RootMOoP3 = False   #Blade 3 out-of-plane moment (i.e., the moment caused by out-of-plane forces) at the blade root (About the yc3-axis) , (NumBl < 3) units= kN*m
        self.RootMzb3 = False   #Blade 3 pitching moment at the blade root (About the zc3- and zb3-axes) , (NumBl < 3) units= kN*m
        self.RootMEdg3 = False   #Blade 3 edgewise moment (i.e., the moment caused by edgewise forces) at the blade root (About the xb3-axis) , (NumBl < 3) units= kN*m
        self.RootMFlp3 = False   #Blade 3 flapwise moment (i.e., the moment caused by flapwise forces) at the blade root (About the yb3-axis) , (NumBl < 3) units= kN*m


class HubNacelleLoadsOut(object):
    def __init__(self):

        # Hub and Rotor Loads
        self.LSShftFxa = False   #Low-speed shaft thrust force (this is constant along the shaft and is equivalent to the rotor thrust force) (Directed along the xa- and xs-axes) , () units= kN
        self.LSShftFya = False   #Rotating low-speed shaft shear force (this is constant along the shaft) (Directed along the ya-axis) , () units= kN
        self.LSShftFza = False   #Rotating low-speed shaft shear force (this is constant along the shaft) (Directed along the za-axis) , () units= kN
        self.LSShftFys = False   #Nonrotating low-speed shaft shear force (this is constant along the shaft) (Directed along the ys-axis) , () units= kN
        self.LSShftFzs = False   #Nonrotating low-speed shaft shear force (this is constant along the shaft) (Directed along the zs-axis) , () units= kN
        self.LSShftMxa = False   #Low-speed shaft torque (this is constant along the shaft and is equivalent to the rotor torque) (About the xa- and xs-axes) , () units= kN*m
        self.LSSTipMya = False   #Rotating low-speed shaft bending moment at the shaft tip (teeter pin for 2-blader, apex of rotation for 3-blader) (About the ya-axis) , () units= kN*m
        self.LSSTipMza = False   #Rotating low-speed shaft bending moment at the shaft tip (teeter pin for 2-blader, apex of rotation for 3-blader) (About the za-axis) , () units= kN*m
        self.LSSTipMys = False   #Nonrotating low-speed shaft bending moment at the shaft tip (teeter pin for 2-blader, apex of rotation for 3-blader) (About the ys-axis) , () units= kN*m
        self.LSSTipMzs = False   #Nonrotating low-speed shaft bending moment at the shaft tip (teeter pin for 2-blader, apex of rotation for 3-blader) (About the zs-axis) , () units= kN*m
        self.CThrstAzm = False   #Azimuth location of the center of thrust. This is estimated using values of LSSTipMys, LSSTipMzs, and RotThrust. (About the xa- and xs-axes) , () units= deg
        self.CThrstRad = False   #Dimensionless radial (arm) location of the center of thrust. This is estimated using values of LSSTipMys, LSSTipMzs, and RotThrust. (nondimensionalized using the undeflected tip radius normal to the shaft and limited to values between 0 and 1 (inclusive)) (Always positive (directed radially outboard at azimuth angle CThrstAzm)) , () units= 
        self.RotPwr = False   #Rotor power (this is equivalent to the low-speed shaft power) (N/A) , () units= kW
        self.RotCq = False   #Rotor torque coefficient (this is equivalent to the low-speed shaft torque coefficient) (N/A) , (.NOT. CompAero) units= 
        self.RotCp = False   #Rotor power coefficient (this is equivalent to the low-speed shaft power coefficient) (N/A) , (.NOT. CompAero) units= 
        self.RotCt = False   #Rotor thrust coefficient (this is equivalent to the low-speed shaft thrust coefficient) (N/A) , (.NOT. CompAero) units= 
        # Shaft Strain Gage Loads
        self.LSSGagMya = False   #Rotating low-speed shaft bending moment at the shafts strain gage (shaft strain gage located by input ShftGagL) (About the ya-axis) , () units= kN*m
        self.LSSGagMza = False   #Rotating low-speed shaft bending moment at the shafts strain gage (shaft strain gage located by input ShftGagL) (About the za-axis) , () units= kN*m
        self.LSSGagMys = False   #Nonrotating low-speed shaft bending moment at the shafts strain gage (shaft strain gage located by input ShftGagL) (About the ys-axis) , () units= kN*m
        self.LSSGagMzs = False   #Nonrotating low-speed shaft bending moment at the shafts strain gage (shaft strain gage located by input ShftGagL) (About the zs-axis) , () units= kN*m
        # Generator and High-Speed Shaft Loads
        self.HSShftTq = False   #High-speed shaft torque (this is constant along the shaft) (Same sign as LSShftTq / RotTorq / LSShftMxa / LSShftMxs / LSSGagMxa / LSSGagMxs) , () units= kN*m
        self.HSShftPwr = False   #High-speed shaft power (Same sign as HSShftTq) , () units= kW
        self.HSShftCq = False   #High-speed shaft torque coefficient (N/A) , (.NOT. CompAero) units= 
        self.HSShftCp = False   #High-speed shaft power coefficient (N/A) , (.NOT. CompAero) units= 
        self.GenTq = False   #Electrical generator torque (Positive reflects power extracted and negative represents a motoring-up situation (power input)) , () units= kN*m
        self.GenPwr = False   #Electrical generator power (Same sign as GenTq) , () units= kW
        self.GenCq = False   #Electrical generator torque coefficient (N/A) , (.NOT. CompAero) units= 
        self.GenCp = False   #Electrical generator power coefficient (N/A) , (.NOT. CompAero) units= 
        self.HSSBrTq = False   #High-speed shaft brake torque (i.e., the moment applied to the high-speed shaft by the brake) (Always positive (indicating dissipation of power)) , () units= kN*m
        # Rotor-Furl Bearing Loads
        self.RFrlBrM = False   #Rotor-furl bearing moment (About the rotor-furl axis) , () units= kN*m
        # Tail-Furl Bearing Loads
        self.TFrlBrM = False   #Tail-furl bearing moment (About the tail-furl axis) , () units= kN*m
        # Tail Fin Aerodynamic Loads
        self.TFinAlpha = False   #Tail fin angle of attack. This is the angle between the relative velocity of the wind-inflow at the tail fin center-of-pressure and the tail fin chordline. (About the tail fin z-axis, which is the axis in the tail fin plane normal to the chordline) , (.NOT. CompAero) units= deg
        self.TFinCLift = False   #Tail fin dimensionless lift coefficient (N/A) , (.NOT. CompAero) units= 
        self.TFinCDrag = False   #Tail fin dimensionless drag coefficient (N/A) , (.NOT. CompAero) units= 
        self.TFinDnPrs = False   #Tail fin dynamic pressure, equal to 1/2*AirDens*Vrel^2 where Vrel is the relative velocity of the wind-inflow at the tail fin center-of-pressure (N/A) , (.NOT. CompAero) units= Pa
        self.TFinCPFx = False   #Tangential aerodynamic force at the tail fin center-of-pressure (Directed along the tail fin x-axis, which is the axis along the chordline, positive towards the trailing edge) , (.NOT. CompAero) units= kN
        self.TFinCPFy = False   #Normal aerodynamic force at the tail fin center-of-pressure (Directed along the tail fin y-axis, which is orthogonal to the tail fin plane) , (.NOT. CompAero) units= kN

        # Other Names
        # Hub and Rotor Loads 
        self.LSShftFxs = False   #Low-speed shaft thrust force (this is constant along the shaft and is equivalent to the rotor thrust force) (Directed along the xa- and xs-axes) , () units= kN
        self.LSSGagFya = False   #Rotating low-speed shaft shear force (this is constant along the shaft) (Directed along the ya-axis) , () units= kN
        self.LSSGagFza = False   #Rotating low-speed shaft shear force (this is constant along the shaft) (Directed along the za-axis) , () units= kN
        self.LSSGagFys = False   #Nonrotating low-speed shaft shear force (this is constant along the shaft) (Directed along the ys-axis) , () units= kN
        self.LSSGagFzs = False   #Nonrotating low-speed shaft shear force (this is constant along the shaft) (Directed along the zs-axis) , () units= kN
        self.LSShftMxs = False   #Low-speed shaft torque (this is constant along the shaft and is equivalent to the rotor torque) (About the xa- and xs-axes) , () units= kN*m
        self.CThrstArm = False   #Dimensionless radial (arm) location of the center of thrust. This is estimated using values of LSSTipMys, LSSTipMzs, and RotThrust. (nondimensionalized using the undeflected tip radius normal to the shaft and limited to values between 0 and 1 (inclusive)) (Always positive (directed radially outboard at azimuth angle CThrstAzm)) , () units= 
        self.LSShftPwr = False   #Rotor power (this is equivalent to the low-speed shaft power) (N/A) , () units= kW
        self.LSShftCq = False   #Rotor torque coefficient (this is equivalent to the low-speed shaft torque coefficient) (N/A) , (.NOT. CompAero) units= 
        self.LSShftCp = False   #Rotor power coefficient (this is equivalent to the low-speed shaft power coefficient) (N/A) , (.NOT. CompAero) units= 
        self.LSShftCt = False   #Rotor thrust coefficient (this is equivalent to the low-speed shaft thrust coefficient) (N/A) , (.NOT. CompAero) units= 
        # Hub and Rotor Loads 
        self.LSSGagFxa = False   #Low-speed shaft thrust force (this is constant along the shaft and is equivalent to the rotor thrust force) (Directed along the xa- and xs-axes) , () units= kN
        self.LSSGagMxa = False   #Low-speed shaft torque (this is constant along the shaft and is equivalent to the rotor torque) (About the xa- and xs-axes) , () units= kN*m
        # Hub and Rotor Loads 
        self.LSSGagFxs = False   #Low-speed shaft thrust force (this is constant along the shaft and is equivalent to the rotor thrust force) (Directed along the xa- and xs-axes) , () units= kN
        self.LSSGagMxs = False   #Low-speed shaft torque (this is constant along the shaft and is equivalent to the rotor torque) (About the xa- and xs-axes) , () units= kN*m
        # Hub and Rotor Loads 
        self.RotThrust = False   #Low-speed shaft thrust force (this is constant along the shaft and is equivalent to the rotor thrust force) (Directed along the xa- and xs-axes) , () units= kN
        self.RotTorq = False   #Low-speed shaft torque (this is constant along the shaft and is equivalent to the rotor torque) (About the xa- and xs-axes) , () units= kN*m
        # Hub and Rotor Loads
        self.LSShftTq = False   #Low-speed shaft torque (this is constant along the shaft and is equivalent to the rotor torque) (About the xa- and xs-axes) , () units= kN*m


class TowerSupportLoadsOut(object):

    def __init__(self):
        # Tower-Top / Yaw Bearing Loads
        self.YawBrFxn = False   #Rotating (with nacelle) tower-top / yaw bearing shear force (Directed along the xn-axis) , () units= kN
        self.YawBrFyn = False   #Rotating (with nacelle) tower-top / yaw bearing shear force (Directed along the yn-axis) , () units= kN
        self.YawBrFzn = False   #Tower-top / yaw bearing axial force (Directed along the zn- and zp-axes) , () units= kN
        self.YawBrFxp = False   #Tower-top / yaw bearing fore-aft (nonrotating) shear force (Directed along the xp-axis) , () units= kN
        self.YawBrFyp = False   #Tower-top / yaw bearing side-to-side (nonrotating) shear force (Directed along the yp-axis) , () units= kN
        self.YawBrMxn = False   #Rotating (with nacelle) tower-top / yaw bearing roll moment (About the xn-axis) , () units= kN*m
        self.YawBrMyn = False   #Rotating (with nacelle) tower-top / yaw bearing pitch moment (About the yn-axis) , () units= kN*m
        self.YawBrMzn = False   #Tower-top / yaw bearing yaw moment (About the zn- and zp-axes) , () units= kN*m
        self.YawBrMxp = False   #Nonrotating tower-top / yaw bearing roll moment (About the xp-axis) , () units= kN*m
        self.YawBrMyp = False   #Nonrotating tower-top / yaw bearing pitch moment (About the yp-axis) , () units= kN*m
        # Tower Base Loads
        self.TwrBsFxt = False   #Tower base fore-aft shear force (Directed along the xt-axis) , () units= kN
        self.TwrBsFyt = False   #Tower base side-to-side shear force (Directed along the yt-axis) , () units= kN
        self.TwrBsFzt = False   #Tower base axial force (Directed along the zt-axis) , () units= kN
        self.TwrBsMxt = False   #Tower base roll (or side-to-side) moment (i.e., the moment caused by side-to-side forces) (About the xt-axis) , () units= kN*m
        self.TwrBsMyt = False   #Tower base pitching (or fore-aft) moment (i.e., the moment caused by fore-aft forces) (About the yt-axis) , () units= kN*m
        self.TwrBsMzt = False   #Tower base yaw (or torsional) moment (About the zt-axis) , () units= kN*m
        # Local Tower Loads
        self.TwHt1MLxt = False   #Local tower roll (or side-to-side) moment of tower gage 1 (About the local xt-axis) , (NTwGages < 1) units= kN*m
        self.TwHt1MLyt = False   #Local tower pitching (or fore-aft) moment of tower gage 1 (About the local yt-axis) , (NTwGages < 1) units= kN*m
        self.TwHt1MLzt = False   #Local tower yaw (or torsional) moment of tower gage 1 (About the local zt-axis) , (NTwGages < 1) units= kN*m
        self.TwHt2MLxt = False   #Local tower roll (or side-to-side) moment of tower gage 2 (About the local xt-axis) , (NTwGages < 2) units= kN*m
        self.TwHt2MLyt = False   #Local tower pitching (or fore-aft) moment of tower gage 2 (About the local yt-axis) , (NTwGages < 2) units= kN*m
        self.TwHt2MLzt = False   #Local tower yaw (or torsional) moment of tower gage 2 (About the local zt-axis) , (NTwGages < 2) units= kN*m
        self.TwHt3MLxt = False   #Local tower roll (or side-to-side) moment of tower gage 3 (About the local xt-axis) , (NTwGages < 3) units= kN*m
        self.TwHt3MLyt = False   #Local tower pitching (or fore-aft) moment of tower gage 3 (About the local yt-axis) , (NTwGages < 3) units= kN*m
        self.TwHt3MLzt = False   #Local tower yaw (or torsional) moment of tower gage 3 (About the local zt-axis) , (NTwGages < 3) units= kN*m
        self.TwHt4MLxt = False   #Local tower roll (or side-to-side) moment of tower gage 4 (About the local xt-axis) , (NTwGages < 4) units= kN*m
        self.TwHt4MLyt = False   #Local tower pitching (or fore-aft) moment of tower gage 4 (About the local yt-axis) , (NTwGages < 4) units= kN*m
        self.TwHt4MLzt = False   #Local tower yaw (or torsional) moment of tower gage 4 (About the local zt-axis) , (NTwGages < 4) units= kN*m
        self.TwHt5MLxt = False   #Local tower roll (or side-to-side) moment of tower gage 5 (About the local xt-axis) , (NTwGages < 5) units= kN*m
        self.TwHt5MLyt = False   #Local tower pitching (or fore-aft) moment of tower gage 5 (About the local yt-axis) , (NTwGages < 5) units= kN*m
        self.TwHt5MLzt = False   #Local tower yaw (or torsional) moment of tower gage 5 (About the local zt-axis) , (NTwGages < 5) units= kN*m
        self.TwHt6MLxt = False   #Local tower roll (or side-to-side) moment of tower gage 6 (About the local xt-axis) , (NTwGages < 6) units= kN*m
        self.TwHt6MLyt = False   #Local tower pitching (or fore-aft) moment of tower gage 6 (About the local yt-axis) , (NTwGages < 6) units= kN*m
        self.TwHt6MLzt = False   #Local tower yaw (or torsional) moment of tower gage 6 (About the local zt-axis) , (NTwGages < 6) units= kN*m
        self.TwHt7MLxt = False   #Local tower roll (or side-to-side) moment of tower gage 7 (About the local xt-axis) , (NTwGages < 7) units= kN*m
        self.TwHt7MLyt = False   #Local tower pitching (or fore-aft) moment of tower gage 7 (About the local yt-axis) , (NTwGages < 7) units= kN*m
        self.TwHt7MLzt = False   #Local tower yaw (or torsional) moment of tower gage 7 (About the local zt-axis) , (NTwGages < 7) units= kN*m
        self.TwHt8MLxt = False   #Local tower roll (or side-to-side) moment of tower gage 8 (About the local xt-axis) , (NTwGages < 8) units= kN*m
        self.TwHt8MLyt = False   #Local tower pitching (or fore-aft) moment of tower gage 8 (About the local yt-axis) , (NTwGages < 8) units= kN*m
        self.TwHt8MLzt = False   #Local tower yaw (or torsional) moment of tower gage 8 (About the local zt-axis) , (NTwGages < 8) units= kN*m
        self.TwHt9MLxt = False   #Local tower roll (or side-to-side) moment of tower gage 9 (About the local xt-axis) , (NTwGages < 9) units= kN*m
        self.TwHt9MLyt = False   #Local tower pitching (or fore-aft) moment of tower gage 9 (About the local yt-axis) , (NTwGages < 9) units= kN*m
        self.TwHt9MLzt = False   #Local tower yaw (or torsional) moment of tower gage 9 (About the local zt-axis) , (NTwGages < 9) units= kN*m
        self.TwHt1FLxt = False   #Local tower roll (or side-to-side) force of tower gage 1 (About the local xt-axis) , (NTwGages < 1) units= kN
        self.TwHt1FLyt = False   #Local tower pitching (or fore-aft) force of tower gage 1 (About the local yt-axis) , (NTwGages < 1) units= kN
        self.TwHt1FLzt = False   #Local tower yaw (or torsional) force of tower gage 1 (About the local zt-axis) , (NTwGages < 1) units= kN
        self.TwHt2FLxt = False   #Local tower roll (or side-to-side) force of tower gage 2 (About the local xt-axis) , (NTwGages < 2) units= kN
        self.TwHt2FLyt = False   #Local tower pitching (or fore-aft) force of tower gage 2 (About the local yt-axis) , (NTwGages < 2) units= kN
        self.TwHt2FLzt = False   #Local tower yaw (or torsional) force of tower gage 2 (About the local zt-axis) , (NTwGages < 2) units= kN
        self.TwHt3FLxt = False   #Local tower roll (or side-to-side) force of tower gage 3 (About the local xt-axis) , (NTwGages < 3) units= kN
        self.TwHt3FLyt = False   #Local tower pitching (or fore-aft) force of tower gage 3 (About the local yt-axis) , (NTwGages < 3) units= kN
        self.TwHt3FLzt = False   #Local tower yaw (or torsional) force of tower gage 3 (About the local zt-axis) , (NTwGages < 3) units= kN
        self.TwHt4FLxt = False   #Local tower roll (or side-to-side) force of tower gage 4 (About the local xt-axis) , (NTwGages < 4) units= kN
        self.TwHt4FLyt = False   #Local tower pitching (or fore-aft) force of tower gage 4 (About the local yt-axis) , (NTwGages < 4) units= kN
        self.TwHt4FLzt = False   #Local tower yaw (or torsional) force of tower gage 4 (About the local zt-axis) , (NTwGages < 4) units= kN
        self.TwHt5FLxt = False   #Local tower roll (or side-to-side) force of tower gage 5 (About the local xt-axis) , (NTwGages < 5) units= kN
        self.TwHt5FLyt = False   #Local tower pitching (or fore-aft) force of tower gage 5 (About the local yt-axis) , (NTwGages < 5) units= kN
        self.TwHt5FLzt = False   #Local tower yaw (or torsional) force of tower gage 5 (About the local zt-axis) , (NTwGages < 5) units= kN
        self.TwHt6FLxt = False   #Local tower roll (or side-to-side) force of tower gage 6 (About the local xt-axis) , (NTwGages < 6) units= kN
        self.TwHt6FLyt = False   #Local tower pitching (or fore-aft) force of tower gage 6 (About the local yt-axis) , (NTwGages < 6) units= kN
        self.TwHt6FLzt = False   #Local tower yaw (or torsional) force of tower gage 6 (About the local zt-axis) , (NTwGages < 6) units= kN
        self.TwHt7FLxt = False   #Local tower roll (or side-to-side) force of tower gage 7 (About the local xt-axis) , (NTwGages < 7) units= kN
        self.TwHt7FLyt = False   #Local tower pitching (or fore-aft) force of tower gage 7 (About the local yt-axis) , (NTwGages < 7) units= kN
        self.TwHt7FLzt = False   #Local tower yaw (or torsional) force of tower gage 7 (About the local zt-axis) , (NTwGages < 7) units= kN
        self.TwHt8FLxt = False   #Local tower roll (or side-to-side) force of tower gage 8 (About the local xt-axis) , (NTwGages < 8) units= kN
        self.TwHt8FLyt = False   #Local tower pitching (or fore-aft) force of tower gage 8 (About the local yt-axis) , (NTwGages < 8) units= kN
        self.TwHt8FLzt = False   #Local tower yaw (or torsional) force of tower gage 8 (About the local zt-axis) , (NTwGages < 8) units= kN
        self.TwHt9FLxt = False   #Local tower roll (or side-to-side) force of tower gage 9 (About the local xt-axis) , (NTwGages < 9) units= kN
        self.TwHt9FLyt = False   #Local tower pitching (or fore-aft) force of tower gage 9 (About the local yt-axis) , (NTwGages < 9) units= kN
        self.TwHt9FLzt = False   #Local tower yaw (or torsional) force of tower gage 9 (About the local zt-axis) , (NTwGages < 9) units= kN
        # Platform Loads
        self.PtfmFxt = False   #Platform horizontal surge shear force (Directed along the xt-axis) , () units= kN
        self.PtfmFyt = False   #Platform horizontal sway shear force (Directed along the yt-axis) , () units= kN
        self.PtfmFzt = False   #Platform vertical heave force (Directed along the zt-axis) , () units= kN
        self.PtfmFxi = False   #Platform horizontal surge shear force (Directed along the xi-axis) , () units= kN
        self.PtfmFyi = False   #Platform horizontal sway shear force (Directed along the yi-axis) , () units= kN
        self.PtfmFzi = False   #Platform vertical heave force (Directed along the zi-axis) , () units= kN
        self.PtfmMxt = False   #Platform roll tilt moment (About the xt-axis) , () units= kN*m
        self.PtfmMyt = False   #Platform pitch tilt moment (About the yt-axis) , () units= kN*m
        self.PtfmMzt = False   #Platform yaw moment (About the zt-axis) , () units= kN*m
        self.PtfmMxi = False   #Platform roll tilt moment (About the xi-axis) , () units= kN*m
        self.PtfmMyi = False   #Platform pitch tilt moment (About the yi-axis) , () units= kN*m
        self.PtfmMzi = False   #Platform yaw moment (About the zi-axis) , () units= kN*m
        # Mooring Line Loads
        self.Fair1Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 1 )) units= kN
        self.Fair1Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 1 )) units= deg
        self.Anch1Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 1 )) units= kN
        self.Anch1Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 1 )) units= deg
        self.Fair2Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 2 )) units= kN
        self.Fair2Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 2 )) units= deg
        self.Anch2Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 2 )) units= kN
        self.Anch2Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 2 )) units= deg
        self.Fair3Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 3 )) units= kN
        self.Fair3Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 3 )) units= deg
        self.Anch3Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 3 )) units= kN
        self.Anch3Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 3 )) units= deg
        self.Fair4Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 4 )) units= kN
        self.Fair4Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 4 )) units= deg
        self.Anch4Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 4 )) units= kN
        self.Anch4Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 4 )) units= deg
        self.Fair5Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 5 )) units= kN
        self.Fair5Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 5 )) units= deg
        self.Anch5Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 5 )) units= kN
        self.Anch5Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 5 )) units= deg
        self.Fair6Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 6 )) units= kN
        self.Fair6Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 6 )) units= deg
        self.Anch6Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 6 )) units= kN
        self.Anch6Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 6 )) units= deg
        self.Fair7Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 7 )) units= kN
        self.Fair7Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 7 )) units= deg
        self.Anch7Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 7 )) units= kN
        self.Anch7Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 7 )) units= deg
        self.Fair8Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 8 )) units= kN
        self.Fair8Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 8 )) units= deg
        self.Anch8Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 8 )) units= kN
        self.Anch8Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 8 )) units= deg
        self.Fair9Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 9 )) units= kN
        self.Fair9Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 9 )) units= deg
        self.Anch9Ten = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 9 )) units= kN
        self.Anch9Ang = False   # () , (( .NOT. CompHydro ) .OR. ( NumLines < 9 )) units= deg

        # Other Names
        # Tower-Top / Yaw Bearing Loads 
        self.YawBrFzp = False   #Tower-top / yaw bearing axial force (Directed along the zn- and zp-axes) , () units= kN
        self.YawBrMzp = False   #Tower-top / yaw bearing yaw moment (About the zn- and zp-axes) , () units= kN*m
        # Tower-Top / Yaw Bearing Loads 
        self.YawMom = False   #Tower-top / yaw bearing yaw moment (About the zn- and zp-axes) , () units= kN*m


class WaveMotionsOut(object):

    def __init__(self):
        # Wave Motions
        self.WaveElev = False   # () , (.NOT. CompHydro) units= m
        self.Wave1Vxi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 1 )) units= m/s
        self.Wave1Vyi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 1 )) units= m/s
        self.Wave1Vzi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 1 )) units= m/s
        self.Wave1Axi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 1 )) units= m/s**2
        self.Wave1Ayi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 1 )) units= m/s**2
        self.Wave1Azi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 1 )) units= m/s**2
        self.Wave2Vxi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 2 )) units= m/s
        self.Wave2Vyi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 2 )) units= m/s
        self.Wave2Vzi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 2 )) units= m/s
        self.Wave2Axi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 2 )) units= m/s**2
        self.Wave2Ayi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 2 )) units= m/s**2
        self.Wave2Azi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 2 )) units= m/s**2
        self.Wave3Vxi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 3 )) units= m/s
        self.Wave3Vyi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 3 )) units= m/s
        self.Wave3Vzi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 3 )) units= m/s
        self.Wave3Axi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 3 )) units= m/s**2
        self.Wave3Ayi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 3 )) units= m/s**2
        self.Wave3Azi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 3 )) units= m/s**2
        self.Wave4Vxi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 4 )) units= m/s
        self.Wave4Vyi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 4 )) units= m/s
        self.Wave4Vzi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 4 )) units= m/s
        self.Wave4Axi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 4 )) units= m/s**2
        self.Wave4Ayi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 4 )) units= m/s**2
        self.Wave4Azi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 4 )) units= m/s**2
        self.Wave5Vxi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 5 )) units= m/s
        self.Wave5Vyi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 5 )) units= m/s
        self.Wave5Vzi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 5 )) units= m/s
        self.Wave5Axi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 5 )) units= m/s**2
        self.Wave5Ayi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 5 )) units= m/s**2
        self.Wave5Azi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 5 )) units= m/s**2
        self.Wave6Vxi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 6 )) units= m/s
        self.Wave6Vyi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 6 )) units= m/s
        self.Wave6Vzi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 6 )) units= m/s
        self.Wave6Axi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 6 )) units= m/s**2
        self.Wave6Ayi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 6 )) units= m/s**2
        self.Wave6Azi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 6 )) units= m/s**2
        self.Wave7Vxi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 7 )) units= m/s
        self.Wave7Vyi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 7 )) units= m/s
        self.Wave7Vzi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 7 )) units= m/s
        self.Wave7Axi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 7 )) units= m/s**2
        self.Wave7Ayi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 7 )) units= m/s**2
        self.Wave7Azi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 7 )) units= m/s**2
        self.Wave8Vxi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 8 )) units= m/s
        self.Wave8Vyi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 8 )) units= m/s
        self.Wave8Vzi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 8 )) units= m/s
        self.Wave8Axi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 8 )) units= m/s**2
        self.Wave8Ayi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 8 )) units= m/s**2
        self.Wave8Azi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 8 )) units= m/s**2
        self.Wave9Vxi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 9 )) units= m/s
        self.Wave9Vyi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 9 )) units= m/s
        self.Wave9Vzi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 9 )) units= m/s
        self.Wave9Axi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 9 )) units= m/s**2
        self.Wave9Ayi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 9 )) units= m/s**2
        self.Wave9Azi = False   # () , (( .NOT. CompHydro ) .OR. ( NWaveKin < 9 )) units= m/s**2


class DOFOut(object):
    def __init__(self):

        # Internal Degrees of Freedom
        self.Q_B1E1 = False   #Displacement of 1st edgewise bending-mode DOF of blade 1 () , () units= m
        self.Q_B2E1 = False   #Displacement of 1st edgewise bending-mode DOF of blade 2 () , () units= m
        self.Q_B3E1 = False   #Displacement of 1st edgewise bending-mode DOF of blade 3 () , (NumBl < 3) units= m
        self.Q_B1F1 = False   #Displacement of 1st flapwise bending-mode DOF of blade 1 () , () units= m
        self.Q_B2F1 = False   #Displacement of 1st flapwise bending-mode DOF of blade 2 () , () units= m
        self.Q_B3F1 = False   #Displacement of 1st flapwise bending-mode DOF of blade 3 () , (NumBl < 3) units= m
        self.Q_B1F2 = False   #Displacement of 2nd flapwise bending-mode DOF of blade 1 () , () units= m
        self.Q_B2F2 = False   #Displacement of 2nd flapwise bending-mode DOF of blade 2 () , () units= m
        self.Q_B3F2 = False   #Displacement of 2nd flapwise bending-mode DOF of blade 3 () , (NumBl < 3) units= m
        self.Q_Teet = False   #Displacement of hub teetering DOF () , (NumBl > 2) units= rad
        self.Q_DrTr = False   #Displacement of drivetrain rotational-flexibility DOF () , () units= rad
        self.Q_GeAz = False   #Displacement of variable speed generator DOF () , () units= rad
        self.Q_RFrl = False   #Displacement of rotor-furl DOF () , () units= rad
        self.Q_TFrl = False   #Displacement of tail-furl DOF () , () units= rad
        self.Q_Yaw = False   #Displacement of nacelle yaw DOF () , () units= rad
        self.Q_TFA1 = False   #Displacement of 1st tower fore-aft bending mode DOF () , () units= m
        self.Q_TSS1 = False   #Displacement of 1st tower side-to-side bending mode DOF () , () units= m
        self.Q_TFA2 = False   #Displacement of 2nd tower fore-aft bending mode DOF () , () units= m
        self.Q_TSS2 = False   #Displacement of 2nd tower side-to-side bending mode DOF () , () units= m
        self.Q_Sg = False   #Displacement of platform horizontal surge translation DOF () , () units= m
        self.Q_Sw = False   #Displacement of platform horizontal sway translation DOF () , () units= m
        self.Q_Hv = False   #Displacement of platform vertical heave translation DOF () , () units= m
        self.Q_R = False   #Displacement of platform roll tilt rotation DOF () , () units= rad
        self.Q_P = False   #Displacement of platform pitch tilt rotation DOF () , () units= rad
        self.Q_Y = False   #Displacement of platform yaw rotation DOF () , () units= rad
        self.QD_B1E1 = False   #Velocity of 1st edgewise bending-mode DOF of blade 1 () , () units= m/s
        self.QD_B2E1 = False   #Velocity of 1st edgewise bending-mode DOF of blade 2 () , () units= m/s
        self.QD_B3E1 = False   #Velocity of 1st edgewise bending-mode DOF of blade 3 () , (NumBl < 3) units= m/s
        self.QD_B1F1 = False   #Velocity of 1st flapwise bending-mode DOF of blade 1 () , () units= m/s
        self.QD_B2F1 = False   #Velocity of 1st flapwise bending-mode DOF of blade 2 () , () units= m/s
        self.QD_B3F1 = False   #Velocity of 1st flapwise bending-mode DOF of blade 3 () , (NumBl < 3) units= m/s
        self.QD_B1F2 = False   #Velocity of 2nd flapwise bending-mode DOF of blade 1 () , () units= m/s
        self.QD_B2F2 = False   #Velocity of 2nd flapwise bending-mode DOF of blade 2 () , () units= m/s
        self.QD_B3F2 = False   #Velocity of 2nd flapwise bending-mode DOF of blade 3 () , (NumBl < 3) units= m/s
        self.QD_Teet = False   #Velocity of hub teetering DOF () , (NumBl > 2) units= rad/s
        self.QD_DrTr = False   #Velocity of drivetrain rotational-flexibility DOF () , () units= rad/s
        self.QD_GeAz = False   #Velocity of variable speed generator DOF () , () units= rad/s
        self.QD_RFrl = False   #Velocity of rotor-furl DOF () , () units= rad/s
        self.QD_TFrl = False   #Velocity of tail-furl DOF () , () units= rad/s
        self.QD_Yaw = False   #Velocity of nacelle yaw DOF () , () units= rad/s
        self.QD_TFA1 = False   #Velocity of 1st tower fore-aft bending mode DOF () , () units= m/s
        self.QD_TSS1 = False   #Velocity of 1st tower side-to-side bending mode DOF () , () units= m/s
        self.QD_TFA2 = False   #Velocity of 2nd tower fore-aft bending mode DOF () , () units= m/s
        self.QD_TSS2 = False   #Velocity of 2nd tower side-to-side bending mode DOF () , () units= m/s
        self.QD_Sg = False   #Velocity of platform horizontal surge translation DOF () , () units= m/s
        self.QD_Sw = False   #Velocity of platform horizontal sway translation DOF () , () units= m/s
        self.QD_Hv = False   #Velocity of platform vertical heave translation DOF () , () units= m/s
        self.QD_R = False   #Velocity of platform roll tilt rotation DOF () , () units= rad/s
        self.QD_P = False   #Velocity of platform pitch tilt rotation DOF () , () units= rad/s
        self.QD_Y = False   #Velocity of platform yaw rotation DOF () , () units= rad/s
        self.QD2_B1E1 = False   #Acceleration of 1st edgewise bending-mode DOF of blade 1 () , () units= m/s**2
        self.QD2_B2E1 = False   #Acceleration of 1st edgewise bending-mode DOF of blade 2 () , () units= m/s**2
        self.QD2_B3E1 = False   #Acceleration of 1st edgewise bending-mode DOF of blade 3 () , (NumBl < 3) units= m/s**2
        self.QD2_B1F1 = False   #Acceleration of 1st flapwise bending-mode DOF of blade 1 () , () units= m/s**2
        self.QD2_B2F1 = False   #Acceleration of 1st flapwise bending-mode DOF of blade 2 () , () units= m/s**2
        self.QD2_B3F1 = False   #Acceleration of 1st flapwise bending-mode DOF of blade 3 () , (NumBl < 3) units= m/s**2
        self.QD2_B1F2 = False   #Acceleration of 2nd flapwise bending-mode DOF of blade 1 () , () units= m/s**2
        self.QD2_B2F2 = False   #Acceleration of 2nd flapwise bending-mode DOF of blade 2 () , () units= m/s**2
        self.QD2_B3F2 = False   #Acceleration of 2nd flapwise bending-mode DOF of blade 3 () , (NumBl < 3) units= m/s**2
        self.QD2_Teet = False   #Acceleration of hub teetering DOF () , (NumBl > 2) units= rad/s**2
        self.QD2_DrTr = False   #Acceleration of drivetrain rotational-flexibility DOF () , () units= rad/s**2
        self.QD2_GeAz = False   #Acceleration of variable speed generator DOF () , () units= rad/s**2
        self.QD2_RFrl = False   #Acceleration of rotor-furl DOF () , () units= rad/s**2
        self.QD2_TFrl = False   #Acceleration of tail-furl DOF () , () units= rad/s**2
        self.QD2_Yaw = False   #Acceleration of nacelle yaw DOF () , () units= rad/s**2
        self.QD2_TFA1 = False   #Acceleration of 1st tower fore-aft bending mode DOF () , () units= m/s**2
        self.QD2_TSS1 = False   #Acceleration of 1st tower side-to-side bending mode DOF () , () units= m/s**2
        self.QD2_TFA2 = False   #Acceleration of 2nd tower fore-aft bending mode DOF () , () units= m/s**2
        self.QD2_TSS2 = False   #Acceleration of 2nd tower side-to-side bending mode DOF () , () units= m/s**2
        self.QD2_Sg = False   #Acceleration of platform horizontal surge translation DOF () , () units= m/s**2
        self.QD2_Sw = False   #Acceleration of platform horizontal sway translation DOF () , () units= m/s**2
        self.QD2_Hv = False   #Acceleration of platform vertical heave translation DOF () , () units= m/s**2
        self.QD2_R = False   #Acceleration of platform roll tilt rotation DOF () , () units= rad/s**2
        self.QD2_P = False   #Acceleration of platform pitch tilt rotation DOF () , () units= rad/s**2
        self.QD2_Y = False   #Acceleration of platform yaw rotation DOF () , () units= rad/s**2


# class InflowWindOut(object):
#     def __init__(self):
# NO FAST OUTPUTS DEFINED FOR THIS YET

class ServoDynOut(object):
    def __init__(self):
        self.BlPitchC1 = False   #Blade 1 pitch angle command
        self.BlPitchC2 = False   #Blade 2 pitch angle command
        self.BlPitchC3 = False   #Blade 3 pitch angle command
        self.GenTq = False   #Electrical generator torque
        self.GenPwr = False   #Electrical generator power
        self.HSSBrTqC = False   #High-speed shaft brake torque command (i.e., the commanded moment applied to the high-speed shaft by the brake)
        self.YawMomCom = False   #Nacelle yaw moment command
        self.NTMD_XQ = False   #Nacelle X TMD position (displacement)
        self.NTMD_XQD = False   #Nacelle X TMD velocity
        self.NTMD_YQ = False   #Nacelle Y TMD position (displacement)
        self.NTMD_YQD = False   #Nacelle Y TMD velocity
        self.TTMD_XQ = False   #Tower X TMD position (displacement)
        self.TTMD_XQD = False   #Tower X TMD velocity
        self.TTMD_YQ = False   #Tower Y TMD position (displacement)
        self.TTMD_YQD = False   #Tower Y TMD velocity


# Output Variable Tree

class FstOutput(object):
    def __init__(self):

        # Motion output channels    
        self.wind_mot_vt = WindMotionsOut()   #wind motions output channels
        self.blade_mot_vt = BladeMotionsOut()   #blade motions output channels
        self.hub_nacelle_mot_vt = HubNacelleMotionsOut()   #hub and nacelle system motions output channels
        self.tower_support_mot_vt = TowerSupportMotionsOut()   #yaw bearing, tower and support motions output channels
        self.wave_mot_vt = WaveMotionsOut()   #wave motions output channels

        # Loads output channels
        self.blade_loads_vt = BladeLoadsOut()   #blade loads output channels 
        self.hub_nacelle_loads_vt = HubNacelleLoadsOut()   #hub and nacelle system loads output channels
        self.tower_support_loads_vt = TowerSupportLoadsOut()   #tower and support loads output channels

        # ServoDyn output channels
        self.servodyn_vt = ServoDynOut()

        # Other output channels
        self.dof_vt = DOFOut()   #degree of freedom output channels
