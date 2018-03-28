# Scrapy settings for properties project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'vevo_scraping'

SPIDER_MODULES = ['properties.spiders']
NEWSPIDER_MODULE = 'properties.spiders'

# Crawl responsibly by identifying yourself (and your website) on
# the user-agent
#USER_AGENT = 'vevo_scraping (+http://www.yourdomain.com)'

ITEM_PIPELINES = {'properties.pipelines.MongoDBPipeline':300, }

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "vevo"
MONGODB_COLLECTION = "vevo_scrapy"


# Disable S3
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
