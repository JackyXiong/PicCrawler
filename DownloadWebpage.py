#coding:utf-8
'''
DownloadWebpage.py
下载网页源代码

'''
import logging

import requests

logger = logging.getLogger('Main_DownloadWeb')


class DownloadWeb(object):

    def __init__(self, url):
        super(DownloadWeb, self).__init__()
        self.url = url
        self.sourcecode = None

    #下载 HTML 源码
    def download(self):
        response = requests.get(self.url)
        if self.is_Response_right(response):
            '''response.content正常输出，response.text#输出到控制台错误'''
            self.sourcecode = response.content
        #    print self.sourcecode
            return True
        else:
            logger.error('Webpage not right,Status code:%d URL:%s' 
                %(response.status_code, self.url)) 
            return False

    def getdata(self):
        return self.url, self.sourcecode

    def is_Response_right(self,response):
        if response.status_code == requests.codes.ok:
            return True
        else:
            return False


if __name__ == '__main__':
    url = 'http://www.22mm.cc/'
    d = DownloadWeb(url)
    d.download()
    print d.getdata()
