# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 19:47:24 2021
@author: Kiran Khanal
"""
#Import packages
import requests
import sys
from sys import argv
import io
import ast
import math
import urllib.request
import flipp_data_extracter
from PIL import Image
from io import BytesIO
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings(action='ignore')


def select_df(list_dics_all):
    '''
    Results a datafram of selected items reading a list of 
    dictionaries of extracted items.
    '''
    #Reading data from Output dictionary
    selected_cols = ['brand', 'merchant', 'name', 'category', 'description', 
                                           'current_price', 'price_text', 'percent_off','image_url','cutout_image_url']
    df_all_items = pd.DataFrame(columns = selected_cols) # dataframe from selected items

    list_dic_selected_items =[]  # list of dictionaries with selected item desriptions only


    for i in range(len(list_dics_all)):
        items_dict = list_dics_all[i]['item']
        selected_dict = {}

        for key in items_dict:
            if key in selected_cols:
                selected_dict[key] = items_dict[key]                   
        list_dic_selected_items.append(selected_dict)   #update list with dictinaries for each group
    df_all_items = df_all_items.append(list_dic_selected_items, True)   # append list to dataframe 
    return df_all_items


def sorted_bestprice(df_final):
    '''
    Returns the lowest priced item from the sorted 
    list.
    '''
    df_sorted = df_final.sort_values(by='current_price')
    df_sorted = df_sorted.reset_index()

    bp_list = [] #list of tuples with best price store name, best price and image url

    if len(df_sorted) <5:
        for i in range(len(df_sorted)):
            store_name = df_sorted['merchant'][i]
            final_price = df_sorted['current_price'][i]
            item_image = df_sorted['image_url'][i]
            bp_list.append((store_name, final_price, item_image))
    else:
        for i in range(len(df_sorted)):
            if i < 5:
                store_name = df_sorted['merchant'][i]
                final_price = df_sorted['current_price'][i]
                item_image = df_sorted['image_url'][i]
                bp_list.append((store_name, final_price, item_image))
    return bp_list

def django_input(item_name, zip_code):
    '''
    Returns the final output.
    '''
    #results list of dictionarys of query items
    Output = flipp_data_extracter.search(item_name, zip_code)
    df_sel = select_df(Output)
    # remove missing values if any from current price
    df_final = df_sel[df_sel['current_price'] != '']
    df_final = df_final.reset_index(drop=True)
    final_list = sorted_bestprice(df_final)
    if final_list ==[]:
        cor_text = ('No Merchant', '0.0', \
                    'https://www.freepnglogos.com/uploads/vegetables-png/buy-high-quality-organic-vegetables-and-fruits-online-7.png')
        return cor_text
    
    return final_list[0]

output_items = django_input(sys.argv[1], sys.argv[2])
print(output_items)    
    
    
    
    