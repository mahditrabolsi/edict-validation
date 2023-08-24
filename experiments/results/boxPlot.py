#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 18:08:45 2023

@author: satrai
"""

import csv
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
import pandas as pd

planemqx_file = '/home/satrai/planemqx/results/mininet/performanceEvaluation/afterRefactoring/responsetimes_planemqx.csv'
emqx_file = '/home/satrai/planemqx/results/mininet/performanceEvaluation/afterRefactoring/responsetimes_emqx.csv'

responsetimes_planemqx = []
responsetimes_emqx = []

with open (planemqx_file) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        responsetimes_planemqx.append(float(row[2]) / 1_000_000)
  
with open (emqx_file) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        responsetimes_emqx.append(float(row[2]) / 1_000_000)
  
s1= pd.Series(responsetimes_planemqx)
print(s1.describe())

s2 = pd.Series(responsetimes_emqx)
print(s2.describe())
#fig, ax = plt.subplots(1, 2, figsize=(10,5))
#ax[0].boxplot(responsetimes_planemqx, vert=False)
#ax[1].boxplot(responsetimes_emqx, vert=False)
#plt.show()       