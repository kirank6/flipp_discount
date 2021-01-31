# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 08:48:21 2021

@author: Kiran Khanal
"""
import sys
from sys import argv
import requests

def django_input(itemname, zipcode):
        import ast       
        import flipp_data_extracter
        import pandas as pd
        import numpy as np
        import re
        import warnings
        warnings.filterwarnings(action='ignore')
        
        # Information needed for data extraction
        item_name = itemname
        zip_code = zipcode
        
        #results list of dictionarys of query items
        Output = flipp_data_extracter.search(item_name, zip_code)
        
        def select_df(list_dics_all):
            '''
            Results a datafram of selected items reading a list of 
            dictionaries of extracted items.
            '''
            #Reading data from Output dictionary
            selected_cols = ['brand', 'merchant', 'name', 
                             'category', 'description', 
                             'current_price', 'price_text', 'percent_off',
                             'image_url','cutout_image_url']
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
        
        df_sel = select_df(Output) # dataframe with selected columns only
        
        #Created two more columns to extract price and weight unit
        df_sel['ext_price'] = np.nan
        df_sel['ext_weight(oz)'] = np.nan
        
        def clean_ext_wt(df_sel):
             '''
             Returns extracted units from different columns 
             '''    
             for i in range(len(df_sel)):
                 comb_text = str(df_sel['name'][i])+ ',' +  \
                    str(df_sel['description'][i]) + ','+  \
                        str(df_sel['price_text'][i])
               
                #Extract oz and lb
                 tw1 = re.findall(r'(\d*\.?\d+)(\s?|\\n|-|.)(?i)(oz|lb|0z|lbs|fl)', comb_text)    
                 tw2 = re.findall(r'(\s?)(?i)(oz|lb)', comb_text)
                
                 fwegt = tw1 or tw2 
                 #print(i, fwegt,  comb_text)
                 if fwegt !=[]:
                    wt_num = fwegt[0]  # pick the first one for multitple entries
                    if len(wt_num)==3:  # there is numerical value, space and unit lb or oz
                        wt_num1 = ast.literal_eval(wt_num[0]) # numerical value
                        wt_unt1 = wt_num[2] # unit becasue second would be space
                        #print(type(wt_num1),wt_num1, wt_unt1)
                        if wt_unt1.lower() == 'lb':  # in order to convert lb to oz
                            #print(type(wt_num1),wt_num1, wt_unt1)
                            if type(wt_num1) == int:
                                if wt_num1 > 0 and wt_num1 <= 9:
                                    num_lb = float(wt_num1 * 16.0) 
                                    df_sel['ext_weight(oz)'][i] = num_lb
                                    #print(wt_num1, wt_unt1, num_lb)
                                else:  # if integer is very large
                                    df_sel['ext_weight(oz)'][i] = float(16.0)
                                    
                            else:               # either emptly or any other large number or decimal
                                str_num = str(wt_num1)
                                cnt_deci =  str_num[::-1].find('.')
                                if cnt_deci == 1:
                                    df_sel['ext_weight(oz)'][i] = float(wt_num1) * 16.0
                                else:
                                    df_sel['ext_weight(oz)'][i] = float(16)
                        elif wt_unt1.lower() =='oz' or wt_unt1.lower() =='0z' or wt_unt1.lower() =='fl': # in case of oz 
                            num_oz = wt_num1
                            df_sel['ext_weight(oz)'][i] = num_oz   
                                           
                    else:  #  either there is space or no space and unit
                        wt_num2 = wt_num[0] # numerical value or empty
                        wt_unt2 = wt_num[1]  #unit lb or oz
                        #print(wt_num2,',', wt_unt2, fwegt)
                        if wt_unt2.lower == 'oz': #it oz so just 1#
                            df_sel['ext_weight(oz)'][i] = float(1.0)
                        else: # it oz so just 1# if it is lb convert ot oz
                            df_sel['ext_weight(oz)'][i] = float(16.0)                
             return df_sel
            
        df_wgt = clean_ext_wt(df_sel).dropna(subset = ['ext_weight(oz)'])
        
        # reindex the dataframe after dropping rows with missing units
        df_wgti = df_wgt.reset_index() 
        
        def clean_ext_price(df_wgti):
            '''
            Returns extracted price if they are missing in current price.
            '''
            for i in range(len(df_wgti)):
                pr_exrt = str(df_wgti['name'][i])+ ',' + \
                          str(df_wgti['description'][i]) + ','+ \
                          str(df_wgti['price_text'][i])
               
               
                if df_wgti['current_price'][i] =='':  # if price is missing in current price
                    #print(i, pr_exrt)
                    pxt1 =  re.findall(r'([$])(\d+(\.?)\d+)', pr_exrt)
                    pxt2 =  re.findall(r'(\d+)(\s|\\n)(\d+)(\s?|\\n)(?i)(lb|lbs|oz|ea)', pr_exrt)
                    pxt3 =  re.findall(r' (?i)(lb|lbs|lb.)(\s?|\\n|.)(\d+)[(.|\\n|\s?)](\d+)', pr_exrt)
                    pxt4 =  re.findall(r'(?i)(Lb|Lbs|lb.)(\s?|.|\\n)(\d+)', pr_exrt)
                    pxt5 =  re.findall(r'(\d+(\s?\.?)\d+)(\s?|\\n|.)(?i)(lb|lbs|\xa2|ea)', pr_exrt)
                    pxt6 =  re.findall(r'(\d+)(\s?|\\n)(?i)(ea)', pr_exrt)
                    
                    fpxt = pxt1 or pxt2 or pxt3 or pxt4 or pxt5 or pxt6
                    #print(i, fpxt, pr_exrt)    
                    if fpxt !=[]:
                        ext_itm = fpxt[0]  # pick the first one for multitple entries
                        #print(i, fpxt[0])
                        #clean data with $ in the front
                        
                        #print(i, fpxt, pr_exrt) 
                        if ext_itm[0] == "$":
                            ext_val1 = ast.literal_eval(ext_itm[1]) # numerical value int or float
                            #print(i, ext_val1, pr_exrt)
                            if type(ext_val1) == float:
                                #print(i, ext_val1, pr_exrt)
                                df_wgti['ext_price'][i]= ext_val1
                            elif type(ext_val1) != float:
                               # print(i, ext_val1, pr_exrt)
                                df_wgti['ext_price'][i]= ext_val1/100   
                                 #print(i, ext_val1, pr_exrt)
                        if ext_itm[-1].lower() == 'lb':
                            #print(i, ext_itm) 
                            ext_lb0 = ast.literal_eval(ext_itm[0])
                            if len(ext_itm[0]) !=1:
                                if type(ext_lb0) == float:
                                    df_wgti['ext_price'][i]=ext_lb0
                                elif len(ext_itm[0]) == 4:
                                    df_wgti['ext_price'][i]=ext_lb0/1000
                                    #print(i, ext_lb0)   
                                elif len(ext_itm[0]) == 3 or len(ext_itm[0])==2:
                                    df_wgti['ext_price'][i]=ext_lb0/100
                                   # print(i, ext_lb0) 
                            elif len(ext_itm[0])==1:  
                                n_ext = ext_itm[0] +''+'99'
                                df_wgti['ext_price'][i]=(ast.literal_eval(n_ext))/100
                        elif ext_itm[0].lower() =='lb' or ext_itm[0].lower() =='lb.':
                           df_wgti['ext_price'][i]=(ast.literal_eval(ext_itm[2]))/100 
                        elif ext_itm[-1].lower() != 'lb' and ext_itm[0] != "$":
                            if len(ext_itm[0])==2 or len(ext_itm[0]) == 3:
                               df_wgti['ext_price'][i]=(ast.literal_eval(ext_itm[0]))/100
                            else:
                                df_wgti['ext_price'][i]=np.nan       
                else:
                    df_wgti['ext_price'][i] = np.nan
            return df_wgti
        
        # new dataframe with required column names only
        df_np = clean_ext_price(df_wgti)[['merchant','current_price', \
                                         'percent_off', 'image_url', \
                                             'ext_price', 'ext_weight(oz)']].copy()
        #Add another column for best price calculation
        df_np['com_price'] = np.nan    
        
        def cal_com_price(df_np):
            '''
             Returns with values on new column from calcualtion.
            '''
            for i in range(len(df_np)):
                old_price = df_np['current_price'][i]
                new_price = df_np['ext_price'][i]
                if old_price != '':
                    df_np['com_price'][i] = old_price
                else:
                    df_np['com_price'][i] = new_price 
            return df_np
            
        # remove missing values if any from new column
        df_final = cal_com_price(df_np).dropna(subset = ['com_price'])
            
        df_final = df_final.reset_index(drop= True)
        
        df_final['final_price($/oz)'] = np.nan
        
        def  cal_final_price(df_final):
            '''
            Returns price per given unit
            '''
            for i in range(len(df_final)):
                pr_indoll = df_final['com_price'][i]
                unit_inoz = df_final['ext_weight(oz)'][i]
                df_final['final_price($/oz)'][i] = round((pr_indoll/unit_inoz),3) 
            
            return df_final
        df_best_price = cal_final_price(df_final)
        
        def sorted_bestprice(df_best_price):
            df_sorted = df_best_price.sort_values(by='final_price($/oz)')
            df_sorted = df_sorted.reset_index()
        
            bp_list = [] #list of tuples with best price store name, best price and image url
        
            if len(df_sorted) <5:
                for i in range(len(df_sorted)):
                    store_name = df_sorted['merchant'][i]
                    final_price = df_sorted['final_price($/oz)'][i]
                    item_image = df_sorted['image_url'][i]
                    bp_list.append((store_name, str(final_price)+'/oz', item_image))
            else:
                for i in range(len(df_sorted)):
                    if i < 5:
                        store_name = df_sorted['merchant'][i]
                        final_price = df_sorted['final_price($/oz)'][i]
                        item_image = df_sorted['image_url'][i]
                        bp_list.append((store_name, str(final_price)+'/oz', item_image))
            return bp_list
        
        #print(len(sorted_bestprice(df_best_price)))    
        #print(sorted_bestprice(df_best_price))
        
        return sorted_bestprice(df_best_price)[0]
    
output_items = django_input(sys.argv[1], sys.argv[2])
print(output_items)
#print(django_input('cheese', 60565))      
