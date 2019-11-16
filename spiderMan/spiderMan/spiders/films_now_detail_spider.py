import scrapy
import re
from ..items import FilmsNowDetailItem
from scrapy import Request

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
            for movie in movies:
                print(movie)
                exit()
                item['movieId'] = movie.css('p.name a::text').extract_first()
                item['poi'] = movie.css('p.star::text').extract_first().strip()
                item['cid'] = movie.css('p.releasetime::text').extract_first().strip()
                item['poi_name'] = movie.css('i.integer::text').extract_first() + movie.css(
                    'i.fraction::text').extract_first()
                item['film_name'] = self.base_url + movie.css('p.name a::attr(href)').extract_first()
                item['city_name'] = movie.css('a.image-link img.board-img::attr(data-src)').extract_first()  # 注意：需要根据网页源码写css选择器，和审查元素中的不同，估计是受JS影响
                yield item
            # 处理下一页
            next = response.xpath('.').re_first(r'href="(.*?)">下一页</a>')
            if next:
                next_url = self.next_base_url + next
                yield Request(url=next_url, callback=self.parse, dont_filter=True)


    #detail的回调
    def praseDetail(self,response):
        print(response)
        exit()
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