import numpy as n
from .SupportingFunctions import *

# ---------------------------------------- Stator Sizing
class m():
    def Stator_Dimensions(Ns,Amps,Nph,eTpS,W_H,Ts,Srex,verbose=False): # inputs all SI

        Ts  =Ts  /1000
        Srex=Srex/1000

        SlotNum = Ns*(SpT)/(eTpS) # Turns * Slots/Turn = Slots
                                  # Slots / ExtraTurnsPerSlot = Slots
        
        WireD,AWGDesig = AWG_Diameter(Amps)
        WireNum=Nph*eTpS # phases * extra turns per slot

        if verbose:
            print('Wire Diam   =',WireD,'mm')
            print('Wire Gauge  =',AWGDesig,'AWG')
            print('Wire Number =',WireNum,'')
        
        Sa = (WireNum) * (WireD**2) # mm^2
        Sl=0
        Sh=0
        
        if W_H > 4:
            W_H=4

        if W_H == 1:           # @ @ @ @ @ @
            Sl = WireNum*WireD
            Sh = WireD
                                      # @ @ @
        if W_H == 2:                  # @ @ @
            Sl = 2/3*WireNum*WireD    
            Sh = (1-2/3)*WireNum*WireD
            
                                    # @ @
                                    # @ @
        if W_H == 3:                # @ @
            Sl = (1-2/3)*WireNum*WireD 
            Sh = (2/3)*WireNum*WireD

                                    # @ 
                                    # @ 
                                    # @ 
        if W_H == 4:                # @
                                    # @
                                    # @
            Sl = WireD
            Sh = WireNum*WireD

        if verbose:
            print('Slots       =',SlotNum)
            print('Slots Length=',Sl,'mm')
            print('Slots Height=',Sh,'mm')

        StatorCirc=SlotNum*(Sl + Ts) # mm
        StatorIDia=StatorCirc/(n.pi) #mm    
        StatorODia=StatorIDia + Srex + Sh #mm

        if verbose:
            print('Stator Circ =',StatorCirc,'mm')
            print('Stator OD   =',StatorODia,'mm')

        print('Stator ID   =',StatorIDia,'mm')
            
        return StatorIDia/1000 # return SI, meters

    # ---------------------------------------- Torque, Power Calc

    def Torque(Ns,Ks,Amps,StatorIDiameter,AxialL,Npo):


        Is_max = Amps # Amps maximum (thermally driven)
        D = StatorIDiameter # air gap diameter average (meters)
        l = AxialL # air gap axial length average (meters)

        Fs_max = 4/n.pi * (Ks*Ns/Npo) * (Is_max) # Maxmimum possible flux contribution

        Bsr = 1.5 # Teslas, saturation limit minimum

        Tmax = (Npo/2) * (n.pi*D*l/2) * Bsr * Fs_max # assumes dsr = -pi/2 (rotor drags = motor)
                                                      # you must further determine f_e to make dsr -pi/2
        print('Torque      =',Tmax,'Nm')
        print(' ')

        return Tmax
