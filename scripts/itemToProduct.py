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
D_YEAR=str(datetime.date.today().year)


def itemToProduct(itemPath,orderPath,order,pos,number):
    print ('itemPath:',itemPath)
    print ('orderPath:',orderPath)
    print ('number:',number)
    msg='Done'
    if not os.path.exists(itemPath):
        msg='Errore: '+itemPath+' non trovato!!!'
    else:
        if not os.path.exists(orderPath):
            os.makedirs(orderPath)
        if os.path.exists(itemPath+'\\LASER'): 
            OLpath=orderPath+'\\LASER'
            shutil.copytree(itemPath+'\\LASER', OLpath)
            thk_folders=os.listdir(OLpath)
            for f in thk_folders:
                dxf_files=os.listdir(OLpath+'\\'+f)
                for d in dxf_files:
                    if d[-3:].upper()=='DXF':
                        read_dxf = ezdxf.readfile(OLpath+'\\'+f+'\\'+d)
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
                        read_dxf.saveas(OLpath+'\\'+f+'\\'+d)                                                            
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
    year=input('Anno['+D_YEAR+']: ') or D_YEAR
    order=input('Commessa: ')
    pos=input('Posizione: ')
    num=input('Quantità: ')
    
    order_path=ORDER_FOLDER+'\\'+year+'\\'+year[2:]+order+'\\'+pos
    item_path=ITEM_FOLDER+'\\'+customer+'\\'+item
        
    print(itemToProduct(item_path, order_path, year[2:]+order, pos, num))