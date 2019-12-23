import scrapy
from ..items import FilmsCityItem
from scrapy import Request
import Crypto.PublicKey.RSA as RSA



#注意使用Crypto需要安装vs C++ 14 build tools

class DiamondSpider(scrapy.Spider):
    name = "diamond"
    allowed_domains = ['www.zzhgia.com']
    start_urls = ['http://www.zzhgia.com/']
    base_url = 'http://www.zzhgia.com/'
    load_url = 'http://www.zzhgia.com/login/pc/dologin_manager_specialty.xhtml'

    #登录系统的帐号密码
    load_info = {
        'username':'钻之恒',
        'password':'zzh2018',
        'www':'www.zzhgia.com'
    }

    #rsa公钥
    rsa_public_key = '9451cf74bef83e6d0192bc3d533177c3353613627e2ec4926355ca88e7b015a656257f9afaa0172a82e9bb01f4e9e3d096fdb82c7936cb72ffc63926bfbe64100b9f341046112b7cbea8e4e5ec74165172afe283fb4b122b23ad7b0a309cb6cce1edea220657c013b42197f2348965c028e22faa88c01d29989b9aa38e896c79'


    def start_requests(self):
        e = int('10001', 16)
        n = int(self.rsa_public_key, 16)  # snipped for brevity
        pubkey = RSA.construct((n, e))
        code = pubkey.encrypt(self.load_info['password'], None)
        print(code)
        exit()
        request = scrapy.FormRequest(self.load_url,formdata=self.load_info)

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