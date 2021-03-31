# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:42:33 2020

@author: Produzione
"""

import os,json

    
ITEM_FOLDER='\\\\192.168.1.11\Archivio\ARTICOLI'



items_list={}
customers=[ n for n in os.listdir(ITEM_FOLDER) if os.path.isdir(os.path.join(ITEM_FOLDER, n)) ]
for c in customers:
    items=[]
    p=ITEM_FOLDER+'\\'+c
    for i in os.listdir(p):
        if os.path.isdir(os.path.join(p,i)):
            file_json=[j for j in os.listdir(ITEM_FOLDER+'\\'+c+'\\'+i) if j[-4:]=='json']
            if len(file_json)>0:
                print (file_json[0])
                fs=open(ITEM_FOLDER+'\\'+c+'\\'+i+'\\'+file_json[0])
                json_item=json.load(fs)
                if "State" in json_item:
                    if json_item["State"]=="ACTIVE":items.append(i)
    items_list[c]=items
    
     
    
f = open(ITEM_FOLDER+"\\itemsList.json", "w")
f.write(json.dumps(items_list))
f.close()
       