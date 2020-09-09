from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import os
from script.models import SiteInfo
import django.utils.timezone as timezone
from django.conf import settings
from datetime import datetime

#忽略HTTPS连接错误的警告
requests.packages.urllib3.disable_warnings()


header = {
    'Accept': '*/*',
    'Cache-Control': 'max-age=0',
    'User-Agen': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com/'
}


def save_info(url, title, code):
    data = SiteInfo.objects.filter(url=url)
    alive = False
    death = False
    print(code)
    for i in data:
        if i.status != code and code != '200':

            print(i.url + "  ===-    " + i.status  + " - - " +code)
            death = True

        elif i.status != code and code == '200':
            print(i.url + "  ---    " + i.status  + " - - " +code)
            alive = True
    info = {
        'url': url,
        'title': title,
        'status': code,
        'updateTime': timezone.now,
        'alive': alive,
        'death': death,
    }

    if data.exists():
        data.update(title=title, status=code, updateTime=datetime.now(), alive=alive, death=death)
    else:
        data = SiteInfo(**info)
        data.save()
# 获取目标状态
def get_status(url):
    url = url.strip()
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    try:
        response = requests.get(url, headers=header, verify=False, allow_redirects=True, timeout=10)
        charset = response.encoding  # 对该html进行编码的获取
        if (charset == "GB2312" or charset is None):
            response.encoding = 'gbk'
        else:
            response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text,'lxml')
        title = str(soup.find('title'))
        if not title:
            title = ''
        if '<title>' in title:
            title = title.replace('<title>','').replace('</title>','')
        code = str(response.status_code)
        #print(url.strip('\n').strip('\r') + "  ===========   " + str(code))

        save_info(url, title, code)
        return code, title
    except requests.RequestException as e:
       # print(url.strip('\n').strip('\r') + "   ------- " + "网站不存在或者已关闭")
        save_info(url, '', '网站不存在或者已关闭')

'''

def get_url():
    urllist = []
    try:
        for parent, dirnames, filenames in os.walk(settings.MEDIA_ROOT):
            for fn in filenames:  # 遍历该目录下的每个文件
                print(os.path.join(parent, fn))
                with open(os.path.join(parent, fn)) as urls:
                    for url in urls:
                        url = url.strip()
                        urllist.append(url)
    except Exception:
        print("文件不存在")
    return list(set(urllist))
'''

# 定时任务调用的函数
def run():
    data = SiteInfo.objects.all()
    data = list(set(data))
    executor = ThreadPoolExecutor(max_workers=10)
    url_list =[]
    for i in data:
        url_list.append(i.url.strip())
    executor.map(get_status, url_list)

# 每次上传目标文件时
def get_single_file(file_path):
    urllist = []
    try:
        with open(settings.MEDIA_ROOT + '/' + str(file_path), 'r') as urls:
            for url in urls:
                url = url.strip()
                urllist.append(url)
    except Exception:
        print("文件不存在")

    urllist = list(set(urllist))
    # 使用多线程加快速度
    executor = ThreadPoolExecutor(max_workers=10)
    executor.map(get_status, urllist)

#print(get_status("http://jd.com"))
#run()
