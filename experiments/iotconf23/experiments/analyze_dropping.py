import pandas as pd

################# VARIABLES ###################
#### variables are in the loop below
###############################################

#  Summary
#     This script is used to analyze the dropping of messages in the system.
#     It takes as input the total_messages.csv file and calculates the total number of messages dropped per subscription.
#     It also calculates the percentage of messages dropped per category.

# Returns:
#     Files:   - dropping_per_category.csv
#              - dropping.csv




# these are the categories for 20 subscribers
# categories={'app_app38': 'VS', 'app_app12': 'TS', 'app_app11': 'TS', 'app_app36': 'VS', 'app_app22': 'RT', 'app_app2': 'AN', 'app_app1': 'AN', 'app_app21': 'RT', 'app_app23': 'RT'}
# def categorize_app(app):
#     return categories[app]



# this is for the Planemqx 
def categorize_app(app):
    if app.endswith('13') or app.endswith('14') or app.endswith('15') or app.endswith('16'):
        return 'ST'
    elif app.endswith('9') or app.endswith('10') or app.endswith('11') or app.endswith('12'):
        return 'TS'
    elif app.endswith('5') or app.endswith('6') or app.endswith('7') or app.endswith('8'):
        return 'RT'
    elif app.endswith('1') or app.endswith('2') or app.endswith('3') or app.endswith('4'):
        return 'AN'
    else:
        return 'None'


for bandwidth in range(8, 13):
    ################# VARIABLES ###################
    type = 'priority'
    # type = 'normal'
    directory = f'Planemqx_{type}/output/bandwidth_{bandwidth}/'
    # directory = f'experiment_20sub/output/bandwidth_300/'

    ###############################################
    data = pd.read_csv(f'{directory}total_messages.csv')
    data['dropping'] = data['message_sent'] - data['received_count']
    data['percentage'] = (data['dropping'] / data['message_sent']) * 100
    data.to_csv(f'{directory}dropping.csv', index=False)
    data = pd.read_csv(f'{directory}dropping.csv')
    data['category'] = data['app'].apply(categorize_app)
    dropping_per_category = data.groupby('category')['dropping'].sum().reset_index(name='total_dropping')
    dropping_per_category['total_messages_sent'] = data.groupby('category')['message_sent'].sum().reset_index(name='total_messages')['total_messages']
    dropping_per_category['total_messages_received'] = data.groupby('category')['received_count'].sum().reset_index(name='total_received')['total_received']
    dropping_per_category['percentage'] = (dropping_per_category['total_dropping'] / dropping_per_category['total_messages_sent']) * 100
    dropping_per_category.to_csv(f'{directory}dropping_per_category.csv', index=False)
    
