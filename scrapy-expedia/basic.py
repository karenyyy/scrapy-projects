# # -*- coding: utf-8 -*-
# import scrapy
#
#
# class BasicSpider(scrapy.Spider):
#     name = 'basic'
#     allowed_domains = ['web']
#     start_urls = ['http://web/']
#
#     def parse(self, response):
#         pass

import re
import urllib
import json
url = "https://www.world-airport-codes.com/world-top-30-airports.html"
content = urllib.urlopen(url).read()
result = re.compile(r'[A-Z]+/[A-Z]+').findall(content)

for i in range(len(result)):
    result[i] = result[i].split('/')[0].lower()

with open('airport_code.json', 'a') as file:
    json.dump(result, file)
