
import pandas as p
from math import sqrt#, sin, cos
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib import transforms

#use distanices in AU (astronomic units)

def calc_orbit(*comets, earth=False, f=0):
    
    ax = plt.subplots(subplot_kw={'aspect': 'equal'})[1]
    amax = 0
    #alphamax = 0

    for elem in comets:
        afelio, perielio, alpha = elem
        a = ((afelio + perielio)/2)
        b = sqrt((a**2)-(((afelio-perielio)/2)**2))
        xc = -(afelio-perielio)/2
        yc = 0
        rot = transforms.Affine2D().rotate_deg_around(*(0,0), alpha)
        orbit = Ellipse((xc, yc), 2*a, 2*b, edgecolor="red", facecolor="None", transform=rot+ax.transData)
        ax.add_artist(orbit)
        if afelio > amax:
            amax = afelio
            alphamax = alpha

    if earth:
        at = 1.00000
        bt = 0.99986	
        xct = -0.01673261485841653
        yct = 0
        orbit = Ellipse((xct, yct), 2*at, 2*bt, edgecolor="black", facecolor="None")
        ax.add_artist(orbit)

    
    plt.plot(0,0, marker="o", color="orange")

#optimized way we set the axis limits to properly  center the subplot
    #ax.set_xlim(-((amax*2)*sin(alphamax-90)+8), ((amax*2)*sin(alphamax-90))+8)
    #ax.set_ylim(-((amax)*cos(alphamax-90)+8), ((amax)*cos(alphamax-90))+8)
    if f == 0:
        ax.set_xlim(-amax, amax)
        ax.set_ylim(-amax, amax)
    elif f == 1:
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)   

    plt.grid(color='lightgray',linestyle='--')
    plt.show()


def calc_energy(m, a):
    h = 2.5 * (10**6)     #end of atmosphere (2500km)
    G = 6,74 * (10**-11)  #universal gravity constant
    K = -(G/(a*2))        #orbital cinetic energy formula: -G/2a (will have to chek i'm not sure)
    Ug = m*h*9.8          #earth's potential gravitational energy
    # -> we maybe will have to calculate not this, but the attraction between the comet and the earth from their massses
    E = K + Ug            #total energy
    return E

data = p.read_csv("C:\\Users\\leosc\\OneDrive\\Desktop\\test\\near-earth-comets.csv")#test directory for dataframe
print(data.head())#.loc[:, ["Object", "Epoch", "q", "Q", "i"]])
x = data.iloc[0]
y = data.iloc[1]
z = data.iloc[2]
calc_orbit([x["Q"], x["q"], x["i"]], [y["Q"], y["q"], z["i"]], [z["Q"], z["q"], z["i"]], earth=True, f=0)
