#coding:utf-8
'''
存取 URL 链接的文件操作
'''

class PicFile(object):
    '''way 表示读取模式，a or r'''
    def __init__(self, filename,way):
        super(PicFile, self).__init__()
        global fileHandle
        fileHandle = open(filename+'.txt',way)
#        print '打开'

    '''对每一个 URL 进行存储'''
    def saveData(self,url):
        fileHandle.write(url+'\n')

    '''取出每一个 URL'''
    def getData(self):
        return fileHandle.readline()

    def close(self):
        fileHandle.close()
