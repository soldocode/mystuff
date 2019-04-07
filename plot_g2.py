# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:32:34 2017

@author: UFFICIO TECNICO
"""

import matplotlib.pyplot as plt
from g2 import *


class Scene:
    def __init__(self,geometries=[],area=[-200,200,-200,200]):
        self.geometries=geometries
        self.area=area

    @property
    def as_dict(self):
       return dict(geometries=self.geometries)
       
    def show(self):
        plt.close()
        plt.axis(self.area)
        for block in self.geometries:
            for g in block:
                plotFunction[g.__class__.__name__](g)
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
  
def plot_a_path(p):
    #print('draw path')
    c=list(p.chain)
    nx=[]
    ny=[]
    while len(c)>0:
        n=p.nodes[c.pop(0)]
        nx.append(n.x)
        ny.append(n.y)
        if len(c)>1:
            c.pop(0)
    #print(nx,ny)
    plt.plot(nx,ny)
    return
        
    
plotFunction={'Point':plot_a_point,
              'Line':plot_a_line,
              'Circle':plot_a_circle,
              'Path':plot_a_path}