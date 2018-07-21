###########################################################################
# Riccardo Soldini - 2018                                                 #
#                                                                         #
# g3.py                                                                   #
#                                                                         #
###########################################################################


import math
from g2 import *
from dxfwrite import DXFEngine as dxf


def rotateX(p, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = -angle * math.pi / 180.0
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = p[1] * cosa - p[2] * sina
        z = p[1] * sina + p[2] * cosa
        return [p[0],y,z]
 
def rotateY(p, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = -angle * math.pi / 180.0
        cosa = math.cos(rad)
        sina = math.sin(rad)
        #z = self.z * cosa - self.x * sina
        #x = self.z * sina + self.x * cosa
        z = p[2] * cosa - p[0] * sina
        x = p[2] * sina + p[0] * cosa
        return [x,p[1],z]
 
def rotateZ(p, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180.0
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = p[0] * cosa - p[1] * sina
        y = p[0] * sina + p[1] * cosa
        return [x, y,p[2]]


def PlaneFrom3Points(p1,p2,p3):

    M=[float(p2[0]-p1[0]),float(p2[1]-p1[1]),float(p2[2]-p1[2]),
       float(p3[0]-p1[0]),float(p3[1]-p1[1]),float(p3[2]-p1[2])]

    K=[M[1]*M[5]-M[2]*M[4],
       M[2]*M[3]-M[0]*M[5],
       M[0]*M[4]-M[1]*M[3]]
    
    P=[K[0],K[1],K[2],-(K[0]*p1[0]+K[1]*p1[1]+K[2]*p1[2])]

    return P
