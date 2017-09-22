# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:32:34 2017

@author: UFFICIO TECNICO
"""

import matplotlib.pyplot as plt
from g2 import *


class Scene:
    def __init__(self,geometries=[]):
        self.geometries=geometries

    @property
    def as_dict(self):
       return dict(geometries=self.geometries)
       
    def show(self):
        plt.close()
        plt.axis([-200,200,-200,200])
        for g in self.geometries:
            plotFunction[type(g[0])](g[0])
        plt.show()
           
    def reset(self):
        plt.close()



def plot_a_line(l=Line(Point(0,0),Point(100,0))):
    plt.plot([l.p1.x,l.p2.x],[l.p1.y,l.p2.y])
    return
    
def plot_a_circle(c=Circle(Point(0,0),50)):
    plt.gcf().gca().add_artist(plt.Circle((c.center.x,c.center.y), c.radius,fill=False))
    return
    
def plot_a_point(p=Point(0,0)):
    plt.plot([p.x],[p.y],marker='D', linestyle='None')
    return    
  
    
plotFunction={Point:plot_a_point,Line:plot_a_line,Circle:plot_a_circle}