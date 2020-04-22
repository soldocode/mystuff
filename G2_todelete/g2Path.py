from g2 import *


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
