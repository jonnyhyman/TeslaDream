import numpy as n
from .SupportingFunctions import *

# ---------------------------------------- Caveats and Assumptions
'''
    This calculator assumes an idealized model of induction motors:
     - model is built on steady-state assumption: not accurate for startup/shutdown
     - stator, rotor, and magnetizing reactances are neglected
     - stator windings estimated based on number of Ns and stator size
     - no end winding accountance
     - no resistance as varied by frequency (proximity effect + skin effect)

'''
# ---------------------------------------- Decisions
class m():
	def __init__(self):
	
		V1   = 228   # Stator Voltage per phase
		Nph  = 3     # phases
		Npo  = 4     # poles
		Ns   = 186   # Ns total (includes all three phases)
		R2   = 0.02  # Rotor resistance (varies with frequency... not modeled)
		f_e  = 380   # Hertz
		s    = 0.01  # Slip = (ns-nr / ns)
		AL   = 0.100 # meters Axial Length

	def T(StateVector):

		V1, f_e, s, Ns, R2, AL = list(StateVector)
		
		# ---------------------------------------- Requirements

		omega_s = (4*n.pi/Npo) * (f_e) # rad/s

		# ---------------------------------------- Resistance Estimate

		WL1=AL  # Stator Windings Axial Length
		WL2=AL  # Rotor Windings Axial Length

		R1=(33.31/1000)*AL*Ns     # Ohms/m*Length/Turns*Turns

		# ---------------------------------------- Calculations

		I1=   8*Nph   # Stator Current per phase
		P1L=(I1**2)*R1# Stator I2R losses

		I2=(1-s)*(I1-(P1L/V1)) # See page 332 & 333 power works analagous to torque since torque just freq multiple
		P2L=I2**2*R2  # Rotor I2R losses

		Torque = ( Nph*(I2**2) * (R2/s) / (omega_s) )

		print('Volts  =',double(V1),'V')
		print('StatorI=',double(I1),'A')
		print('RotorI =',double(I2),'A')
		print(' ')
		print('Ohms1  =',double(R1),'Ohms')
		print('Ohms2  =',double(R2),'Ohms')
		print(' ')
		print('Loss1  =',double(P1L),'W')
		print('Loss2  =',double(P2L),'W')
		print(' ')
		print('Freq   =',double(f_e),'Hz')
		print('Torque =',double(Torque),'Nm')

		return Torque,omega_s*30/n.pi # Return Nm, rpm
