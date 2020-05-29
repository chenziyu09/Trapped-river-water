# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:29:26 2019

@author: zchen44
"""

import numpy as np
import pandas as pd 


# read observed discharge date
discharge = pd.read_csv("discharge.csv",header=0,index_col=None)
discharge['t']= pd.to_datetime(discharge['t'])


# read the gate closure results for specific SLR
now = pd.read_csv("1mSLR.csv",header=0,index_col=None)
now['t']= pd.to_datetime(now['t'])

index_min = discharge['t'][0]
i_min=pd.to_datetime(index_min)
index_max = discharge['t'][211080] 
i_max=pd.to_datetime(index_max) 
extract = (now.t>=i_min)&(now.t<=i_max)
now_table=now[extract]  
now_table= now_table.reset_index(drop=True)


#Calculate the trapped river volume 

t_i =[]
t_o =[]
dis =[]


for index in range(len(now_table)):
    t_max = now_table.t[index] + pd.Timedelta('6H') + (now_table.tide_cyc[index]-now_table.peak_num[index])*pd.Timedelta('12H')
    t_o.append(t_max)
    t_min = now_table.t[index] - pd.Timedelta('6H') - (now_table.peak_num[index] -1)*pd.Timedelta('12H')
    t_i.append(t_min)
    
    extract = (discharge.t>=t_min)&(discharge.t<t_max)
    discharge_tep=discharge[extract]  
    dis.append(3600*discharge_tep.total.sum())
   
    
    
now_table['t_i'] =  (pd.to_datetime(np.asarray(t_i))).ravel()
now_table['t_o'] =  (pd.to_datetime(np.asarray(t_o))).ravel()
now_table['trapped_river_volume(m3)'] =  (np.asarray(dis)).ravel()

    
    
now_table.to_csv('results.csv') 

    

#%%
