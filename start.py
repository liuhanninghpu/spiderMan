from multiprocessing import Process
from scrapy import cmdline
import time
import logging
from lib import MysqlHelper
import json

def start_spider(name,seleep_times,params,next_time,frequence):
    if params is not None:
        paramsDict = json.loads(params)
        args = ["scrapy", "crawl", name, "-a","cid="+str(paramsDict['cid'])]
    else:
        args = ["scrapy", "crawl", name]
    start = time.time()
    p = Process(target=cmdline.execute, args=(args,))
    p.start()
    p.join()
    logging.debug("### use time: %s" % (time.time() - start))
    updatePosition()
    time.sleep(1)

def updatePosition():
    pass



def getConf():
    mysqlHelper = MysqlHelper.MysqlHelper('localhost', 'root', '123456789', 'spider', 3306)
    mysqlHelper.connect()
    sql = "select id,spider_name,seleep_time,last_time,params,next_time,frequence from spider_conf where 1=1"
    result = mysqlHelper.fetchall(sql,None)
    taskList = {}
    for task in result:
        if task[0] in taskList:
            taskList[task[0]].update({
                'name':task[1],
                'seleep_times':task[2],
                'last_time':task[3],
                'params':task[4],
                'next_time':task[5],
                'frequence':task[6]
            })
        else:
            taskList.update({task[0]:{
                'name': task[1],
                'seleep_times': task[2],
                'last_time': task[3],
                'params': task[4],
                'next_time':task[5],
                'frequence':task[6]
            }})
    return taskList


def chcekConf(conf):
    #检查是否到执行时间
    now = int(time.time())
    if conf['next_time'] is not None and conf['next_time'] <= now:
        print('没有到执行时间')
        exit()

#更新任务
# def updateConfig():
#     mysqlHelper = MysqlHelper.MysqlHelper('localhost', 'root', '123456789', 'spider', 3306)
#     mysqlHelper.connect()
#     date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
#     cid_map = getCidMap()
#     for cid,cityName in cid_map.items():
#         params = {
#             'cid':cid,
#         }
#         jsonStr = json.dumps(params)
#         sql = "insert into spider_conf(spider_name,spider_frequence,last_time,update_time,create_time,params) values(%s,%s,%s,%s,%s,%s)"
#         params = ['films_now',24,0,date_time,date_time,jsonStr]
#         mysqlHelper.insert(sql,params)
#     mysqlHelper.close()

if __name__ == '__main__':
    confs = getConf()
    for id,conf in confs.items():
        print("params:"+str(conf['params']))
        chcekConf(conf)
        process = Process(target=start_spider, args=(conf['name'],conf['seleep_times'],conf['params'],conf['next_time'],conf['frequence']))
        process.start()
        time.sleep(5)
