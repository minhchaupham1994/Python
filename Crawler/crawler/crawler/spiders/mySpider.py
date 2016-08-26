import scrapy

from crawler.items import CommentItem
from crawler.items import PostItem

class TinhteSpider(scrapy.Spider):
	name = "tinhte"
	allowed_domains = ["tinhte.vn"]
	start_urls = [
		"https://tinhte.vn/",
	]
			

	def parse(self, response):
		self.TITLE_PATH = "//*[@id='content']/div/div/div/div/div/div[2]/div[1]/div/p[1]/text()"
		self.AUTHOR_PATH = "//*[@id='content']/div/div/div/div/div/div[2]/div[1]/a[2]/span/text()"
		self.MAIN_CONTENT = "//*[@id='messageList']/li[1]/div/div[2]/div[1]/article/blockquote/text()"
		self.HEAD_CONTENT_PATH = "//*[@id='messageList']/li"
		self.CONTENT_OFFSET = "div/div[2]/div[1]/article/blockquote/text()"
		self.COMMENT_AUTHOR_OFFSET = "div/div[1]/div/h3/div/a/text()"
		self.NEXT_PATH = "//*[@id='content']/div/div/div/div/div/div[4]/div[2]/nav/a[contains(text(), 'Sau')]/@href"
		
		flag = 0
		for href in response.css("div > h2 > a::attr('href')"):
			if(flag < 3):
				flag += 1
				url = response.urljoin(href.extract())
				yield scrapy.Request("https://tinhte.vn/threads/facebook-mo-he-thong-nhan-dien-hinh-anh-cua-minh-cho-tat-ca-moi-nguoi.2636679/", callback=self.parse_dir_contents, encoding="UTF-8")

	def parse_dir_contents(self, response): 
		self.is_main_content = True
		for t in response.xpath('//body'):
			item = PostItem()
			item['title'] = t.xpath(self.TITLE_PATH).extract()
			item['author'] = t.xpath(self.AUTHOR_PATH).extract()
			item['content'] = t.xpath(self.MAIN_CONTENT).extract()
			item['comment'] = list(self.parse_comment_xpath(response))
			yield item
	
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
			
		next_page = response.xpath(self.NEXT_PATH)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, callback=self.parse_comment_xpath)	
			
		
		
	
