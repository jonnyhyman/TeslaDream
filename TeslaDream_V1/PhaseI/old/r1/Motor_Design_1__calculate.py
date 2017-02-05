import numpy as np
from .SupportingFunctions import *

class m(object):

    def __init__(self,R={},S={}):
        self.R = R
        self.S = S

    def T(self,R,S):

        Fs_max = 4/np.pi * (R['Kr']*S['Nr']/R['Npo']) * (S['Ir']) # Maxmimum possible flux contribution

        Bsr = 1.5 # Teslas, saturation limit minimum

        Tmax = (R['Npo']/2) * (np.pi*S['Ag_D']*S['Ag_L']/2) * Bsr * Fs_max # assumes dsr = -pi/2 (rotor drags = motor)
                                                                    # you must further determine f_e to make dsr -pi/2
        #print('Torque      =',Tmax,'Nm')
        #print(' ')

        return Tmax


    def psOpt(self,R,P):

        from pyswarm import pso
        import time as time

        #R has setup parameters : Nph , Npo , Kr , PeakT , PeakRad

        #P has weight parameters
        #P =[
        #     2,  # Airgap Diameter
        #     1,  # Airgap Length
        #     1,  # Rotor Current
        #     1   # Rotor Effective Turns
        #   ]
        
        def Cost(x,*args):

            R,P = args
            
            x={'Nr':x[0],'Ir':x[1],'Ag_D':x[2],'Ag_L':x[3]}
        
            SizeCost    = P[0]*x['Ag_D'] + P[1]*x['Ag_L']
            CurrentCost = P[2]*x['Ir']
            TurnsCost   = P[3]*x['Nr']
            
            Cost = CurrentCost + SizeCost + TurnsCost
            return Cost

        def Constraint(x,*args):

            R,P = args
            x={'Nr':x[0],'Ir':x[1],'Ag_D':x[2],'Ag_L':x[3]}
            DeltaTorque = self.T(R,x)-R['PeakT']        

            return DeltaTorque

        # var def:
        #      Nr ,  Ir,   Ag_D   ,   Ag_L
        lb =[   1 ,  1  ,  0.04   ,   0.05    ]
        ub =[   500,  250,  0.3   ,    0.3    ]

        args = R,P

        st = time.time()
        
        xopt, fopt = pso(Cost, lb, ub, f_ieqcons=Constraint, args=args)
        xopt={'Nr':xopt[0],'Ir':xopt[1],'Ag_D':xopt[2],'Ag_L':xopt[3]}

        print('Done! PSO Time = ',time.time()-st,'sec')
        
        return xopt

    def singleOpt(self):
        print(' ')
        print('Sorry buddy! This optimization not yet implemented. :/')
        print('''To implement, use "singleOpt" function in Motor_Design_1__calculate''')
        print(' ')
