import requests
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor,wait,ALL_COMPLETED
from tqdm import tqdm
import os
from loguru import logger
import tempfile
import random
import string


class MClient():
    '''
    多线程/进程下载客户端
    '''
    def __init__(self,url_list=[]):
        self.url_list = url_list

    def __download_file(self,url,save_path,timeout=10) -> None:
        """
        下载ts文件
        :param url: ts文件的URL
        :param save_path: 保存的路径
        """
        # 发送stream请求
        response = requests.get(url, stream=True,verify=False,timeout=timeout)
        
        response.raise_for_status()
        # 获取文件大小
        total_size = int(response.headers.get("Content-Length", 0))    
        # 显示下载进度
       
        progress = tqdm(response.iter_content(1024), f"Downloading {os.path.basename(save_path)}", total=total_size, unit="B", unit_scale=True, unit_divisor=1024)
       
       
        try:
            with open(save_path, "wb") as f:
                for data in progress.iterable:
                    # 写入文件
                    f.write(data)
                    # 更新进度条
                    progress.update(len(data))
        except requests.exceptions.RequestException:
            raise Exception(f"Download {save_path} failed")

    def _confirm_download_file(self,url,base_dir=".",timeout=10,retry_count=3):
        '''
        拥有尝试机制,下载文件
        '''
        c = 0
        save_path = f"{base_dir}/{os.path.basename(url)}"
        while c < retry_count:
            c += 1
            try:
                self.__download_file(url,save_path,timeout)
                break
            except Exception as e:
                logger.error(f"retry [{c}]...{url}\n{e}")

    def __init_output(self,save_path):
        '''
        初始化视频输出目录，
        没指定位置，默认同级out目录default_*****
        '''
        if not save_path:
            save_path = f"default_{''.join(random.choices(string.ascii_letters,k=5))}.mp4"
        out_dir = os.path.dirname(save_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
        return save_path

    def __download_ts(self,url,pbar,ts_save_path,retry=3):
        '''
        ts 文件下载
        '''
        c = 0
        while c < retry:
            c += 1
            try:
                with open(ts_save_path,"wb") as f:
                    f.write(requests.get(url,verify=False,timeout=20).content)
                    pbar.update()
                break
            except Exception as e:
                logger.error(f"retry [{c}]...{url}\n{e}")

    
    def download_vedio_info(self,save_path=None,workers=1,thread=True):
        '''
        单进度条显示视频下载进度
        '''
        with tempfile.TemporaryDirectory() as ts_temp_dir:
            save_path = self.__init_output(save_path)
            logger.debug(f"临时文件夹: {ts_temp_dir}")
            #多线程或进程下载，属性进度条
            total = len(self.url_list)
            with tqdm(desc=f"Downloading {os.path.basename(save_path)}", total=total, unit="个", unit_scale=True) as pbar:
                if thread:
                    executor = ThreadPoolExecutor(max_workers=workers)
                else:
                    executor = ProcessPoolExecutor(max_workers=workers)
                tasks = {executor.submit(self.__download_ts,url,pbar,f"{ts_temp_dir}/{os.path.basename(url)}"):f"{ts_temp_dir}/{os.path.basename(url)}" for url in self.url_list}
                wait(tasks,return_when=ALL_COMPLETED)
                logger.debug(f"ts 文件下载完成")
            # 合并ts文件
            
            with open(save_path,"wb+") as ww:
                for ts in tasks.values():
                    if os.path.exists(ts):
                        with open(ts,"rb") as rr:
                            ww.write(rr.read())
            logger.success(f"{save_path} 下载完成")
            return save_path

    def download_vedio(self,save_path=None,workers=1,thread=True,debug=False):
        if debug:
            return self.download_vedio_debug(save_path,workers,thread)
        else:
            return self.download_vedio_info(save_path,workers,thread)


    def download_vedio_debug(self,save_path=None,workers=1,thread=True):
        '''
        下载视频文件
        save_path: 保存路径
        workers: 任务数目
        thread: True,False采用进程模式
        '''
    
        with tempfile.TemporaryDirectory() as ts_temp_dir:
            logger.debug(f"临时文件夹: {ts_temp_dir}")
            save_path = self.__init_output(save_path)
        
            #多线程下载
            if thread:
                executors = ThreadPoolExecutor(max_workers=workers)
            else:
                executors = ProcessPoolExecutor(max_workers=workers)
            logger.info(f"开始下载，共 ({len(self.url_list)}) 文件")
            tasks = {executors.submit(self._confirm_download_file,file_url,ts_temp_dir):os.path.basename(file_url) for file_url in self.url_list}
            wait(tasks,return_when=ALL_COMPLETED)
            logger.debug("下载完成,开始合并")
            #合并ts文件
            with open(save_path,"wb+") as ww:
                for ts in tasks.values():
                    if os.path.exists(f"{ts_temp_dir}/{ts}"):
                        with open(f"{ts_temp_dir}/{ts}","rb") as rr:
                            ww.write(rr.read())
            logger.success(f"Download {os.path.abspath(save_path)} success")
            return save_path
            