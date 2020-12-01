# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:42:33 2020

@author: Produzione
"""

import os,shutil,json

    
ITEM_FOLDER='\\\\192.168.1.11\Archivio\ARTICOLI'
ORDER_FOLDER='\\\\192.168.1.11\Archivio\COMMESSE'


items_list=[]
customers=[ n for n in os.listdir(ITEM_FOLDER) if os.path.isdir(os.path.join(ITEM_FOLDER, n)) ]
for c in customers:
    p=ITEM_FOLDER+'\\'+c
    items=[ i for i in os.listdir(p) if os.path.isdir(os.path.join(p,i)) ]
    items_list.append({'Customer':c,'Items':items})
    
    
f = open(ITEM_FOLDER+"\\itemsList.json", "w")
f.write(json.dumps(items_list))
f.close()
       