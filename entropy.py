import numpy as np
import xlrd
 


#  从excel文件读取数据矩阵(去掉表头)
def readexcel():
    # 读数据并求熵
    path = 'data/indicators2.xls'
    sheetname = 'table_indicators'
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name(sheetname)
    nrows = table.nrows
    data=[]
    for i in range(nrows):
        data.append(table.row_values(i))
    return np.array(data)


#  完成数据的归一化
def normal(data):

    # data = data.astype(np.float)
    # 每一列的最值
    maxium=np.max(data,axis=0)
    minium=np.min(data,axis=0)
    data= (data-minium)*1.0/(maxium-minium)
    return data


def entropy(data):

    # 样本数，指标个数
    n, m = np.shape(data)
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


if __name__ == '__main__':

    data = readexcel()
    data = normal(data)
    weight = entropy(data)
    print(weight)