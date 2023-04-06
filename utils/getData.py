from .querys import *
import jieba
import re
import time
import json

def getAllData():
    def map_fn(item):
        item = list(item)
        if item[7]:
            item[7] = item[7].split(',')
        return item
    allData = list(query('select * from readbookinfos', [], 'select'))
    allData = list(map(map_fn, allData))
    for index, i in enumerate(allData):
        for index, j in enumerate(i[7]):
            if j == '#':
                i[7].pop(index)
        try:
            i.append(len(i[7]))
        except:
            i.append(0)

        i[11] = i[11].split(sep=',')
        i[13] = json.loads(i[13])

    return allData

def getHomeData(type='all'):
    def map_fn(item):
        item = list(item)
        if item[7]:
            item[7] = item[7].split(',')
        return item
    dataLen = len(query('select * from readbookinfos',[],'select'))
    words = query('select content from readbookinfos', [], 'select')
    dianZans = query('select heartCount from readbookinfos',[],'select')
    allData = list(query('select * from readbookinfos',[],'select'))
    text = ''
    for i in words:
        text = text + i[0]
    wordLen = len(list(jieba.cut(text)))
    newDianZans = []
    for i in dianZans:
        if i[0].find('万') != -1:
            num = re.findall('\d+\.\d+',i[0])[0]
            newDianZans.append(int(float(num) * 10000))
        else:
            newDianZans.append(int(i[0]))
    newDianZans.sort(reverse=True)
    allData = list(map(map_fn,allData))
    for index,i in enumerate(allData):
        for index,j in enumerate(i[7]):
            if j == '#':
                i[7].pop(index)
        try:
            i.append(len(i[7]))
        except:
            i.append(0)

        i[11] = i[11].split(sep=',')
        i[13] = json.loads(i[13])

    address = []
    types = []
    for i in allData:
        address.append(i[8])
        types.append(i[9])

    # 饼图数据
    typesDic = {}
    for i in types:
        if typesDic.get(i,-1) == -1:
            typesDic[i] = 1
        else:
            typesDic[i] += 1
    typesData = []
    for key,value in typesDic.items():
        typesData.append({
            'name':key,
            'value':value
        })

    # 漏斗图数据
    addressDic = {}
    for i in address:
        if addressDic.get(i, -1) == -1:
            addressDic[i] = 1
        else:
            addressDic[i] += 1

    if type != 'all':
        allData = list(filter(lambda x:True if x[9] == type else False,allData))

    return dataLen,wordLen,newDianZans[0],allData,max(address),max(types),typesData,types,addressDic

def getDetailDataById(id):
    allData = getAllData()
    return list(filter(lambda x:x[10] == id,allData))

def getTimeData(type):
    allData = list(query('select * from readbookinfos',[],'select'))
    def map_fn(item):
        item = list(item)
        item[4] = item[4].split(' ')
        item[4][1] =  time.mktime(time.strptime(item[4][1],'%Y-%m-%d'))
        return item
    allData = list(map(map_fn,allData))
    def sort_fn(item):
        return item[4][1]
    allData = sorted(allData, key=sort_fn, reverse=True)
    if type != 'all':
        allData = list(filter(lambda x: x[9] == type, allData))
    row = []
    column = []
    for i in allData[:20]:
        row.append(i[3])
        if i[5].find('万') != -1:
            num = re.findall('\d+\.\d+',i[5])[0]
            column.append(int(float(num) * 10000))
        else:
            column.append(int(i[5]))
    return row,column

def getTypeList():
    allData = list(query('select * from readbookinfos',[],'select'))
    typeList = []
    for i in allData:
        typeList.append(i[9])
    return list(set(typeList))

def getCommentTimeData():
    nowSecond = time.mktime(time.localtime())
    print(nowSecond)
    allData = getAllData()
    timeThree = ['昨天', '今天', '前天']
    typeList = []
    commentsTimeList = []
    for i in allData:
        typeList.append(i[9])
        for j in i[-2]:
                commentsTimeList.append({
                    'type': i[9],
                    'commentsTime': j["commentTime"]
                })
    typeList = list(set(typeList))
    typeListData = []
    for i in typeList:
        typeListData.append({
            'type':i,
            'value':[0,0,0,0]
        })
    for i in commentsTimeList:
        for j in timeThree:
            if i['commentsTime'].find(j) != -1:
                for index,k in enumerate(typeListData):
                    if k['type'] == i['type']:
                        typeListData[index]['value'][0] += 1
            elif len(i['commentsTime']) == 5:
                second = time.mktime(time.strptime('2022-' + i['commentsTime'],'%Y-%m-%d'))
                if nowSecond - second <= 604800:
                    for index, k in enumerate(typeListData):
                        if k['type'] == i['type']:
                            typeListData[index]['value'][1] += 1
                elif nowSecond - second <= 2592000:
                    for index, k in enumerate(typeListData):
                        if k['type'] == i['type']:
                            typeListData[index]['value'][2] += 1
                elif nowSecond - second <= 7776000:
                    for index, k in enumerate(typeListData):
                        if k['type'] == i['type']:
                            typeListData[index]['value'][3] += 1
    result = []
    for i in typeListData:
        i['value'].insert(0,i['type'])
        result.append(i['value'])
    result.insert(0,['time', '三天内', '一周内', '一月内', '三月内'])
    return result

def getHeaderCountData():
    allData = list(query('select * from readbookinfos',[],'select'))
    def map_fn(item):
        item = list(item)
        if item[5].find('万') != -1:
            num = re.findall('\d+\.\d+', item[5])[0]
            item[5] = int(float(num) * 10000)
        else:
            item[5] = int(item[5])
        return item
    allData = list(map(map_fn,allData))
    dataDic = {
        '小于1000次':0,
        '小于2000次':0,
        '小于3000次':0,
        '小于6000次':0,
        '小于8000次':0,
        '大于1万次':0
    }
    for i in allData:
        count = i[5]
        if count <= 1000:
            dataDic['小于1000次'] = dataDic['小于1000次'] + 1
        elif count <= 2000:
            dataDic['小于2000次'] = dataDic['小于2000次'] + 1
        elif count <= 3000:
            dataDic['小于3000次'] = dataDic['小于3000次'] + 1
        elif count <= 6000:
            dataDic['小于6000次'] = dataDic['小于6000次'] + 1
        elif count <= 8000:
            dataDic['小于8000次'] = dataDic['小于8000次'] + 1
        else:
            dataDic['大于1万次'] = dataDic['大于1万次'] + 1
    return list(dataDic.keys()),list(dataDic.values())

def getCountByType():
    allData = getAllData()
    typeList = []
    for i in allData:
        typeList.append(i[9])
    typeList = set(typeList)
    typeData = []
    for i in typeList:
        typeData.append({
            'name':i,
            'value':0
        })
    for i in allData:
        for j in typeData:
            if i[9] == j['name']:
                j['value'] += int(i[5])

    return typeData


def getArticleData():
    allData = list(query('select * from readbookinfos',[],'select'))
    dic = {

    }
    for i in allData:
        if dic.get(i[6],-1) == -1:
            dic[i[6]] = 1
        else:
            dic[i[6]] = dic[i[6]] + 1
    print(dic)
    return list(dic.keys()),list(dic.values())

def getTagData(type='all'):
    allData = getAllData()
    if type != 'all':
        allData = list(filter(lambda x:x[9] == type,allData))
    for index,item in enumerate(allData):
        item[7] = list(filter(lambda x:x != '#',item[7]))
        print(item[7])
    dic = {}
    for i in allData:
        for j in i[7]:
            if dic.get(j,-1) == -1:
                dic[j] = 1
            else:
                dic[j] = dic[j] + 1
    dicData = []
    for key,value in dic.items():
        dicData.append({
            'name':key,
            'value':value
        })
    return dicData