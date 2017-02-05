from .Motor_Design_2__calculate import *
import numpy as n

class PhaseII_(object):
    def __init__(self,Last):

        self.Reqs,self.Size = Last

        # Reqs has: Nph, Npo, Kr, PeakRad
        # Size has: Nr,  Ir,  Ag_D, Ag_L
        
        V1   = 228   # Stator Voltage per phase
        Ns   = 186   # Ns total (includes all three phases)
        R2   = 0.02  # Rotor resistance (varies with frequency... not modeled)
        f_e  = n.arange(42,380,10)   # Hertz
        s    = 0.01  # Slip = (ns-nr / ns)
        AL   = 0.100 # meters Axial Length

    def Sweep(self):
        rpms=[]
        torques=[]
        for n in range(len(f_e)):
                StateVector = [V1, f_e[n], s, Ns, R2, AL]
                t,r = m.T(StateVector)
                rpms.append(r)
                torques.append(t)

        plot2d(rpms,torques)

    def Interface(self):
        
        def printMenu():
            print(' ')
            print('- Main Menu:')
            print('''   'go3'       - transfer states to next design phase''')
            print('''   'quit'      - back to design phase select''')
            print(' ')
    
        print("Welcome to Phase II")
        printMenu()
        
        while True:
            user = input('--> ')
            valid=0

            if user=='go3':
                return True
            
            if user=='quit':
                return False
            
            if user=='help' or user=='?' or user==0:
                printMenu()

            if valid==0:
                print(' ')
                print('!! You entered an invalid command :/')

            printMenu()
