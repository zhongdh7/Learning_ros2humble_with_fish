import threading
import requests
import time

class Download:
    def download(self,url,callback_word_count):
        print(f"线程:{threading.get_ident()},开始下载:{url}")
        response=requests.get(url)
        response.encoding='utf-8'
        callback_word_count(url,response.text)

    def start_download(self,url,callback_word_count):
        # self.download(url,callback_word_count)
        thread=threading.Thread(target=self.download,args=[url,callback_word_count])
        thread.start()


def word_count(url,result):
    """
    普通函数，用于回调
    """
    print(f"{url}:{len(result)}->{result[:5]}")
    # time.sleep(2.0)


def main():
    download=Download()
    # begin=time.time()
    download.start_download('http://0.0.0.0:8000/novel1.txt',word_count)
    download.start_download('http://0.0.0.0:8000/novel2.txt',word_count)
    download.start_download('http://0.0.0.0:8000/novel3.txt',word_count)
    end=time.time()
    # print(f"总共用时{end-begin}")
    