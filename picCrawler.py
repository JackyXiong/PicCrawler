#coding:utf-8
'''
picCrawler.py
多线程图片爬取类
'''
import os
from collections import deque

from threadPool import ThreadPool
from picFile import PicFile

import requests

class Crawler(object):
	
	def __init__(self,threadnum,pathname,limit):
		'''limit指定图片数目，path指定存放路径'''
		super(Crawler, self).__init__()
		self.threadPool = ThreadPool(threadnum)
		self.file = PicFile('imgfile','r')
		self.urlqueue = deque()
		self.count = 1
		self._makePath(pathname)
		self.savaPath = os.getcwd()+'/'+pathname
		self._getUrl(limit)

	'''当前目录下创建指定目录'''
	def _makePath(self,pathname):
		if not os.path.isdir(os.getcwd()+'/'+pathname):
			os.mkdir(os.getcwd()+'/'+pathname)
		else:
			pass

	'''从文件取出 URL 到双向列表'''
	def _getUrl(self,num):
		while len(self.urlqueue) < num:
			self.urlqueue.append(self.file.getData().rstrip('\n'))
		self.file.close()
		
	def start(self):
		print '---start downloading picture---'
		self.threadPool.startThreads()
		while self.urlqueue!=deque([]):
			self.threadPool.putTask(self._handleTask,self.urlqueue.popleft())
		self.stop()

	def stop(self):
		self.threadPool.stopThreads()
		print '---end downloading picture---'

	'''任务处理'''
	def _handleTask(self,url):
		self._download(url)
	
	'''下载图片,以数字升序命名'''
	def _download(self,url):
		retry = 2 
		try:
			r = requests.get(url)
			with open(self.savaPath +'/'+str(self.count)+'.jpg','wb') as jpg:
				jpg.write(r.content)
				self.count+=1
			print url
		except Exception,e:
			if retry > 0:
				retry = retry - 1
				self._download(url)


if __name__ == '__main__':
	 c = Crawler()
	 c.start()

