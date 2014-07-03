#coding:utf-8
'''
DownloadWebpage.py
下载网页源代码

'''
import requests

class DownloadWeb(object):

	def __init__(self, url):
		super(DownloadWeb, self).__init__()
		self.url = url
		self.sourcecode = None

	#下载 HTML 源码
	def download(self):
		response = requests.get(self.url)
		if self.is_Response_right(response):
			self.sourcecode = response.content
			return True
		else:
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
