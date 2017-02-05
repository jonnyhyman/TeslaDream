from .Motor_Design_1__calculate import * 
import time as time
import numpy as n

class PhaseI_(object):
    def __init__(self):

        self.Reqs={}
        self.Size={}
        
    # ---------------------------------------- Processor Controller
    def Interface(self):

        def printMenu():
            print(' ')
            print('- Main Menu:')
            print('''   'setup'     - set design spec & requirements''')
            print('''   'see reqs'  - see design spec & requirements''')
            print('''   'see size'  - see size & requirements''')
            print('''   'optimize'  - run multi-/single-var optimizations''')
            print('''   'torque'    - evaluate torque maximum with states''')
            print('''   'go2'       - transfer states to next design phase''')
            print('''   'quit'      - back to design phase select''')
            print(' ')

        def printDict(dictionary):
            print(' ')
            for i,j in dictionary.items():
                print('  ',i,'=',j)
            
        print('Welcome to Phase I!')
        printMenu()
        
        while True:

            user=input('--> ')
            valid=0

            if user=='setup':
                valid=1
                mode = input("'all' or 'any'? ")
                if mode=='all':
                    try:
                        poles =  int(input("# Poles        = "))
                        phases=  int(input("# Phases       = "))
                        kr  =  float(input("Winding Factor = "))
                        print(' ')
                        tau =  float(input("Maximum Torque = "))
                        rpm =  float(input("Max Torque RPM = "))
                        rad =  rpm*n.pi/30 # rad/s

                        self.Reqs = {'Npo':poles,'Nph':phases,
                                      'Kr':kr,'PeakT':tau,'PeakRad':rad}
                    except ValueError:
                        print(' ')
                        print('Something went wrong. Try again!')
                else:
                    if self.Reqs!={} :

                        print('Which of these?')
                        printDict(self.Reqs)
                        
                        anywhichone = input('--> ')
                        setas       = input('Set to: ')

                        try:                        
                            self.Reqs[anywhichone]=float(setas)
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
                    mode = input("'swarm', or 'single'? ")

                    if mode=='swarm' or mode=='pso' or mode=='ps':
                        weights    = [2,1,1,1]
                        chgWeights = input("Change weights? 'Yes'/'No' ")
                        if chgWeights=='Yes' or chgWeights.lower()=='y':

                            weights[0] = float(input('Stator Inner Diameter Cost > '))
                            weights[1] = float(input('Air Gap Axial Length  Cost > '))
                            weights[2] = float(input('Rotor Currents Cost        > '))
                            weights[3] = float(input('Rotor Effective Turns Cost > '))
                            
                        self.Size=m().psOpt(self.Reqs,weights)
                        printDict(self.Size)
                        
                    if mode=='single'  or mode=='1':
                        m().singleOpt()
                else:
                    print('Requirements not setup yet!')

            if user=='d': # super top secret debug / default run function
                valid=1
                weights  = [2,1,1,1]
                self.Reqs={'Nph':3 , 'Npo':4 , 'Kr':0.95 , 'PeakT':21 , 'PeakRad':1250*n.pi/30}
                self.Size=m().psOpt(self.Reqs,weights)
                printDict(self.Size)
                
            if user=='torque':
                valid=1
                if self.Reqs!={} or self.Size!={}:
                    Torque=m().T(self.Reqs,self.Size)
                    print('Torque =',Torque,'Nm')
                else:
                    print("Requirements or Size not setup yet!")
                
            if user=='go2':
                return [self.Reqs,self.Size]
            
            if user=='quit':
                return False

            if user=='help' or user=='?':
                valid=1
                
            if valid==0:
                print(' ')
                print('!! You entered an invalid command :/')
                print(' ')

            printMenu()
