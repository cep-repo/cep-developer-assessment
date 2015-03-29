#/urs/bin/env python
import os
from os.path import abspath, join, dirname
import pandas as pd
import numpy as np
import filecmp

# Set some module level constants for input and output directories
PROGDIR = dirname(abspath(__file__))
INDIR = abspath(join(PROGDIR,os.pardir,"input"))
OUTDIR = abspath(join(PROGDIR,os.pardir,"output"))

def calculate_mean_data(client_col='fdntext', infile="", usecols=None, datacols=None):
    # Input integrity checks
    if not usecols:
        raise ValueError("You must pass in a list/tuple of columns to use")
    if not datacols:
        raise ValueError("You must pass in a list/tuple of data cols to use for mean calculation")

    if not os.path.isfile(infile):
        raise IOError("File %s not found"%(infile))


    # Read in the input data xl.csv
    input_data = pd.read_csv(infile, usecols=usecols)

    # Note: Instructions say recode 77 and 88 to blank
    # however blank gives TypeErrors, so I converted to NumPy NaN instead.
    input_data = input_data.replace(88, np.nan).replace(77, np.nan)

    #Generate a sorted list of unique Client Codes
    client_codes = sorted(list(set(input_data['fdntext'])))

    # Initialize a DataFrame for the median data
    mean_data = pd.DataFrame(
        index=np.arange(0, len(client_codes)),
        columns=input_data.columns.values
    )

    # Loop over Client Codes and calculate mean of each column and assign to mean_data 
    for row ,cc in enumerate(client_codes):
        mean_data['fdntext'][row] = cc
        cc_data = input_data[input_data['fdntext'] == cc]
        for name in datacols:
            mean_data[name][row] = cc_data[name].mean()

        # Note means can also be calculated in bulk like
        #means =  cc_data[datacols].mean()

    return mean_data

def calculate_stats_data(mean_data, datacols=None):
    # Input integrity checks
    if not datacols:
        raise ValueError("You must provide datacols")

    #   Part 2:   
    #   Calculate the highest, lowest, median, and quartile ratings for each of the 9 questions. Generate a CSV file stats.csv
    stats_data = pd.DataFrame(
        index=('count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'),
        columns=datacols,
    )
       
    # Technically this produces numbers that are very close to the output
    # though there are slight rounding errors.  I'm guessing that in practice
    # this would be the preferred method, but in an effort to exactly match
    # the example output a more verbose method is taken. 
    
    #mean_data = mean_data.convert_objects() # convert object data to numeric data
    #stats_data = mean_data.describe()
       
    # Verbose method to exaclty match output precision
    for colname in datacols:
        stats_data[colname]['count'] = "%.1f"%mean_data[colname].count()
        stats_data[colname]['mean'] = mean_data[colname].mean()
        stats_data[colname]['std'] = mean_data[colname].std()
        stats_data[colname]['min'] = mean_data[colname].min()
        stats_data[colname]['25%'] = mean_data[colname].quantile(0.25)
        stats_data[colname]['50%'] = mean_data[colname].quantile(0.50)
        stats_data[colname]['75%'] = mean_data[colname].quantile(0.75)
        stats_data[colname]['max'] = mean_data[colname].max()

    return stats_data

if __name__ == '__main__':
    #
    # Part 1:  Calculate mean data for specfic fields at the Client Code level.
    #
    # NOTE Instructions said to use:  'undrorg'  but the output file example contains 'impsust'
    # NOTE In order to match the output file I am using impsust, but changing this would be a trivial change
    #      in the usecols tuple below.
    usecols=('fdntext', 'fldimp', 'undrfld', 'advknow', 'pubpol', 'comimp', 'undrwr', 'undrsoc', 'orgimp', 'impsust')
    datacols=usecols[1:]
    mean_data = calculate_mean_data(
        client_col='fdntext', 
        infile=join(INDIR, "xl.csv"),
        usecols=usecols,
        datacols=datacols
    )
    # Write output file and ignore row names/indexes
    outfile = join(OUTDIR, "mean_comp.csv")
    mean_data.to_csv(outfile, index=False)

    # Check that the output file is identical with example file
    assert filecmp.cmp(outfile, join(OUTDIR, "mean.csv")) is True

    #
    # Part 2)  Calculate addition stats aginst mean data
    #
    stats_data = calculate_stats_data(mean_data=mean_data, datacols=datacols)

    # write stats data, this time with row names
    stat_output = join(OUTDIR, "stat_comp.csv")
    stats_data.to_csv(stat_output, index=True)

    # check that output file is identical with example file
    assert filecmp.cmp(stat_output, join(OUTDIR, "stats.csv")) is True

    print "Output files are ../output/mean_comp.csv and ../output/stats_comp.csv"
