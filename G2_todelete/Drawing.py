
###############################################################################
# Drawing.py
#
#
###############################################################################


from g2 import *
from dxfwrite import DXFEngine as dxf


class Table:

    def __init__(self):
        self.Layout={}
        self._boundBox=BoundBox()
        self.update()

    def update(self):
        bb=BoundBox()
        l=len(self.Layout)
        if l>0:
            ls=list(self.Layout)
            bb=self.Layout[ls[0]]['Geo'].boundBox
            for g in ls:
                if self.Layout[g]['Class']=='GEO':
                   g_bb=self.Layout[g]['Geo'].boundBox
                   bb.updateWithPoint(g_bb.bottomleft)
                   bb.updateWithPoint(g_bb.topright)
        self._boundBox=bb
        return

    @property
    def boundBox(self):
        return self._boundBox

    def insertGeo(self,id,geo,position=Point(0,0),rotation=Angle(0)):
        ## rotation for the moment not considered!!!!!!
        self.Layout[id]={'Class':'GEO','Geo':geo,'Position':position,'Rotation':rotation}
        self.update()


    def insertText(self,id,text,position=Point(0,0),height=15,rotation=Angle(0)):
        ## rotation for the moment not considered!!!!!!
        self.Layout[id]={'Class':'TXT',
                        'Txt':text,
                        'Position':[position.x,position.y],
                        'Height':height,
                        'Rotation':rotation}
        self.update()


    def getDXF(self):
        output = io.StringIO()
        drawing = dxf.drawing('drawing.dxf')
        for id in self.Layout:
            if self.Layout[id]['Class']=='GEO':
               geo=self.Layout[id]['Geo']
               pos=self.Layout[id]['Position']
               drawing.add(dxf.line((geo._p1._x+pos.x,geo._p1._y+pos.y),
                                    (geo._p2._x+pos.x,geo._p2._y+pos.y)))
            if self.Layout[id]['Class']=='TXT':
               text = dxf.text(self.Layout[id]['Txt'],
                               height=self.Layout[id]['Height'],)
               text['insert']=(self.Layout[id]['Position'][0],
                               self.Layout[id]['Position'][1])
               text['layer'] = 'TEXT'
               text['color'] = 7
               drawing.add(text)


        drawing.save_to_fileobj(output)
        dxf_result=output.getvalue()
        return dxf_result
