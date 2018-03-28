# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.conf import settings


class ImdbPipeline(object):
    def process_item(self, item, spider):
        with open('imdb.json', 'w') as file:
            json.dump(dict(item), file)
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
            for i in range(len(dict(item)['Title'])):
                dict_ = {}
                dict_['Title'] = dict(item)['Title']
                dict_['Ranking'] = dict(item)['Ranking']
                dict_['Rating'] = dict(item)['Rating']
                dict_['ReleaseDate'] = dict(item)['ReleaseDate'].replace("\(\)", "")
                dict_['MainPageUrl'] = dict(item)['MainPageUrl']

                dict_['Director'] = dict(item)['Director'] if dict(item)['Director'] else None
                dict_['Writers'] = dict(item)['Writers'] if dict(item)['Writers'] else None
                dict_['Runtime'] = dict(item)['Runtime'] if dict(item)['Runtime'] else None
                dict_['Sinopsis'] = dict(item)['Sinopsis'].replace("\n", "") if dict(item)['Sinopsis'] else None
                dict_['Genres'] = dict(item)['Genres'] if dict(item)['Genres'] else None
                dict_['MpaaRating'] = dict(item)['MpaaRating'] if dict(item)['MpaaRating'] else None
                dict_['Budget'] = dict(item)['Budget'].replace("\n", "") if dict(item)['Budget'] else None
                dict_['Language'] = dict(item)['Language'] if dict(item)['Language'] else None
                dict_['GrossProfit'] = dict(item)['GrossProfit'].replace("\n", "") if dict(item)[
                    'GrossProfit'] else None
                dict_['OpeningWeekendProfit'] = dict(item)['OpeningWeekendProfit'].replace(",\n", "") if dict(item)[
                    'OpeningWeekendProfit'] else None
                dict_['AspectRatio'] = dict(item)['AspectRatio'].replace("\n", "") if dict(item)[
                    'AspectRatio'] else None
                dict_['SoundMix'] = dict(item)['SoundMix'] if dict(item)['SoundMix'] else None
                dict_['Color'] = dict(item)['Color'] if dict(item)['Color'] else None
                dict_['CastMembers'] = dict(item)['CastMembers'] if dict(item)['CastMembers'] else None

                print dict_
                self.collection.insert(dict_)

            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
