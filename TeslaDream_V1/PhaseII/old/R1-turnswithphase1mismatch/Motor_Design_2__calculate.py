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

        # R has Nph, Npo, V1, Is, f_ePeak, PeakT
        # S has Ag_D, Ax_L
        # P has Ns, R2, s, Topology, WireDensity
        
        omega_s = (4*np.pi*R['f_ePeak']/R['Npo']) # rad/s synchronous angular velocity
        
        R1=(33.31/1000)*(S['Ax_L']*2)*P['Ns']# (Ohms/m)*(Length(m)/Turn)*(Turns), resistance estimate
        
        I1  = R['Is']*(1+P['s'])             # Stator Current total all phases rough estimate        
        I2  = R['V1']/(P['R2']/P['s'])  # Rotor  Current total all phases rough estimate, (eq6.32) pg 323 of [1]
        
        Torque = ( (I2**2) * (P['R2']/P['s']) / (omega_s) ) #  R['Nph'] ommitted because I2 = all phases
        
        ## Stator Sizing. Here is a good place, since we have all the variables we need!
        
        Iph=I1/R['Nph'] # Stator Current per Phase
        
        Sw = AWG_Diameter(Iph)[0]/1000      # Amps/Phase -> Wire Diameter (m)
        Sw = Sw*P['Topology']               # Diameter/Wire * Wires/Slot = Stator Slot Width (m)
        
        Sh = (P['WireDensity']/Sw)        # Wires/Slot / Width = Wires/SlotWidth = Wires (in height)
        Sh = Sh*AWG_Diameter(Iph)[0]/1000 # Wires * Width/Wires = SlotHeight
        
        Nslots = (2*P['Ns'])/P['WireDensity'] # (Wire=Turns*2)(Slots/Wire) bc each 1 turn = 2 slotwires
        
        return Torque,[I1,I2,R1,P['R2']],[Sw,Sh,Nslots]

    def psOpt(self,R,S,W):

        from pyswarm import pso
        import time as time

        # R has Nph, Npo, V1, Ir, f_ePeak, PeakT
        # S has Ag_D, Ax_L
        # P has Ns, s, Topology, WireDensity, + 'Perf','Stator' appended later
        
        #W has weight parameters
        #W =[
        #     1,  # Topology (Size) Cost
        #     1   # Stator Turns Cost
        #   ]
        
        def Cost(x,*args):

            R,S,W = args
            
            x={'Ns':x[0],'R2':x[1],'s':x[2],'Topology':x[3],'WireDensity':x[4]}
        
            SizeCost    = W[0]*x['Topology']
            TurnsCost   = W[1]*x['Ns']
            WiringCost  = W[2]*x['WireDensity']
            SlipCost    = W[3]*x['s'] # less slip? better efficiency!
            R2Cost      = W[4]*x['R2']
            
            Cost = SizeCost + TurnsCost + WiringCost + SlipCost + R2Cost
            return Cost

        def Constraint(x,*args):

            R,S,W = args
            
            x={'Ns':x[0],'R2':x[1],'s':x[2],'Topology':x[3],'WireDensity':x[4]}
            T=self.T(R,S,x)
            DeltaTorque = T[0]-R['PeakT']
            DeltaTopology=(2*np.pi)-T[2][2]*(T[2][0]/(S['Ag_D']/2))  # Nslots * angle/slot (length/radius) >= 2pi
                                                  # Max Slotwidth given Ag_D,Nslots (radius*2pi)/Nslots

            return DeltaTorque,DeltaTopology

        # var def:
        #      Ns,      R2,    s,   Topology, WireDensity
        lb =[R['Npo'],  0.1 , 0.0001  ,  1  ,   1    ]
        ub =[   500,    100 , 0.9999   , 15  ,    15    ]

        args = R,S,W

        st = time.time()
        
        xopt, fopt = pso(Cost, lb, ub, f_ieqcons=Constraint, args=args,maxiter=1000)

        xopt={
              'R2':xopt[1],
              's':xopt[2],
              'Topology':xopt[3],
              'WireDensity':xopt[4],
              }

        xopt['Perf'] = self.T(R,S,xopt)[1]
        xopt['Stator']=self.T(R,S,xopt)[2]

        print('Done! PSO Time = ',time.time()-st,'sec')
        
        return xopt


    def gradOpt(self,R,S,W):
        print(' ')
        print('Sorry buddy! This optimization not yet implemented. :/')
        print('''To implement, use "gradOpt" function in Motor_Design_2__calculate''')
        print(' ')

    


