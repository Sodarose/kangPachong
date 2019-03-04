import requests
import os
from multiprocessing import Process
from pyquery  import PyQuery as pq
import time

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Host':	'www.gugu5.com'
}
data={

}

address='http://www.gugu5.com/all/'
paddress='http://www.gugu5.com'
ticai={

}
reData={

}
# 搜索分类
def f():
    r = requests.get(url=address,headers=headers)
    r.encoding="UTF-8"
    if r.status_code==200:
        html = r.text
        doc = pq(html)
        doc = doc('.classid111').siblings()('a').items()
        global ticai
        for i in doc:
            ticai[str(i.text())]=str(i.attr('href'))


# 单页扫描函数
def z(address):
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
def x(title,leixing):
    r = requests.get(url=paddress+leixing)
    r.encoding='UTF-8'
    doc = pq(r.text)
    doc = doc('.NewPages ul li:last-child a')
    maxHref = str(doc.attr('href'))
    maxPage = maxHref[0:len(maxHref)-5]
    leData=[]
    for i in range(1,int(maxPage)+1):
        address = paddress+leixing+str(i)+'.html'
        leData.append(z(address))
    # 写入数据
    w(title,leData)




# 写入数据
def w(title,data):
    f = open('标题'+title+'清单','w')
    for i in data:
        for j in i:
            f.write(str(j))
    f.close()

# 开启进程池写入数据
def p():
    pass

def run():
    print(os.getpid())
    print('子程序')

def f(name):
    print('hello', name)
    time.sleep(1)
class Ps(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(os.getpid())
        print('%s 正在和女主播聊天' % self.name)

if '__name__' == '__main__':
    p_lst = []
    for i in range(5):
        p = Process(target=f, args=('bob',))
        p.start()
        p_lst.append(p)
        p.join()
    # [p.join() for p in p_lst]
    print('父进程在执行')
    p1 = Ps('wupeiqi')
    p2 = Ps('yuanhao')
    p3 = Ps('nezha')
    p1.start()
    p2.start()
    p3.start()






