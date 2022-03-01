import requests
import csv
import re
from bs4 import BeautifulSoup
 
# Getting page HTML through request
keys_page = requests.get('https://songkeyfinder.com/learn/songs-in-key')

# Parsing content using beautifulsoup
keys_soup = BeautifulSoup(keys_page.content, 'html.parser')
key_links = keys_soup.select("#content > p > a")

# Output file
writer = csv.writer(open("songs.csv", 'w', encoding='utf8', newline=''))

# Handle each song key
for anchor in key_links:

    key_name = anchor.text
    print(key_name)
    
    url = 'https://songkeyfinder.com' + anchor['href']
    has_next_page = True
    
    while has_next_page:
        print(url)

        songs_page = requests.get(url)
        songs_soup = BeautifulSoup(songs_page.content, 'html.parser')    
        table = songs_soup.find("table", class_="searchresults")
        rows = table.find("tr").find_all("tr") # HACK: Fix for a dangling <tr> on the header...
        
        for row in rows:        
            scrapedInfo = {
                "artist": row.contents[0].text,
                "song": row.contents[1].text,
                "popularity": row.contents[2].text,
                "key": key_name,
            }
            writer.writerow(scrapedInfo.values())
        
        next_page = songs_soup.find("a", string=re.compile("^Next Page"))
        if next_page:
            url = 'https://songkeyfinder.com' + next_page['href']
        else:
            has_next_page = False
