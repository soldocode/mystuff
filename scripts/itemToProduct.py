

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:42:33 2020

@author: Produzione
"""

import os,shutil
import ezdxf
import datetime
    
ITEM_FOLDER='\\\\192.168.1.11\Archivio\ARTICOLI'
ORDER_FOLDER='\\\\192.168.1.11\Archivio\COMMESSE'



def copyCuts(orderPath,itemPath,lav,number,order,pos):
    dest_path=orderPath+'\\'+lav
    source_path=itemPath+'\\'+lav
    if not os.path.exists(dest_path):os.makedirs(dest_path)
    thk_folders=os.listdir(source_path)
    for f in thk_folders:
        dxf_files=os.listdir(source_path+'\\'+f)
        if not os.path.exists(dest_path+'\\'+f):os.makedirs(dest_path+'\\'+f)
        for d in dxf_files:
            if d[-3:].upper()=='DXF':
                read_dxf = ezdxf.readfile(source_path+'\\'+f+'\\'+d)
                msp=read_dxf.modelspace()
                for e in msp.query('TEXT'):
                            txt=e.dxf.text
                            spl=txt.split(':')
                            if spl[0]=='PEZZI':
                                txt=spl[0]+':'+str(int(spl[1])*int(number))
                                e.dxf.text=txt
                                #print (e.dxf.text)
                            if spl[0]=='NOME':
                                name=spl[1].split('_')
                                txt='NOME:'+order+pos+'_'+name[-1]
                                e.dxf.text=txt
                            if spl[0]=='COMM':
                                txt='COMM:'+order
                                e.dxf.text=txt
                            if spl[0]=='POS':
                                txt='POS:'+pos
                                e.dxf.text=txt
                read_dxf.saveas(dest_path+'\\'+f+'\\'+d)
    return



def itemToProduct(itemPath,orderPath,order,pos,number):
    print ('itemPath:',itemPath)
    print ('orderPath:',orderPath)
    print ('number:',number)
    msg='Done'
    not_found=True
    if not os.path.exists(itemPath):
        msg='Errore: '+itemPath+' non trovato!!!'
    else:
        if not os.path.exists(orderPath):
            os.makedirs(orderPath)
        if os.path.exists(itemPath+'\\PLASMA'):
            copyCuts(orderPath,itemPath,'PLASMA',number,order,pos)
            not_found=False
        if os.path.exists(itemPath+'\\LASER'):
            copyCuts(orderPath,itemPath,'LASER',number,order,pos)
            not_found=False
    if not_found:print('Nessuna lavorazione presente!!!!')        
    
                                                                       
    return msg


if __name__ == "__main__":
    
    #ONLY FOR TESTING
    #customer='ALM01'
    #item='000048B'
    #year=D_YEAR
    #order='555'
    #pos='P01'
    #num=6
    
    customer=input('Cliente: ')
    item=input('Articolo: ')
    order=input('Commessa: ')
    pos=input('Posizione: ')
    num=input('Quantità: ')
    year=order[0:2]
    
    order_path=ORDER_FOLDER+'\\20'+year+'\\'+order+'\\'+pos
    item_path=ITEM_FOLDER+'\\'+customer+'\\'+item
        
    print(itemToProduct(item_path, order_path, order, pos, num))