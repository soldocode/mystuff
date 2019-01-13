from g2 import *

def build(width=0,height=0,center=Point(0,0),rotation=Angle(deg=0)):
    outlines=Path()
    outlines.chain=[0,'Line',1,'Line',2,'Line',3,'Line',0]
    outlines.nodes=[Point(-width/2,-height/2),
                    Point(-width/2,height/2),
                    Point(width/2,height/2),
                    Point(width/2,-height/2),Point(0,0)]
    result=Shape(outlines)
    result.model="BOX"
    return result


ShapeFromModel["BOX"]=build
