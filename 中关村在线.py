import requests
from bs4 import BeautifulSoup
import json
import os
from concurrent.futures import ThreadPoolExecutor

"""
爬取中关村评测数据
    包括:
    标题 详情 图片(可能是多个) 详情连接 发布时间 浏览量
    生成json文件
"""

# url = "http://labs.zol.com.cn/"
# url2 = "http://labs.zol.com.cn/router.php?c=TestChannel_Default&a=GetChannelNew&module=new&page=2"
current_dir = os.path.dirname(__file__)
pool = ThreadPoolExecutor(5)


def parser(num):
    url = "http://labs.zol.com.cn/"
    resp = requests.get(url,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
                        })

    soup = BeautifulSoup(resp.text, 'lxml')

    # print(soup.find_all("li", attrs={"class": "content-list-item"}))
    news_list = soup.find_all("li", attrs={"class": "content-list-item"})
    # print(news_list)
    for news in news_list:

        news = str(news)
        # print(news)
        new_soup = BeautifulSoup(news, 'lxml')
        # 标题
        title = new_soup.li.div.div.a.text
        print(title)
        # 链接
        src = new_soup.li.a.attrs.get('href')
        print(src)
        # 图片列表
        picture_list = new_soup.li.find_all("img")
        picture_container = []
        for picture in picture_list:
            picture_soup = BeautifulSoup(str(picture), 'lxml')
            picture = picture_soup.img.attrs.get("src")
            picture_container.append(picture)
            print(picture_container)
        # 详情
        content = new_soup.li.div.p.text
        print(content)
        # 发布时间
        publish_time = new_soup.li.div.span.text
        print(publish_time)
        news_detail = {"title": title, "src": src, "picture_list": picture_container, "content": content,
                       "publish_time": publish_time}
        pool.submit(save_json, title, news_detail)

    # 加载更多
    if num >= 2:
        for page in range(2, num):
            url = "http://labs.zol.com.cn/router.php?c=TestChannel_Default&a=GetChannelNew&module=new&page=%s" % page
            resp = requests.get(url,
                                headers={
                                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
                                })
            # print(resp.json(), type(resp.json()))
            for news in resp.json():
                # print(news, type(news))
                if news.get("content", None):
                    news_detail = {"title": news["title"], "src": news["url"], "picture_list": news["picture"],
                                   "content": news["content"],
                                   "publish_time": news["date"]}
                    pool.submit(save_json, news["title"], news_detail)
                elif news.get("picArr", None):
                    news_detail = {"title": news["title"], "src": news["url"], "picture_list": news["picture"],
                                   "content": news["picArr"],
                                   "publish_time": news["date"]}
                    pool.submit(save_json, news["title"], news_detail)


def save_json(title, news_detail):
    target_path = os.path.join(current_dir, "中关村json/%s" % title)
    # print(target_path)
    with open(target_path, "wt") as f:
        f.write(json.dumps(news_detail))


if __name__ == '__main__':
    # 传入爬取页数
    parser(5)
