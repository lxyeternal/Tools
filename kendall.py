# -*- coding: utf-8 -*-
# @Project ：content_analysis2
# @Time    : 2020-08-12 17:33
# @Author  : honywen
# @FileName: kendall.py
# @Software: PyCharm


import pandas as pd
from scipy.stats import kendalltau



#   肯德尔相关性系数计算方法
def kendall(list1,list2):

    x = pd.Series(list1)
    y = pd.Series(list2)
    result = x.corr(y, method="kendall")
    return result


#   kendall函数测试
def test_kendall():

    list1 = ['3','1','2','2','1','3']
    list2 = ['1','2','3','2','1','1']
    result = kendall(list1,list2)
    print(result)


#   肯德尔相关性系数计算方法  2
def kendall_scipy(a,b):

    Lens = len(a)
    ties_onlyin_x = 0
    ties_onlyin_y = 0
    con_pair = 0
    dis_pair = 0
    for i in range(Lens - 1):
        for j in range(i + 1, Lens):
            test_tying_x = np.sign(a[i] - a[j])
            test_tying_y = np.sign(b[i] - b[j])
            panduan = test_tying_x * test_tying_y
            if panduan == 1:
                con_pair += 1
            elif panduan == -1:
                dis_pair += 1

            if test_tying_y == 0 and test_tying_x != 0:
                ties_onlyin_y += 1
            elif test_tying_x == 0 and test_tying_y != 0:
                ties_onlyin_x += 1

    Kendallta1 = (con_pair - dis_pair) / np.sqrt(
        (con_pair + dis_pair + ties_onlyin_x) * (dis_pair + con_pair + ties_onlyin_y))
    Kendallta2, p_value = kendalltau(a, b)
    print(Kendallta1)
    print(Kendallta2)



