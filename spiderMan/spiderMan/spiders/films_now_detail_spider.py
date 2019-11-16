import scrapy
import re
import json
from ..items import FilmsNowDetailItem
from scrapy import Request
from ..pipelines import SpidermanPipeline

#正在热映
class FilmsNowDetailSpider(scrapy.Spider):
    name = "films_now_detail"

    allowed_domains = ['maoyan.com']


    # 每部电影详情页的基本前缀url
    base_url = 'https://maoyan.com'

    # 下一页前缀url
    next_base_url = 'https://maoyan.com/cinemas'


    # 城市ID
    cid = None

    def __init__(self, cid=None, *args, **kwargs):
        super(FilmsNowDetailSpider, self).__init__(*args, **kwargs)
        self.cid = cid

    def start_requests(self):
        url = self.next_base_url+"?offset=0"
        yield scrapy.Request(url=url, callback=self.praseBase, dont_filter=True,cookies=self.getCookies(),meta={'cid':self.cid})

    def praseBase(self, response):
        item = FilmsNowDetailItem()
        if response:
            movies = response.css('div.cinemas-list')
            cityInfo = self.getCityByCid(self.cid)
            item['cid'] = int(cityInfo[0])
            item['city_name'] = cityInfo[1]
            for movie in movies:
                #filmNameList = response.xpath("//div[@class='channel-detail movie-item-title']/@title").getall()
                item['poi_name'] = movie.css('div.cinema-info a::text').extract_first()
                item['poi_addr'] = movie.css('div.cinema-info p.cinema-address::text').extract_first()
                jsonStr = movie.css('div.cinema-info a::attr(data-val)').extract_first()
                item['poi'] = re.match(".*?cinema_id: (\d+)", jsonStr).group(1)
                url = self.base_url + movie.css('div.buy-btn a::attr(href)').extract_first()
                yield scrapy.Request(url=url, callback=self.praseCiname, dont_filter=True, cookies=self.getCookies(),
                                     meta={'item': item})
                #yield item
            # 处理下一页
            next = response.xpath('.').re_first(r'href="(.*?)">下一页</a>')
            if next:
                next_url = self.next_base_url + next
                yield Request(url=next_url, callback=self.praseBase, dont_filter=True)


    #detail的回调
    def praseCiname(self,response):
        # filename = 'test.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        # exit()
        item = response.meta['item']
        if response:
            item['poi_tel'] = response.css('div.telphone::text').extract_first()
            item['poi_addr'] =response.css('div.address::text').extract_first()
            movieList = response.css("div.show-list")
            for movie in movieList:
                item['film_name'] = movie.xpath('//div[1]/div[1]/h3/text()').extract_first()
                item['film_score'] = movie.xpath('//div[1]/div[1]/span/text()').extract_first()
                item['film_time'] = movie.xpath('//div[1]/span[2]/text()').extract_first()
                item['film_type'] = movie.xpath('//div[2]/span[2]/text()').extract_first()
                item['film_actor'] = movie.xpath('//div[3]/span[2]/text()').extract_first()
                dateList = movie.xpath('//div[@class="show-date"]')
                for date in dateList:
                    index = date.xpath('//span[@class="date-item"]/*').extract_first()
                    print(index)
                exit()
                dateIndex = movie.xpath('//div[2]/div[2]/span[2]/@data-index').extract_first()

        exit()
        pass

    def parseCinameSite(self, response):
        pass

    #这里cookie需要枚举，先写死
    def getCookies(self):
        cookies = {
            'ci':self.cid
        }
        return cookies

    #拿到所有filmID
    def getFilmIdList(self,response):
        filmIdList = []
        if response:
            tmpList = response.css('dl.movie-list dd').xpath('div[@class="movie-item"]/a/@href').getall()
            for node in tmpList:
                filmIdList.append(re.match(".*?(\d+).*", node).group(1))
        return filmIdList


    #拿到所有的电影明细
    def getFilmDetail(self,filmId):
        #组装参数
        movieDetailUrl = self.movive_detail_url+str(filmId)
        yield from Request(url=movieDetailUrl, callback=self.praseDetail, dont_filter=True,cookies=self.getCookies())
        pass

    def getCityByCid(self, cid):
        obj = SpidermanPipeline()
        return obj.getCityByCid(cid)