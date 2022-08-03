import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import font_manager
import os

def datalist():
    data_path = r'景点数据\\'
    # 获取爬到的数据的文件名
    csv_data = os.listdir(data_path)
    for i in range(len(csv_data)):
        csv_data[i] = data_path + csv_data[i]
    # 返回文件完整的路径
    return csv_data

def open_csv(csv_data):
    # pandas读csv文件
    data = pd.read_csv(csv_data, encoding='gbk')
    # 取文件里1000条数据
    data = data.loc[:1000, :'评论']
    return data

# 算一下平均评论星数
def ave_star(stars):
    sum = 0
    for star in stars:
        sum += star
    return '%.3f' % (sum / len(stars))

def ave_s():
    csv_datas = datalist()
    # 获取文件名称
    file_names = ['%s' % (os.path.split(csv_data))[1] for csv_data in csv_datas]
    aver_star = []
    # 每个文件都算一下平均星数，一共十个
    for csv_data in csv_datas:
        data = open_csv(csv_data)
        stars = data['评价']
        aver_star.append(float(ave_star(stars)))
    # 作图
    plt.figure(figsize=(20, 12), dpi=120)
    # 条形图，10个条，纵坐标平均星数，横坐标1到10
    plt.bar([i for i in range(1, 11)], aver_star)
    # 横坐标改成景点名称
    plt.xticks(range(1, 11), ['%s' % file_name[:-4] for file_name in file_names], fontproperties=myfont, rotation=20)
    # y轴的坐标上下限改一下，没有低于两星的景点
    plt.ylim((2, 5))
    # y轴刻度2-5
    plt.yticks(range(2, 6))
    # x轴y轴标签设置一下
    plt.xlabel('景点', fontproperties=myfont)
    plt.ylabel('评价', fontproperties=myfont)
    # 做出来的图片保存起来
    plt.savefig('aver_star.png')
    plt.show()

def population():
    csv_datas = datalist()
    # 生成一个日期列表，开始时间2015年12月31日，结束时间2021年12月31日，间隔3个月（一个季度）
    date_list = pd.date_range(start='20151231', end='20211231', freq='3M')
    # 反过来取，从2021年12月31日到2015年12月31日
    date_list = date_list[::-1]
    plt.figure(figsize=(20, 8), dpi=120)
    for csv_data in csv_datas:
        data = open_csv(csv_data)
        popu = data['评价日期'][:1000]
        # 把文件里的日期转成pandas里的日期类型（没转就是string类型）
        popu = pd.to_datetime(popu)
        num = {}
        for date in popu:
            for com in range(len(date_list)):
                # 把每个季度每个景点评论的人数存在一个字典num里面
                # 月份转成季度，比如9月9//3%4+1 = 4季度
                key = f'{str(date_list[com])[2:4]}年{int(str(date_list[com])[5:7])//3%4+1}季度'
                if key[3] == '1':
                    key = f'{int(key[0:2])+1}{key[2:]}'
                # 找不到对应的季度说明这个季度还没加到字典，把这个季度加到字典，值设为1
                if date > date_list[com] and (key not in num.keys()):
                    num[key] = 1
                    break
                # # 找到数据对应的季度，递增这个季度的评论人数
                elif date > date_list[com] and (key in num.keys()):
                    num[key] += 1
                    break
        # 最后一个季度的人数因为每到月底，数据不准确，所以最后一个季度数据去掉
        number = list(num.values())[:-1]
        period = list(num.keys())[:-1]
        # 算出来的季度是21年到15年的，应该反过来取，做出来图
        plt.plot(list(range(20))[::-1][:len(number)], number, label='%s' % (os.path.split(csv_data))[1][:-4])
        plt.xlabel('时间', fontproperties=myfont)
        plt.ylabel('评论数', fontproperties=myfont)
        plt.legend(prop=myfont)
    plt.xticks(list(range(len(period))), period[::-1], fontproperties=myfont, rotation=45)
    plt.savefig('tendency.png')
    plt.show()

if __name__=='__main__':
    myfont = font_manager.FontProperties(fname=r'C:\WINDOWS\Fonts\MSYH.TTC')
    ave_s()
    population()
    print(123)
    print(456)
    print(789)
    print(101112)
    print(101112)
    print(3432)
    print(3432)