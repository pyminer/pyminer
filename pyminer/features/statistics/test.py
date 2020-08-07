# -*- coding: utf-8 -*-

import random,math

import numpy as np

n=1000

normal_population=list(np.random.normal(size=n))

mean_population=np.mean(normal_population)

#总体标准差

sigma=np.std(normal_population,ddof=0)

#存放多个随机样本

list_samples=[]

#多个随机样本的平均数

list_samplesMean=[]

#求单个样本估算的标准误

def Standard_error(sample):

    std=np.std(sample,ddof=0)

    standard_error=std/math.sqrt(len(sample))

    return standard_error

#求真实标准误

def Standard_error_real():

    for i in range(100):

        sample=random.sample(normal_population,100)

        list_samples.append(sample)

    list_samplesMean=[np.mean(i) for i in list_samples]

    standard_error_real=np.std(list_samplesMean,ddof=0)

    return standard_error_real

#plt.hist(normal_values)

#真实标准误

standard_error_real=Standard_error_real()

print(standard_error_real)

#随机抽样

print(Standard_error(list_samples[0]))

print(Standard_error(list_samples[1]))

print(Standard_error(list_samples[2]))