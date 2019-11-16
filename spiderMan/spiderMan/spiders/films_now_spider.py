import scrapy
from ..items import FilmsNowItem
from scrapy import Request
from ..pipelines import SpidermanPipeline
import re

#正在热映
class FilmsNowSpider(scrapy.Spider):
    name = "films_now"

    allowed_domains = ['maoyan.com']

    #start_urls = ['https://maoyan.com/films?offset=0']

    # 每部电影详情页的基本前缀url
    base_url = 'https://maoyan.com'

    # 下一页前缀url
    next_base_url = 'https://maoyan.com/films'

    #电影详情页的url前缀
    movive_detail_url = 'https://maoyan.com/cinemas?movieId='

    #城市ID
    cid = None

    def __init__(self, cid=None, *args, **kwargs):
        super(FilmsNowSpider,self).__init__(*args,**kwargs)
        self.cid = cid

    def start_requests(self):
        print('startPorject:CID:'+self.cid)
        url = self.next_base_url+"?offset=0"
        yield scrapy.Request(url=url, callback=self.parse,meta={'cid':self.cid},dont_filter=True)

    def parse(self, response):
        cid = response.meta['cid']
        cityInfo = self.getCityByCid(cid)
        item = FilmsNowItem()
        if response:
            item['cid'] = int(cityInfo[0])
            item['city_name'] = cityInfo[1]
            #yield item
            # 根据内页地址爬取
            url = self.next_base_url + "?offset=0"
            yield scrapy.Request(url, meta={'item': item}, callback=self.parseDetail,cookies=self.getCityCookies(cid))

    def parseDetail(self,response):
        # filename = 'test.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        # exit()
        item = response.meta['item']
        if 'cid' not in item:
            print('error')
            exit()
        filmNameList= response.xpath("//div[@class='channel-detail movie-item-title']/@title").getall()
        movieIdList = response.xpath('//div[@class="movie-item"]/a/@href').getall()
        filmImgList= response.xpath('//div[@class="movie-poster"]/img[not(@class)]/@data-src').getall()
        for key,film in enumerate(filmNameList):
            item['film_name'] = film
            item['movieId'] = int(re.match(".*?(\d+).*", movieIdList[key]).group(1))
            item['film_img'] = filmImgList[key]
            yield item
        next = response.xpath('.').re_first(r'href="(.*?)">下一页</a>')
        if next:
            next_url = self.next_base_url + next
            yield scrapy.Request(next_url, meta={'item': item}, callback=self.parseDetail, cookies=self.getCityCookies(item['cid']))



    def getCityCookies(self,cid):
        cookies = {
            'ci':cid
        }
        return cookies

    def getCityByCid(self,cid):
        obj = SpidermanPipeline()
        return obj.getCityByCid(cid)


