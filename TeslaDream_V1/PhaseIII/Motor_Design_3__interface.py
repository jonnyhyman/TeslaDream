from .Motor_Design_3__calculate import *
import numpy as np

class Interface(object):

    def __init__(self,S):

        self.State=S # { 'omega_s',  'Nph', 'V1' , 'R1' , 'X1' , 'X2' , 'PeakT' }

        print('Welcome to Phase III!')

        self.printMenu()

    def printMenu(self):
        print(' ')
        print('- Main Menu:')
        print('''   'state'     - define state variables''')
        print('''   'see state' - print state variables''')
        print('''   'set state' - set state variables''')
        print('''   'tmax'      - run Tmax given state''')
        print('''   'optimize'  - run optimization on X1 & X2''')
        print('''   'quit'      - back to design phase select''')
        print(' ')

    def parseRedirect(self): # reads input and redirects to the function

        user = input('--> ')
        valid=0

        if user=='see state' or user=='see':
            self.seeState()
            valid=1

        if user=='set state' or user=='set':
            self.setState()
            valid=1

        if user=='tmax':
            self.tMax()
            valid=1

        if user=='optimize' or user=='opt':
            weights    = [-1,-1]
            chgWeights = input("Change weights? 'Yes'/'No' ")
            if chgWeights=='Yes' or chgWeights=='y' or chgWeights=='Y':

                weights[0] = float(input('Stator Cost > '))
                weights[1] = float(input('Rotor Cost  > '))
                
            self.State['X1'],self.State['X2']=m().psOpt(self.State,weights)
            valid=1

        if user=='d': # super top secret debug / default run function
            valid   = 1
            weights = [-1,-1]
            self.State['X1'],self.State['X2']=m().psOpt(self.State,weights)
            self.tMax()
            
        if user=='quit':
            return False

        if valid==0:
            print(' ')
            print('!! You entered an invalid command :/')

        self.printMenu() 
        return True

    def seeState(self):
        print(' ')
        print("Synch Speed ",self.State['omega_s'],'rad/s')
        print("Torque  Tgt ",self.State['PeakT'],'Nm')
        print("# Phases    ",self.State['Nph'])
        print("Stator Volts",self.State['V1'],'Volts')
        print("Stator Ohms ",self.State['R1'],'Ohms')
        print("Stator React",self.State['X1'],'Ohms')
        print("Rotor  React",self.State['X2'],'Ohms')

    def setState(self):
        print(' ')
        print("   Synch Speed ","'omega_s'",'rad/s')
        print("   # Phases    ","'Nph'")
        print("   Torque  Tgt ","'PeakT'",'Nm')
        print("   Stator Volts","'V1'",'Volts')
        print("   Stator Ohms ","'R1'",'Ohms')
        print("   Stator React","'X1'",'Ohms')
        print("   Rotor  React","'X2'",'Ohms')
        print("   Set all one by one = 'all' ")
        print("   <---< Back to menu = 'back' ")
        print(' ')

        which = input('Which variable? ')

        if which=='all':
            for k in list(self.State.keys()):
                what = input('Set '+str(k)+' to: ')
                self.State[k]=float(what)

        else:
            if which!='back':
                what = input('Set to: ')
                self.State[which]=float(what)

    def tMax(self):
        print(' ')
        print('----------------------------------')
        print('   Tmax =',m().Tmax(self.State),'Nm')
        print('----------------------------------')

class PhaseIII_(object):
    
    def __init__(self,Last):
        
        if not isinstance(Last,bool):
            self.State = self.TranslateToPhase3(Last) # user came from Phase 2
        else:
            self.State={}
        

    def TranslateToPhase3(self,Last):

        R,S,P = Last
        # R has Nph, Npo, V1, Ns, Ir, omega_e, PeakT
        # S has Ag_D, Ax_L
        # P has Ns, s, Topology, WireDensity, + 'Perf','Stator' appended later

        omega_s = (2/R['Npo'])*R['omega_e']
        
        State  ={ 'omega_s':omega_s,  'Nph':R['Nph'] , 'V1':R['V1'] , 'R1':P['Perf'][0] , 'X1':1 , 'X2':1 , 'PeakT':R['PeakT']}

        return State
    
    def Interface(self):
        I=Interface(self.State)
        ON=True
        while ON:
            ON=I.parseRedirect()
