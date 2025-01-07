import datetime
import numpy as np
import time

# According to the time of the data
date_min='2013-01-01'
date_max='2013-12-31'
# date_min='2005-02-16'
# date_max='2015-01-10'
date_min=datetime.datetime.strptime(date_min,"%Y-%m-%d")
date_max=datetime.datetime.strptime(date_max,"%Y-%m-%d")
file=open('../output/Ymd_book_dict_BS.txt', 'r')
file_Ymd=open('../output/Ymd_book_dict_BS_time.txt', 'w')
for line in file.readlines():
    l = dict()
    l_date=dict()
    for key in l.keys():
        # print(type(key))#str
        key_1=key.strip('[]')
        key_list=key_1.split(',')
        key_list[1].replace(' ', '')
        p = []
        for i in range(len(key_list)):
            unixdate=((float(key_list[i])*(41639-41275)+41275-70*365-19)*864000)-8*3600
            timeArray = time.localtime(unixdate)
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
            t=time_str[:10]
            p.append(t)

        l_date[str(p)]=l[key]
    file_Ymd.write(str(l_date)+'\n')
file.close()
file_Ymd.close()
def deal():
    file = open('../output/Ymd_book_dict_BS_time.txt', 'r')
    file_w = open('../output/Ymd_book_dict_BS_list_time.txt', 'w', encoding='utf-8')
    while 1:
        dict_l=dict()
        dict_t=dict()
        l=list()
        line_del=file.readline()
        line_del=line_del.strip("\n")
        if len(line_del)>2:
            try:
                dict_l=eval(line_del)
            except Exception as ex:
                print("000000|")
        for key in dict_l.keys():
                dict_t[key]=dict_l[key]
                if dict_t!= None:
                    print(dict_t)
                    file_w.write(str(dict_t)+"\n")
                dict_t.clear()

        if not line_del:
            break
        for line in line_del:
            pass
    file_w.close()
deal()