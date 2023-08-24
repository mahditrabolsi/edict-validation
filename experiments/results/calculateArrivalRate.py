#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 11:04:06 2023

@author: satrai
"""

import json 

file_path = '/home/satrai/planiot--priorities/subscribers/data/scenario_planner.json'

app_categories_subscriptions = dict()
app_categories_subscriptions['AN'] = []
app_categories_subscriptions['RT'] = []
app_categories_subscriptions['TS'] = []
app_categories_subscriptions['VS'] = []


rate_an, rate_rt, rate_ts, rate_vs = 0, 0, 0, 0
topic_rate = dict()

f = open(file_path)

data = json.load(f)


for i in data['IoTdevices']:
    topic = i['deviceName'].replace('_source', '')
    messageSize = i['messageSize']
    publishFrequency = i['publishFrequency']
    topic_rate[topic] = messageSize*8*publishFrequency

for i in data['applications']:
    category = i['applicationCategory']
    for topic in i['subscribesTo']:
        app_categories_subscriptions[category].append(topic.replace('topic_', ''))
        
        
#print(app_categories_subscriptions)
#print(topic_rate)
        
for topic in app_categories_subscriptions['AN']:
    rate_an += topic_rate[topic]
        
for topic in app_categories_subscriptions['RT']:
    rate_rt += topic_rate[topic]
    
for topic in app_categories_subscriptions['TS']:
    rate_ts += topic_rate[topic]
    
for topic in app_categories_subscriptions['VS']:
    rate_vs += topic_rate[topic]
    
print(rate_an / 1000000, rate_rt / 1000000, rate_ts / 1000000, rate_vs / 1000000)