from em3u8.sites import Site
import requests
from bs4 import BeautifulSoup
import re
from loguru import logger



class YunBTV(Site):
    '''
    云播
    '''
    name = "云播TV"

    @property
    def m3u8(self):
        if not self.text:
            self.text = requests.get(self.url,verify=False,timeout=20).text
        soup = BeautifulSoup(self.text,"html.parser")
        scripts = soup.find_all("script")
        #js中获取m3u8路径
        for script in scripts:
            if script.get("type") == "text/javascript":
                
                pattern = re.compile(r'"url":"([^"]+)"')
                r = pattern.findall(str(script))
                
                if r:
                    return [r[0].replace("\\","")]
        self.err = "not found m3u8 addr"
        return None

    @property
    def title(self):
        if not self._title:
            if not self.text:
                self.text = requests.get(self.url,verify=False,timeout=20).text
            soup = BeautifulSoup(self.text,"html.parser")
            self._title = "-".join(soup.title.string.split("_")[0:2])
        return self._title
