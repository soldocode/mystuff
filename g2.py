# -*- coding: utf-8 -*-
"""
@author: Riccardo Soldini
@email: riccardo.soldini@gmail.com
"""

import math

class cNode:
    def __init__(self,parent=None,child=None):
        self.parent=parent
        self.child=child
        

class Point:
    def __init__(self, x=0, y=0,node=cNode()):
        self._x=x
        self._y=y
        self.node=node

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, x):
        if  self.node.parent:
            self.node.parent.__setattr__(self.node.child,Point(x=x,y=self._y))
        else:    
            self._x = x
        
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, y):
        if  self.node.parent:
            self.node.parent.__setattr__(self.node.child,Point(x=self._x,y=y))
        else:    
            self._y = y
        
    def __repr__(self):
       return 'Point (X='+str(self._x)+', Y='+str(self._y)+')'
          

class Angle:
    def __init__(self, deg=None, rad=None, parent=None):
        if deg is not None:
           self._deg = deg
           self._rad = math.radians(deg)
        elif rad is not None:
           self._rad = rad
           self._deg = math.degrees(rad)
        self.parent=parent   

    @property
    def deg(self):
        return self._deg
    @deg.setter
    def deg(self, value):
        if self.parent: 
            self.parent.angle=Angle(deg=value,parent=self.parent)
        else:
           self._deg = value
           self._rad = math.radians(value)

    @property
    def rad(self):
        return self._rad
    @rad.setter
    def rad(self, value):
        if self.parent:
            self.parent.angle=Angle(rad=value,parent=self.parent)
        self._rad = value
        self._deg = math.degrees(value)
        
    def __repr__(self):
        return 'degrees='+str(self._deg)+' | radians='+str(self._rad)
     

class Delta:
    def __init__(self, x=0, y=0, parent=None):
        self._x=x
        self._y=y
        self.parent=parent

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, x):
        if self.parent:
            self.parent.delta=Delta(x=x,y=self._y,parent=self.parent)
        else:    
            self._x = x
        
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        if self.parent:
            self.parent.delta=Delta(x=self._x,y=value,parent=self.parent)
        else:    
            self._y = value
        
    def __repr__(self):
       return 'Delta (X='+str(self._x)+', Y='+str(self._y)+')'    

       
class Polar:
    def __init__(self,module=0,angle=Angle(),parent=None):
        self._module=module
        self._angle=angle
        self._angle.parent=self
        self.parent=parent
       
    @property    
    def module(self): 
        return self._module
    @module.setter
    def module(self,module):
        if self.parent:
            self.parent.polar=Polar(module,self._angle,parent=self.parent)
        else:    
            self._module=module
            
    @property    
    def angle(self): 
        return self._angle
    @angle.setter
    def angle(self,angle):
        if self.parent:
            self.parent.polar=Polar(self._module,angle,parent=self.parent)
        else:    
            self._angle=angle
    
    def __repr__(self):
        return 'Polar (module='+str(self._module)+', angle='+repr(self.angle)+' )'           

        
class Line:
    def __init__(self, p1=Point(),p2=Point()):
        self._p1=p1
        self._delta=Delta(0,0)
        self._p2=Point()
        if type(p2)==Delta:
            self._p2=Point(self._p1.x+p2.x,self._p1.y+p2.y)
            self._delta=p2
            self._polar=VectorFromTwoPoints(self._p1,self._p2)
        elif type(p2)==Polar:
            self.delta=Delta(p2.module*math.cos(p2.angle.rad),p2.module*math.sin(p2.angle.rad))
            self._polar=p2
        else:
            self._p2=p2
            self._delta=Delta(self._p2.x-self._p1.x,self._p2.y-self._p1.y)
            self._polar=VectorFromTwoPoints(self._p1,self._p2)
        self._polar.parent=self._delta.parent=self
        self._p1.node=cNode(parent=self,child='p1')
        self._p2.node=cNode(parent=self,child='p2')
    
    @property
    def p1(self):
        return self._p1
    @p1.setter
    def p1(self, p):
        self._p1 = p
        self._p1.node=cNode(parent=self,child='p1')
        self._delta=Delta(self._p2.x-self._p1.x,self._p2.y-self._p1.y,parent=self)
        self._delta.parent=self
        self._polar=VectorFromTwoPoints(self._p1,self._p2) 
        self._polar.parent=self
                
    @property
    def p2(self):
        return self._p2
    @p2.setter
    def p2(self, p):
        self._p2 = p
        self._p2.node=cNode(parent=self,child='p2')
        self._delta=Delta(self._p2.x-self._p1.x,self._p2.y-self._p1.y,parent=self)       
        self._delta.parent=self
        self._polar=VectorFromTwoPoints(self._p1,self._p2) 
        self._polar.parent=self
        
    @property
    def delta(self):
        return self._delta
    @delta.setter
    def delta(self,delta):
        self._delta=delta
        self._delta.parent=self
        self._p2._x=self._p1.x+self._delta.x
        self._p2._y=self._p1.y+self._delta.y
        self._polar=VectorFromTwoPoints(self._p1,self._p2) 
        self._polar.parent=self

    @property
    def polar(self):
        return self._polar
    @polar.setter
    def polar(self,polar):
        self._polar=polar
        self._polar.parent=self
        self._p2=PointFromVector(self._p1,polar) 
        self._p2.node=cNode(parent=self,child='p2')
        self._delta.x=self._p2.x-self._p1.x
        self._delta.y=self._p2.y-self._p1.y
        
    def __repr__(self):
       return 'Line from '+repr(self._p1)+' to '+repr(self._p2)
       
class Circle:
    def __init__(self,center=Point(),radius=0.0):
        self._center=center
        self._radius=radius
        
    @property
    def center(self):
        return self._center
        
    @property
    def radius(self):
        return self._radius  
        
    @property
    def diameter(self):
        return self._radius*2    
        
    @property    
    def pointUp(self):
        return Point(self._center.x,self._center.y+self._radius)

    @property
    def pointBottom(self):
        return Point(self._center.x,self._center.y-self._radius)
    
    @property
    def pointRight(self):
        return Point(self._center.x+self._radius,self._center.y)
        
    @property
    def pointLeft(self):
        return Point(self._center.x-self._radius,self._center.y)
        
    
       
def AngleFromTwoPoints(p1,p2):
    deltaX=float(p2.x-p1.x)
    deltaY=float(p2.y-p1.y)
    degree=math.degrees(math.atan2(deltaY,deltaX))
    return Angle(deg=degree)           


def VectorFromTwoPoints(p1,p2):   
    module=math.sqrt(math.pow(p2.x-p1.x,2)+math.pow(p2.y-p1.y,2))
    return Polar(module,AngleFromTwoPoints(p1,p2))
    
    
def PointFromVector(p,v):
    return Point(p.x+v.module*math.cos(v.angle.rad),p.y+v.module*math.sin(v.angle.rad))
    
        
    