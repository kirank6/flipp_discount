# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:42:49 2021

@author: Kiran Khanal
"""
import pandas as pd
import numpy as np
import sklearn 
from ast import literal_eval
from sklearn.metrics.pairwise import cosine_similarity

in_df = pd.read_csv('embedded_vetors.csv')


def calc_cosim(item):
    cosim_dic = {}
    if item in in_df['Nodes'].values:
        for i in range(len(in_df)):
            if in_df['Nodes'][i] == item:
                ele1 = literal_eval(in_df['emb_vect'][i])
                #print(ele1)
                for j in range(len(in_df)):
                    ele2 = literal_eval(in_df['emb_vect'][j])
                    cos_sim = cosine_similarity([ele1], [ele2])
                    # dictionary of nodes with corresponding cosine similary  
                    cosim_dic[in_df['Nodes'][j]] = cos_sim[0][0] 
        cosim_df = pd.DataFrame(cosim_dic.items(), columns=['Nodes', 'Cosine_sim'])
        cosim_df = cosim_df.sort_values(by = 'Cosine_sim', ascending = False)   
        cosim_df = cosim_df.reset_index(drop = True)
    
        #recomm_list = [cosim_df['Nodes'][i] for i in range(1,6)]
        recomm_list = []
        for i in range(6):
            if i !=0:
                recomm_list.append(cosim_df['Nodes'][i])
    else:
         return []
    return  recomm_list 
#print(calc_cosim('garlic')) 
