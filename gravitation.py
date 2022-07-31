
from math import sqrt
from matplotlib import pyplot as plt

def draw_corps(*corps, focus=0, show=False, v=None, m=0):
    if m == 0:
        corps = list(corps)
    elif m == 1:
        corps = corps[0]
    print(corps)
    f = corps[focus]
    
    def draw_focus():
        for c in corps:
            ax.plot([c[0], f[0]], [c[1], f[1]], [c[2], f[2]], color="black", linewidth=.1)

    ax = plt.axes(projection='3d')
    max_r = max([c[4] for c in corps]) #r:x=max:750 => x=750*r/max
    print(max_r)
    [ax.scatter(c[0], c[1], c[2], marker="o", s=(750*c[4]/max_r)) for c in corps] #fix ordine di grandezza of radius
    [ax.text(c[0], c[1], c[2], f"m:{c[3]}; \ng:{round(calculate_g(c[3], c[4]), 3)}", size=5, zorder=10, color='k') for c in corps]
    
    if show:
        draw_focus()

    if v != None:
        ax.plot([v[0], f[0]], [v[1], f[1]], [v[2], f[2]], color="red", linewidth=2)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    #plt.plot(0,0)

    plt.show()

def calculate_g(m, r):
    g = 6.674*m/(r**2) #omitted e-11
    return g

def calc_gravity(*corps, focus=0, show=False):
    
    corps = list(corps)
    c1 = corps.copy()
    f = corps[focus]
    corps.remove(f)

    Fx = 0
    Fy = 0
    Fz = 0

    for c in corps:
        d = sqrt(((c[0] - f[0])**2 + (c[1] - f[1])**2 + (c[2] - f[2])**2))
        G = 6.674*10**(-11)
        #new way using versori
        Fx += G*((c[3]*f[3])*(c[0]-f[0])/(d**3))
        Fy += G*((c[3]*f[3])*(c[1]-f[1])/(d**3))
        Fz += G*((c[3]*f[3])*(c[2]-f[2])/(d**3))

    if show == True:
        print([Fx, Fy, Fz])
        draw_corps(c1, show=True, m=1, v=[Fx+f[0], Fy+f[1], Fz+f[2]])
    
    return Fx, Fy, Fz


calc_gravity([4,4,4,500,8],[1,2,3,300,5], [5,6,3,25,3], [7,4,3,400,6], [2,4,5,70,3.5], [2, 4, 6, 355, 3], show=True)
