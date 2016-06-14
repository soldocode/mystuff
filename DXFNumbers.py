#***************************************************************************
#*                                                                         *
#*   DXFnumber - 2016                                                      *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#***************************************************************************


import math
from dxfwrite import DXFEngine as dxf
import geoFun as geo

nodes=[[0,0],       #0
       [0,25],      #1
       [0,50],      #2
       [0,75],      #3     
       [0,100],     #4
       [25,100],    #5
       [50,100],    #6
       [50,75],     #7
       [50,50],     #8
       [50,25],     #9
       [50,0],      #10
       [25,0],      #11
       [25,25],     #12
       [25,75],     #13
       [37.5,100],  #14
       [37.5,0],    #15
       [45,60],     #16
       [25,50],     #17
       [50,37.5],   #18
       [23.5,64.2], #19
       [0,37.5],    #20
       [25,62.5],   #21
       [14.2,78.3], #22
       [50,62.5],   #23
       [25,37.5],   #24
       [0,62.5],    #25
       [39.2,11],   #26
       [0,39]       #27
      ]
numbers={"0":[['arc',9,1,11],['line',1,3],['arc',3,7,5],['line',7,9]],
         "1":[['line',2,14],['line',14,15]],
         "2":[['arc',3,16,5],['line',16,0],['line',0,10]],
         "3":[['arc',3,17,5],['arc',17,1,11]],
         "4":[['line',9,1],['line',1,14],['line',14,15]],
         "5":[['line',6,4],['line',4,2],['arc',2,18,19],['line',18,9],['arc',9,1,11]],
         "6":[['arc',20,18,21],['line',18,9],['arc',9,1,11],['line',1,27],['arc',27,6,22]],
         "7":[['line',4,6],['line',6,0]],
         "8":[['circle',12,9],['circle',13,7]],
         "9":[['arc',23,25,24],['line',25,3],['arc',3,7,5],['line',7,18],['arc',18,0,26]]
        }



def Draw(p):

    lay=0
    path=p['path']
    n=p['nodes']
    d=p['drawing']
    rx=p['position'][0]
    ry=p['position'][1]
    if p['layer']: lay=p['layer']

    for c in path:
        if c[0]=='line':
            d.add(dxf.line((rx+n[c[1]][0],ry+n[c[1]][1]),
                           (rx+n[c[2]][0],ry+n[c[2]][1]),layer=lay))
            #print 'L ',n[c[1]],n[c[2]]
        elif c[0]=='arc':
            cr=geo.CircleFrom3Points(n[c[1]],n[c[3]],n[c[2]])
            #print cr['P1Degree'] ,cr['P3Degree']
            d.add(dxf.arc(center=(rx+cr['Center'][0],ry+cr['Center'][1]),
                          radius=cr['Radius'],
                          startangle=math.degrees(cr['P3Degree']),
                          endangle=math.degrees(cr['P1Degree']),
                          layer=lay))
            #print 'A'
        elif c[0]=='circle':
            rds=n[c[2]][0]-n[c[1]][0]
            d.add(dxf.circle(rds,(rx+n[c[1]][0],ry+n[c[1]][1]),layer=lay))
            #print 'C'

