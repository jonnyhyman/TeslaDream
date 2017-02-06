import numpy as np
from PhaseI import Motor_Design_1__interface
from PhaseII import Motor_Design_2__interface
from PhaseIII import Motor_Design_3__interface

print(' ')
print('Welcome To TeslaDream V1.1')
print(' ')
print('''  There is something within me that might be illusion ''')
print('''  as it is often case with young delighted people, but if ''')
print('''  I would be fortunate to achieve some of my ideals, it would''')
print('''  it would be on the behalf of the whole of humanity.''')
print(' ')
print('''                                       - Nikola Tesla''')
print(' ')

def printMenu():
    print(' ')
    print('''- Main Menu:''')
    print('''   '1', '2', or '3' to select design phase''')
    print('''   'save' to save the spec file''')
    print('''   'quit' to exit the program''')
    print(' ')

Motor={}
Design=True
while Design:

    printMenu()
    Phase = input('--> ')
    print(' ')

    if Phase not in ['1','2','3']:
        if Phase == 'save':
            Design=False
        else:
            if Phase == 'quit':
                import sys
                sys.exit()
            else:
                print('Input 1, 2, or 3 phase, please!')
                print(' ')
    else:

        Next =False
        Phase=int(Phase)

        if Phase == 1:
            P1=Motor_Design_1__interface
            Next=(P1.PhaseI_()).Interface()
            if Next:
                Phase = 2
                Motor['P1']=Next

        if Phase == 2:
            P2=Motor_Design_2__interface
            Next=(P2.PhaseII_(Next)).Interface()
            if Next:
                Phase = 3
                Motor['P2']=Next

        if Phase == 3:
            P3=Motor_Design_3__interface
            Next=(P3.PhaseIII_(Next)).Interface()
            if Next:
                Motor['P3']=Next



# Gone through all the steps?
# Great! Let's save to a spec file for CAD use!

if len(Motor.keys())>=3:
    print("Calculating Motor Specifications...")
    print(' ')
    Specs={}
    Specs['SlotH    (mm)']=(Motor['P2'][2])['Stator'][1]*1000
    Specs['StatorID (mm)']=(Motor['P1'][1])['Ag_D'] * 1000 # mm
    Specs['StatorOD (mm)']=Specs['StatorID (mm)'] + Specs['SlotH    (mm)'] # mm
    Specs['ArcLn_PS (mm)']=(Motor['P2'][2])['Stator'][0]*1000 # Arc Length / Slot or SlotWidth
    Specs['RotorOD  (mm)']=Specs['StatorID (mm)'] - 1 # 1mm = airgap length (constant)
    Specs['RotorR2(Ohms)']=(Motor['P2'][2])['Perf'][3]
    Specs['AxialL   (mm)']=(Motor['P1'][1])['Ag_L'] * 1000 # mm
    Specs['WireAWG (AWG)']=(Motor['P2'][2])['Stator'][3]  # Stator
    Specs['N_Slots      ']=int((Motor['P2'][2])['Stator'][2]) # Slots
    Specs['N_Turns      ']=int((Motor['P1'][1])['Ns'])         # Stator
    Specs['WDensity     ']=2*Specs['N_Turns      ']/Specs['N_Slots      '] # Wires / Slot
    Specs['Angle_PS(rad)']=Specs['N_Slots      ']*(Specs['ArcLn_PS (mm)']/Specs['StatorID (mm)'])
                                                             # Angle / Slot
    import os.path

    num=0
    while (os.path.isfile("./SpecificationFiles/MotorSpecifications_"+str(num)+".csv")):
        num+=1
    else:
        outfile = open("./SpecificationFiles/MotorSpecifications_"+str(num)+".csv", "w")

    for s in Specs.keys():
        print('  ',s,Specs[s])

    for k in Specs.keys():
        outfile.write(k+',')
    outfile.write('\r')

    for v in Specs.keys():
        outfile.write(str(Specs[v])+',')
    outfile.write('\r')


else:
    print("Not enough data to save. Keys =",Motor.keys())
    print(" -- Needs P1,P2,P3")
    print(' ')
