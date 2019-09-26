# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 14:01:24 2019

@author: Guanhua
"""


import xlsxwriter
import xlrd
import numpy as np
import pandas as pd

match=xlrd.open_workbook(r'C:\Users\Guanhua\Desktop\IDmatch.xlsx')

test=r'C:\Users\Guanhua\Desktop\testing.xlsx' ## Enter correct path for record excel workbook 输入正确的记录excel路径##

##NEED ENTER PATH FOR DESTINATION EXCEL ONCE A MONTH##
##每个月需要更改记录的excel的路径## 

ICP_File=r'E:3.xlsx' ##Path for excel from ICP 输入ICP输出的excel文件路径##

data_1= xlrd.open_workbook(ICP_File) 

data = pd.read_excel(ICP_File, sheet_name=2) 

Number_of_Elements=1 ##Please Enter Number of Elements 请输入测量的元素个数 ##

number_for_qc=2 ##Please enter the value of x in qc-2-x 请输入结束测量的qc-2-x中x的值#


n=Number_of_Elements
elements_removal=[]
elements_dup=[]
for c in range(7,7+n):
    elements_removal.append(''.join([x for x in str(data.columns.values[c]) if x.isalpha()]))
for e in range(len(elements_removal)):
    elements_dup.append(elements_removal[e].replace("mgL",""))

## locate stop and start rows##
for indexs in data.index:
    for i in range(len(data.loc[indexs].values)):
        if (data.loc[indexs].values[i] == 'qc-2-'+str(number_for_qc)):  ## 输入正确的结束qc-2-x的值  entering correct ending sample id qc-2-x ##
            stop_row=indexs+1
for indexs in data.index:
    for i in range(len(data.loc[indexs].values)):
        if (data.loc[indexs].values[i] == 'qc-2-1'):
            start_row=indexs+3
print (stop_row)
print (start_row)

table=data_1.sheet_by_index(2)
raw_data=[]
raw_sample_id=[]
for u in range (7,7+n): 
    ##reason for using this loop is due to the fact entered end row has useless qc-2-(x-1/x-2/x-3.....) data##
    for i in range(start_row,stop_row):
        raw_data.append(table.cell_value(i,u))
        if (table.cell_value(i,1)=='mblk'):
            raw_data.remove(table.cell_value(i,u))
        for m in range(2,100):
            if (table.cell_value(i,1)==('qc-2-{}').format('u')):
                        raw_data.remove(table.cell_value(m,7))
values=np.asarray(raw_data)

for i in range(start_row,stop_row):
    raw_sample_id.append(table.cell_value(i,1))
    if (table.cell_value(i,1)=='mblk'):
        raw_sample_id.remove(table.cell_value(i,1))
        for m in range(2,100):
            if (table.cell_value(i,1)==('qc-2-{}').format('u')):
                 raw_sample_id.remove(m,1)

                 
raw_id=[]
for f in range(len(elements_dup)):
    for g in range(len(raw_sample_id)):
        if type(raw_sample_id[g])==float or type(raw_sample_id[g])==int:
            raw_id.append(str(int(raw_sample_id[g]))+elements_dup[f])
        else:
            raw_id.append(str(raw_sample_id[g])+elements_dup[f])
from itertools import chain, repeat
elements=list(chain.from_iterable(zip(*repeat(elements_dup, len(raw_sample_id)))))
elements=np.asarray(elements)
sample_id=np.asarray(raw_id)

##trial number generate##
trial=[]
test_1=xlrd.open_workbook(test)
check=test_1.sheet_by_index(0)
his_len=len(list(check.col_values(1)))
hist_list= list((check.col_values(1)))

for s in range(len(raw_id)):
    if len(raw_id)>len(set(raw_id)):
        if s>0 and raw_id[s]==raw_id[s-1]:
            trial.append(2)
        else:
            trial.append(1)
    else:
        if raw_id[s] in hist_list:
            trial.append(2)
        else:
            trial.append(1)
trial=np.asarray(trial)

## reshaping arrays##
values=values.reshape(len(values),1)
elements=elements.reshape(len(elements),1)
sample_id=sample_id.reshape(len(sample_id),1)
trial=trial.reshape(len(trial),1)

## dataframing arrays##
df_name=pd.read_excel(test, usecols=[1]) ## id on the ICP##
df_id=pd.DataFrame(sample_id,columns=['Sample ID'])
df_IDICP=pd.concat([df_name,df_id],ignore_index=True, join='outer') ##GOAL##
df_ICP=pd.read_excel(test, usecols=[11]) ## value from ICP##
df_value=pd.DataFrame(values,columns=['ICP(mg/L)'])
ICP_value=pd.concat([df_ICP,df_value],ignore_index=True, join='outer') ##GOAL##
df_trial= pd.read_excel(test, usecols=[3]) ##trial numbers##
df_addition_trial=pd.DataFrame(trial,columns=['Trial Number'])
df_trial=pd.concat([df_trial,df_addition_trial],ignore_index=True, join='outer') ##GOAL##
df_element=pd.read_excel(test, usecols=[2]) ##elements##
df_addition_element= pd.DataFrame(elements,columns=['Elements'])
df_element=pd.concat([df_element,df_addition_element],ignore_index=True, join='outer') ##GOAL##

## From ID on ICP to full ID##
ICP_id_for_matching=[]
for y in raw_id:
    ICP_id_for_matching.append(y[:10])
ICP_id_for_matching=np.asarray(ICP_id_for_matching)
df_ICP_id_for_matching=pd.DataFrame(ICP_id_for_matching,columns=['Sample ID'])

id_for_matching=match.sheet_by_index(0).col_values(1)
Real_ID=[]
for a in range (len(df_ICP_id_for_matching)):
    for b in range(len(id_for_matching)):
        if float(df_ICP_id_for_matching.iloc[a]['Sample ID'])== float(id_for_matching[b]):
            Real_ID.append(match.sheet_by_index(0).cell_value(b,0))
Real_ID=np.asarray(Real_ID)
Real_id=Real_ID.reshape(len(df_ICP_id_for_matching),1)

## Datafrmaing of Real ID##
df_real_id=pd.read_excel(test, usecols=[0]) ## id for real##
df_id_addition=pd.DataFrame(Real_id,columns=['Full Sample ID'])
df_full_id=pd.concat([df_real_id,df_id_addition], join='outer').reindex() ##GOAL##
df_full_id.reset_index(drop=True,inplace=True)
df_IDICP.reset_index(drop=True,inplace=True)
df_element.reset_index(drop=True,inplace=True)
df_trial.reset_index(drop=True,inplace=True)

df_w1=pd.read_excel(test, usecols=[4])
df_w2=pd.read_excel(test, usecols=[5])
df_w3=pd.read_excel(test, usecols=[6])
df_w4=pd.read_excel(test, usecols=[7])
df_w5=pd.read_excel(test, usecols=[8])
df_w6=pd.read_excel(test, usecols=[9])
df_DF=pd.read_excel(test, usecols=[10])

df_w1.reset_index(drop=True,inplace=True)
df_w2.reset_index(drop=True,inplace=True)
df_w3.reset_index(drop=True,inplace=True)
df_w4.reset_index(drop=True,inplace=True)
df_w5.reset_index(drop=True,inplace=True)
df_w6.reset_index(drop=True,inplace=True)
df_DF.reset_index(drop=True,inplace=True)

dfs=pd.concat([df_full_id,df_IDICP,df_element,df_trial,df_w1,df_w2,df_w3,df_w4,df_w5,df_w6,df_DF,ICP_value],axis=1)
#outer
dfs.sort_values(by=['Sample ID','Trial Number'],inplace=True)
writer = pd.ExcelWriter(test, engine='xlsxwriter')
dfs.to_excel(writer,index=False)
writer.save()














    








