####Census Scripts####

These are a set of scripts that will assist in pulling down the Monroe County Jail Inmate 
Census, Parse the PDF document into human readable text, format that text in a way that 
removes erroneous data, and finally parse out all of the inmates as well as their booking 
data. 


    pullpdf.py
        This file containts the pullpdf() function which will pull down the latest census 
        PDF document from the Monroe County website and convert it to human readable text.
        This file also handles removal of unused header and footer data, as well as reformats
        some of the booking data so it is easier to consume farther down the line.

    pullinmates.py
        This file contains the pullinmates() function which will pull all of the inmates
        and the raw version of all of their booking data out of the converted and formatted
        PDF document.

    parseinmate.py
        This file is the last step where the row data is parsed and placed into an array of
        inmate classes so it can be used down stream.

    census.py
        The entry point to the scripts shown above.  This script pulls down the latest census
        file and pushes all of it's contents into a sqlite3 database for easy querying and 
        over all use.


These files were purposly broken out as such to make portability easier.  There are some 
helper functions within each script - so feel free to dive in and see how they work!
