import numpy as np
import xlrd
 
#读数据并求熵
path=u'/Users/blue/Downloads/indicators2.xls'
hn,nc=1,1
#hn为表头行数,nc为表头列数
sheetname=u'table_indicators'
def readexcel(hn,nc):
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name(sheetname)
    nrows = table.nrows
    data=[]
    for i in range(nrows):
        data.append(table.row_values(i)[0:])
    return np.array(data)
def entropy(data0):
    #返回每个样本的指数
    #样本数，指标个数
    n,m=np.shape(data0)
    #一行一个样本，一列一个指标
    #下面是归一化
    maxium=np.max(data0,axis=0)
    minium=np.min(data0,axis=0)
    data= (data0-minium)*1.0/(maxium-minium)
    ##计算第j项指标，第i个样本占该指标的比重
    sumzb=np.sum(data,axis=0)
    data=data/sumzb
    #对ln0处理
    a=data*1.0
    a[np.where(data==0)]=0.0001
#    #计算每个指标的熵
    e=(-1.0/np.log(n))*np.sum(data*np.log(a),axis=0)
#    #计算权重
    w=(1-e)/np.sum(1-e)
    recodes=np.sum(data*w,axis=1)
    return recodes
data=readexcel(hn,nc)
grades=entropy(data)