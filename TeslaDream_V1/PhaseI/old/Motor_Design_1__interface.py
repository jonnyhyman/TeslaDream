from .Motor_Design_1__calculate import * 
import time as time
import numpy as n

class PhaseI_(object):
    def __init__(self):
        # ---------------------------------------- Requirements

        PowerRange = [0.82 , 5.47]       # kW
        RPMRange   = [1250.00 , 11400.00]# RPM
        RADRange   = [1250.00*n.pi/30 , 11400.00*n.pi/30]# rad/s
        TorqueRange= [2.29 , 20.91]      #Nm

        # ---------------------------------------- Optimization Variables

        W_H     = 3.0     # Slot Width / Height Ratio
        Ns      = 198     # Turns
        Amps    = 10.0    # Amps

        SD      = 50/1000 # m Slot Diameter
        AL      = 70/1000 # m Axial Length

        self.StateVector=[SD,AL,Ns,W_H,Amps]

    def pMaximize(self,func,parmstart,deltaparm,lim=1.0e100000): # partial derivative maximization

        parmdir='pos'
        parmindex=parmstart[0]
        parm=parmstart[parmindex]

                # print('startparm=',parmindex)
        time.sleep(1)
        lastparm=0
        lastvar=0
        lastderivative=0
        derivative=1000 # starting only
        maximized=False

        while maximized is False:

            if parmdir is 'pos':
                parm+=deltaparm

            if parmdir is 'neg':
                parm-=deltaparm

            parmsend=[]
            for i in range(1,len(parmstart)):
                parmsend.append(parmstart[i])

            parmsend[parmindex-1]=parm

            parmsend=tuple(parmsend)

            print(parmsend)

            var=func(parmsend)

            # Check if var past maximum limit
            if lim[1]<1.0e100000: # if actually defined
                if parm>lim[1]:
                    print('Over the top!')
                    return lastparm

                if parm<lim[0]:
                    print('Under the sea!')
                    return lastparm

            derivative = (var-lastvar)/(parm-lastparm)

            if lastderivative < 0 and derivative < 0 :
                # reverse parameter direction
                parmdir='neg'

            if lastderivative > 0 and derivative < 0 and parmdir is 'pos':
                # don't just return if negative derivative -> must be a max
                maximized=True
                return (parm+lastparm)/2

            if lastderivative < 0 and derivative > 0 and parmdir is 'neg':
                # negative direction has opposite signs
                # don't just return if negative derivative -> must be a max
                maximized=True
                return (parm+lastparm)/2

            lastparm=parm
            lastvar=var
            lastderivative=derivative

	# ---------------------------------------- Sizing & Torque

    def S(self):
        Sd,Al,Ns,W_H,Amps = list(self.StateVector)

        print(' ')

        StatorIDia = m.Stator_Dimensions(
                                   Ns,
                                   Amps,
                                   m.Nph,
                                   m.eTpS,
                                   W_H,
                                   m.Ts,
                                   m.Srex,
                                   verbose=True
                                   )
        print(' ')

    def T(self):

        global StateVector
        Sd,Al,Ns,W_H,Amps = list(StateVector)

        StatorIDia = m.Stator_Dimensions(
                                   Ns,
                                   Amps,
                                   m.Nph,
                                   m.eTpS,
                                   W_H,
                                   m.Ts,
                                   m.Srex
                                   )


        Torque=m.Torque(
                        Ns,
                        m.Ks,
                        Amps,
                        StatorIDia,
                        Al,
                        m.Npo
                        )

        return Torque,Ns,W_H,Amps

    # ---------------------------------------- Processors

    def NS_opt():

        stime = time.time()

        print(' ')

        target_delta = T()[0]-TorqueRange[1]

        while target_delta < 0.1 :
            self.StateVector[2]+=2
            target_delta = T()[0]-TorqueRange[1]

        while target_delta > 0.1 :
            self.StateVector[2]-=2
            target_delta = T()[0]-TorqueRange[1]
        print('NS =',self.StateVector[2],'')    
        print('Time=',time.time()-stime,'sec')

    def WH_opt():

        stime = time.time()

        print(' ')

        target_delta = T()[0]-TorqueRange[1]

        while target_delta < 0.1 :
            StateVector[3]+=0.1
            target_delta = T()[0]-TorqueRange[1]

        while target_delta > 0.1 :
            StateVector[3]-=0.1
            target_delta = T()[0]-TorqueRange[1]
            
        print('WH =',StateVector[3],'')
        print('Time =',time.time()-stime,'sec')

    def AMPS_opt():

        stime = time.time()

        print(' ')

        global StateVector

        target_delta = T()[0]-TorqueRange[1]

        while target_delta < 0.1 :
            StateVector[4]+=0.5
            target_delta = T()[0]-TorqueRange[1]

        while target_delta > 0.1 :
            StateVector[4]-=0.5
            target_delta = T()[0]-TorqueRange[1]

        print('Amps =',StateVector[4],'A')
        print('Time =',time.time()-stime,'sec')

    def PostProcess():

        print(' ')

        Current_T = StateVector[4]*m.Nph
        Voltage_T = PowerRange[1]*1000 / Current_T # W / A = V

        print('Voltage =',Voltage_T,'V')
        print('Current =',Current_T,'A')
        print(' ')
        T()

    def SetVar():

        conclusion=False
        while not conclusion:

            whichvar=input('Which variable? : ')
            whichvar=whichvar.lower()

            if ('ns' == whichvar) or  ('turns' == whichvar):
                value=float(input('Set it to: '))
                StateVector[2]=value
                conclusion=True

            if 'wh' == whichvar:
                value=float(input('Set it to: '))
                StateVector[3]=value
                conclusion=True

            if 'amps' == whichvar:
                value=float(input('Set it to: '))
                StateVector[4]=value
                conclusion=True

            if 'al' == whichvar:
                value=float(input('Set it to: '))
                StateVector[1]=value
                conclusion=True
                
            print("That variable doesn't seem to exist. Try again!")

    # ---------------------------------------- Processor Controller
    def Interface(self):
        ON=True
        
        print('Welcome to Phase I!')
        
        while ON:

            message=input('--> ')
            valid=0
            message=message.lower()

            if message=='ns':
                self.NS_opt()
                valid=1

            if message=='wh':
                self.WH_opt()
                valid=1

            if message=='amps':
                self.AMPS_opt()
                valid=1

            if message=='post':
                self.PostProcess()
                valid=1

            if message=='reset':
                StateVector=[SD,AL,Ns,W_H,Amps]
                valid=1

            if message=='set':
                self.SetVar()
                valid=1
                
            if message=='state':
                SD,AL,Ns,W_H,Amps=list(self.StateVector)
                print(' ')
                print('Axial Length    =',AL,'m')
                print('Number of Turns =',Ns,'')
                print('Slot Wide/High  =',W_H,'')
                print('Amps Per Phase  =',Amps,'A')
                print(' ')

            if message=='size':
                S()
                valid=1
            
            if message=='quit':
                ON=False
                valid=1

            if message=='help' or message=='?':
                print("You can request: ns, amps, wh, post, reset, set, state, & size")
                valid=1
                
            if valid==0:
                print(' ')
                print('!! You entered an invalid command :/')
