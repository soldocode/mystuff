
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:14:59 2019

@author: Disegno
"""


import g2
import os

            
def paths_from_DXF(dwg,layers=''):

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
    SHAPES=[]
    msp = dwg.modelspace()
    if len(layers)==0: layers='all'
    layers=layers.split(',')

    for e in msp:
        if layers[0]=='all' or e.dxf.layer in layers:
            if e.dxftype() == 'LINE':
                n=e.dxf.start
                id1=indexNode(n[0],n[1])
                n=e.dxf.end
                id2=indexNode(n[0],n[1])
                GEOS.append(['Line',id1,id2])
            elif e.dxftype() == 'CIRCLE':
                n=e.dxf.center
                r=e.dxf.radius
                id1=indexNode(n[0],n[1])
                id2=indexNode(n[0]+r,n[1])
                GEOS.append(['Circle',id1,id2])
            elif e.dxftype() == 'ARC':
                id1=0
                id2=1
                id3=2
                GEOS.append(['Arc',id1,id2,id3])
            
    pp=g2.PathsFromGeos(GEOS,NODES)
    areas={}
    area=0
    for p in pp:
        if p.isClosed:
            area=p.area        
        if area in areas:
            areas[area].append(p)
        else:
            areas[area]=[p]
    return areas




def parse(txts,read_dxf):
    '''
    Parameters
        - txts :array of texts to write in dxf
                example:
                    NOME:20181P01_AA50510
                    PEZZI:5
                    MAT:DUROX
                    SP:8
                    COMM:20181
                    POS:P01
        - read_dxf : drawing object of ezdxf.drawing module

    Returns
        - dxf  : dxf file ready for Lantek
        - svg  : svg file for html
        - vals : dict of values
                     tlen---------> shape's perimeter
                     npierce -----> number of cut piercing
                     tarea -------> shape's area
                     nbrushings --> number of welded brushings

    '''
    
    AREA_MIN_GRAIN=154
    AREA_MIN_BUSHINGS=575
    TXT_HEIGHT=18
    
    vals={'tlen':0,'npierce':0,'tarea':0,'nbushings':0}
    
    write_dxf=g2.Drawing()
    w_id=0
    p=paths_from_DXF(read_dxf)
    
    area_list=list(p.keys())
    area_list.sort(reverse=True)
    
    
    if len(area_list)>0:
        # get shape with larger area
        shape=p[area_list[0]][0]
        vals['tlen']=shape.lenght
        vals['npierce']=1
        vals['tarea']=shape.area
        bb=shape.boundBox
        
        # put shape into new drawing
        for k in range(0,len(shape.geometries)):
            write_dxf.insertGeo(w_id,shape.geo(k))
            w_id+=1
        
        
        # find all internal shapes
        del p[area_list[0]]
        in_shape=[]
        for s in p:
             for c in p[s]:
                 if shape.boundBox.includeBoundBox(c.boundBox) and c.isClosed:
                     in_shape.append(c)
                     
        # refine valid internal shape  
        to_draw=[]
        for c in in_shape:
            added=False
            for t in to_draw:
                if (t.boundBox.center.x==c.boundBox.center.x) and (t.boundBox.center.y==c.boundBox.center.y):
                    added=True
                    if c.area>t.area:
                        to_draw.remove(t)
                        to_draw.append(c)
                        
            if not added: to_draw.append(c)        
        vals['npierce']+=len(to_draw)
            
        # put internal shapes into the drawing
        for t in to_draw:
            for k in range(0,len(t.geometries)):
                if t.area<AREA_MIN_GRAIN:
                    write_dxf.insertGeo(w_id,g2.Circle(t.boundBox.center,1.5))
                else: 
                    write_dxf.insertGeo(w_id,t.geo(k))
                    vals['tlen']+=t.lenght
                    vals['tarea']-=t.area
                    if t.area<AREA_MIN_BUSHINGS: vals['nbushings']+=1
            w_id+=1
        
        # put texts into the drawing
        text_pos=shape.boundBox.bottomleft
        text_pos.y-=TXT_HEIGHT
        for txt in txts:
            text_pos.y-=TXT_HEIGHT*1.25        
            write_dxf.insertText(w_id,txt,text_pos,TXT_HEIGHT)
            w_id+=1
        
        # get output dxf and svg
        output_dxf=write_dxf.toDXF()
        output_svg=write_dxf.toSVG()
        
        return dict(dxf=output_dxf,svg=output_svg,vals=vals)
        



