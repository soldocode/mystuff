# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:32:34 2017

@author: UFFICIO TECNICO
"""

import matplotlib.pyplot as plt
from g2 import *
import random

def random_color():
    r=random.randrange(10,255)
    g=random.randrange(10,255)
    b=random.randrange(10,255)
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

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
                geos=g['path']
                color=g['color']
                #print (geos)
                for geo in geos:
                    plotFunction[geo.__class__.__name__](geo,color)
        plt.show()
           
    def reset(self):
        plt.close()


def plot_a_line(l=Line(Point(0,0),Point(100,0)),color=random_color()):
    plt.plot([l.p1.x,l.p2.x],[l.p1.y,l.p2.y],color=color)
    return
    
def plot_a_circle(c=Circle(Point(0,0),50),color=random_color()):
    plt.gcf().gca().add_artist(plt.Circle((c.center.x,c.center.y), c.radius,fill=False))
    return
    
def plot_a_point(p=Point(0,0),color=random_color()):
    plt.plot([p.x],[p.y],marker='D', linestyle='None')
    return    
  
def plot_a_path(p,color=random_color()):
    #print('draw path')
    c=list(p.chain)
    #print (c)
    nx=[]
    ny=[]
    while len(c)>0:
        index=c.pop(0)
        #print (index)
        n=p.nodes[index]
        nx.append(n.x)
        ny.append(n.y)
        if len(c)>1:
            geo=c.pop(0)
            if geo=='Arc':
                c.pop(0)
    #print(nx,ny)
    plt.plot(nx,ny,color)
    return
        
    
plotFunction={'Point':plot_a_point,
              'Line':plot_a_line,
              'Circle':plot_a_circle,
              'Path':plot_a_path}