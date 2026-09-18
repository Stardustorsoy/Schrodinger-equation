#Import Numerical Python for high performance arrays, entire array calculations and for advance math
import numpy as np


#Ask the user which sublevel they want
ask_l = input("What sublevel do you want?")

#If they entered the s sublevel, set the secondary quantum number (l) equal to 0
#Automatically set the third quantum number (m) equal to 0 since there are no other orbitals that an electron could exist in the s sublevel
if(ask_l == "s"):
    l = 0
    m = 0

#If they entered the p sublevel, set the l equal to 1
elif(ask_l == "p"):
    l = 1
    #Created a boolean to track if the user entered a correct orbital
    done = False
    while done == False:

        #Ask the user for the specific orbital they want
        m = int(input("Which orbital do want?"))

        #Check if m is not valid for the p level (m is not equal to -1, 0 , or 1)
        if m != -1 and m != 0 and m != 1:
            #Tell the user that their input was not valid and repeat the loop
            print("Not a valid orbital")
        else:
            #Break the loop
            done = True


#Make an array to track the potential energy which is filled with 2000 zeros
potential_energy = np.zeros(2000)

#Make an array for the radius. Starts from 0.01 and goes to 20 Bohr radius'. The value of the array are split into 2000 pieces
r = np.linspace(0.01,20,2000) 

#Fill each value of the potential_energy array using this equation
#The first bracket represents electrostatic attraction between the nucleus and electron
#Typically the formula is PE = - kZe^2 / r, however since atomic number of hydrogen is 1 and atomic units are used, the numerator is just 1.0
#The second bracket represents the centrifugal barrier
#If the electron has a non 0 l-value, there exists true angular momentum from "rotating around the nucleus" which be accounted for
#To find the rotational KE, combine the formulas L^2 = l(l+1) * h-bar , L^2 / 2I , and I = mr^2 to make l(l+1) / 2r^2 (m and h-bar are 1 since atomic units are used)
potential_energy = (-1.0/r) + ((l*(l+1))/(2.0 * r ** 2))

#Set the mass equal to 1.0 electron mass
mass_e = 1.0

#Set h-bar to 1.0 planck action
h_bar = 1.0

#Calculate the step size between two adjacent points
h = r[1] - r[0]

#Create an array to store the value of the wave function at each point
psi = np.zeros(2000)

total_energy_guess = float(input("Enter an energy guess: "))
#energy = -1/2 * n ** 2

#Shooting Method
psi[1] = 0.0001

for i in range(1, 1999):
    psi[i+1] = 2 * psi[i] - psi[i-1] - h ** 2 * 2 * (total_energy_guess - potential_energy[i]) * psi[i]

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
    sphe_har = 1.0 / (4.0 * np.pi) ** 0.5
elif (l == 1):
    if(m == -1):
        sphe_har = ((3.0 / (8.0 * np.pi)) ** 0.5) * np.sin(theta) * np.exp(-1j * phi)
    elif(m == 0):
        sphe_har = ((3.0 / (4.0 * np.pi)) ** 0.5) * np.cos(theta)
    else:
        sphe_har = -((3.0 / (8.0 * np.pi))  ** 0.5) * np.sin(theta) * np.exp(1j * phi)

#OR just use sphe_har = sph_harm(m, l, phi, theta)

psi_3D = psi_1D * sphe_har

probabilty_density = np.abs(psi_3D) ** 2.0

print(psi_3D[-1])