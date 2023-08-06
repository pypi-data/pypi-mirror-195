import re
import requests
from loguru import logger
from urllib.parse import urlparse
from em3u8 import MClient
from Crypto.Cipher import AES
import os



class EM3U8:
    '''
    m3u8 类模块
    基于url或内容创建
    '''


    def __init__(self,content:str = None,url:str = None,timeout=10) -> None:
        self._content = content
        self.url = url
        self.timeout = timeout
        self._tss = []
        self._key = {}

    @property
    def key(self):
        if not self._key:
            key_pattern = re.compile(r'#EXT-X-KEY:([^\n]+)\n')
            if not self._content:
                self._content = self._get_content_from_url()
            keys = key_pattern.findall(self._content)
            if keys:
                self._key = dict(re.findall(r'([^=,]+)=([^,]+)', keys[0]))
            else:
                self._key = {}
        return self._key

    @property
    def content(self):
        if not self._content:
            pass

    @property
    def tss(self):
        '''
        content中获取ts列表
        '''
        if self._tss:
            return self._tss
        if not self._content:
            if not self.url:
                self._tss = []
            else:
                self._content = self._get_content_from_url()
        self._tss = self._get_ts_list_from_content()
        return self._tss
        

    def _get_ts_list_from_content(self):
        '''
        正则获取ts列表
        '''
        if not self._content:
            return []
        ts_pattern = re.compile(r'#EXTINF:[0-9.]+,\n([^\n]+)\n')
        data = ts_pattern.findall(self._content)
        return [self._get_absolute_url(ts_url) for ts_url in data]
            
    def _get_content_from_url(self):
        '''
        从url中获取content,解决302,sub等问题
        '''
        
        url = self.url
        while True:
            logger.debug(f"请求 {url}")
            res = requests.get(url,verify=False,timeout=self.timeout)
            if res.status_code == 302:
                url = res.headers["location"]
                
                logger.debug(f"302 -> {url}")
                continue
            elif res.status_code == 200:
                result,data = self._valid_ts_data(res.text)
                if len(res.text) > 400:
                    logger.debug(res.text[:200] + "\n...\n" + res.text[-200:])
                else:
                    logger.debug(res.text)
                if result:
                    
                    break
                else:
                    url = data
                   
                    logger.debug(f"sub - > {data}")
            else:
                logger.error(f"status code: {res.status_code}")
                logger.error(res.text)
                break
        self.url = url
        self._content = res.text       
        return res.text

    def _valid_ts_data(self,data:str):
        '''
        检测是否是最终m3u8文件
        '''
        if "#EXTINF" in data:
            return True,None
        else:
            for line in data.split("\n"):
                if not line.startswith("#"):
                    new_url = line
                    break
            return False,self._get_baseurl(new_url) + new_url

    def _get_baseurl(self,ts_url):
        '''
        获取baseurl
        '''
        
        if not self.url or ts_url.startswith("http"):
            return ""
        elif ts_url.startswith("/"):
            urlp = urlparse(self.url)
            return urlp.scheme + "://" + urlp.netloc
        else:
            return self.url[0:self.url.rfind("/")+1]
    
    def _get_absolute_url(self,url:str):
        '''
        获取绝对url
        '''
        url = url.replace('"','')
        return self._get_baseurl(url) + url

    def download_vedio(self,save_path=None,workers=1,thread=True,debug=False):
        '''
        下载视频
        '''
        # save_path = MClient(self.tss).download_vedio(save_path,workers,thread)
        save_path = MClient(self.tss).download_vedio(save_path,workers,thread,debug=debug)
        if self.key.get("URI",None):
            logger.debug(f"视频加密，开始解密")
            if os.path.dirname(save_path):
                self.dencrypt(save_path,f"{os.path.dirname(save_path)}/解密-{os.path.basename(save_path)}")
            else:
                self.dencrypt(save_path,f"解密-{save_path}")

    def dencrypt(self,src,dst,key=None,iv=b"\x00"*16):
        '''
        解密
        '''
        if not key:
            key = self.key.get("URI",None)
            key = self._get_absolute_url(key)
        
        if self.key.get("IV",None):
            iv = self.key.get("IV",None)

        
        logger.debug(f"dencrypt: {src} -> {dst}")
        logger.debug(f"dencrypt: key_url -> {key}")
        key = requests.get(key,verify=False).content
        logger.debug(f"dencrypt: key -> {key}-{len(key)},iv:[{iv}]")
        cipher = AES.new(key,AES.MODE_CBC,iv)
        with open(src,"rb") as rr:
            with open(dst,"wb") as ww:
                ww.write(cipher.decrypt(rr.read()))
        logger.debug("dencrypt done")
        
        
