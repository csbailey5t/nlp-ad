import JSON_scraper
import json

JSON_search = input("Enter the JSON value you are interested in: ")

fp = open('catalog_results_metadata.json')
data = json.load(fp)
for i in range(len(data)):
    print(data[i][JSON_search])
fp.close()
