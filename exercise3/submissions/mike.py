import json
from collections import OrderedDict
import pandas as pd


# Read CSV files
mean = pd.read_csv('exercise3/input/mean.csv', index_col='fdntext')
stats = pd.read_csv('exercise3/input/stats.csv', index_col='Unnamed: 0')
pct = pd.read_csv('exercise3/input/pct.csv', index_col='fdntext')

# Construct the JSON object

# JSON file
elements_dict = OrderedDict()
report_dict = OrderedDict()

json_template = OrderedDict()
json_template["version"] = "1.0"
report_dict["name"] = "Tremont 14S Report"
report_dict["title"] = "Tremont 14S Report"
report_dict["cohorts"] = []
report_dict["segmentations"] = []
report_dict["elements"] = elements_dict
json_template["reports"] = [report_dict]

# Percentile Chart Object
current_dict = {}
abs_val_list = []

pchart_template = OrderedDict()
pchart_template['type'] = "percentileChart"
pchart_template['absolutes'] = abs_val_list
pchart_template['current'] = current_dict
pchart_template['cohorts'] = []
pchart_template['past_results'] = []
pchart_template['segmentations'] = []

# Current Dict
value = 0
percentage = 0
current_template = OrderedDict()
current_template['name'] = '2014'
current_template['value'] = value
current_template['percentage'] = percentage


# Retrieve the data points
val_list = mean.columns
for v in val_list:
    # Construct current_dict
    value = mean.get_value('Tremont 14S', v)
    percentage = pct.get_value('Tremont 14S', v)
    current_dict = current_template
    current_dict['value'] = value
    current_dict['percentage'] = percentage
    # Construct abs_val_list
    abs_val_list = stats[v].ix[['min', '25%', '50%', '75%', 'max']].tolist()
    # Construct pchart_dict
    pchart_dict = pchart_template
    pchart_dict['absolutes'] = abs_val_list
    pchart_dict['current'] = current_dict
    # Now assign the key v to elements_dict
    elements_dict[v] = pchart_dict

# Finally assign elements_dict to JSON template
json_dict = json_template
json_dict['reports'][0]['elements'] = elements_dict

# Now write to JSON
with open('output.json', 'wb') as fp:
    json.dump(json_dict, fp, indent=4, separators=(',', ': '))