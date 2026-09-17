import numpy as np
import math

ask_l = input("What sub-level do you want?")

l = 0
m = 0

if(ask_l == "s"):
    l = 0
    m = 0

elif(ask_l == "p"):
    l = 1
    done = False
    while done == False:
        m = int(input("Which orbital do want?"))
        if m != -1 and m != 0 and m != 1:
            print("Not a valid orbital")
        else:
            done = True

voltage = np.zeros(2000)
#Make an array for the radius. Starts from 0.01 and goes to 20 Bohr radius'. The value of the array are split into 1000 
r = np.linspace(0.01,20,2000) 

voltage = (-1.0/r) + (l*(l+1))/(2.0 * r ** 2)

#Make the mass 1.0 electron mass
mass_e = 1.0
#Make h-bar 1.0 planck action
h_bar = 1.0
#Calculate the step size between two adjacent points
h = r[1] - r[0]
#Create an array to store the value of the wave function at each point
psi = np.zeros(2000)

energy = float(input("Enter an energy guess: "))
#energy = -1/2n ** 2

#Shooting Method
psi[1] = 0.0001

for i in range(1, 1999):
    psi[i+1] = 2 * psi[i] - psi[i-1] - h ** 2 * 2 * (energy - voltage[i]) * psi[i]
    

print(psi[-1])



grid_line = np.linspace(-10,10,100);
X, Y, Z = np.meshgrid(grid_line, grid_line, grid_line)
#Solve for the distance from 0, 0, 0
distance = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
#Solve for the polar angle, represented theta and is the angle between the z-axis and the line
#Add the 1e-15 to prevent dividing by 0. Can't used arccos2 to negate this since it doesn't exist
theta = np.arccos(Z / (distance + 1e-15))
#Solve for the azimulthal angle, represented by phi and is the angle between the y-axis and the line
#Use arctan2 since it is able to deal with false angles and dividing by 0
#Will automatically do Y / X
phi = np.arctan2(Y,  X)

#Interpolate psi into the 3D grid
psi_1D = np.interp(distance, r, psi)

#Spherical Harmonics
if (l == 0):
    sphe_Har = 1.0 / (4.0 * np.pi) ** 0.5
elif (l == 1):
    if(m == -1):
        sphe_Har = (3.0 / (8.0 * np.pi * np.sin(theta) * np.exp(-1j * phi))) ** 0.5
    elif(m == 0):
        sphe_Har = (3.0 / (4.0 * np.pi * np.cos(theta))) ** 0.5
    else:
        sphe_Har = -(3.0 / (8.0 * np.pi * np.sin(theta) * np.exp(1j * phi))) ** 0.5

psi_3D = psi_1D * sphe_Har

probabilty_density = np.abs(psi_3D) ** 2.0

