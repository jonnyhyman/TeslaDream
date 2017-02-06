import numpy as np

'''

State is type dict, and consists of:

{ 'omega_s', 'Nph' , 'V1' , 'R1' , 'X1' , 'X2' }

'''

# ---------------------------------------- Caveats and Assumptions
'''
This calculator assumes an idealized model of induction motors:
- model is built on steady-state assumption: not accurate for startup/shutdown
- stator windings estimated based on number of Ns and stator size
- no end winding accountance
- no resistance as varied by frequency (proximity effect + skin effect)
'''


class m():

    def Tmax(self,State): # From "Electric Machinery", ref [1] page 325

        Tmax = (1/State['omega_s'])

        Tmax = Tmax*( 0.5 * State['Nph'] * State['V1']**2 ) # Numerator

        Tmax = (Tmax

                        /( (State['R1'])
                           + np.sqrt( State['R1']**2  +  (State['X1'] + State['X2'])**2 ) )
                        )

                        # Denominator

        return Tmax

    def psOpt(self,S,W):

        from pyswarm import pso
        import time as time

        #S has setup parameters : omega_s , Nph , V1 , R1 , X1 , X2, PeakT

        #W has weight parameters
        #W =[
        #     1,  # Stator Reactance
        #     1,  # Rotor Reactance
        #   ]

        def Cost(x,*args):

            S,W = args

            S['X1']=x[0]
            S['X2']=x[1]

            RotorCost  = W[0]*S['X1']
            StatorCost = W[1]*S['X2']

            Cost = RotorCost + StatorCost
            return Cost

        def Constraint(x,*args):

            S,W = args

            S['X1']=x[0]
            S['X2']=x[1]

            DeltaTorque = self.Tmax(S)-S['PeakT']

            return DeltaTorque

        # var def:
        #        X1 ,    X2
        lb =[    1  ,   1  ]
        ub =[    50 ,   50 ]

        args = S,W

        st = time.time()

        xopt, fopt = pso(Cost, lb, ub, f_ieqcons=Constraint, args=args)

        print('Done! PSO Time = ',time.time()-st,'sec')

        return xopt[0],xopt[1]
