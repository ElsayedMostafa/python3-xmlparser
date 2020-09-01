import requests
import xml.etree.ElementTree as ET
import csv

# news XML URL
url = 'http://www.hindustantimes.com/rss/topnews/rssfeed.xml'
# spoof header to bypass access denied.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

# get XML
xml = requests.get(url, headers=headers).content

with open('news.xml', 'wb') as f:
    f.write(xml)

# tree element
tree = ET.parse("news.xml")
# root element
root = tree.getroot()
# empty list for news
newsList = []

# iterate news items
for item in root.findall('./channel/item'):

    # empty news dictionary
    news = {}

    # iterate child elements of item
    for child in item:

        # special checking for namespace object content:media
        if child.tag == '{http://search.yahoo.com/mrss/}content':
            news['media'] = child.attrib['url']
        else:
            if child.text:
                news[child.tag] = child.text

    # append news dictionary to news items list
    newsList.append(news)

fields = ['guid', 'title', 'pubDate', 'description', 'link', 'media']

with open("out.csv", 'w', encoding='utf-8') as csvfile:

    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    # writing headers (field names)
    writer.writeheader()

    # writing data rows
    writer.writerows(newsList)
