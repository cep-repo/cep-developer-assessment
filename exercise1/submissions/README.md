Exercise 1 Notes
================

*Output files are written to the output directory and have a _comp extension.
For instance mean.csv is replicated in mean_out.csv and stats.csv is replicated
as stats_comp.csv.


*The Instructions said to use:  'undrorg'  but the output file example contains 'impsust'

In an effort to get an exact diff match to the file I used the same cols as the example
output files.  If this is undesired it would be a trivial change to add in the correct
field in the __main__ section of the driver code:  john_furr.py

*I have also highlighed via comments in the code alternative (simplified) way's of doing things.
In some cases I took a more verbose approach to calculating values or saving output, 
but this was striclty to match the test files. I'd guess that in the real world you 
wouldn't care about precission to 16 decimal places..  

* Testing for exercise 1 was simply enough to use a single assert statement to ensure that
The test files and output files were identical.  
