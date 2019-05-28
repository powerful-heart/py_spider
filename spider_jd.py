"""
使用selenium交互爬取京东手机信息
驱动搜索手机列表
获取内容
包括页数
for循环总页数
驱动下拉到最下方点击下一页
继续获取所需信息
"""

from selenium.webdriver.chrome.options import Options
from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.common.by import By
import time
from lxml import etree
import pymysql
from concurrent.futures import ThreadPoolExecutor
import pypinyin
from xpinyin import Pinyin


# 页面下滑, 解决惰性加载
def scroll_down():
    height = driver.execute_script("return document.body.clientHeight")
    # print(height)
    dis = 0
    while dis < height:
        driver.execute_script("""
                    window.scrollTo({
                        top: %s,
                        behavior: "smooth"});""" % dis)
        dis += 40
        time.sleep(0.1)
    driver.implicitly_wait(10)


def parse(kw):
    try:
        driver.get("https://www.jd.com/")

        input_tag = driver.find_element_by_id("key")
        input_tag.send_keys(kw)
        input_tag.send_keys(Keys.ENTER)
        # scroll_down()

        # 指定爬多少页
        for i in range(3):
            time.sleep(1)
            search_window = driver.current_window_handle  # 此行代码用来定位当前页面
            scroll_down()

            # 解析数据
            goods_list = driver.find_elements_by_class_name("gl-item")
            # print(goods, type(goods))
            for goods in goods_list:
                # 标题
                title = goods.find_element_by_class_name("p-name").find_element_by_css_selector("a>em").text
                print(title)
                # 链接
                url = goods.find_element_by_class_name("p-name").find_element_by_css_selector("a").get_attribute("href")
                print(url)
                # 图片
                picture_src = goods.find_element_by_class_name("p-img").find_element_by_css_selector("a>img").get_attribute(
                    "src")
                print(picture_src)
                # 价格
                price = goods.find_element_by_class_name("p-price").find_element_by_css_selector("strong").text
                print(price)
                # 评价数
                comments_count = goods.find_element_by_class_name("p-commit").find_element_by_css_selector(
                    "strong").text
                print(comments_count)
                # 店铺名称(飞利浦手机无店铺信息)
                try:
                    shop_name = goods.find_element_by_class_name("p-shop").find_element_by_css_selector(
                        "span>a").get_attribute(
                        "title")
                    print(shop_name)
                except Exception as error:
                    print(error)
                    continue
                phone_detail = {'title': title, 'url': url, 'picture_src': picture_src, 'price': price,
                                'comments_count': comments_count, 'shop_name': shop_name}
                pool.submit(save_mysql, phone_detail)

            # 去往下一页
            next_page_tag = driver.find_element_by_class_name("pn-next")
            next_page_tag.click()
            # next_page_tag.send_keys(Keys.LEFT)

    except Exception as e:
        print(e)
    finally:
        driver.close()


def save_mysql(phone_detail):
    table_list = []
    try:
        conn = pymysql.connect(host="localhost", port=3306, db='jd', user='root', password='123456')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 查询所有表, 判断将要建的表是否已经存在
        find_sql = "show tables"
        cursor.execute(find_sql)
        data = cursor.fetchall()
        # print(data)
        for i in data:
            for j in i.values():
                table_list.append(j)
        if kw_pinyin not in table_list:  # 表不存在则创建
            create_sql = "create table %s( id int primary key auto_increment, title char(64) unique key,url varchar(1024)," \
                         "picture_src varchar(256), price char(16), comments_count char(10), shop_name char(32))" % kw_pinyin
            cursor.execute(create_sql)
            conn.commit()
        sql = 'insert into {}(title, url, picture_src, price, comments_count, shop_name) values (%s, %s, %s, %s, %s, %s)'.format(kw_pinyin)
        # 在内存中一次插入一条
        cursor.execute(sql, (
            phone_detail["title"], phone_detail["url"], phone_detail["picture_src"], phone_detail["price"],
            phone_detail["comments_count"], phone_detail["shop_name"]))
        # 将内存中的数据提交到硬盘中
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    kw = input("搜索商品")
    # 拼音模块, 用于生成搜索关键字的表名
    p = Pinyin()
    kw_pinyin = p.get_pinyin(u"%s" % kw, "")
    # selenium配置
    option = webdriver.ChromeOptions()
    option.add_argument("disable-infobars")  # 隐藏浏览器被控制提示
    option.add_argument('blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(chrome_options=option)
    # chrome_option = Options()
    # chrome_option.add_argument('blink-settings=imagesEnabled=false')
    pool = ThreadPoolExecutor(5)
    parse(kw)
