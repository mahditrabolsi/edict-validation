import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

########## Important ##########
# You should first run the analyze_planemqx.py (priority and normal) script first to generate the average_categorized_response_time.csv file.
###############################
# summary 
# This script is used to plot the box plots for the average response time per category for the planemqx with and without the priority.
# It takes as input the average_categorized_response_time.csv file and plots the box plots.

for bandwidth in range(8, 13):
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    
    data1 = pd.read_csv(f'Planemqx_normal/output/bandwidth_{bandwidth}/average_categorized_response_time.csv')
    data2 = pd.read_csv(f'Planemqx_priority/output/bandwidth_{bandwidth}/average_categorized_response_time.csv')

    sns.boxplot(x='category', y='mean', data=data1, showfliers=False, ax=ax1)
    sns.boxplot(x='category', y='mean', data=data2, showfliers=False, ax=ax2)

    ax1.set_ylabel('Response time (ms)')
    ax1.set_xlabel('Normal')
    ax2.set_xlabel('Priority')
    ax2.set_ylabel('')

    plt.savefig(f'../results/box_plots/combined/bandwidth_{bandwidth}_box.pdf')
