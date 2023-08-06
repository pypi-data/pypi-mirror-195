from bs4 import BeautifulSoup
import requests
import re



class Site():
    name = "SITE"
    
    def __init__(self,url):
        self.url = url
        self.text = None
        self._title = None
        self.err = None
        
        
    @property
    def m3u8(self):
        # 视频资源通用查找
        data = []
        if not self.text:
            self.text = requests.get(self.url,verify=False,timeout=20).text
        soup = BeautifulSoup(self.text,"html.parser")
        scripts = soup.find_all("script")
        #js中获取m3u8路径
        for script in scripts:           
            pattern = re.compile(r"http([^\",\']+)m3u8")
            r = pattern.findall(str(script))            
            if r:
                # data.append(("http"+ r[0] + "m3u8").replace("\\",""))
                data.extend(r)
        #if get m3u8 returned or give err reason
        if data:
            return [("http" + m3u8 + "m3u8").replace("\\","") for m3u8 in data]
        else:
            self.err = "Site: not found m3u8 addr"
            return None

    @property
    def title(self):
        if not self._title:
            if not self.text:
                self.text = requests.get(self.url,verify=False,timeout=20).text
            soup = BeautifulSoup(self.text,"html.parser")
            self._title = soup.title.string
        return self._title
