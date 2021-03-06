
###############################################################################
# g2.py - 2d framework module - 2017
#
# Riccardo Soldini - riccardo.soldini@gmail.com
###############################################################################


import math, sympy, json
import sys
if sys.version_info[0]==3:
    import io
else:
    import cStringIO as io


class cNode:
    def __init__(self,parent=None,child=None):
        self.parent=parent
        self.child=child

    def toJson(self):
        return json.dumps(self.__dict__)


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
    def __dict__(self):
        return dict(Y=self._y, X=self._x)

    def toJson(self):
        return json.dumps(self.__dict__)

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
    def __dict__(self):
       return dict(deg=self._deg)

    def __repr__(self):
        return 'angle (degrees='+str(self._deg)+' | radians='+str(self._rad)+')'

    def get_diff_to (self,angle,orientation): ## da sistemare!!!!
        a1=angle.normalized.deg
        a2=self.normalized.deg
        if orientation==1 :
            if a2>a1: diff=a2-360-a1
            else:diff=-(a1-a2)
        else:
            if a2>a1: diff=a2-a1
            else: diff=a2-a1+360
        return Angle(deg=diff)


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
        self.area=0
        self.updateArea()

    def updateWithPoint(self,p):
        if p.x>self.topright.x:self.topright.x=p.x
        if p.x<self.bottomleft.x:self.bottomleft.x=p.x
        if p.y>self.topright.y:self.topright.y=p.y
        if p.y<self.bottomleft.y:self.bottomleft.y=p.y
        self.updateArea()#### is it necessary?

    def updateArea(self):#### to be deleted?????
        dx=self.topright.x-self.bottomleft.x
        dy=self.topright.y-self.bottomleft.y
        self.area=dx*dy
        return

    def includeBoundBox(self,bb):
        result=False
        cond1=(self.bottomleft.x<=bb.bottomleft.x) and (self.bottomleft.y<=bb.bottomleft.y)
        cond2=(self.topright.x>=bb.topright.x) and (self.topright.y>=bb.topright.y)
        if cond1 & cond2:
            result=True
        return result

    @property
    def height(self):
        return self.topright.y-self.bottomleft.y

    @property
    def width(self):
        return self.topright.x-self.bottomleft.x

    @property
    def center(self):
        x=self.bottomleft.x+self.width/2
        y=self.bottomleft.y+self.height/2
        return Point(x,y)

    @property
    def __dict__(self):
       result={}
       result['BottomLeft']=self.bottomleft.as_dict
       result['TopRight']=self.topright.as_dict
       return result

    def toJson(self):
        return json.dumps(self.__dict__)

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

    def writeDXF(self,dwg,pos=Point(0,0)):
        dwg.add(dxf.line((self._p1._x+pos.x,self._p1._y+pos.y),
                          (self._p2._x+pos.x,self._p2._y+pos.y)))

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

    def get_coeff_equation(self):
        m=math.tan(self._polar.angle.rad)
        if self._p1.y==self._p2.y:
            m=0.0
        q=self._p1.y-m*self._p1.x
        return dict(m=m,q=q)

    def get_general_form_coeff(self):
        A = self.p1.y - self.p2.y
        B = self.p2.x - self.p1.x
        C = self.p1.x*self.p2.y - self.p2.x*self.p1.y
        return dict(a=A,b=B,c=-C)

    def is_parallel_to(self,line):
        result=[False]
        c1=self.get_coeff_equation()
        c2=line.get_coeff_equation()
        m1=round(c1['m'],8)
        m2=round(c2['m'],8)
        if m1==m2:
            q1=round(c1['q'],8)
            q2=round(c2['q'],8)
            qd=q1-q2
            a=math.atan(m1)
            d=qd*math.cos(a)
            result=[True,d]
        return result

    @property
    def __dict__(self):
        return dict(geo='Line',p2=self._p2.__dict__,p1=self._p1.__dict__)

    def toJson(self):
        return json.dump(self.__dict__)

    def __repr__(self):
        return 'Line ('+repr(self._p1)+', '+repr(self._p2)+')'


class Circle:
    def __init__(self,center=Point(),arg=0.0):
        self._center=center

        if arg.__class__.__name__ == 'Point': # --> run both
        # if type(arg)==Point: # --> run only in 3.x
            self._radius=Line(center,arg).polar.module
        else:
            self._radius=arg

    def pointAt(self,value):
        result=None
        if (value>=0.0) and (value<=self.lenght):
            l=Line(self._center,Polar(self._radius,Angle(deg=360/self.lenght*value)))
            result=l.p2
        return result

    def writeDXF(self,dwg,pos=Point(0,0)):
        dwg.add(dxf.circle(self._radius,(self._center._x+pos.x,self._center._y+pos.y)))
        return

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
        bottom_left=Point(self._center.x-self._radius,self._center.y-self._radius)
        top_right=Point(self._center.x+self._radius,self._center.y+self._radius)
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
    def __dict__(self):
        return dict(geo='Circle',radius=self._radius, center=self._center.__dict__)

    def toJson(self):
        return json.dumps(self.__dict__)

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
        self._update()

    def pointAt(self,value):
        result=None
        if (value>=0.0) and (value<=self.lenght):
            a=self.angleStart.deg+(self.angle.deg/self.lenght)*value
            l=Line(self._center,Polar(self._radius,Angle(deg=a)))
            result=l.p2
        return result


    def writeDXF(self,dwg,pos=Point(0,0)):
        if self.orientation>0:
            dwg.add(dxf.arc(self.radius,
                            (self._center.x+pos.x,self._center.y+pos.y),
                            self.angleEnd.deg,
                            self.angleStart.deg))
        else:
            dwg.add(dxf.arc(self.radius,
                            (self._center.x+pos.x,self._center.y+pos.y),
                            self.angleStart.deg,
                            self.angleEnd.deg))
        return


    def _update(self):
        print(self)
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

        self._center=Point(detA/detM/2,detB/detM/2)
        #self._center.x=detA/detM/2
        #self._center.y=detB/detM/2

        self.radius=VectorFromTwoPoints(self._center,self._pointStart).module
        self.updateBoundBox()


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
        return Angle(deg=abs(diff))

    @property
    def lenght(self):
        return abs(self._radius*self.angle.rad)

    @property
    def boundBox(self):
        return self._boundBox

    @property
    def orientation(self):
        return Triangle(self._pointStart,self._pointMiddle,self._pointEnd).orientation

    @property
    def toCircle(self):
        return Circle(self._center,self._radius)

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
    def __dict__(self):
       return dict(geo='Arc',pEnd=self._pointEnd.__dict__, pMiddle=self._pointMiddle.__dict__, pStart=self._pointStart.__dict__)

    def toJson(self):
        return json.dump(self.__dict__)

    def __repr__(self):
        return 'arc (start='+repr(self._pointStart)+', middle='+repr(self.pointMiddle)+', end='+repr(self.pointEnd)+' )'


class Path:
    def __init__(self,nodes=[Point(0,0)],chain=[0]):
        self._nodes=nodes
        self._chain=chain
        self._geometries=[]
        self._lenght=0
        self.update()

    def update(self):
        gg=[]
        # cc=self._chain.copy()# --> run only with 3.x
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


    def writeDXF(self,dwg,pos=Point(0,0)):
        for i in range(0,len(self._geometries)):
            self.geo(i).writeDXF(dwg,pos)
        return


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


    def appendGeo(self,geo,points=[0]):
        self._chain+=[geo]
        for pp in points:
            if type(pp)==int:
                self._chain+=[pp]
            else:
                self._nodes.append(pp)
                self._chain+=[len(self._nodes)-1]
        self.update()


    def insertGeo(self,geo,points,idGeo):
        # cc=self._chain.copy()# --> run only with 3.x
        cc=list(self._chain) # --> try with 2.7
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
        gg=[geo]
        for pp in points:
            if type(pp)==int:
                gg+=[pp]
            else:
                self._nodes.append(pp)
                gg+=[len(self._nodes)-1]
        self._chain[i:1]=gg
        self.update()


    def removeNode (self,idNode):
        tpn=self.getTotalPathNodes()
        if (idNode==-1) or (idNode==tpn-1):
           self._chain.pop(-1)
           g=self._chain.pop(-1)
           if type(g)==int:
              self._chain.pop(-1)
        elif (idNode>-1) and (idNode<tpn-1):
            # cc=self._chain.copy()# --> run only with 3.x
            cc=list(self._chain) # --> try with 2.7
            i=0
            while idNode>0:
                cc.pop(0)
                g=cc.pop(0)
                if g=='Arc':
                    cc.pop(0)
                    i=i+3
                else:
                    i=i+2
                idNode-=1
            self._chain.pop(i)
            g=self._chain.pop(i)
            if g=='Arc': self._chain.pop(i)
        self.update()


    def getTotalPathNodes (self):
        num=1
        for i in self._chain:
            if type(i)!=int:
                num+=1
        return num


    def traslateXY(self,x=0,y=0):
        for n in self._nodes:
            n._x+=x
            n._y+=y
        self.update()
        return


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
        if len(self._chain)>2:
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
    def __dict__(self):
        nodes=[]
        for node in self._nodes:
            nodes.append(node.__dict__)
        return dict(nodes=nodes, geometries=self._geometries)

    def __repr__(self):
        return 'Path (boundBox='+repr(self._boundBox)+', lenght='+repr(self._lenght)+' )'


class Shape:
    def __init__(self,outline=Path(),internal=[],boundBox=[Point(),Point()]):
        self.outline=outline
        self.internal=internal
        self._boundBox=boundBox
        self._perimeter={'outline':0,'internal':[],'total':0}
        self._area={'outline':0,'internal':[],'total':0}
        self.update()

    def update(self):
        perimeter=self._perimeter['outline']=self.outline.lenght
        area=self._area['outline']=self.outline.area
        self._boundBox=self.outline.boundBox
        for contour in self.internal:
            self._perimeter['internal'].append(contour.lenght)
            self._area['internal'].append(contour.area)
            area-=contour.area
            perimeter+=contour.lenght
            self._boundBox.updateWithPoint(contour.boundBox.bottomleft)
            self._boundBox.updateWithPoint(contour.boundBox.topright)
        self._area['total']=area
        self._perimeter['total']=perimeter

    def writeDXF(self,dwg,pos=Point(0,0)):
        self.outline.writeDXF(dwg,pos)
        for p in self.internal:
            p.writeDXF(dwg,pos)
        return

    def isWithin(self,shape):
        result=False
        #check if self.boundBox is smaller then shape.boundBox
        bb1=self.boundBox
        bb2=shape.boundBox
        if bb1.area<bb2.area:
            #check if self.boundBox is within shape.boundBox
            btmlft1=bb1.bottomleft
            btmlft2=bb2.bottomleft
            btmlft_inside=(btmlft1.x>=btmlft2.x) and (btmlft1.y>=btmlft2.y)
            tprgt1=bb1.topright
            tprgt2=bb2.topright
            tprgt_inside=(tprgt1.x<=tprgt2.x) and (tprgt1.y<=tprgt2.y)
            if  btmlft_inside and tprgt_inside:
                #check if any self geos intersect with shape geos
                #check if self random nodes is within shape
                result=True
        return result

    @property
    def boundBox(self):
        return self._boundBox

    @property
    def perimeter(self):
        return self._perimeter

    @property
    def area(self):
        return self._area

    @property
    def __dict__(self):
        result={}
        result['Outline']=self.outline.__dict__
        internal=[]
        for i in self.internal:
            internal.append(i.__dict__)
        result['Internal']=internal
        return result

    def toJson(self):
        return json.dumps(self.__dict__)

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


def IntersectionLineLine(l1,l2):

    def is_between(v,l1,l2):
        #v=number to be valued
        #l1,l2=edges of the range
        if l1>=l2:
            if v>=l2 and v<=l1: return True
        else:
            if v>=l1 and v<=l2: return True
        return False


    L1=l1.get_general_form_coeff
    L2=l2.get_general_form_coeff
    D  = L1['a'] * L2['b'] - L1['b'] * L2['a']
    Dx = L1['c'] * L2['b'] - L1['b'] * L2['c']
    Dy = L1['a'] * L2['c'] - L1['c'] * L2['a']
    if D != 0:
        x = Dx / D
        y = Dy / D
        if is_between(x,l1.p1.x,l1.p2.x) and is_between(x,l2.p1.x,l2.p2.x):
            return [Point(x,y)]

    return []


def IntersectionCircleCircle(c1,c2):

    result=[]

    x1,y1,r1 = c1.center.x,c1.center.y,c1.radius
    x2,y2,r2 = c2.center.x,c2.center.y,c2.radius

    dx = x2-x1
    dy = y2-y1

    d = math.sqrt(dx*dx+dy*dy)
    if d > r1+r2:
         # the circles are separate
         return result
    if d < abs(r1-r2):
         # one circle is contained within the other
         return result
    if d == 0 and r1 == r2:
         # circles are coincident
         return result

    a = (r1*r1-r2*r2+d*d)/(2*d)
    h = math.sqrt(r1*r1-a*a)
    xm = x1 + a*dx/d
    ym = y1 + a*dy/d
    ix1 = xm + h*dy/d
    ix2 = xm - h*dy/d
    iy1 = ym - h*dx/d
    iy2 = ym + h*dx/d

    result.append(Point(ix1,iy1))
    if ix1!=ix2 or iy1!=iy2:
        result.append(Point(ix2,iy2))

    return result


def IntersectionCircleLine(circle,line):

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


def IntersectionArcLine(arc,line):
    result=[]
    ii=IntersectionCircleLine(arc.toCircle,line)
    for r in ii:
        a=VectorFromTwoPoints(arc._center,r).angle
        d=abs(a.get_diff_to(arc.angleStart,arc.orientation).deg)
        if arc.angle.deg>=d:
            result.append(r)
    return result


def IntersectionArcCircle(arc,circle):
    result=[]
    ii=IntersectionCircleCircle(Circle(arc.center,arc.radius),circle)
    for r in ii:
        a=VectorFromTwoPoints(arc._center,r).angle
        d=abs(a.get_diff_to(arc.angleStart,arc.orientation).deg)
        if arc.angle.deg>=d:
            result.append(r)
    return result


def IntersectionArcArc(arc1,arc2):
    result=[]
    ii=IntersectionCircleCircle(arc1.toCircle,arc2.toCircle)
    for r in ii:
        a1=VectorFromTwoPoints(arc1._center,r).angle
        d1=abs(a1.get_diff_to(arc1.angleStart,arc1.orientation).deg)
        a2=VectorFromTwoPoints(arc2._center,r).angle
        d2=abs(a2.get_diff_to(arc2.angleStart,arc2.orientation).deg)
        if (arc1.angle.deg>=d1) and (arc2.angle.deg>=d2):
            result.append(r)
    return result

def IntersectionPathPath(path1,path2):
    result=[]
    lp1=len(path1.geometries)
    lp2=len(path2.geometries)
    for m in range(0,lp1):
        print(m)#path1.geo(m)
    return result

def PathsFromGeos(geos=[],nodes=[]):
    gg=list(geos)
    chains=[]
    while len(gg)>0:
        empty_search=False
        found=False
        g=gg.pop()
        chain=[g[1],g[0]]
        if g[0]=='Arc':
            chain.append(g[2])
        chain.append(g[-1])
        node_to_find=g[-1]

        while not empty_search:
            i=0
            empty_search=True
            while i<len(gg):
                if gg[i][1]==node_to_find:
                    found=True
                    chain.append(gg[i][0])
                    if gg[i][0]=='Arc':
                        chain.append(gg[i][2])
                    chain.append(gg[i][-1])
                    node_to_find=gg[i][-1]
                elif gg[i][-1]==node_to_find:
                    found=True
                    chain.append(gg[i][0])
                    if gg[i][0]=='Arc':
                        chain.append(gg[i][2])
                    chain.append(gg[i][1])
                    node_to_find=gg[i][1]
                if found:
                    empty_search=False
                    g=gg[i]
                    gg.pop(i)
                    found=False
                else:
                    i=i+1
        chains.append(chain)
    #print ('chains:',chains)
    paths=[]
    for c in chains:
        paths.append(Path(nodes,c))
    return paths


def ShapesFromPaths(paths=[]):
    shapes=[]
    return shapes
