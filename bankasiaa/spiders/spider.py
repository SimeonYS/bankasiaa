import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbankasiaaItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BbankasiaaSpider(scrapy.Spider):
	name = 'bankasiaa'
	start_urls = ['https://www.bankasia.com/en/news-and-insights.htm']

	def parse(self, response):
		post_links = response.xpath('//div[@class="wrpNewsInsightItemInfo"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('(//h3[@class="eleInline"])[1]/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="conNewsContentLeft"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "", ' '.join(content))

		item = ItemLoader(item=BbankasiaaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
