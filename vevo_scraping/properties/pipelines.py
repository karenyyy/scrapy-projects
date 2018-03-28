# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log



class PropertiesPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            for i in range(len(dict(item)['artist'])):
                dict_ = {}
                dict_['artist']= dict(item)['artist'][i]
                dict_['songtitle'] = dict(item)['songtitle'][i]
                dict_['image'] = dict(item)['image'][i]
                dict_['video'] = dict(item)['video'][i]
                print dict_
                #self.collection.insert(dict_)
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item