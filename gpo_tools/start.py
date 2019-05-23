from scrape import Scraper

scraper = Scraper(db = 'postgres', user = 'postgres', password = '123456', 
                     host = 'localhost', update_stewart_meta = False)
scraper.scrape()

'''
## to run the parser
from parse import Parser
parser = Parser(db ='postgres', user='postgres',password='123456',host='localhost')
#can either answer 'y' or put an integer congress number (eg, 100), or put a single hearing in quotes (eg, "CHRG-105shrg46105")
parser.parse_gpo_hearings(n_cores=1)


## to dump the output to json (one json file per hearing)
import json

count = 0
for res in parser.results:
  try:
    jacket = res[0]["jacket"]
    data = res
    with open('results/' + jacket + '.txt', 'w') as outfile:
        json.dump(data, outfile)
    count += 1
  except:
    continue

print (count)

'''
