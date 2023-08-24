import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
########## Important ##########
# You should first run the analyze_planemqx.py (priority and normal) script first to generate the 
# average_categorized_response_time.csv file.
###############################
# summary 
# This script is used to plot the bar charts for the average response time 
# per category for the planemqx with and without the priority.
for bandwidth in range(8, 13):
    ################# VARIABLES ###################
    priority_data = pd.read_csv(f'C:/Users/houss/Desktop/repos/planemqx/experiments/iotconf23/experiments/Planemqx_priority/output/bandwidth_{bandwidth}/average_categorized_response_time.csv')
    normal_data = pd.read_csv(f'C:/Users/houss/Desktop/repos/planemqx/experiments/iotconf23/experiments/Planemqx_normal/output/bandwidth_{bandwidth}/average_categorized_response_time.csv')
    output = f'C:/Users/houss/Desktop/repos/planemqx/experiments/iotconf23/results/emqx_vs_planemqx/bandwidth_{bandwidth}_barchart.pdf'
    ###############################################
    priority_data['priority'] = 'PlanEMQX'
    normal_data['priority'] = 'EMQX'

    data = pd.concat([normal_data, priority_data])

    sns.barplot(x='category', y='mean', hue='priority', data=data,errorbar=None)
    plt.ylabel('Response Time (ms)')
    plt.xlabel('Application Category')

    plt.savefig(output, bbox_inches='tight')

    plt.clf()