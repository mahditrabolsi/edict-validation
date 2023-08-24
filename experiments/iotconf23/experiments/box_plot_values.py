import pandas as pd
import numpy as np
########## Important ##########
# You should first run the analyze_planemqx.py (priority and normal) script first to generate the average_categorized_response_time.csv file.
###############################
# This script is used to calculate the box plot "values"(lower whisker, Q1, median, Q3, upper whisker)
# for the average response time per category for the planemqx with or without the priority.
for bandwidth in range(8, 13):

    ################# VARIABLES ###################
    # type = 'priority'
    type = 'normal'
    directory = f'Planemqx_{type}/output/bandwidth_{bandwidth}/'
    # directory = f'experiment_20sub/output/bandwidth_300/'
    ###############################################

    priority_data = pd.read_csv(f'{directory}average_categorized_response_time.csv')

    grouped_data = priority_data.groupby('category')
    with open(f'{directory}box_values.csv', 'w') as f:
        f.write('category,lower_whisker,Q1,median,Q3,upper_whisker\n')
    for category, group in grouped_data:
        Q1 = np.percentile(group['mean'], 25)
        Q2 = np.percentile(group['mean'], 50)
        Q3 = np.percentile(group['mean'], 75)
        
        IQR = Q3 - Q1
        
        lower_whisker = max(group['mean'].min(), Q1 - 1.5 * IQR)
        upper_whisker = min(group['mean'].max(), Q3 + 1.5 * IQR)
        
        print(f'Category: {category}')
        print(f'Lower whisker: {lower_whisker}')
        print(f'Q1: {Q1}')
        print(f'Median: {Q2}')
        print(f'Q3: {Q3}')
        print(f'Upper whisker: {upper_whisker}')
        with open(f'{directory}box_values.csv', 'a') as f:
            f.write(f'{category},{lower_whisker},{Q1},{Q2},{Q3},{upper_whisker}\n')