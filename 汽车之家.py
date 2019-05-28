import requests
from bs4 import BeautifulSoup

html_doc = """
<li class="content-list-item" style="display:block;">
<a class="pic" href="http://mobile.zol.com.cn/713/7135134.html">
<img .src="https://article-fd.zol-img.com.cn/t_s160x120/g2/M00/05/03/ChMlWlylxzKIeWyFAAFyWvrsRP8AAJOxALhGdAAAXJy078.jpg" alt="HUAWEI WATCH GT活力款评测 久续航的智能管家" height="120" src="https://article-fd.zol-img.com.cn/t_s160x120/g2/M00/05/03/ChMlWlylxzKIeWyFAAFyWvrsRP8AAJOxALhGdAAAXJy078.jpg" width="160"/>
</a>
<div class="info">
<div class="info-hd">
<a href="http://mobile.zol.com.cn/713/7135134.html">HUAWEI WATCH GT活力款评测 久续航的智能管家</a>
</div>
<p>说不想拥有一个完美的身材？都说“一年之计在于春”，当下就是最好的时机。因此春季也是智能运动手表出货量较大的一个节点。其实说到智能手表，已经有大批量的科...</p>
<div class="info-ft clearFix">
<div class="icon info-comment">0</div>
<span class="info-time">39分钟前</span>
</div>
</div>
</li>
"""
soup = BeautifulSoup(html_doc, 'lxml')
print(soup.text)
