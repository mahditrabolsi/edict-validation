import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
########## Important ##########
# You should first run the analyze_planemqx.py (priority and normal) script first to generate the average_categorized_response_time.csv file.
###############################
# summary 
# This script is used to plot the box plots for the average response time per category for the planemqx with or without the priority.
# It takes as input the average_categorized_response_time.csv file and plots the box plots.

for bandwidth in range(8, 13):
    ################# VARIABLES ###################
    type = 'priority'
    # type = 'normal'

    data = pd.read_csv(f'Planemqx_{type}/output/bandwidth_{bandwidth}/average_categorized_response_time.csv')
    ###############################################


    sns.boxplot(x='category', y='mean', data=data, showfliers=False)
    
    plt.ylabel('Response time (ms)')
    plt.xlabel('Category')
    plt.savefig(f'../results/box_plots/{type}/bandwidth_{bandwidth}_box.pdf')

    # Clear the current figure
    plt.clf()