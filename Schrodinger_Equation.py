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

psi = psi * np.exp(-r / 3.0)

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



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1. Flatten our 3D grid matrices into 1D lists for the scatter plotter
x_flat = X.flatten()
y_flat = Y.flatten()
z_flat = Z.flatten()
prob_flat = probabilty_density.flatten()

# 2. Normalize the probabilities so they scale cleanly from 0.0 to 1.0
prob_max = np.max(prob_flat) if np.max(prob_flat) > 0 else 1.0
prob_normalized = prob_flat / prob_max

# 3. Filter out points with almost zero probability to keep the cloud sharp
# Change 0.05 higher or lower to change how 'dense' or 'fuzzy' the cloud looks
threshold = 0.05 
mask = prob_normalized > threshold

x_plot = x_flat[mask]
y_plot = y_flat[mask]
z_plot = z_flat[mask]
colors = prob_normalized[mask]

# 4. Generate the 3D Plot Window
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# 5. Create the fuzzy dot cloud
# 'c=colors' maps the brightness to the density, 'cmap=magma' gives a cool neon glow
scatter = ax.scatter(x_plot, y_plot, z_plot, c=colors, cmap='magma', 
                     s=2, alpha=0.3, edgecolors='none')

# 6. Add labels and style the box
ax.set_title(f"3D Electron Probability Cloud (l={l}, m={m})", fontsize=14)
ax.set_xlabel("X (Bohr radii)")
ax.set_ylabel("Y (Bohr radii)")
ax.set_zlabel("Z (Bohr radii)")

# Set visual boundaries to focus on the orbital center
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_zlim(-8, 8)

# Add a color bar to show the density scale
fig.colorbar(scatter, ax=ax, label="Relative Probability Density", shrink=0.5)

plt.show()
