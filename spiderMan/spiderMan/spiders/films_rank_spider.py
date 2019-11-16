import scrapy
from ..items import FilmsRankItem
from scrapy import Request

class FilmsRankSpider(scrapy.Spider):
    name = "films_rank"

    allowed_domains = ['maoyan.com/board/4?offset=']
    start_urls = ['https://maoyan.com/board/4?offset=']

    # 每部电影详情页的基本前缀url
    base_url = 'https://maoyan.com'

    # 下一页前缀url
    next_base_url = 'https://maoyan.com/board/4'

    # def start_requests(self):
    #     #循环10次
    #     for times in range(0,11):
    #         url = self.next_base_url+"?offset="+str(times)
    #         yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = FilmsRankItem()
        if response:
            movies = response.css('dl.board-wrapper dd')
            for movie in movies:
                item['title'] = movie.css('p.name a::text').extract_first()
                item['actors'] = movie.css('p.star::text').extract_first().strip()
                item['releasetime'] = movie.css('p.releasetime::text').extract_first().strip()
                item['score'] = movie.css('i.integer::text').extract_first() + movie.css(
                    'i.fraction::text').extract_first()
                item['detail_page'] = self.base_url + movie.css('p.name a::attr(href)').extract_first()
                item['cover_img'] = movie.css('a.image-link img.board-img::attr(data-src)').extract_first()  # 注意：需要根据网页源码写css选择器，和审查元素中的不同，估计是受JS影响
                yield item
            # 处理下一页
            next = response.xpath('.').re_first(r'href="(.*?)">下一页</a>')
            if next:
                next_url = self.next_base_url + next
                yield Request(url=next_url, callback=self.parse, dont_filter=True)