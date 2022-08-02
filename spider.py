import requests
import json
import time
import random
import getpass

def search(spot_id):
    offset = 0
    # 爬的数据有 用户名称 价格 评价 评价日期 票务类型评论每个景点1000条
    # 所以建1000 * 6 的二维数组
    data = [['' for i in range(6)] for j in range(1000)]
    row = 0
    # 美团评论每个页面10条评论，所以爬100个页面就是1000条
    for page in range(100):
        if offset == 0:
            # 这个spot_id是美团不同景点有个id，手动找的10个存在下面的spots_id字典里
            # url就是评论页面
            url = f'https://www.meituan.com/ptapi/poi/getcomment?id={spot_id}&offset=0&pageSize=10&mode=0&sortType=1'
        else:
            url = f'https://www.meituan.com/ptapi/poi/getcomment?id={spot_id}&offset={offset}&pageSize=10&mode=0&starRange=&userId=&sortType=1'
        while True:
            try:
                # 美团反爬比较严，random.choice每次请求随机从headers里选个user—agent和网上找的免费代理。不至于老被封ip，想不被封ip爬慢点也可以
                res = requests.get(url, headers={'User-Agent': random.choice(my_headers)}, proxies={'http': random.choice(proxy_list)})
                break
            except:
                # 休眠一下以防被封ip
                time.sleep(2)
                pass
        res = res.text
        # 爬到的数据用json解析一下，解析成dictionary
        js = json.loads(res)
        # 获取js里面的comments
        comments = js["comments"]
        for i in comments:
            # comments还是一个字典，里面是我们想要的数据。
            id = i['userName']
            price = i['avgPrice']
            comment = i['comment']
            # 把评论里面的回车删掉，不然存的时候会乱掉，因为存的时候就是用\n分隔的
            comment = comment.replace('\n', '')
            # 评论日期是时间戳格式，时间戳就是从1970年1月1日到现在的秒数，这里面的评论日期有13位
            # 前十位是年月日，所以我们取前十位
            date = time.localtime(int(i['commentTime'][:-3]))
            # 用time.strftime把时间戳格式化成年月日
            date = time.strftime("%Y.%m.%d", date)
            menu = i['menu']
            # 评价几颗星爬出来是10 20.。。50这样，一般评价是满心5颗星的，所以转成5星满星那种
            star = int(i['star'])//10

            data[row] = [id, price, star, date, menu, comment]
            row += 1
            print(id, price, star, date, menu, comment)
        offset += 10
        # 随机休眠一下，更不会被封ip
        time.sleep(random.randint(2, 5))
    return data

def save():
    spots_id = {"九寨沟": 962956,
                "黄山": 951905,
                "黄龙风景名胜区": 962957,
                "武陵源": 87232670,
                "兰州极地海洋世界": 97262583,
                "华山": 660752,
                "三清山": 910121,
                "颐和园": 271925,
                "故宫": 271772,
                "鸣沙山月牙泉": 2293317
                }
    for spot_id in spots_id:
        # search就是爬数据那个函数
        data = search(spots_id[spot_id])
        # csv默认用\n分隔，比excel方便
        f = open(database+spot_id+'.csv', 'w')
        for row in data:
            for col in row:
                try:
                    f.write(f'{col},')
                except:
                    f.write(' ,')
            f.write('\n')
        f.close()

if __name__ == '__main__':
    # 设置请求头
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    ]
    #设置代理
    proxy_list = [
        '183.95.80.102:8080',
        '123.160.31.71:8080',
        '115.231.128.79:8080',
        '166.111.77.32:80',
        '43.240.138.31:8080',
        '218.201.98.196:3128'
    ]
    # 获取你电脑的用户名，
    usr_name = getpass.getuser()
    # 数据存的路径
    database = r'C:\Users\\'+usr_name+r'\\Desktop\meituan\景点数据\\'

    save()