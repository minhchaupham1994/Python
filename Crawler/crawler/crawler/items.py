# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ResultItem(scrapy.Item):
	post_item = scrapy.Field()
	comment_items = scrapy.Field()

class PostItem(scrapy.Item):
	url = scrapy.Field()
	title = scrapy.Field()
	author = scrapy.Field()
	content = scrapy.Field()
	
class CommentItem(scrapy.Item):
	url = scrapy.Field()
	author = scrapy.Field()
	content = scrapy.Field()
	
