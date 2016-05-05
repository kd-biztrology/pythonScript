from multiprocessing import Pool
import requests
import bs4
import time
import json
'''
抓取 one 一个首页的脚本
'''

root_url = 'http://wufazhuce.com'


def get_url(num):
    return root_url + '/one/' + str(num)


def get_urls(num):
    urls = map(get_url, range(100, 100 + num))## main 里面的参数更改了以后这里许要对应的更改
    return urls


def get_data(url):
    dataList = {}
    response = requests.get(url)
    if response.status_code != 200:
        return {'noValue': 'noValue'}
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    dataList["index"] = soup.title.string[4:7]
    for meta in soup.select('meta'):
        if meta.get('name') == 'description':
            dataList["content"] = meta.get('content')
    dataList["imgUrl"] = soup.find_all('img')[1]['src']
    return dataList


if __name__ == '__main__':
    pool = Pool(4)
    dataList = []
    urls = get_urls(10)## 10 这个参数可以更改
    start = time.time()
    dataList = pool.map(get_data, urls)
    end = time.time()

    jsonData = json.dumps({'data': dataList})
    print(dataList)
