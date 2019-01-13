from g2 import *

def build(**kwargs):
    
    result=Line(Point(0,0),Point(100,100))
    result.model="UNP"
    return result


ShapeFromModel["UNP"]=build
