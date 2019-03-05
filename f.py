import requests
import os
from multiprocessing import Pool
from pyquery  import PyQuery as pq
import time
import random

# 搜索分类
def f(address,headers):
    r = requests.get(url=address,headers=headers)
    r.encoding="UTF-8"
    if r.status_code==200:
        ticai={}
        html = r.text
        doc = pq(html)
        doc = doc('.classid111').siblings()('a').items()
        for i in doc:
            ticai[str(i.text())]=str(i.attr('href'))
        return ticai


# 单页扫描函数
def z(address,headers):
    r = requests.get(url=address,headers=headers)
    r.encoding="UTF-8"
    if(r.status_code==200):
        html = r.text
        doc = pq(html)
        doc = doc(".cy_list_mh ul").items()
        pageDate = []
        for i in doc:
            data = {}
            # 标题
            data['标题'] = i(".title").text()
            # 链接
            data['链接'] = str(i("a").attr('href'))
            # 图片
            data['图片链接'] = str(i('img').attr('src'))
            # 状态
            data['状态'] = i('.status').text()
            # 更新
            data['更新'] = {
                '最新':i('.updata span').text(),
                'url':str(i('.updata a').attr('href'))
            }
            # 标签
            biaoqian = []
            for t in i('.biaoqian a').items():
                biaoqian.append({t.text():str(t.attr('href'))})
            # 简介 info
            data['标签'] = biaoqian
            data['简介'] = str(i('.info').text())[3:len(str(i('.info').text()))]
            pageDate.append(data)
        return pageDate

# 根据类型搜索
def x(title,leixing,paddress,headers):
    r = requests.get(url=paddress+leixing)
    r.encoding='UTF-8'
    doc = pq(r.text)
    doc = doc('.NewPages ul li:last-child a')
    maxHref = str(doc.attr('href'))
    maxPage = maxHref[0:len(maxHref)-5]
    leData=[]
    for i in range(1,int(maxPage)+1):
        address = paddress+leixing+str(i)+'.html'
        leData.append(z(address,headers))
    # 写入数据
    w(title,leData)




# 写入数据
def w(title,data):
    f = open('./漫画清单/'+title+'清单.txt','w',encoding='UTF-8')
    for i in data:
        for j in i:
            f.write(str(j)+'\n')
    f.close()

# 开启进程池写入数据
def p():
    print("进程:"+str(os.getpid())+"完成")


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Host': 'www.gugu5.com'
    }
    initUrl = 'http://www.gugu5.com/all/'
    paddress = 'http://www.gugu5.com'
    fenlei=f(initUrl,headers)
    pool = Pool(os.cpu_count()+1)
    if not os.path.exists('./漫画清单/'):
        os.mkdir('./漫画清单/')
    for key in fenlei:
        pool.apply_async(func=x,args=(key,fenlei[key],paddress,headers))
    pool.close()
    pool.join()
    print("程序退出")