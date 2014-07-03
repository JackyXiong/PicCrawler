#coding:utf-8
'''
urlFetcher.py
多线程下载网页并解析所有可用图片链接，存储到文件
'''
import logging ,re, time
from urlparse import urljoin
from collections import deque

from DownloadWebpage import DownloadWeb
from Database import Database
from threadPool import ThreadPool
from picFile import PicFile

from bs4 import BeautifulSoup

class Fetch(object):

	def __init__(self,url,threadnum,limit):
		#self.database = Database('pichref.sql')
		self.file = PicFile('imgfile','a')
		self.threadPool = ThreadPool(threadnum)
		self.unaccesshref = deque()#双向列表
		self.accessedhref = set()#已访问的链接集合
		self.unaccesshref.append(url)#添加初始链接
		self.limit = limit
		self.picUrlCount = 1


	def start(self):
		print '--start downloading url--'
		self.threadPool.startThreads()
		while self.unaccesshref!=deque([]):#不为空 一直分配任务
				self._organise()

		self.stop()

	def stop(self):
		self.threadPool.stopThreads()
		self.file.close()
		print '--Stop downloading url--'

	#往线程池分配任务
	def _organise(self):
		while self.unaccesshref:
			url = self.unaccesshref.popleft()#从双向队列左取URL
			self.threadPool.putTask(self._handle_task,url)#分配任务
			self.accessedhref.add(url)#添加到已处理
			time.sleep(2)#中断操作，让unaccesshref可以及时得到数据


	#处理任务
	def _handle_task(self,url):
		webpage = DownloadWeb(url)
		if webpage.download():
			self._addUrlToUnaccesshref(webpage)

	#添加普通链接到未访问链接列表
	def _addUrlToUnaccesshref(self,webpage):
		url, webpagecontent = webpage.getdata()
		hrefs = self._getLinkFromPage(url,webpagecontent)

		for href in hrefs:
			if not self._isUsedhref(href):
				self.unaccesshref.append(href)

	
	#解析源码，获取普通链接和图片链接，将正确的图片链接存储到文件
	def _getLinkFromPage(self,url,source_code):
		pic_links, hrefs = [], []
		soup = BeautifulSoup(source_code)
		href_res = soup.find_all('a',href=True)#获取普通链接
		pic_link_res = soup.find_all(src=re.compile('http://.*?\.jpg'))#获取图片链接
		for h in href_res:
			href = h.get('href').encode('utf-8')
			if not href.startswith('http') and href!='/' and href!='#' and href.find(';')==-1:
				href = urljoin(url, href)
				hrefs.append(href)

		for pic_link in pic_link_res:
			pic_link = pic_link.get('src').encode('utf-8')
			self.file.saveData(pic_link)#图片链接存储到文件
			
			self.picUrlCount+=1
			if self.picUrlCount >= self.limit:
				##由于线程池是当self.unaccesshref为空时才结束，当链接数满足要求，结束线程池的工作
				self.unaccesshref=deque()
				return []#
		return hrefs

	'''判断是否是已经获取的 url'''
	def _isUsedhref(self,href):
		if href in self.accessedhref or href in self.unaccesshref:
			return True
		else:
			return False

'''
def main():
	f=Fetch('http://www.22mm.cc/')
	f.start()
'''
if __name__ == '__main__':
	main()
