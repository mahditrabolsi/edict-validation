# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:08:28 2023

@author: houss
"""

import csv 
import matplotlib.pyplot as plt
import numpy as np

#baseline_file = 'C:\\Users\\houss\\Desktop\planiot--priorities\\experiments\\results\\susbcribers_results_baseline.csv'
#planner_file = 'C:\\Users\\houss\\Desktop\planiot--priorities\\experiments\\results\\susbcribers_results_planner.csv'
#categoriesfile = 'C:\\Users\\houss\\Desktop\planiot--priorities\\experiments\\results\\appCategories.csv'

baseline_file = '/home/satrai/planiot--priorities/results/mininet/performanceEvaluation/planemqx-beforeChanges/result_subscribers.csv'
planner_file = '/home/satrai/planiot--priorities/results/mininet/performanceEvaluation/planemqx-afterChanges/result_subscribers.csv'
categoriesfile = '/home/satrai/planiot--priorities/experiments/results/appCategories.csv'

app_cat_dict = dict()
app_response_time_dict = dict()
app_nb_subscriptions_dict = dict()

with open(categoriesfile) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        app = row[0]
        category = row[1]
        app_cat_dict[app] = category
   
for app in app_cat_dict.keys():
    app_response_time_dict[app] = 0
    app_nb_subscriptions_dict[app] = 0
    
def return_response_times(resultsfile):
    with open(resultsfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in reader:
            if i != 0:
                app = row[0]
                responsetime = float(row[6])
                app_response_time_dict[app] += responsetime
                app_nb_subscriptions_dict[app] += 1
            i+=1

    for app in app_response_time_dict.keys():
        if app_nb_subscriptions_dict[app] != 0:
            app_response_time_dict[app] = app_response_time_dict[app] / app_nb_subscriptions_dict[app]
            


    resptime_an = 0
    resptime_rt = 0
    resptime_ts = 0
    resptime_vs = 0

    for app in app_response_time_dict.keys():
        if app_cat_dict[app] == ' AN':
            resptime_an += app_response_time_dict[app]
        elif app_cat_dict[app] == ' RT':
            resptime_rt += app_response_time_dict[app]
        elif app_cat_dict[app] == ' TS':
            resptime_ts += app_response_time_dict[app]
        elif app_cat_dict[app] == ' VS':
            resptime_vs += app_response_time_dict[app]
            
    resptime_an = resptime_an / 4.0
    resptime_rt = resptime_rt / 4.0
    resptime_ts = resptime_ts /4.0
    resptime_vs = resptime_vs / 4.0
    
    return [resptime_an, resptime_rt, resptime_ts, resptime_vs]

    
responsetimes_baseline = return_response_times(baseline_file)
responsetimes_planner = return_response_times(planner_file)
print(responsetimes_baseline)
print(responsetimes_planner)
categories = ['AN', 'RT', 'TS', 'VS']

fig, ax = plt.subplots()
X_axis = np.arange(len(categories))

ax.bar(X_axis - 0.15, responsetimes_baseline, 0.3, color='orange', label='before changes')
ax.bar(X_axis + 0.15, responsetimes_planner, 0.3, color='blue', label='after changes')
ax.legend()
ax.set_xlabel('Application Category')
ax.set_ylabel('Response Time (sec)')
plt.xticks(X_axis, categories)
#plt.savefig("/home/satrai/planiot--priorities/results/mininet/without-agent/responsetime.pdf", bbox_inches="tight")
plt.show()
# plt.xlabel('Application Category')
# plt.ylabel('Response Time (sec)')
# plt.bar(categories, responsetimes)
# plt.show()

