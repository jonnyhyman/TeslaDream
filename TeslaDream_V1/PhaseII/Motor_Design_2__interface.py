from .Motor_Design_2__calculate import *
import numpy as np

class PhaseII_(object):
    def __init__(self,Last):

        if not isinstance(Last,bool):
            self.Reqs, self.Size  = self.TranslateToPhase2(Last)
            # Reqs has: Nph, Npo, *V1, Ns, Is, omega_e, PeakT
            # Size has: Ag_D, Ax_L
            self.P={}
        else:
            self.Reqs, self.Size,self.P = {},{},{}

        # *these variables initialized, but not set!
        
    def TranslateToPhase2(self,Last):

        Reqs1,Size1 = Last
        # Reqs1 has: Nph, Npo, Kr, PeakRad, PeakT
        # Size1 has: Ns,  Is,  Ag_D, Ag_L

        Reqs2={'Nph' :Reqs1['Nph'],  'Npo' :Reqs1['Npo'], 'V1':1,'Ns':Size1['Ns'], 'Is':Size1['Is'], 'omega_e':Reqs1['PeakRad'], 'PeakT':Reqs1['PeakT']}
        Size2={'Ag_D':Size1['Ag_D'], 'Ax_L':Size1['Ag_L'] }

        return Reqs2,Size2

    def Interface(self):
        
        def printMenu():
            print(' ')
            print('- Main Menu:')
            print('''   'setup'     - set design spec & requirements''')
            print('''   'see reqs'  - see design spec & requirements''')
            print('''   'see size'  - see design size requirements''')
            print('''   'see all'   - see size, reqs, and performance states''')
            print('''   'optimize'  - run multi-var optimization''')
            print('''   'torque'    - evaluate torque maximum with states''')
            print('''   'go3'       - transfer states to next design phase''')
            print('''   'quit'      - back to design phase select''')
            print(' ')

        def printDict(dictionary):
            print(' ')
            for i,j in dictionary.items():
                print('  ',i,'=',j)
    
        print("Welcome to Phase II")
        printMenu()
        
        while True:
            user = input('--> ')
            valid=0

            if user=='setup':
                valid=1
                mode = input("'all' or 'any'? ")
                if mode=='all':
                    if self.Reqs=={}: # User didn't come from Phase 1
                        try:
                            print(' ')
                            print('Reccomend that you run Phase I first!')
                            print(' ')
                            
                            poles =  int(input("# Poles        = "))
                            phases=  int(input("# Phases       = "))
                            
                            V1 =   float(input("Input Voltage  = "))
                            Is  =  float(input("Stator Current = "))
                            Ns  =  float(input("Stator Turns   = "))
                            
                            print(' ')
                            tau =  float(input("Maximum Torque = "))
                            rpm =  float(input("Max Torque RPM = "))
                            rad =  rpm*n.pi/30 # rad/s
                            
                            self.Reqs={'Nph' :phases, 'Npo' :poles, 'V1':V1,'Is':Ns,'Is':Is, 'omega_e':rad, 'PeakT':tau}
                            print(' ')
                            Ag_D =  float(input("Stator ID (mm)  = "))/1000    # mm -> m
                            Ag_L =  float(input("Motor Length(mm)= "))/1000    # mm -> m 
                            self.Size={'Ag_D':Ag_D, 'Ax_L':Ag_L }
                             
                        except ValueError:
                            print(' ')
                            print('Something went wrong. Try again!')
                    else:
                        try:                        
                            V1 =   float(input("Input Voltage  = "))
                            self.Reqs['V1']=V1
                             
                        except ValueError:
                            print(' ')
                            print('Something went wrong. Try again!')
                else: #any
                    if self.Reqs!={} :

                        print('Which of these?')
                        printDict(self.Reqs)
                        printDict(self.Size)
                        print(' ')
                        
                        anywhichone = input('--> ')
                        setas       = input('Set to: ')
                        if anywhichone in self.Reqs.keys():
                            try:                        
                                self.Reqs[anywhichone]=float(setas)
                            except ValueError:
                                print(' ')
                                print('Something went wrong. Try again!')
                        else:
                            try:                        
                                self.Size[anywhichone]=float(setas)
                            except ValueError:
                                print(' ')
                                print('Something went wrong. Try again!')
                    else:
                        print(' ')
                        print("!!! You must do 'all' first !!!")

            if user=='see reqs':
                valid=1
                if self.Reqs!={}:
                    printDict(self.Reqs)
                else:
                    print('Requirements not setup yet!')

            if user=='see size':
                valid=1
                if self.Size!={}:
                    printDict(self.Size)
                else:
                    print('Size not setup yet!')

            if user=='optimize' or user=='opt':
                valid=1
                if self.Reqs!={}:
                    mode = input("'swarm', or 'gradientdesc'? ")

                    if mode=='swarm' or mode=='pso' or mode=='ps':
                        weights    =[-2,1,1,1,-1]
                        chgWeights = input("Change weights? 'Yes'/'No' ")
                        if chgWeights=='Yes' or chgWeights.lower()=='y':

                            weights[0] = float(input('Topology (Size) Cost > '))
                            weights[1] = float(input('Stator Turns    Cost > '))
                            weights[2] = float(input('Wire Density    Cost > '))
                            weights[3] = float(input('High Slip       Cost > '))
                            weights[3] = float(input('Resistance Rotor Cost> '))
                            
                        self.P=m().psOpt(self.Reqs,self.Size,weights) # P is an shorthand for performance params
                        printDict(self.P)

                    if mode=='gradientdesc' or mode=='grad' or mode=='g':
                        self.P=m().gradOpt(self.Reqs,self.Size,weights)
                        
                else:
                    print('Requirements not setup yet!')

            if user=='see all':
                valid=1
                if self.Size!={} and self.Reqs!={} and self.P!={}:
                    printDict(self.Size)
                    printDict(self.Reqs)
                    printDict(self.P)
                else:
                    print('Size, Reqs, or Perf not setup yet!')

            if user=='torque' or user=='t':
                valid=1
                if self.Reqs!={} and self.Size!={} and self.P!={}:
                    Torque=m().T(self.Reqs,self.Size,self.P)[0]
                    print('Torque =',Torque,'Nm')
                else:
                    print("Requirements,Size,or Steady State not setup yet!")

            if user=='d': # super top secret debug / default run function
                valid=1
                weights=[-2,1,1,1,-1]
                self.Reqs['V1']=230
                self.P=m().psOpt(self.Reqs,self.Size,weights) # P is an shorthand for performance params
                printDict(self.P)

            if user=='go3':
                return self.Reqs,self.Size,self.P
            
            if user=='quit':
                return False
            
            if user=='help' or user=='?' or user==0:
                printMenu()

            if valid==0:
                print(' ')
                print('!! You entered an invalid command :/')

            printMenu()

        
