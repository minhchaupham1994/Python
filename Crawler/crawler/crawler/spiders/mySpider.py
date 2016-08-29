import scrapy
import logging


from crawler.items import CommentItem
from crawler.items import PostItem
from crawler.items import ResultItem

class TinhteSpider(scrapy.Spider):
	name = "tinhte"
	allowed_domains = ["tinhte.vn"]
	start_urls = [
		"https://tinhte.vn/",
	]
			
	def __init__(self):
		self.TITLE_PATH = "//*[@id='content']/div/div/div/div/div/div[2]/div[1]/div/p[1]/text()"
		self.AUTHOR_PATH = "//*[@id='content']/div/div/div/div/div/div[2]/div[1]/a[2]/span/text()"
		self.MAIN_CONTENT = "//*[@id='messageList']/li[1]/div/div[2]/div[1]/article/blockquote/text()"
		self.HEAD_CONTENT_PATH = "//*[@id='messageList']/li"
		self.CONTENT_OFFSET = "div/div[2]/div[1]/article/blockquote/text()"
		self.COMMENT_AUTHOR_OFFSET = "div/div[1]/div/h3/div/a/text()"
		self.NEXT_PATH = "//*[@id='content']/div/div/div/div/div/div[4]/div[2]/nav/a[contains(text(), 'Sau')]/@href"
		self.result = ["chau"]
		

		
	def parse(self, response):
		self.chau = {"temp":""}
		self.first = True
		
		flag = 0
		for href in response.css("div > h2 > a::attr('href')"):
			if(flag < 3):
				flag += 1
				url = response.urljoin(href.extract())
				yield scrapy.Request(url, callback=self.parse_dir_contents, encoding="UTF-8")

	def parse_dir_contents(self, response):
		logging.warning("This is parse_dir_contents")
		self.is_main_content = True
		item = ResultItem()
		item['post_item'] = list(self.parse_post_xpath(response))
		item['comment_items'] = list(self.parse_comment_xpath(response))
		
		next_page = response.xpath(self.NEXT_PATH)
		if next_page:
			logging.warning("This is next_page")
			url = response.urljoin(next_page[0].extract())
			my_meta = {"item": item}
			scrapy.Request(url, meta=my_meta, callback=self.parse_comment_helper)

		return item
		
	
	def parse_post_xpath(self, response): 
		#parse content
		for t in response.xpath('//body'):
			item = PostItem()
			item['url'] = [response.url]
			item['title'] = t.xpath(self.TITLE_PATH).extract()
			item['author'] = t.xpath(self.AUTHOR_PATH).extract()
			item['content'] = t.xpath(self.MAIN_CONTENT).extract()
			yield item
			
	def parse_comment_helper(self, response):
		item = response.meta['item']	
		item['comment_items'] += list(parse_comment_xpath(response))
		
		next_page = response.xpath(self.NEXT_PATH)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			scrapy.Request(url, meta=response.meta, callback=self.parse_comment_helper) 
			
	def parse_comment_xpath(self, response):		
		for c in response.xpath(self.HEAD_CONTENT_PATH):
			if(self.is_main_content):
				self.is_main_content = False
			else:
				item = CommentItem()
				item['author'] = c.xpath(self.COMMENT_AUTHOR_OFFSET).extract()
				item['content'] = c.xpath(self.CONTENT_OFFSET).extract()
				item['url'] = [response.url]
				yield item
				
				
		
			
		
		
		
	
