# -*- coding: utf-8 -*-
import scrapy

class FilmsRankItem(scrapy.Item):
    title = scrapy.Field()  # 电影标题
    actors = scrapy.Field()  # 演员
    releasetime = scrapy.Field()  # 上映时间
    cover_img = scrapy.Field()  # 缩略图
    detail_page = scrapy.Field()  # 电影详情页url
    score = scrapy.Field()  # 电影评分

class FilmsNowItem(scrapy.Item):
    movieId = scrapy.Field()  # 电影ID
    cid = scrapy.Field()  # 城市ID
    film_name = scrapy.Field()  # 电影名称
    city_name = scrapy.Field()  # 城市名称
    film_img = scrapy.Field() #电影海报


class FilmsCityItem(scrapy.Item):
    city_name = scrapy.Field()
    cid = scrapy.Field()


class FilmsNowDetailItem(scrapy.Item):
    movieId = scrapy.Field()  # 电影ID
    cid = scrapy.Field()  # 城市ID
    poi = scrapy.Field() #影院ID
    poi_name = scrapy.Field() #电影院名称
    film_name = scrapy.Field()  # 电影名称
    city_name = scrapy.Field()  # 城市名称
    price = scrapy.Field() #价格
    show_place = scrapy.Field() #放映厅
    lang_type = scrapy.Field() #语言版本
    show_time = scrapy.Field() #放映时间
    odd = scrapy.Field() #剩余票数
    show_date = scrapy.Field() #放映日期
    poi_addr = scrapy.Field()#影院地址
    poi_tel = scrapy.Field()#影院电话
    film_type = scrapy.Field()#电影类型
    film_time = scrapy.Field()#电影时长
    film_actor = scrapy.Field()#电影演员
    film_score = scrapy.Field()#电影评分


