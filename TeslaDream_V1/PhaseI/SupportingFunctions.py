def double(data):
    return '{0:.2f}'.format(data)

def AWG_Diameter(Amps):

    AWG=[ #AWG Designation "Gauge"
            '0000 (4/0)',
            '000 (3/0)',
            '00 (2/0)',
            '0 (1/0)',
            '1',
            '2',
            '3',
            '4',
            '6',
            '8',
            '10',
            '12',
            '14',
            '16',
            '18',
            '20',
            '22',
            '24',
            '26',
            '28',
            '30',
            '32',
            '34'
        ]


    Diameters=[ #mm
                11.684,
                10.405,
                9.266,
                8.251,
                7.348,
                6.544,
                5.827,
                5.189,
                4.115,
                3.264,
                2.588,
                2.053,
                1.628,
                1.291,
                1.024,
                0.812,
                0.644,
                0.511,
                0.405,
                0.321,
                0.255,
                0.202,
                0.16
                ]

    Ampacity=[ #A
            195,
            165,
            145,
            125,
            110,
            95,
            85,
            70,
            55,
            40,
            30,
            20,
            15,
            22,
            10,
            11,
            7,
            3.5,
            2.2,
            1.4,
            0.86,
            0.53,
            0.3
        ]

    nums = len(Ampacity) #number of entries in database

    for i in range(0,nums):
        if Ampacity[(nums-1)-i]>Amps: # count from bottom UP to avoid undersizing
            return Diameters[(nums-1)-i],AWG[(nums-1)-i] # return when proper size found
        
import matplotlib.pyplot as plt
#==============================================================================
# 
# Plot Functions
# 
#==============================================================================
def plot2d(x,y): 
    
    plt.plot(x, y,color='Blue')  
    plt.yscale('linear')
    plt.grid(True)
    axes = plt.gca()
    plt.show()
    
def plot3d(xyz_List,title,save,savename='3DFullPlot'):  # usage: plot3d([x,y,z],"Full Airfoil Plot",1,"nameofpic")
    from mpl_toolkits.mplot3d import Axes3D  
    x,y,z = xyz_List
         
    fig = plt.figure( figsize=(6, 8), dpi=80, facecolor='w', edgecolor='k')
    ax = fig.gca(projection='3d')
    ax.set_xlim([0,1])
    ax.set_ylim([-0.5,0.5])
  #  ax.set_zlim([0,1])
    
    ax.plot(x,y,z,color='Blue') 
    if save:
        plt.savefig('./3D_Plots/'+savename+'.png',bbox_inches='tight')
        plt.close()
    else:
        plt.show()
