from urllib.parse import urlparse
from em3u8.sites import *
from loguru import logger
import random
import string



class Parse():
    '''
    解析网站类型，获取m3u8地址
    '''
    def __init__(self,url):
        self.__m3u8 = None
        self.__url:str = url
        self.__title = None
        self.__sites = {
            "www.yunbtv.net": YunBTV,
            
        }
        self.__parser = None
        self.err = None
        

    @property
    def title(self):
        try:
            if not self.__title:
                self.__title = self.parser.title
        except Exception as e:
            self.err = e
            self.__title = e
        return self.__title
    
    @property
    def parser(self):
        if not self.__parser:
            # parser_class = self.__sites.get(self.host,Site)
            parser_class = self.__get_parser_class(self.host)
            self.__parser = parser_class(self.__url)
        return self.__parser
    
    def __get_parser_class(self,host):
        '''
        根据host获取解析类
        '''
        for site in self.__sites:
            if site in host:
                return self.__sites[site]
        return Site

    @property
    def m3u8(self):
        try:
            if not self.__m3u8:
                if self.__url.endswith(".m3u8"):
                    self.__m3u8 = self.__url
                    self.__title = f"m3u8_{''.join(random.choices(string.ascii_letters+string.digits,k=10))}"
                else:
                    self.__m3u8 = self.parser.m3u8
                    self.err = self.parser.err
        except Exception as e:
            self.err = e
            self.__m3u8 = None
        
        return self.__m3u8

    @property
    def sites(self):
        return self.__sites

    def show_support(self):
        for url,name in self.__sites.items():
            print("当前版本支持以下站点:")
            print(f"{name.name}:\t\t{url}")

    @property
    def host(self):
        urlp = urlparse(self.__url)
        return urlp.netloc
            