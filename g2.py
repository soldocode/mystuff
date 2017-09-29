
###############################################################################
# g2.py - 2d framework module - 2017
#
# Riccardo Soldini - riccardo.soldini@gmail.com
###############################################################################


import math, sympy


class cNode:
    def __init__(self,parent=None,child=None):
        self.parent=parent
        self.child=child

    @property
    def as_dict(self):
       return dict(parent=self.parent,child=self.child)


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
            
    @property
    def to_sympy(self):
        return sympy.Point2D(self._x,self._y)         

    @property
    def as_dict(self):
        return dict(y=self._y, x=self._x)

    def __repr__(self):
        return 'Point (x='+str(self._x)+', y='+str(self._y)+')'


       
class Angle:
    def __init__(self, deg=None, rad=None, parent=None):
        self._deg=0
        self._rad=0
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
        
    @property
    def normalized(self):
        n=self._deg-int(self._deg/360)*360
        if n<0:n=n+360
        return Angle(deg=n)

    @property
    def as_dict(self):
       return dict(deg=self._deg)

    def __repr__(self):
        return 'angle (degrees='+str(self._deg)+' | radians='+str(self._rad)+')'


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
       return 'delta (X='+str(self._x)+', Y='+str(self._y)+')'


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
        return 'polar (module='+str(self._module)+', angle='+repr(self.angle)+' )'


class BoundBox:
    def __init__(self,bottomleft=Point(),topright=Point()):
        self.bottomleft=bottomleft
        self.topright=topright

    def updateWithPoint(self,p):
        if p.x>self.topright.x:self.topright.x=p.x
        if p.x<self.bottomleft.x:self.bottomleft.x=p.x
        if p.y>self.topright.y:self.topright.y=p.y
        if p.y<self.bottomleft.y:self.bottomleft.y=p.y
        
    def __repr__(self):
        return 'BoundBox(bottomleft='+str(self.bottomleft)+', toprigth='+str(self.topright)+')'


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
        
    def pointAt(self,value):
        result=None
        if (value>=0.0) and (value<=self._polar.module):
            l=Line(self._p1,Polar(value,self._polar.angle))
            result=l.p2
        return result

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

    @property
    def lenght(self):
        return self._polar.module

    @property
    def boundBox(self):
        bottom_left=Point()
        top_right=Point()
        if self._p1.x<self._p2.x :
            bottom_left.x=self._p1.x
            top_right.x=self._p2.x
        else:
            bottom_left.x=self._p2.x
            top_right.x=self._p1.x
        if self._p1.y<self._p2.y :
            bottom_left.y=self._p1.y
            top_right.y=self._p2.y
        else:
            bottom_left.y=self._p2.y
            top_right.y=self._p1.y
        return BoundBox(bottom_left,top_right)

    @property
    def to_sympy(self):
        return sympy.Line(self._p1.to_sympy,self.p2.to_sympy)
        
    @property
    def get_coeff_equation(self):
        m=math.tan(self._polar.angle.rad)
        if self._p1.y==self._p2.y:
            m=0.0
        q=self._p1.y-m*self._p1.x
        return dict(m=m,q=q)

    @property
    def as_dict(self):
        return dict(p2=self._p2.as_dict,p1=self._p1.as_dict)

    def __repr__(self):
        return 'Line ('+repr(self._p1)+', '+repr(self._p2)+')'

class Circle:
    def __init__(self,center=Point(),arg=0.0):
        self._center=center
        if type(arg)==Point:
            self._radius=Line(center,arg).polar.module
        else:
            self._radius=arg
        
    def pointAt(self,value):
        result=None
        if (value>=0.0) and (value<=self.lenght):
            l=Line(self._center,Polar(self._radius,Angle(deg=360/self.lenght*value)))
            result=l.p2
        return result    

    @property
    def center(self):
        return self._center

    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self,radius):
        self._radius=radius

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

    @property
    def lenght(self):
        return self._radius*math.pi*2
       
    @property    
    def area(self):
        return math.pow(self._radius,2)*math.pi    

    @property
    def boundBox(self):
        bottom_left=Point(self._center.x-self._radius,
                          self._center.y-self._radius)
        top_right=Point(self._center.x+self._radius,
                        self._center.y+self._radius)
        return BoundBox(bottom_left,top_right)


    @property
    def to_sympy(self):
        return sympy.Circle(self._center.to_sympy,self._radius)
 
    @property
    def get_coeff_equation(self):
         a=-2*self._center.x
         b=-2*self._center.y
         c=math.pow(self._center.x,2)+math.pow(self._center.y,2)-math.pow(self._radius,2)
         return dict(a=a,b=b,c=c)
        
    @property
    def as_dict(self):
        return dict(radius=self._radius, center=self._center.as_dict)

    def __repr__(self):
        return 'circle (center='+repr(self._center)+', radius='+repr(self.radius)+' )'


class Arc(Circle):
    def __init__(self,pointStart=Point(),pointMiddle=Point(),pointEnd=Point()):
        Circle.__init__(self)
        self._pointStart=pointStart
        self._pointEnd=pointEnd
        self._pointMiddle=pointMiddle
        self._pointStart.node=cNode(self,'pointStart')
        self._pointEnd.node=cNode(self,'pointEnd')
        self._pointMiddle.node=cNode(self,'pointMiddle')
        self._boundBox=BoundBox(pointStart,pointStart)
        self.updateArc()
        
    def pointAt(self,value):
        result=None
        if (value>=0.0) and (value<=self.lenght):
            a=self.angleStart.deg+(self.angle.deg/self.lenght)*value
            l=Line(self._center,Polar(self._radius,Angle(deg=a)))
            result=l.p2
        return result      

    @property
    def pointStart(self):
        return self._pointStart
    @pointStart.setter
    def pointStart(self,p):
        self._pointStart=p
        self.updateArc()

    @property
    def pointEnd(self):
        return self._pointEnd
    @pointEnd.setter
    def pointEnd(self,p):
        self._pointEnd=p
        self.updateArc()

    @property
    def pointMiddle(self):
        return self._pointMiddle
    @pointMiddle.setter
    def pointMiddle(self,p):
        self._pointMiddle=p
        self.updateArc()
        
    @property
    def chord(self):    
        return Line(self.pointStart,self.pointEnd)
        
    @property
    def segmentArea(self):
        alfa=self.angle.rad
        return ((alfa-math.sin(alfa))/2)*math.pow(self._radius,2)

    def updateArc(self):
        a=[0,0,0]
        b=[0,0,0]
        c=[0,0,0]
        d=[0,0,0]

        a[0]=self._pointStart.x
        b[0]=self._pointStart.y
        c[0]=1
        d[0]=math.pow(self._pointStart.x,2)+math.pow(self._pointStart.y,2)

        a[1]=self._pointMiddle.x
        b[1]=self._pointMiddle.y
        c[1]=1
        d[1]=math.pow(self._pointMiddle.x,2)+math.pow(self._pointMiddle.y,2)

        a[2]=self._pointEnd.x
        b[2]=self._pointEnd.y
        c[2]=1
        d[2]=math.pow(self._pointEnd.x,2)+math.pow(self._pointEnd.y,2)

        detM=DetMatrix3x3(a,b,c)
        detA=DetMatrix3x3(d,b,c)
        detB=DetMatrix3x3(a,d,c)

        self._center.x=detA/detM/2
        self._center.y=detB/detM/2

        self.radius=VectorFromTwoPoints(self._center,self._pointStart).module
        self.updateBoundBox()
        
    @property
    def angleStart(self):
        return VectorFromTwoPoints(self._center,self._pointStart).angle

    @property
    def angleEnd(self):
        return VectorFromTwoPoints(self._center,self._pointEnd).angle

    @property
    def angle(self):
        s=self.angleStart.deg
        e=self.angleEnd.deg
        if s<e:s=s+360
        diff=s-e
        if Triangle(self._pointStart,self._pointMiddle,self._pointEnd).orientation==-1:
            diff=diff-360
        return Angle(deg=(-diff))

    @property
    def lenght(self):
        return abs(self._radius*self.angle.rad)

    @property
    def boundBox(self):
        return self._boundBox
        
    @property
    def orientation(self):
        return Triangle(self._pointStart,self._pointMiddle,self._pointEnd).orientation
        
    def updateBoundBox(self):    

        if self.orientation==1:
            s=self.angleEnd.normalized.deg
        else:
            s=self.angleStart.normalized.deg

        e=s+abs(self.angle.deg)
    
        aa=[s]
        go=True
        while go:
            go=False
            if (s>=0) & (s<90) & (s<e) & (e>90):
                aa.append(90)
                s=90
                go=True
            if (s>=90) & (s<180) & (s<e) & (e>180):
                aa.append(180)
                s=180
                go=True
            if (s>=180) & (s<270) & (s<e) & (e>270):
                aa.append(270)
                s=270
                go=True
            if (s>=270) & (s<360) & (s<e) & (e>360):
                aa.append(0)
                s=0
                e=e-360
                go=True

        aa.append(e)

        newBoundBox=Line(self._pointStart,self._pointEnd).boundBox
        for a in aa:
            newBoundBox.updateWithPoint(PointFromVector(self._center,Polar(self._radius,Angle(deg=a))))

        self._boundBox=newBoundBox    


    @property
    def as_dict(self):
       return dict(pEnd=self._pointEnd.as_dict, pMiddle=self._pointMiddle.as_dict, pStart=self._pointStart.as_dict)

    def __repr__(self):
        return 'arc (start='+repr(self._pointStart)+', middle='+repr(self.pointMiddle)+', end='+repr(self.pointEnd)+' )'

class Path:
    def __init__(self,nodes=[],chain=[]):
        self._nodes=nodes
        self._chain=chain
        self._geometries=[]
        self._lenght=0
        self.update()
  
    
    def update(self):
        gg=[]
        # cc=self._chain.copy()--> run only wirh 3.x
        cc=list(self._chain) # --> try with 2.7
        if len(cc)>0:p1=cc.pop(0)
        while len(cc)>0:
            geo=cc.pop(0)
            p2=cc.pop(0)
            if geo=='Arc': 
                p3=cc.pop(0)
                gg.append([geo,p1,p2,p3])
                p1=p3
            else :
                gg.append([geo,p1,p2])
                p1=p2

        self._geometries=gg        

        cbb=BoundBox()
        cl=0
        l=len(gg)
        if l>0:
            cbb=self.geo(0).boundBox
            cl=self.geo(0).lenght
            for g in range(1,l):
                g_bb=self.geo(g).boundBox
                cbb.updateWithPoint(g_bb.bottomleft)
                cbb.updateWithPoint(g_bb.topright)
                cl+=self.geo(g).lenght
        self._boundBox=cbb
        self._lenght=cl 
        
  
    def geo(self,id_geometry):
        g=''
        nn=[]
        if id_geometry<len(self._geometries)+1:
            g=self._geometries[id_geometry][0]
            for n in self._geometries[id_geometry][1:]:
                nn.append(self._nodes[n])
        return Geo(g,nn)     

        
    def pointAt(self,value):
        result=None
        if (value>=0.0) and (value<=self.lenght):
            i=0
            compute_len=0
            compute_len_old=0       
            while (compute_len<value) and (i<len(self._geometries)):
                compute_len_old=compute_len
                compute_len+=self.geo(i).lenght
                i=i+1 
            compute_len_old+=0.0000000001    
            result=self.geo(i-1).pointAt(value-compute_len_old)    
        return result
     
        
    def appendGeo(self,element):
        self._chain+=element
        self.update()
        
        
    def insertGeo(self,element,idGeo):
        cc=self._chain.copy()
        i=1
        while idGeo>0:
            cc.pop(0)
            g=cc.pop(0)
            if g=='Arc':
                cc.pop(0)
                i=i+3
            else:
                i=i+2
            idGeo-=1
        self._chain[i:1]=element
        self.update()
        
        
    def removeGeo (self,idGeo):
        cc=self._chain.copy()
        i=1
        while idGeo>0:
            cc.pop(0)
            g=cc.pop(0)
            if g=='Arc':
                cc.pop(0)
                i=i+3
            else:
                i=i+2
            idGeo-=1
        self._chain.pop(i)
        self._chain.pop(i)
        if g=='Arc': self._chain.pop()
        self.update()
        
    @property
    def chain(self):
        return self._chain
    @chain.setter
    def chain(self,chain):
        self._chain=chain
        self.update()
        
    @property
    def nodes(self):
        return self._nodes
    @nodes.setter
    def nodes(self,nodes):
        self._nodes=nodes
        self.update()    
    
    @property
    def geometries(self):
        return self._geometries
        
    @property
    def boundBox(self):
        return self._boundBox

    @property
    def lenght(self):
        return self._lenght
        
    @property
    def isClosed(self):        
        result=False
        if self._chain[0]==self._chain[-1]:result=True
        if self._chain[1]=='Circle':result=True
        return result
        
    @property
    def orientation(self):  #to be fixed
        o=0
        p1=self._chain[0]
        for geo in self._geometries:
           o+=Triangle(self._nodes[p1],
                       self._nodes[geo[1]],
                       self._nodes[geo[2]]).orientation
           if geo[0]=='Arc':
               o+=Triangle(self._nodes[p1],
                           self._nodes[geo[1]],
                           self._nodes[geo[2]]).orientation
        return (o>0) - (o<0)    
        
    @property
    def area(self):
        if self.isClosed:
            if self._chain[1]=='Circle':
                result=self.geo(0).area
            else:
                result=0
                p1=self._chain[0]
                for geo in self._geometries:
                    if geo[0]=='Arc':
                       result+=Triangle(self._nodes[p1],
                                        self._nodes[geo[1]],
                                        self._nodes[geo[3]]).area            
                       result+=Arc(self._nodes[geo[1]],
                                   self._nodes[geo[2]],
                                   self._nodes[geo[3]]).segmentArea       
                    else:               
                       result+=Triangle(self._nodes[p1],
                                        self._nodes[geo[1]],
                                        self._nodes[geo[2]]).area       
                    
        else:
            result=0
        return abs(result)    

    @property
    def as_dict(self):
        nodes=[]
        for node in self._nodes:
            nodes.append(node.as_dict)
        return dict(nodes=nodes, geometries=self._geometries)
        
    def __repr__(self):
        return 'Path (boundBox='+repr(self._boundBox)+', lenght='+repr(self._lenght)+' )'       

        
class Shape:
    def __init__(self,outline=Path(),internal=[],boundBox=[Point(),Point()]):
        self.outline=outline
        self.internal=internal
        self._boundBox=boundBox
        self._perimeter={'outline':0,'internal':[]}
        self._area={'outline':0,'internal':[]}
        self.update()

    def update(self):
        self._perimeter['outline']=self.outline.lenght
        self._area['outline']=self.outline.area
        self._boundBox=self.outline.boundBox
        for contour in self.internal:
            self._perimeter['internal'].append(contour.lenght)
            self._area['internal'].append(contour.area)
            self._boundBox.updateWithPoint(contour.boundBox.bottomleft)
            self._boundBox.updateWithPoint(contour.boundBox.topright) 
            
    @property
    def boundBox(self):
        return self._boundBox

    @property
    def perimeter(self):
        return self._perimeter

    @property
    def area(self):
        return self._area
        
    def __repr__(self):
        return 'Shape (boundBox='+repr(self.boundBox)+')'

        
class Triangle:
    def __init__(self,p1=Point(),p2=Point(),p3=Point()):
        self.p1=p1
        self.p2=p2
        self.p3=p3
      
    @property
    def orientation(self):
        o=((self.p3._x-self.p1._x) * (self.p2._y-self.p1._y))
        o-= ((self.p2._x-self.p1._x) * (self.p3._y-self.p1._y))
        return (o>0) - (o<0)
    
    @property
    def area(self):
        a=[self.p1._x,self.p1._y,1]
        b=[self.p2._x,self.p2._y,1]
        c=[self.p3._x,self.p3._y,1]
        return 0.5*DetMatrix3x3(a,b,c)  
        
    def __repr__(self):
        return 'Triangle (p1='+repr(self.p1)+', p2='+repr(self.p2)+' ,p3='+repr(self.p3)+')'
        
        
        
def Geo (geometry,nodes):
    makeGeo={'Line':Line,'Circle':Circle,'Arc':Arc}
    return makeGeo[geometry](*nodes)
        
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

def DetMatrix3x3(A,B,C):
    return A[0]*(B[1]*C[2]-B[2]*C[1])+ \
           A[1]*(B[2]*C[0]-B[0]*C[2])+ \
           A[2]*(B[0]*C[1]-B[1]*C[0])
           
def StepsBetweenAngles(a1,a2,d):
    a1=a1.normalized
    a2=a2.normalized
    angles=[a1]
    if a2.deg>a1.deg:step=(a2.deg-a1.deg)/d
    else:  step=(a2.deg+360-a1.deg)/d
    for i in range(1,d):
        s=a1.deg+step*i
        if s>360:s=s-360
        angles.append(Angle(deg=s))
    angles.append(a2)
    return angles

    
def IntersectionCircleToLine(circle,line):
    
    result=[]
    xmin=line.boundBox.bottomleft.x
    ymin=line.boundBox.bottomleft.y
    xmax=line.boundBox.topright.x
    ymax=line.boundBox.topright.y

    # (x - xc)^2 + (y - yc)^2 = r^2
    # x^2+y^2+ax+by+c=0
    # get a,b,c value of circle equation
    eqC=circle.get_coeff_equation
    
    if line.p1.x==line.p2.x:       
        # get system equation coefficient
        A=1
        B=eqC['b']
        C=math.pow(line.p1.x,2)+eqC['a']*line.p1.x+eqC['c']

        #solve
        DELTA=math.pow(B,2)-4*A*C
        if DELTA>=0:
            y1=(-B-math.sqrt(DELTA))/(2*A)
            if y1>=ymin and y1<=ymax:
                result.append(Point(line.p1.x,y1))
            if DELTA>0:
                y2=(-B+math.sqrt(DELTA))/(2*A)
                if y2>=ymin and y2<=ymax:
                    result.append(Point(line.p1.x,y2))
                    
    else:      
        # get m,q
        eqL=line.get_coeff_equation

        # get system equation coefficient
        A=1+math.pow(eqL['m'],2)
        B=2*eqL['m']*eqL['q']+eqC['a']+eqC['b']*eqL['m']
        C=math.pow(eqL['q'],2)+eqC['b']*eqL['q']+eqC['c']

        # solve
        DELTA=math.pow(B,2)-4*A*C
        if DELTA>=0:
            x1=(-B-math.sqrt(DELTA))/(2*A)
            y1=eqL['m']*x1+eqL['q']
            if x1>=xmin and x1<=xmax:
                result.append(Point(x1,y1))
            if DELTA>0:   
                x2=(-B+math.sqrt(DELTA))/(2*A)
                y2=eqL['m']*x2+eqL['q']
                if x2>=xmin and x2<=xmax:
                    result.append(Point(x2,y2))
               
    # Index adjustment           
    if len(result)==2:
        if Line(line.p1,result[0]).polar.module>Line(line.p1,result[1]).polar.module:
            result.reverse()

    return result  