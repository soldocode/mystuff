

# -*- coding: utf-8 -*-
###############################################################################
# itemToProduct.py - 2020
#
# Riccardo Soldini - riccardo.soldini@gmail.com
###############################################################################


import os,shutil
from distutils.dir_util import copy_tree
import ezdxf



def copyWorking(orderPath,itemPath,quantity,order,pos):
    found_works=0
    if os.path.exists(itemPath+'\\PLASMA'):
        found_works+=copyCuts(orderPath,itemPath,'PLASMA',quantity,order,pos)
    if os.path.exists(itemPath+'\\LASER'):
        found_works+=copyCuts(orderPath,itemPath,'LASER',quantity,order,pos)
    if os.path.exists(itemPath+'\\CESOIATURA'):
        found_works+=copyCuts(orderPath,itemPath,'CESOIATURA',quantity,order,pos)
    if os.path.exists(itemPath+'\\PIEGATURA'):
        found_works+=1
        copyBends(orderPath,itemPath,quantity,order,pos)

    if os.path.exists(itemPath+'\\COMPONENTI'):
            components=os.listdir(itemPath+'\\COMPONENTI')
            for component in components:
                comp_path=itemPath+'\\COMPONENTI\\'+component
                found_works+=copyWorking(orderPath,comp_path,quantity,order,pos)
    return found_works


def copyDXF (dest_path,source_path,number,order,pos):
    print('DXF:',source_path)
    if source_path[-3:].upper()=='DXF':
        read_dxf = ezdxf.readfile(source_path)
        msp=read_dxf.modelspace()
        for e in msp.query('TEXT'):
                    txt=e.dxf.text
                    spl=txt.split(':')
                    if spl[0]=='MAT':mat=spl[1]
                    if spl[0]=='SP':sp=spl[1]
                    if spl[0]=='PEZZI':
                        txt=spl[0]+':'+str(int(spl[1])*int(number))
                        e.dxf.text=txt
                    if spl[0]=='NOME':
                        name=spl[1].split('_')[-1]
                        txt='NOME:'+order+pos+'_'+name
                        e.dxf.text=txt
                    if spl[0]=='COMM':
                        txt='COMM:'+order
                        e.dxf.text=txt
                    if spl[0]=='POS':
                        txt='POS:'+pos
                        e.dxf.text=txt
        dest_path+='\\'+mat+'_'+sp
        if not os.path.exists(dest_path):os.makedirs(dest_path)
        read_dxf.saveas(dest_path+'\\'+name+'.dxf')
    return


def copyBends(orderPath,itemPath,quantity,order,pos):
    dest_path=orderPath+'\\'+'PIEGATURA'
    source_path=itemPath+'\\'+'PIEGATURA'
    print(source_path)
    copy_tree(source_path,dest_path)



def copyCuts(orderPath,itemPath,lav,number,order,pos):
    found_works=False
    dest_path=orderPath+'\\'+lav
    source_path=itemPath+'\\'+lav
    print(source_path)
    if not os.path.exists(dest_path):os.makedirs(dest_path)
    thk_folders=os.listdir(source_path)
    if len(thk_folders)>0:found_works=True
    for f in thk_folders:
        if os.path.isdir(source_path+'\\'+f):
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
        else:
            copyDXF (dest_path,source_path+'\\'+f,number,order,pos)
    return found_works


def itemToProduct(itemPath,orderPath,order,pos,quantity):
    print ('itemPath:',itemPath)
    print ('orderPath:',orderPath)
    print ('quantity:',quantity)
    msg='Nessuna lavorazione presente!!!!'
    if not os.path.exists(itemPath):
        msg='Errore: '+itemPath+' non trovato!!!'
    else:
        if not os.path.exists(orderPath):
            os.makedirs(orderPath)
        found_works=copyWorking(orderPath,itemPath,quantity,order,pos)
        if found_works>0:msg='Articolo in produzione'
    return msg


if __name__ == "__main__":

    ITEM_FOLDER='\\\\192.168.1.11\Archivio\ARTICOLI'
    ORDER_FOLDER='\\\\192.168.1.11\Archivio\COMMESSE'

    customer=input('Cliente: ')
    item=input('Articolo: ')
    order=input('Commessa: ')
    pos=input('Posizione: ')
    num=input('Quantità: ')
    year=order[0:2]

    order_path=ORDER_FOLDER+'\\20'+year+'\\'+order+'\\'+pos
    item_path=ITEM_FOLDER+'\\'+customer+'\\'+item

    print(itemToProduct(item_path, order_path, order, pos, num))
