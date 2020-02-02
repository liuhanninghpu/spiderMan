# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

#需要动态加载的爬虫
#主要做两件事，什么爬虫下的哪个链接需要做什么事情以及做事情需要的参数
dynamicSpiderMap = {
    'films_citys':[],
    # 'diamond':[
    #     {
    #       'url':'http://www.zzhgia.com/newManager/index.html',
    #       'action':'login',
    #       'params':['username','password','www'],
    #       'formIds':{
    #           'username':'loginName',
    #           'password':'loginPass',
    #           'loginButton':'login_btn'
    #       },
    #       'sessionStorage':'oUid'
    #     }
    # ] #这个需要拿到sessionStorage
}

#浏览器驱动
webdriverFileConf = {
    'chrome':'D:\source\scrapy\chromedriver.exe',
    'firefox':''
}

class SpidermanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpidermanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        self._get_web_driver('chrome')
        if spider.name in dynamicSpiderMap:
            for spiderConf in dynamicSpiderMap[spider.name]:
                if spiderConf['url'] == request.url:
                    self.driver.get(request.url)
                    # 显性等待，直到用户名控件加载出来才进行下一步
                    #WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located((By.ID, "loginName")))
                    #是否有其他操作
                    # if request.meta is not None:
                    #     meta = self._do_action(spiderConf,request)
                    html = self.driver.page_source.encode('utf-8')
                    # filename = 'test.html'
                    # with open(filename, 'wb') as f:
                    #     f.write(html)
                    # exit()
                    self.driver.quit()
                    return scrapy.http.HtmlResponse(url=request.url, body=html, encoding='utf-8',
                                                    request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    #获取浏览器模式
    def _get_web_driver(self,type):
        web_driver_options = Options()
        web_driver_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        web_driver_options.add_argument('--disable-gpu')
        web_driver_options.add_argument('--no-sandbox')
        # 指定浏览器路径
        self.driver = webdriver.Chrome(chrome_options=web_driver_options,
                                       executable_path=webdriverFileConf[type])

    #做操作
    def _do_action(self,conf,request):
        request_url,request_meta = request.url,request.meta
        conf_url,conf_action,conf_params,conf_form_ids,conf_session_storage = conf['url'],conf['action'],conf['params'],conf['formIds'],conf['sessionStorage']
        if request_url != conf_url:
            return None
        if conf_action is None:
            return None
        if conf_action == 'login':
            #做模拟登录操作
            # 填写用户名
            self.driver.find_element_by_id("loginName").send_keys('钻之恒')
            self.driver.find_element_by_id("loginPass").send_keys('zzh2018')
            exit()
            for key in conf_form_ids:
                if key in request_meta:
                    self.driver.find_element_by_id('"'+conf_form_ids[key]+'"').send_keys(request_meta[key])
            # 点击登录
            self.driver.find_element_by_id('"'+conf_form_ids['loginButton']+'"').click()
            time.sleep(5)
            #获取sessionStorage
            if conf_session_storage is not None:
                session_storage_result = dict()
                for session_storage_key in conf_session_storage:
                    script_str = 'return sessionStorage.getItem("{0}");'.format(session_storage_key)
                    session_storage_result[session_storage_key] = self.driver.execute_script(script_str)
                    print(session_storage_result)
                    exit()
        else:
            #后续有新的再加上
            pass


