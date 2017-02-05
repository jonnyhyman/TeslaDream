import numpy as np
from .SupportingFunctions import *

# ---------------------------------------- Caveats and Assumptions
'''
This calculator assumes an idealized model of induction motors:
- model is built on steady-state assumption: not accurate for startup/shutdown
- stator, rotor, and magnetizing reactances are neglected
- stator windings estimated based on number of Ns and stator size
- no end winding accountance
- no resistance as varied by frequency (proximity effect + skin effect)
'''

class m():

    def T(self,R,S,P):

        # R has Nph, Npo, V1, Ns, Is, omega_e, PeakT
        # S has Ag_D, Ax_L
        # P has Ns, R2, s, Topology, WireDensity
        
        omega_s = (2/R['Npo'])*R['omega_e'] # rad/s synchronous angular velocity
        
        R1=(33.31/1000)*(S['Ax_L']*2)*R['Ns']# (Ohms/m)*(Length(m)/Turn)*(Turns), resistance estimate
        
        I1  = R['Is']*(1+P['s'])             # Stator Current total all phases rough estimate        
        I2  = R['V1']/(P['R2']/P['s'])  # Rotor  Current total all phases rough estimate, (eq6.32) pg 323 of [1]
        
        Torque = ( (I2**2) * (P['R2']/P['s']) / (omega_s) ) #  R['Nph'] ommitted because I2 = all phases
        
        ## Stator Sizing. Here is a good place, since we have all the variables we need!
        
        Iph=I1/R['Nph'] # Stator Current per Phase
        
        Sw = AWG_Diameter(Iph)[0]/1000      # Amps/Phase -> Wire Diameter (m)
        Sw = Sw*P['Topology']               # Diameter/Wire * Wires/Slot = Stator Slot Width (m)
        
        Sh = (P['WireDensity']/Sw)        # Wires/Slot / Width = Wires/SlotWidth = Wires (in height)
        Sh = Sh*AWG_Diameter(Iph)[0]/1000 # Wires * Width/Wires = SlotHeight
        
        Nslots = (2*R['Ns'])/P['WireDensity'] # (Wire=Turns*2)(Slots/Wire) bc each 1 turn = 2 slotwires
        
        return Torque,[I1,I2,R1,P['R2']],[Sw,Sh,Nslots]

    def psOpt(self,R,S,W):

        from pyswarm import pso
        import time as time

        # R has Nph, Npo, V1, Ns, Ir, omega_e, PeakT
        # S has Ag_D, Ax_L
        # P has Ns, s, Topology, WireDensity, + 'Perf','Stator' appended later
        
        #W has weight parameters
        #W =[
        #     1,  # Topology (Size) Cost
        #     1   # Stator Turns Cost
        #   ]

        def XtoDict(x):
            return {'R2':x[0],'s':x[1],'Topology':x[2],'WireDensity':x[3]}
        
        def Cost(x,*args):

            R,S,W = args
            
            x=XtoDict(x)
            
            SizeCost    = W[0]*x['Topology']
            WiringCost  = W[1]*x['WireDensity']
            SlipCost    = W[2]*x['s'] # less slip? better efficiency!
            R2Cost      = W[3]*x['R2']
            
            Cost = SizeCost + WiringCost + SlipCost + R2Cost
            return Cost

        def Constraint(x,*args):

            R,S,W = args
            
            x=XtoDict(x)
            T=self.T(R,S,x)
            
            DeltaTorque = T[0]-R['PeakT']
            DeltaTopology=(2*np.pi)-T[2][2]*(T[2][0]/(S['Ag_D']/2))
            # Nslots * angle/slot (length/radius) >= 2pi
            # Max Slotwidth given Ag_D,Nslots (radius*2pi)/Nslots

            return DeltaTorque,DeltaTopology

        # var def:
        #      R2,    s,   Topology, WireDensity
        lb =[  10 , 0.0001   ,  1  ,     1    ]
        ub =[  100 , 0.9999   , 15  ,    6    ]

        args = R,S,W

        st = time.time()
        
        xopt, fopt = pso(Cost, lb, ub, f_ieqcons=Constraint, args=args,maxiter=1000)

        xopt=XtoDict(xopt)

        xopt['Perf']  =self.T(R,S,xopt)[1]
        xopt['Stator']=self.T(R,S,xopt)[2]

        print('Done! PSO Time = ',time.time()-st,'sec')
        
        return xopt


    def gradOpt(self,R,S,W):
        print(' ')
        print('Sorry buddy! This optimization not yet implemented. :/')
        print('''To implement, use "gradOpt" function in Motor_Design_2__calculate''')
        print(' ')

    


