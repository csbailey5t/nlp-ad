import re
import pandas as pd
import urllib.request

# Get input from user
search_string = input("Input string you want to search the catalog for: ")

# Replaces any spaces in a user input with '+' to make URL-friendly
search_string = search_string.replace(' ', '+')

# Modify URL with search string input
catalogURL = ("https://catalog.lib.ncsu.edu/catalog?q=" + search_string +
    "&search_field=all_fields")

# Retrieve HTML of the modified URL and assign it to a decoded string
with urllib.request.urlopen(catalogURL) as res:
    catalogHTML = res.read().decode("utf-8")

# Use regex to find all catalog IDs from HTML results
pattern = "(?<=\/catalog\/)(.*?)(?=\/track)"
catalogIDs = re.findall(pattern, catalogHTML)

# Save catalog base URL to append with specific catalog IDs
catalogURL = 'https://catalog.lib.ncsu.edu/catalog/'

# Creates a list of valid .JSON urls for each catalog ID
catalogJSON_list = [catalogURL + i + '.json' for i in catalogIDs]

# Create a data frame for the URL list
df = pd.DataFrame(catalogJSON_list, columns=["JSON-Links"])

# Function to convert authority URLs into clickable form
def fun(path):
    return '<a href="{}">{}</a>'.format(path, url)

# Applying function to authIDs column
df = df.style.format({'catalog-JSON-Links' : fun})

# Convert to excel without indexing
df.to_excel('json-links.xlsx', index=False)
