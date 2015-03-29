Exercise 2 Notes
================

*Output files are written to the output directory and have a _comp extension.
For instance pct.csv is replicated as pct_comp.csv in the output directory


*I looked through the panda, numpy and scipy docs and didn't turn up a percentile function?  
Perhaps I just missed it, but in any event the calculation is straight forward with numpy 
array's so I did it by hand.

*For this example I simply could not achieve an exact decimal match.. I got really close 
with a few different examples.  This means testing wasn't as simply as a single line
assert to ensure matching files. However, testing was still as simple as looping 
over the fields, converting to numbers to strings and then testing for matches.

Again testing was easy enough that I just did it at the end of the driver script.
Typically testing would be done with python's unit testing framework.
