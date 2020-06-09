# dblpfy

[dib-lip-fy] is a simple tool to convert a bibtex file from heterogeneous sources to entries from DBLP

If you have a bibtex file with entries from various sources, they might differ in style and completeness. In order to get a more consistent bibtex database for your paper or thesis, this tool queries the **great [DBLP](https://dblp.uni-trier.de/)** for every entry in your database and stores the response in a new bibtex file.

## Features
* new entries will keep bibtex key/ID from original file
* entries not found on DBLP will be copied as is to the result file
* progress bar! ;-)
