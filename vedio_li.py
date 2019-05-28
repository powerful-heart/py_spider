import requests
import re
from concurrent.futures import ThreadPoolExecutor
import os

def pear_spider(category):
    data_list = []
    url = "https://www.pearvideo.com/category_%s" % category
    resp = requests.get(url)
    if resp.status_code == 200:
        # print(resp.text)

        # 解析视频
        res = re.findall('<a href="(video_\d+)" ', resp.text)
        # print(res)
        base_url = "https://www.pearvideo.com/"
        for i in res:
            detail_url = base_url + i
            detail_resp = requests.get(detail_url)
            print('页面链接:', detail_url)
            # print(detail_resp.text)
            # 标题
            title = re.search('<h1 class="video-tt">(.*?)</h1>', detail_resp.text).group(1)
            print('标题:', title)
            # 时间
            date = re.search('<div class="date">(.*?)</div>', detail_resp.text).group(1)
            print('发布时间:', date)
            # 作者
            author = re.search('</i>(.*?)</div>', detail_resp.text).group(1)
            print('作者:', author)
            # 点赞数
            up_count = re.search('<div class="fav" data-id="\d+">(\d+)</div>', detail_resp.text).group(1)
            print('点赞数:', up_count)
            # 详情
            content = re.search('data-summary="(.*?)" ', detail_resp.text).group(1)
            print('详情:', content)
            # 视频地址
            video_url = re.search('srcUrl="(.*?)"', detail_resp.text).group(1)
            print('视频链接:', video_url)
            print('-------------------------------------------')
            pool.submit(down_load, video_url, title)
    return data_list


def down_load(video_url, title):
    resp = requests.get(video_url)
    data = resp.content
    path = os.path.dirname(__file__)
    file_path = os.path.join(path, title+'.mp4')
    with open(file_path, 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    pool = ThreadPoolExecutor(6)
    pear_spider(9)

