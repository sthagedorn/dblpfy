import sys
import time

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

import requests

from tqdm import tqdm

dblp = "https://dblp.org/search/publ/api?format=bibtex&h=1&q="

if __name__ == "__main__":

  if len(sys.argv) != 3:
    print(f"Please provide input bib tex file and outout file: {sys.argv[0]} <input.bib> <output.bib>")
    sys.exit(1)

  inputFile = sys.argv[1]
  outputFile = sys.argv[2]


  # the error file to log unmatched IDs to
  errfile = "./err.log"

  # our bibtex DB for DBLP entries
  outdb = BibDatabase()

  # reader for the input file
  parser = BibTexParser()
  parser.ignore_nonstandard_types = False
  parser.homogenize_fields = False
  parser.common_strings = False 
  
  # open the input file and parse it
  with open(inputFile) as bibtex_file, open(errfile,"w") as errorFile:
    bibtex_database = bibtexparser.load(bibtex_file)

    # loop over every bibtex entry in the input DB
    for entry in tqdm(bibtex_database.entries[:10]):

      # title has { and } -- remove them and wrap title in quotation marks
      title = entry["title"]
      title = title.replace("{","").replace("}","")
      title = f"\"{title}\""

      # ask DBLP for this title
      with requests.get(dblp+title) as r:

        # maybe it's not there... 
        if len(r.content) <= 0 or not r.ok:
          
          # we add the original entry to the output
          outdb.entries.append(entry)
          # log it
          errorFile.write(f"{entry['ID']}\n")

        else:
          # parse the DBLP response
          newdb = parser.parse(r.content, False)
          # there might be multiple entries ... only the first
          newentry = newdb.entries[0]
          # set ID to old original ID since we already used it in some documents
          newentry["ID"] = entry["ID"]
          # add new entry to output DB
          outdb.entries.append(newentry)
          
          # clear temporary DB
          del newdb.entries[:]

      # don't DOS the DBLP server
      time.sleep(2)


  # now that we've queried all entries, write them to a actual file
  writer = BibTexWriter()
  writer.contents = ['comments', 'entries']
  writer.indent = '  '
  bibtex_str = bibtexparser.dumps(outdb, writer)

  with open(outputFile,"w") as outfile:
    outfile.writelines(bibtex_str)
