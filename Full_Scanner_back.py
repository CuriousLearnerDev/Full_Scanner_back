# -*- coding:utf-8 -*-

'''
主程序
'''


import urllib.request
import threading
from urllib import error
import time
import queue
from urllib.parse import quote # urllib请求url里面带中文就会报错用这个抱住就可以了
import random
import argparse

schedule = 0 # 记录请求多少次
pl=0 # 记录批量扫描的数量
count=0 # 记录文件内容一个多少行
current_time_=time.strftime("%Y-%m-%d%H:%M:%S", time.localtime())

# 提取出来的结果保存起来
def Searchresults(results_IP):

    Searchresults_document = open(current_time_+".txt", 'a')  # 打开文件写的方式
    Searchresults_document.write((results_IP+'\n'))  # 写入
    Searchresults_document.close()  # 关闭文件

# 批量扫描
def Batch_scan(path):
    Batch=[]
    i = 1
    # 叫文件内容变成
    search_url=queue.Queue()
    thefile=open(path, encoding="UTF-8")

    # 统计有多少行
    while True:
        buffer = thefile.read(1024 * 8192)
        if not buffer:
            break
        i += buffer.count('\n')

    print(UseStyle("文件一共有"+str(i)+"条目标",fore='yellow'))
    # 叫每一行内容都保存到search_url中
    for i in open(path, encoding="UTF-8"):
        Batch.append(i.rstrip())

    return Batch

# 读取字典文件内容
def Read_dictionary(document):
    global count # 记录文件内容一个多少行

    # 叫文件内容变成
    search_url=queue.Queue()
    thefile=open(document)

    # 统计有多少行
    while True:
        buffer = thefile.read(1024 * 8192)
        if not buffer:
            break
        count += buffer.count('\n')

    print(UseStyle("文件一共有"+str(count)+"条",fore='yellow'))
    print(Wire())
    # 叫每一行内容都保存到search_url中
    for i in open(document, encoding="UTF-8"):
        search_url.put(i.rstrip())

    return search_url



def ask(search_url,url):
    HeadersConfig = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    }
    while not search_url.empty():

        searchurl=search_url.get()
        #time.sleep(1)  # 暂停 1 秒
        #print(searchurl)
        try:
            global schedule
            print(current_time() + f"进度: {schedule}/{count}", "\r", end='')
            #back=requests.get(url+i,headers=config.HeadersConfig)
            back = urllib.request.Request(url=(url+quote(searchurl)), headers=HeadersConfig, method='GET')
            response = urllib.request.urlopen(back, timeout=7)
            print()
            if response.status==200:
                schedule+=1
                print(current_time()+UseStyle(f"请求第[{str(schedule)}]这个地址存在："+url+searchurl,fore='green'))
                print("\r", end="")
                Searchresults(url + searchurl)
                print(current_time()+f"进度: {schedule}/{count}","\r", end='')
            elif response.status==301:
                schedule += 1
                print(current_time()+UseStyle(f"请求第[{str(schedule)}]这个地址存在："+url+searchurl,fore='green'))
                print("\r", end="")
                Searchresults(url + searchurl)
                print(current_time()+f"进度: {schedule}/{count}","%\r", end='')
        except error.HTTPError as cw:
            if str(cw) in "HTTP Error 404: Not Found":  # 报错404的
                schedule += 1
            if str(cw) in "<urlopen error [Errno 113] No route to host>": # 报错超时的
                print('\n目标未7响应时间超时了！')
                break
            #print(UseStyle(f'请求第[{str(schedule)}][*]这个地址不存在：',fore='yellow')+UseStyle(url+searchurl+'\t\t\t\t\t[*]'+"状态码："+str(e.code),fore='red'))


def Thread(url,T,document):
    threadpool = []
    search_url=Read_dictionary(document)
    for _ in range(int(T)):
        Threads = threading.Thread(target=ask, args=(search_url, url))
        threadpool.append(Threads)
    for th in threadpool:
        th.start()
    for th in threadpool:
        threading.Thread.join(th)

def Interface(args):

    args.url=args.url.strip()

    if args.url[-1]!='/': # 查看最后一个是否有/没有添加/
        args.url+='/'
    args.thread=int(args.thread)

    Thread(args.url,args.thread,args.document)


def UseStyle(string, fore):
    return f"\033[1;{STYLE[fore]}m{string}\033[0m"

def Wire():
    return f'\033[0;33m {"—"*60}\033[0m'
def current_time():
    return UseStyle(time.strftime("[%Y-%m-%d_%H:%M:%S]: [*]", time.localtime()),fore='blue')


STYLE = {   # 前景色
            'black'    : 30,   #  黑色
            'red'      : 31,   #  红色
            'green'    : 32,   #  绿色
            'yellow'   : 33,   #  黄色
            'blue'     : 34,   #  蓝色
            'purple'   : 35,   #  紫红色
            'cyan'     : 36,   #  青蓝色
            'white'    : 37,   #  白色
        }

banner_1 = r"""    
         ___     _ _     ___                            
        | __|  _| | |___/ __| __ __ _ _ _  _ _  ___ _ _ 
        | _| || | | |___\__ \/ _/ _` | ' \| ' \/ -_) '_|
        |_| \_,_|_|_|   |___/\__\__,_|_||_|_||_\___|_| 
"""

banner_2 = r'''

             _____                                               
        () |_       |\ |\    ()  _   _,               _  ,_  
          /| ||  |  |/ |/----/\ /   / |  /|/|  /|/|  |/ /  | 
         (/    \/|_/|_/|_/  /(_)\__/\/|_/ | |_/ | |_/|_/   |/
'''

banner_3 = """


         __|    | |       __|                              
         _||  | | |____|\__ \  _|  _` |   \    \   -_)  _| 
        _|\_,_|_|_|     ____/\__|\__,_|_| _|_| _|\___|_|  
"""

banner_4 = """


                 _       __                 
                |_  ||__(_  _ _.._ ._  _ ._ 
                ||_|||  __)(_(_|| || |(/_|
"""

def picture_choice():
    i = random.choice(range(4))
    if i == 0:
        return banner_1
    elif i == 1:
        return banner_2
    elif i == 2:
        return banner_3
    elif i == 3:
        return banner_4

def choose_color_2(cb):

    i = random.choice(range(4))

    if i == 0:
        return "\033[1;32m{}\033[0m".format(cb)
    elif i == 1:
        return "\033[1;31m{}\033[0m".format(cb)
    elif i == 2:
        return "\033[1;33m{}\033[0m".format(cb)
    elif i == 3:
        return "\033[1;36m{}\033[0m".format(cb)

def banner():
    Author='\033[0;33m作者：w啥都学\033[0m'
    Blog='\033[0;33mBlog地址：www.zssnp.top\033[0m'
    blbl = '\033[0;33m哔哩哔哩：https://space.bilibili.com/432899074\033[0m'
    github='\033[0;33mgithub项目地址：https://github.com/Zhao-sai-sai/Full_Scanner_back\033[0m'
    Frame=f'\033[0;33m {"—"*60}\033[0m'
    help="""\033[0;31m 本程序是一个Full_Scanner工具的子工具，Full_Scanner还在写
    本工具是一个后台扫描器，支持多线程和批量扫描\033[0m"""

    picture_=choose_color_2(picture_choice())

    icon=f"""\n{Frame}\n{picture_}\n\n{Author}\n{Blog}\n{github}\n{Frame}\n{help}\n{Frame}                          """

    return  icon

if __name__ == '__main__':
    print(banner())

    parser = argparse.ArgumentParser(description=UseStyle("警告：请勿用于非法用途！否则自行承担一切后果",'red'),
                                     usage=choose_color_2('python3 Full_Scanner_back.py  [目标] [其他参数]'))

    Active_collect_message = parser.add_argument_group(choose_color_2("参数"),
                                                       choose_color_2("下面是参数和参数的使用说明"))

    Active_collect_message.add_argument('-u','--url',
                                        dest='url',
                                        type=str,
                                        nargs='?',
                                        help=choose_color_2("指定扫描的目标，比如https://baidu.com/"))

    Active_collect_message.add_argument('-t','-thread',
                                        dest='thread',
                                        type=int,
                                        nargs='?',
                                        help=choose_color_2("指定线程默认是30"))
    Active_collect_message.add_argument('-d','-document',
                                        dest='document',
                                        type=str,
                                        nargs='?',
                                        help=choose_color_2("指定字典默认是用的php.txt"))
    Active_collect_message.add_argument('-many',
                                        dest='many',
                                        type=str,
                                        nargs='?',
                                        help=choose_color_2("多个目标保存到一个文件里面进行批量扫描"))

    args = parser.parse_args()

    if args.url != None or args.many != None:
        # 默认字典
        if args.document == None:
            args.document = "dictionary/PHP.txt"

        # 默认线程
        if args.thread == None:
            args.thread = 10



        if args.many == None:
            print(UseStyle('扫描结果保存在result文件夹下\n' +
                           '目标地址是：' +
                           args.url +
                           "\n线程数是：" +
                           str(args.thread) +
                           '\n字典：' +
                           args.document,
                           fore='yellow'))
            Interface(args)

        else:
            # 批量扫描
            Many_Batch=Batch_scan(args.many)
            for url in Many_Batch:
                count = 1  # 记录请求多少次
                schedule = 1  # 重置字典的数量
                args.url=url
                pl += 1  # 记录批量扫描的数量
                print(choose_color_2('\n\n\n扫描结果保存在result文件夹下' +
                                     '\n字典：' +
                                     args.document+
                                     f"\n正在扫描：{url} 第{str(pl)}个目标"+
                                     f"\n线程数是：{str(args.thread)}"))
                Interface(args)