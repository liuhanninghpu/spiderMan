# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import time

mysqlConf = {
    'host':'localhost',
    'user':'root',
    'password':'123456789',
    'db':'spider',
    'port':3306
}


spiderNameListMap = {
    'films_now_rank':'saveFilmsRank',
    'films_citys':'saveFilmsCity',
    'films_now':'saveFilmsNow',
    'films_now_detail':'saveFilmsNowDetail'
}



class SpidermanPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',user='root',password='123456789',db='spider',port=3306)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        #中央路由
        if spider.name in spiderNameListMap:
            getattr(SpidermanPipeline,spiderNameListMap[spider.name])(self,item)
        else:
            print('error')
        #return item


    def saveFilmsRank(self,item):
        update_time = self.getDateTime("%Y--%m--%d %H:%M:%S")
        self.cursor.execute(
            'insert into films_rank(title,actors,releasetime,score,cover_img,detail_page,update_time)VALUES ("{}","{}","{}","{}","{}","{}","{}")'.format(
                item['title'], item['actors'], item['releasetime'], item['score'], item['cover_img'],
                item['detail_page'], update_time))
        self.connect.commit()

    def saveFilmsNow(self,item):
        update_time = self.getDateTime("%Y--%m--%d %H:%M:%S")
        self.cursor.execute(
            'insert into films_now(movieId,cid,film_name,city_name,film_img,update_time)VALUES ("{}","{}","{}","{}","{}","{}") ON DUPLICATE KEY UPDATE film_name= "{}",city_name= "{}",film_img = "{}",update_time = "{}"'.format(
                item['movieId'], item['cid'], item['film_name'],
                item['city_name'],item['film_img'],update_time,item['film_name'],item['city_name'],item['film_img'],update_time))
        self.connect.commit()

    def saveFilmsCity(self,item):
        update_time = self.getDateTime("%Y--%m--%d %H:%M:%S")
        self.cursor.execute(
            'insert into films_city(cid,city_name,update_time)VALUES ("{}","{}","{}") ON DUPLICATE KEY UPDATE city_name= "{}",update_time = "{}"'.format(
                item['cid'], item['city_name'],update_time,item['city_name'],update_time))
        self.connect.commit()


    def getCidMap(self):
        sql = "select cid,city_name from films_city where 1=1 limit 1"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        cityList = {}
        for citys in result:
            cityList[citys[0]] = citys[1]
        return cityList

    def getCityByCid(self,cid):
        sql = 'select cid,city_name from films_city where cid="{}"'.format(cid)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def getDateTime(self,formate):
        return  time.strftime(formate, time.localtime(time.time()))


    def __del__(self):
        self.cursor.close()
        self.connect.close()