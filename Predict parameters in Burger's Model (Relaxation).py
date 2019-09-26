# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 15:13:43 2019

@author: Guanhua
"""


import scipy, matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import differential_evolution
import warnings
import pandas as pd
from scipy import ndimage
data_time= pd.read_csv(r'C:\Users\Guanhua\Desktop\x.txt', sep=" ", header=None)
list_len_x=len(data_time)
list_len_y=list_len_x
xData=np.asarray(data_time).reshape(list_len_x)
data_shear= pd.read_csv(r'C:\Users\Guanhua\Desktop\y.txt', sep=" ", header=None)
yData=np.asarray(data_shear).reshape(list_len_y)


def func(x, a1, b1, Offset):
    return (a1)*np.exp(-x/b1)+Offset

def sumOfSquaredError(parameterTuple):
    warnings.filterwarnings("ignore")
    val = func(xData, *parameterTuple)
    return np.sum((yData - val) ** 2.0)

def Guess_Initial_Parameters():
    # min and max used for bounds
    maxX = max(xData)
    minX = min(xData)
    maxY = max(yData)
    minY = min(yData)

    parameterBounds = []
    parameterBounds.append([0, 100000])
    parameterBounds.append([0, 100000])
    parameterBounds.append([0.0, minY])
    print (parameterBounds)

    result = differential_evolution(sumOfSquaredError, parameterBounds, strategy='best1bin', popsize=60) # Change popsize for better guessing, which may not have an effect on the final value
    return result.x

Initial_Parameters = Guess_Initial_Parameters()

fittedParameters, pcov = curve_fit(func, xData, yData, Initial_Parameters,maxfev=100000)

print('Parameters', fittedParameters)

modelPredictions = func(xData, *fittedParameters) 

absError = modelPredictions - yData

SE = np.square(absError) 
MSE = np.mean(SE)
RMSE = np.sqrt(MSE) 
Rsquared = 1.0 - (np.var(absError) / np.var(yData))
print('RMSE=', RMSE)
print('R^2=', Rsquared)

def Plt_Relax(graphWidth, graphHeight):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    axes = f.add_subplot(111)
    axes.plot(xData, yData,  '.')
    xModel = np.linspace(min(xData), max(xData))
    yModel = func(xData, *fittedParameters)      
    axes.plot(xData, yModel)
    axes.set_xlabel('Time (s)')
    axes.set_ylabel('Strain (%)')
    plt.show()
    plt.close('all')
    #plt.savefig(r'C:\Users\Guanhua\Desktop\relax.png')

graphWidth = 500
graphHeight = 500
Plt_Relax(graphWidth, graphHeight)


















                




