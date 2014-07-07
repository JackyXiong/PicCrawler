#coding:utf-8
'''
参数解析
'''
import argparse

def url(urlstr):
    if not urlstr.startswith('http://'):
        newurl = 'http://' + urlstr
        print newurl
        return newurl

parser = argparse.ArgumentParser(description='Picture Crawler')

parser.add_argument('-u', type=str, required=True, dest='url', 
    metavar='URL',help='set your url')

parser.add_argument('-n', type=int, default=10, dest='threadNum',
    metavar='Thread Nun', help='set the thread number')

parser.add_argument('-o', type=str, default='pic', dest='path', 
    metavar='Path', help='set the path of picture')

parser.add_argument('-l', type=int, dest='limit',default=200, 
    metavar='Limit', help='''set the picture's limit''')

def main():
    args = parser.parse_args()
    print args

if __name__ == '__main__':
    main()
