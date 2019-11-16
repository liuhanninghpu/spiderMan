import scrapy
from ..items import FilmsCityItem
from scrapy import Request

class FilmsCitysSpider(scrapy.Spider):
    name = "films_citys"
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com']
    base_url = 'https://maoyan.com'

    def parse(self, response):
        item = FilmsCityItem()
        if response:
            citysDomName = response.xpath('//a[@class="js-city-name"]/text()').getall()
            citysDomId = response.xpath('//a/@data-ci').getall()
            citysMap = dict(zip(citysDomId,citysDomName))
            for cityId,cityName in citysMap.items():
                item['city_name'] = cityName
                item['cid'] = cityId
                yield item