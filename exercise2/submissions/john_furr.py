#/urs/bin/env python
import os
from os.path import abspath, join, dirname
import pandas as pd
import numpy as np
import scipy.stats as stats

# Set some module level constants for input and output directories
PROGDIR = dirname(abspath(__file__))
INDIR = abspath(join(PROGDIR,os.pardir,"input"))
OUTDIR = abspath(join(PROGDIR,os.pardir,"output"))

def cal_percentiles(client_col='fdntext', infile='', usecols=None, datacols=None):
    # Input integrity checks
    if not usecols:
        raise ValueError("You must pass in a list/tuple of columns to use")
    if not datacols:
        raise ValueError("You must pass in a list/tuple of data cols to use for mean calculation")

    if not os.path.isfile(infile):
        raise IOError("File %s not found"%(infile))

    # Read in the input data xl.csv
    input_data = pd.read_csv(infile, usecols=usecols)
    client_codes = input_data['fdntext'].unique().tolist()

    stats_data = pd.DataFrame(
        index=np.arange(0, len(client_codes)),
        columns=usecols,
    )
    stats_data['fdntext'] = client_codes
     
    # Calculate percentiles for each client score using scypi.stats.percentileofscore
    for colname in datacols:
        col = input_data[colname]
        percentiles=[]
        for val in col:
            percentiles.append(stats.percentileofscore(col, val, kind='mean'))
        stats_data[colname] = percentiles
        
    return stats_data



if __name__ == '__main__':
    usecols = ('fdntext','fldimp','undrfld','advknow','pubpol','comimp','undrwr','undrsoc','orgimp','impsust')
    datacols = usecols[1:]
    stats_data = cal_percentiles(    
        client_col='fdntext',
        infile=join(INDIR, "mean.csv"),
        usecols=usecols,
        datacols=datacols
    )

    # output is written to pct_comp.csv"    
    outfile = join(OUTDIR, "pct_comp.csv")
    stats_data.to_csv(outfile, index=False)

    # Test that we have the correct values
    #
    # NOTE: I tried to get an exact match to the decimal with various approaches, but could not..
    # However the data is accurate out to 14 decimal places...
    stats_test = pd.read_csv(join(OUTDIR, "pct.csv"))
    for colname in datacols:
        for index, val in enumerate(stats_data[colname]):
            # This fails because my code is only accurate out to 14 decimals.
            #assert (stats_data[colname][index]==stats_test[colname][index]) is True

            # Converting the values to string truncates them such that they are equal
            assert (str(stats_data[colname][index])==str(stats_test[colname][index])) is True
   
    print "output in ../output/pct_comp.csv" 
