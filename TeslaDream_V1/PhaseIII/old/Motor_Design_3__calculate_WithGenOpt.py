import numpy as np

'''

State is type dict, and consists of:

{ 'omega_s', 'Nph' , 'V1' , 'R1' , 'X1' , 'X2' }

'''

def Tmax(State): # From "Electric Machinery", ref [1] page 325


    Tmax = (1/State['omega_s'])

    Tmax = Tmax*( 0.5 * State['Nph'] * State['V1'] ) # Numerator

    Tmax = (Tmax

            /( (State['R1'])
               + np.sqrt( State['R1']**2  +  (State['X1'] + State['X2'])**2 ) )
            )

            # Denominator

    return Tmax


def GenOpt(Target):

    import pyeasyga as gen

    # Target = { 'torque'=value } #, 'diameter'=float   }

    State=[{ 'omega_s':1,  'Nph':3 , 'V1':1 , 'R1':1 , 'X1':1 , 'X2':1 }]

    ga = gen.GeneticAlgorithm(State)

    def fitness(individual,data):

        DeltaTorque = abs(Target['torque']-Tmax(State))
        DeltaTorque = abs(Target['torque']-Tmax(State))
        #DeltaDiamet = abs(Target['diameter']-

        if DeltaTorque < 0.5:
            return 1
        else:
            return 0 # 0 if not fit

    ga.fitness_function = fitness
    ga.run()

    print('--> GA completed')

    return ga.best_individual()
