#***************************************************************************
#*                                                                         *
#*   meDXF - 2016                                                          *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#*   Last Update: 14/03/17                                                 *                      *
#***************************************************************************



import math
from dxfwrite import DXFEngine as dxf
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
            
            
