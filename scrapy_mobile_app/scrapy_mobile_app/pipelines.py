# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# import pymongo
#
# from scrapy.conf import settings
# from scrapy.exceptions import DropItem
# from scrapy import log

class ScrapyMobileAppPipeline(object):
    def process_item(self, item, spider):
        return item



# class MongoDBPipeline(object):
#
#     def __init__(self):
#         connection = pymongo.MongoClient(
#             settings['MONGODB_SERVER'],
#             settings['MONGODB_PORT']
#         )
#         db = connection[settings['MONGODB_DB']]
#         self.collection = db[settings['MONGODB_COLLECTION']]
#
#     def process_item(self, item, spider):
#         valid = True
#         for data in item:
#             if not data:
#                 valid = False
#                 raise DropItem("Missing {0}!".format(data))
#         if valid:
#             for i in range(len(dict(item)['title'])):
#                 dict_ = {}
#                 dict_['description']= dict(item)['description'][i]
#                 dict_['title'] = dict(item)['title'][i]
#                 dict_['url'] = dict(item)['url'][i]
#                 dict_['price'] = dict(item)['price'][i]
#                 dict_['address'] = dict(item)['address'][i]
#                 print dict_
#                 self.collection.insert(dict_)
#             log.msg("Question added to MongoDB database!",
#                     level=log.DEBUG, spider=spider)
#         return item