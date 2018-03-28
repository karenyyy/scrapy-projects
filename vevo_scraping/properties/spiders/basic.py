import datetime
import urlparse
import socket
import scrapy

from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader

from properties.items import PropertiesItem



class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["web"]

    # Start on a property page
    # start_urls = (
    #     'https://www.vevo.com/trending-now',
    # )
    def start_requests(self):
        urls = []
        for i in range(1, 10):
            urls.append('https://www.vevo.com/trending-now?page={}'.format(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ This function parses a property page.

        @url http://web:9312/vevo_scraping/property_000000.html
        @returns items 1
        @scrapes title price description address image_urls
        @scrapes url project spider server date
        """

        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), response=response)

        # Load fields using XPath expressions

        # l.add_xpath('title', '//*[@itemprop="name"][1]/text()',
        #             MapCompose(unicode.strip, unicode.title))
        # l.add_xpath('price', './/*[@itemprop="price"][1]/text()',
        #             MapCompose(lambda i: i.replace(',', ''), float),
        #             re='[,.0-9]+')
        # l.add_xpath('description', '//*[@itemprop="description"][1]/text()',
        #             MapCompose(unicode.strip), Join())
        # l.add_xpath('address',
        #             '//*[@itemtype="http://schema.org/Place"][1]/text()',
        #             MapCompose(unicode.strip))
        # l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src',
        #             MapCompose(lambda i: urlparse.urljoin(response.url, i)))


        l.add_xpath('artist', '//*[@class = "feed-item-title"]/text()',
                    MapCompose(unicode.strip))
        l.add_xpath('songtitle', '//*[@class = "feed-item-subtitle"]/h3/text()',
                    MapCompose(lambda i: i.replace('\'', '')))
        l.add_xpath('image', '//*[@class = "image-shaped"]/@src',
                    MapCompose(lambda i: urlparse.urljoin(response.url, i)))
        l.add_xpath('video', '//*[@class = "feed-item-subtitle"]/@href',
                    MapCompose(lambda i: urlparse.urljoin(response.url, i)))

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()



