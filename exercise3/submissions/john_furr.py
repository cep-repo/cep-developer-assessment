#/urs/bin/env python
import os
from os.path import abspath, join, dirname
import pandas as pd
import json
from collections import OrderedDict

# Set some module level constants for input and output directories
PROGDIR = dirname(abspath(__file__))
INDIR = abspath(join(PROGDIR,os.pardir,"input"))
OUTDIR = abspath(join(PROGDIR,os.pardir,"output"))

def get_absolutes(key, stat_data):
    """ return an array of five numeric values. 
        These values represent the 0th, 25th, 50th, 75th, and 100th 
        percentile values for the given question
    """
    return [
        stat_data[key]['min'],
        stat_data[key]['25%'],
        stat_data[key]['50%'],
        stat_data[key]['75%'],
        stat_data[key]['max'],
    ]

def get_report_for_customer(name=None):
    mean_data = pd.read_csv(join(INDIR, "mean.csv"), index_col=0)
    stat_data = pd.read_csv(join(INDIR, "stats.csv"), index_col=0)
    pct_data = pd.read_csv(join(INDIR, "pct.csv"), index_col=0)

    # Create base json skeleton for the Client Report.
    report = OrderedDict([
        ("name","{0} Report".format(name)),
        ("title","{0} Report".format(name)),
        ("cohorts", []),
        ("segmentations", []),
        ("elements",OrderedDict())
    ])

    elements = report['elements']

    # fill in the elements dictionary with the data from the 9 reports
    for key in stat_data.columns.values:
        elements[key] = OrderedDict([
            ("type", "percentileChart"),
            ("absolutes", get_absolutes(key, stat_data)),
            ("current",OrderedDict([
                ("name", "2014"),
                ("value", mean_data[key][name]),
                ("percentage", pct_data[key][name]),
            ])),
            ("cohorts", []),
            ("past_results", []),
            ("segmentations", [])
        ])

    return report 

def test_output(outfile):
    # Simple test that we have correct fields and field types
    # data is assumed to be correct from previous steps
    with open(outfile, 'r') as data_file:    
        data = json.load(data_file)

    
    assert (data.get('version') =="1.0") is True
    assert isinstance(data.get('reports'), list) is True
    
    for report in data['reports']:
        assert(isinstance(report, dict)) is True

        assert isinstance(report.get("name"), unicode) is True
        assert isinstance(report.get("title"), unicode) is True
        assert isinstance(report.get("segmentations"), list) is True
        assert isinstance(report.get("cohorts"), list) is True

        assert isinstance(report.get("elements"), dict) is True
        assert len(report['elements'].keys()) == 9
        
        elements = report['elements']
        for r in ["fldimp", "undrfld", "advknow", "pubpol", "comimp", "undrwr", "undrsoc", "orgimp", "impsust"]:
            assert isinstance(elements.get(r), dict) is True
            assert elements[r].get('type') == "percentileChart"
            assert isinstance(elements[r].get('absolutes'), list) is True
            assert len(elements[r]['absolutes']) == 5
   
            assert isinstance(elements[r].get('current'), dict) is True 
            assert elements[r]['current'].get('name') == "2014"
            assert isinstance(elements[r]['current'].get('value'), float) is True
            assert isinstance(elements[r]['current'].get('percentage'), float) is True
           
            assert isinstance(elements[r].get('cohorts'), list) is True 
            assert isinstance(elements[r].get('past_results'), list) is True 
            assert isinstance(elements[r].get('segmentations'), list) is True 
            
            

if __name__ == '__main__':
    # build base skeleton report.  All Client repots should be stored as a 
    # a dictionary of values in the reports section. 
    output = OrderedDict({
        "version":"1.0",
        "reports":[
            get_report_for_customer("Tremont 14S"),
            # you can hard code additional reports like above
            # or you could loop over a list and append the reports 
            # to the output['reports'[ list.
        ]
    })
 
    outfile = (join(OUTDIR, "output_comp.json"))
    with open(outfile, 'w') as f:
        f.write(json.dumps(output, indent=4))

    test_output(outfile)
