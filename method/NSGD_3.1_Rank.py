import datetime
import sqlite3
from math import *
import os
import time
# 最后的虚假群组
start_time = time.time()
fr = '../output/final_groups.txt'
fw = '../output/spammer groups.txt'


def find_str(str):  
    counts = 0
    file = open(fr, 'r', encoding='utf-8')
    while 1:
        l = dict()
        lines = file.readline()
        lines = lines.strip("\n")
        if len(lines) > 2:
            try:
                l = eval(lines)
            except Exception as ex:
                print("Null")
        for key in l.keys():
            time1 = l[key].count(str)
            counts += time1
        return counts


# 全局变量
con = sqlite3.connect('../dataset/DB/Books_data13.db')
cursor = con.cursor()
file_w = open(fw, 'w', encoding='utf-8')
file = open(fr, 'r', encoding='utf-8')
while 1:
    l = dict()
    ger_f = dict()
    rd_f = dict()
    gs_f = dict()
    gcar_f = dict()
    ad_f = dict()
    gor_f = dict()
    grt_f = dict()
    lines = file.readline()
    lines = lines.strip("\n")
    try:
        l = eval(lines)
    except Exception as ex:
        print("表达式为空,结束")
    community_GER = list()
    community_RD = list()
    community_gs = list()
    community_GCAR = list()
    community_AD = list()
    community_GOR = list()
    community_GRT = list()

    # GER
    for key in l.keys():
        community_rating_1_5 = 0
        community_rating_all = 0
        for i in range(len(l[key])): 
            cursor_rating = con.cursor()
            cursor_rating.execute(
                'select overall from review13 where overall in (1,5) and reviewerID= \'' + l[key][i] + '\'')
            rating_1_5 = cursor_rating.fetchall()
            community_rating_1_5 += len(rating_1_5)  #
            cursor_rating_all = con.cursor()
            cursor_rating_all.execute('select overall from review13 where  reviewerID= \'' + l[key][i] + '\'')
            rating_all = cursor_rating_all.fetchall()
            community_rating_all += len(rating_all)
        if round((community_rating_1_5 / community_rating_all), 4) > 1:
            m_end = 1
        else:
            m_end = round((community_rating_1_5 / community_rating_all), 4)
        community_GER.append(m_end)
        ger_f[key] = community_GER
        print(ger_f)
    # RD
    for key in l.keys():
        community_rating_every = 0 
        community_rating_avg = 0  
        n = 0
        x = 0
        y = 0
        community_rating_all = 0
        l_set = list(set(l[key]))
        for i in range(len(l_set)): 
            cursor_rating = con.cursor()
            cursor_rating.execute(
                'select overall from review13 where  reviewerID= \'' + l_set[i] + '\'')
            rating_every_1 = cursor_rating.fetchone()
            # print(rating_every[0])
            community_rating_all += rating_every_1[0]  
            x += 1
        community_rating_avg = community_rating_all / x
        for i in range(len(l_set)): 
            cursor_rating_all = con.cursor()
            cursor_rating_all.execute('select overall from review13 where  reviewerID= \'' + l_set[i] + '\'')
            rating_every_2 = cursor_rating_all.fetchone()
            community_rating_every = rating_every_2[0]
            n += abs(rating_every_2[0] - community_rating_avg) / 4
            y += 1
        m = n / y
        if round(m, 4) > 1:
            m_end = 1
        else:
            m_end = round(m, 4)
        community_RD.append(m_end)
        rd_f[key] = community_RD
        print(rd_f)
    # GS
    for key in l.keys():
        gs = 1 / (1 + exp(-(len(l[key]) - 3)))
        if round(gs, 4) > 1:
            m_end = 1
        else:
            m_end = round(gs, 4)
        community_gs.append(m_end)
        gs_f[key] = community_gs
    print(gs_f)
    # GCAR
    for key in l.keys():
        keys = dict()
        counts_in_time = 0
        counts_all = 0
        keys = eval(key)
        for i in range(len(l[key])):
            cursor_count = con.cursor()
            cursor_count.execute('select count(*) from review13  where reviewerID = \'' + l[key][i] + '\'')
            time1 = cursor_count.fetchone()
            counts_all += time1[0]  
            cursor_in_time = con.cursor()
            cursor_in_time.execute('select unixReviewTime from review13  where reviewerID = \'' + l[key][i] + '\'')
            user_all_time = cursor_in_time.fetchall()
            # print(user_all_time)
            time_session_start = datetime.datetime.strptime(keys[0], "%Y-%m-%d")
            time_session_end = datetime.datetime.strptime(keys[1], "%Y-%m-%d")
            days = time_session_end - time_session_start
            for i in range(len(user_all_time)):
                timeArray = datetime.datetime.utcfromtimestamp(int(user_all_time[i][0]))
                user_time = timeArray.strftime("%Y-%m-%d")
                user_time = datetime.datetime.strptime(user_time, "%Y-%m-%d")
                # print(user_time)
                if user_time - time_session_start <= days:
                    counts_in_time += 1
        x = round(counts_in_time / counts_all, 4)
        community_GCAR.append(x)
        gcar_f[key] = community_GCAR
        print(gcar_f)

        # AD
        for key in l.keys():
            avg = 0
            set_l = list(set(l[key]))
            print(len(set_l))
            for i in range(len(set_l)):
                # print(l[key][i])
                unixtime = []
                cursor_unixTime = con.cursor()
                cursor_unixTime.execute(
                    'select unixReviewTime from review13 where reviewerID=\'' + set_l[
                        i] + '\'order by unixReviewTime desc')
                review_time = cursor_unixTime.fetchall()
                for i in range(len(review_time)):
                    unixtime.append(int(review_time[i][0]))
                ad = 1 - (max(unixtime) - min(unixtime)) / (86400000 * 365)
                avg += ad
            avg = avg / len(set_l)
            if avg > 1:
                m_end = 1
            else:
                m_end = round(avg, 4)
            community_AD.append(m_end)
            ad_f[key] = community_AD
        print(ad_f)

        sumANR = 0
        for key in l.keys():
            set_l = list(set(l[key]))
            for i in range(len(set_l)):
                cursor = con.cursor()
                cursor.execute(
                    'select count(*) from review13 where reviewerID=\'' + set_l[i] + '\'group by unixReviewTime')
                rows = cursor.fetchall()
                num = len(rows)
                nor = []
                for r in rows:
                    nor.append(r[0])
                an = 0
                for i in nor:
                    if i >= 5:
                        an += 1
                anr = an / num
                sumANR += anr
            avgANR = sumANR / int(len(set_l))
            community_GOR = list()
            if avgANR > 1:
                m_end = 1
            else:
                m_end = round(avgANR, 4)
            community_GOR.append(m_end)
            gor_f[key] = community_GOR
        print(gor_f)
        # GRT
        for key in l.keys():
            set_l = list(set(l[key]))
            # print(len(set_l))
            rg = len(set_l)
            pg_list = set()
            rg_list = set()
            vg = 0
            for i in range(len(set_l)):
                cursor = con.cursor()
                cursor.execute('select reviewerID,asin from review13 where reviewerID=\'' + set_l[i] + '\'')
                rows = cursor.fetchall()
                for j in range(len(rows)):
                    pg_list.add(rows[j][1])
                    rg_list.add(rows[j][0])
                    if len(rg_list) > 0:
                        if set_l[i] in rg_list:
                            vg += 1
            grt = vg / (rg * len(pg_list))
            if grt > 1:
                m_end = 1
            else:
                m_end = round(grt, 4)
            community_GRT.append(m_end)
            grt_f[key] = community_GRT

        print(grt_f)
        list_AVG = list()
        for i in range(1):
            list_AVG.append(round((community_RD[i] + community_GER[i] + community_GCAR[i] + community_GRT[i] +
                                   community_GOR[i] + community_gs[i]) / 6, 4))
        print(list_AVG)
        file_w.write(str(list_AVG[0]) + "\n")
        file_w.flush()
        print("+++++++++++++++++")
    if not lines:
        break
    for line in lines:
        pass
file_w.close()
end_time = time.time()
print(end_time-start_time)