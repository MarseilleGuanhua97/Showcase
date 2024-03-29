# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 09:04:32 2019

@author: Guanhua
"""
import scipy, matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import differential_evolution
import warnings
import pandas as pd

data_time= pd.read_csv(r'C:\Users\Guanhua\Desktop\x_c.txt', sep=" ", header=None)
list_len_x=len(data_time)
list_len_y=list_len_x
xData=np.asarray(data_time).reshape(list_len_x)
data_shear= pd.read_csv(r'C:\Users\Guanhua\Desktop\y_c.txt', sep=" ", header=None)
yData=np.asarray(data_shear).reshape(list_len_y)


def func_creep(x, n_1, k_2, C):
    return  C+(k_2)*(1-np.exp(-x/255.805493))+n_1*x ##Enter your tao value from previous relaxation process

def sumOfSquaredError(ktarget):
    val = func_creep(xData, *ktarget)
    return np.sum(((yData - val)/yData) ** 2.0)

def generate_Initial_Parameters():
    result = differential_evolution(sumOfSquaredError, [[0,100000],[0,100000],[0,max(yData)]],popsize=60) # Change popsize for better guessing, which may not have an effect on the final value
    return result.x


geneticParameters = generate_Initial_Parameters()

fittedParameters, pcov = curve_fit(func_creep, xData, yData, geneticParameters, maxfev=20000000)

print('Parameters', fittedParameters)


modelPredictions = func_creep(xData, *fittedParameters) 

absError = modelPredictions - yData

SE = np.square(absError) 
MSE = np.mean(SE) 
RMSE = np.sqrt(MSE) 
Rsquared = 1.0 - (np.var(absError) / np.var(yData))
print('RMSE=', RMSE)
print('R^2=', Rsquared)


def Plt_creep(graphWidth, graphHeight):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    axes = f.add_subplot(111)

    axes.plot(xData, yData,  '.')

    xModel = np.linspace(min(xData), max(xData))
    yModel = func_creep(xData, *fittedParameters)

    axes.plot(xData, yModel)
    axes.set_xlabel('Time (s)')
    axes.set_ylabel('Strain (%)') 

    plt.show()
    plt.close('all')

graphWidth = 500
graphHeight = 500
Plt_creep(graphWidth, graphHeight)