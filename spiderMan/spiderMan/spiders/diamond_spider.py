import scrapy
import rsa
import binascii
from scrapy.http.cookies import CookieJar
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from scrapy_splash import SplashRequest
from scrapy.selector import Selector

class DiamondSpider(scrapy.Spider):
    name = "diamond"
    allowed_domains = ['www.zzhgia.com']
    start_urls = ['http://www.zzhgia.com/']
    base_url = 'http://www.zzhgia.com/'

    #登录页面的url
    login_index = 'http://www.zzhgia.com/newManager/index.html'
    #登录的URL
    login_url = 'http://www.zzhgia.com/login/pc/dologin_manager_specialty.xhtml'


    #登录系统的帐号密码
    load_info = {
        'username':'钻之恒',
        'password':'zzh2018',
        'www':'www.zzhgia.com'
    }

    #rsa
    #模数和指数
    modulus = '9451cf74bef83e6d0192bc3d533177c3353613627e2ec4926355ca88e7b015a656257f9afaa0172a82e9bb01f4e9e3d096fdb82c7936cb72ffc63926bfbe64100b9f341046112b7cbea8e4e5ec74165172afe283fb4b122b23ad7b0a309cb6cce1edea220657c013b42197f2348965c028e22faa88c01d29989b9aa38e896c79'
    exponent = '10001'

    def start_requests(self):
        #初始化登录页面
        #return [scrapy.Request(self.login_index,callback=self.after_login_index,meta=self.load_info)]
        # modulus = int(self.modulus,16)
        # exponent = int(self.exponent,16)
        # public_key = rsa.PublicKey(modulus,exponent)
        # password_rsa_code = binascii.b2a_hex(rsa.encrypt(self.load_info['password'].encode(),public_key))#加密信息转换成16进制
        # self.load_info['password'] = password_rsa_code
        # return [scrapy.FormRequest(self.login_url,formdata=self.load_info,callback=self.after_login)]
        yield SplashRequest(self.login_index
                                , self.after_login_index
                                , args={'wait': '2'}
                                ,endpoint='execute'
                                )

    def after_login_index(self,response):
        print(response.html())
        pass

    def after_login(self,response):
        #print(response.session)
        print(response)
        exit()
        #scrapy.Request(self.url_somebody, dont_filter=True, meta={'proxy': 'http://127.0.0.1:8888'})
        pass

    def parse(self, response):
        pass
        # item = FilmsCityItem()
        # if response:
        #     citysDomName = response.xpath('//a[@class="js-city-name"]/text()').getall()
        #     citysDomId = response.xpath('//a/@data-ci').getall()
        #     citysMap = dict(zip(citysDomId,citysDomName))
        #     for cityId,cityName in citysMap.items():
        #         item['city_name'] = cityName
        #         item['cid'] = cityId
        #         yield item
