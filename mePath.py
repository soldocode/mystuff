#***************************************************************************
#*                                                                         *
#*   mePath - 2016                                                         *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#***************************************************************************

class Outline(object):
    def __init__(self,):
        self.Id=''
        self.BoundBox=[[0,0],[0,0]] #[x1,y1],[x2,y2]
        self.Nodes=[]
        self.Path=[]
        self.Child={}
    

def makePattern(model,parameters):
    result=MODELS[model](parameters)
    return result

MODELS={}

from PathModels import *
