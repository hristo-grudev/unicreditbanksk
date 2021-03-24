import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import UnicreditbankskItem
from itemloaders.processors import TakeFirst


class UnicreditbankskSpider(scrapy.Spider):
	name = 'unicreditbanksk'
	start_urls = ['https://www.unicreditbank.sk/sk/o-banke/tlacove-centrum/tlacove-spravy.html.html']

	def parse(self, response):
		post_links = response.xpath('//div[@class="item"]')
		for post in post_links:
			title = post.xpath('.//span[@class="font-title-4"]/text()').get()
			description = post.xpath('.//div[contains(@class, "accordion-body")]//text()[normalize-space()]').getall()
			description = [p.strip() for p in description]
			description = ' '.join(description).strip()
			try:
				date = re.findall(r'\d{1,2}\.\s*\d{1,2}\.\s*\d{4}', title)[0]
			except:
				date = ''

			item = ItemLoader(item=UnicreditbankskItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
