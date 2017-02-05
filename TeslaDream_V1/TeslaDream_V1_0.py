from PhaseI import Motor_Design_1__interface
from PhaseII import Motor_Design_2__interface
from PhaseIII import Motor_Design_3__interface

print(' ')
print('Welcome To TeslaDream V1.0')
print(' ')
print('''  “There is something within me that might be illusion ''')
print('''  as it is often case with young delighted people, but if ''')
print('''  I would be fortunate to achieve some of my ideals, it would''')
print('''  it would be on the behalf of the whole of humanity.”''')
print(' ')
print('''                                       - Nikola Tesla''')
print(' ')

while True:

    Phase = input('Select your design phase! -> ')
    print(' ')

    if Phase not in ['1','2','3']:
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
                
        if Phase == 2:
            P2=Motor_Design_2__interface
            Next=(P2.PhaseII_(Next)).Interface()
            if Next:
                Phase = 3
                
        if Phase == 3:
            P3=Motor_Design_3__interface
            Next=(P3.PhaseIII_(Next)).Interface()
            if Next:
                print("This is where we save files")
