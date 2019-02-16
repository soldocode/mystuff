#***************************************************************************
#*                                                                         *
#*   meDXF - 2016                                                          *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#*   Last Update: 16/02/19                                                 *                      *
#***************************************************************************



import math
from dxfwrite import DXFEngine as dxf
import ezdxf
import g2
import mePath
import geoFun as geo


class Drawing (object):
    def __init__(self,
                 filename=''):
        self.FileName=filename
        self.DXFDrawing=dxf.drawing(filename)
        self.Paths=[] #???
        
    
    def drawPath(self,
                 outlines=mePath.Outline(),
                 xy=[0,0],
                 layer=-1):
        
                     
        self.Paths.append(outlines)#???
        lay=layer
        path=outlines.Path
        n=outlines.Nodes
        d=self.DXFDrawing
        rx=xy[0]
        ry=xy[1]

        for c in path:
         if c[0]=='line':
            d.add(dxf.line((rx+n[c[1]][0],ry+n[c[1]][1]),
                           (rx+n[c[2]][0],ry+n[c[2]][1]),layer=lay))
         elif c[0]=='arc':
            cr=geo.CircleFrom3Points(n[c[1]],n[c[3]],n[c[2]])
            if cr['Direction']<0:
                d.add(dxf.arc(center=(rx+cr['Center'][0],ry+cr['Center'][1]),
                              radius=cr['Radius'],
                              startangle=math.degrees(cr['P1Degree']),
                              endangle=math.degrees(cr['P3Degree']),
                              layer=lay))
            else:    
                d.add(dxf.arc(center=(rx+cr['Center'][0],ry+cr['Center'][1]),
                              radius=cr['Radius'],
                              startangle=math.degrees(cr['P3Degree']),
                              endangle=math.degrees(cr['P1Degree']),
                              layer=lay))
            
         elif c[0]=='circle':
            rds=n[c[2]][0]-n[c[1]][0]
            d.add(dxf.circle(rds,(rx+n[c[1]][0],ry+n[c[1]][1]),layer=lay))
        


        

    def save(self):   
        self.DXFDrawing.save()
    
    
#******************************************************                                                  
#   Draw(p)                                          
#   p:{'path'                                        
#      'nodes'                                    
#      'drawing'
#      'position':[x,y]
#      'layer'


def Draw(p):

    lay=0
    path=p['path']
    n=p['nodes']
    d=p['drawing']
    rx=p['position'][0]
    ry=p['position'][1]
    if 'layer' in p.keys(): lay=p['layer']

    for c in path:
        if c[0]=='line':
            d.add(dxf.line((rx+n[c[1]][0],ry+n[c[1]][1]),
                           (rx+n[c[2]][0],ry+n[c[2]][1]),layer=lay))
        elif c[0]=='arc':
            cr=geo.CircleFrom3Points(n[c[1]],n[c[3]],n[c[2]])
            if cr['Direction']<0:
                d.add(dxf.arc(center=(rx+cr['Center'][0],ry+cr['Center'][1]),
                              radius=cr['Radius'],
                              startangle=math.degrees(cr['P1Degree']),
                              endangle=math.degrees(cr['P3Degree']),
                              layer=lay))
            else:    
                d.add(dxf.arc(center=(rx+cr['Center'][0],ry+cr['Center'][1]),
                              radius=cr['Radius'],
                              startangle=math.degrees(cr['P3Degree']),
                              endangle=math.degrees(cr['P1Degree']),
                              layer=lay))
            
        elif c[0]=='circle':
            rds=n[c[2]][0]-n[c[1]][0]
            d.add(dxf.circle(rds,(rx+n[c[1]][0],ry+n[c[1]][1]),layer=lay))
            
def ShapesFromDXF(dwg):

    def indexNode(_x,_y):
        i=0
        x=round(_x,2)
        y=round(_y,2)
        found=False
        while not found and i<len(NODES):
            if (x==NODES[i].x) and (y==NODES[i].y):
                found=True
                i=i-1
            i=i+1
        if not found: 
                NODES.append(g2.Point(x,y))
        return i

    NODES=[]
    GEOS=[]
    PATHS=[]
    msp = dwg.modelspace()

    for e in msp:
        if e.dxftype() == 'LINE':
            n=e.dxf.start
            id1=indexNode(n[0],n[1])
            n=e.dxf.end
            id2=indexNode(n[0],n[1])
            GEOS.append(['line',id1,id2])
        elif e.dxftype() == 'CIRCLE':
            n=e.dxf.center
            r=e.dxf.radius
            id1=indexNode(n[0],n[1])
            id2=indexNode(n[0]+r,n[1])
            GEOS.append(['circle',id1,id2])
        elif e.dxftype() == 'ARC':
            id1=0
            id2=1
            id3=2
            GEOS.append(['arc',id1,id2,id3])
        
    gg=list(GEOS)
    while len(gg)>0:
            geo=gg.pop()
            if geo[0]=='circle':
                PATHS.append([geo])
            elif geo[0]=='line':
                    p=[geo]
                    c_node=geo[2]
                    found= False
                    ind=0
                    while (len(gg)>0) and (not found) and (ind<len(gg)):
                        compare=gg[ind]
                        if compare[0]=='line':
                            if compare[1]==c_node:
                                p.append(['line',compare[1],compare[2]])
                                found=True
                                c_node=compare[2]
                            elif compare[2]==c_node:   
                                p.append(['line',compare[2],compare[1]])
                                found=True
                                c_node=compare[1]
                        if found:
                            gg.pop(ind)
                            found=False
                        else:
                            ind+=1
                    PATHS.append(p) 
    print(NODES)                
    return PATHS