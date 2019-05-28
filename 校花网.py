import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(10)
base_url = 'http://www.xiaohuar.com'
current_path = os.path.dirname(__file__)
names = []


def parse_xiaohua(page_num):
    for page in range(page_num):
        url = 'http://www.xiaohuar.com/list-1-%s.html' % page
        res = requests.get(url,
                           headers={
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                           })
        picture_list = re.findall('src="(.*?).jpg" />', res.text)
        name_list = re.findall('<span class="price">(.*?)</span>', res.text)
        # print(picture_list)
        # print(len(picture_list))
        for picture in picture_list:
            if picture.startswith('http'):
                picture_path = picture + '.jpg'
            else:
                picture_path = base_url + picture + '.jpg'
            name = name_list.pop(0)
            print(name)
            print(picture_path)
            pool.submit(download, picture_path, name)


def download(path, name):
    try:
        target_path = os.path.join(current_path, 'test\%s' % name + '.jpg')
        # print(target_path)
        if os.path.exists(target_path):
            print('已下载')
            return

        pic_res = requests.get(path,
                               headers={
                                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                               }, timeout=10)
        content = pic_res.content

        with open(target_path, 'wb') as f:
            f.write(content)
        print('下载成功')
    except Exception as e:
        print(name, e)


if __name__ == '__main__':
    parse_xiaohua(3)

