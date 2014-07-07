
#coding:utf-8
'''
'''

from picCrawler import Crawler
from urlFetcher import Fetch
from options import parser

def main():
    args = parser.parse_args()

    Fetcher =Fetch(args.url, args.threadNum, args.limit)
    Fetcher.start()

    PicCrawler = Crawler(args.threadNum, args.path, args.limit)
    PicCrawler.start()

if __name__ == '__main__':
    main()
