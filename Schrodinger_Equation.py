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

#Set the mass equal to 1.0 electron mass since atomic units are used. This helps to simplify calculations and remove terms
mass_e = 1.0

#Set h-bar to 1.0 atomic unit of action for the same reason as using atomic units for the mass of an electron
h_bar = 1.0

#Calculate the step size between two adjacent points
h = r[1] - r[0]

#Create an array to store the value of the wave function at each point. Fill this array with zeros initially
psi = np.zeros(2000)

#Prompt the user for their total energy value guess
total_energy_guess = float(input("Enter an energy guess: "))
#You can calculate the energy using total_energy_guess = -1/2 * n ** 2

#Shooting Method
#This method requires two values of the wave function to begin. The first value of the wave function must be 0 if we start r at 0 since psi_true(r) = r * psi(r)
#Although our first r index is 0.01 not 0, it is a close enough approximation
#We can set out next value to 0.0001 since the schrodinger equation is linear and does not contain any exponents greater than 1 to the wave function itself
#This 0.0001 will just scale the wave function vertically up and down and is accounted for with Born's rule stating that the total probability of finding an electron must equal exactly 100%
#Born's rule mathematically means that the integral of the probabilty density must equal 1
psi[1] = 0.0001

#Use the shooting method and solve for all the other indexs of the wave function
for i in range(1, 1999):
    psi[i+1] = 2 * psi[i] - psi[i-1] - h ** 2 * 2 * (total_energy_guess - potential_energy[i]) * psi[i]

psi = psi * np.exp(-r / 3.0)

#Square the wave function since that equals the probabilty density
#Multiply by the step size as it gives you the width of the part under the curve
#Multiply by 4 * pi * r^2 since the electron is found in a sphere
#However if you don't get the true wave function first and you square the wave function to get the probabilty density, you have real_wave_function ^ 2 * r * 2
#And instead of adding the r ^ 2 from the 4 pi r ^ 2, you use the r ^ 2 from the built in non real wave function instead
total_probability = np.sum(np.abs(psi) ** 2) * h * 4.0 * np.pi

#total_probabilty finds the intergral of the wrong, unscaled probabilty density and divides our unscaled psi by sqrt total_probabilty so that we get a probabilty density summation of 1.0 when we later square this wave function
psi_normalized = psi / np.sqrt(total_probability)

#Convert the wave function to the actual wave function by dividing by r
#This is needed since the calculated wave function is psi in the equation, psi_true(r) = r * psi(r)
#So to obtain the true radial wave function, we divide by r
psi_normalized_true = psi_normalized / r

#Print the final value of the scaled and accurate wave function. The closer to 0, the better the data
print(psi_normalized_true[-1])


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
psi_1D = np.interp(distance, r, psi_normalized_true)

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

#OR just use sphe_har = sph_harm_y(m, l, phi, theta)

psi_3D = psi_1D * sphe_har

probabilty_density = np.abs(psi_3D) ** 2.0

#3D Canvas