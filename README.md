Dukascopy historical data time converter
========================================

Converts a Dukascopy historical quote file line by line from quote time in GMT time zone to quote time in MET/MEST time zone.

**usage:** Dukascopy_time_converter.py *input.csv* ...

will create output files named *input.converted.csv* ...  in same directory as input files. 

Needs package **pytz**, which can be installed with the command:
    
    easy_install --upgrade pytz 
    or perhaps some similiar as: easy_install-2.7 --upgrade pytz 
