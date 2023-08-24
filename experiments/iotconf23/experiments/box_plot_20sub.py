import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

################# VARIABLES ###################
input ='experiment_20sub/output/bandwidth_300/average_categorized_response_time.csv'
output ='../results/box_plots/20sub/bandwidth_300_box.pdf'

###############################################

data=pd.read_csv(input)

sns.boxplot(x='category', y='mean', data=data, showfliers=False)

plt.ylabel('Response time (ms)')
plt.xlabel('Category')
plt.savefig(output)
plt.clf()