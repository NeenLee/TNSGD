import sqlite3
import datetime
import time
#群组净化+打标签#
#还没写完//2022/4/7
start_time = time.time()
con = sqlite3.connect('G:\\DB\\Books_data13.db')
cursor = con.cursor()
fr = open('../output/candidate groups merge norepeat.txt', 'r')
fw = open('../output/final groups.txt','w')
# date_min = '2005-02-16'
# date_max = '2015-01-10'

# date_min = datetime.datetime.strptime(date_min, "%Y-%m-%d")
# date_max = datetime.datetime.strptime(date_max, "%Y-%m-%d")
count_num_line = 0
while 1:
    count_num_line += 1
    print(f"第{count_num_line}次循环")

    dict_all = dict()
    dict_all_group = dict()
    line_EXR_dict = dict()
    line_MNR_dict = dict()
    line_AD_dict = dict()
    line_ATR_dict = dict()
    line_RD_dict = dict()
    lines = fr.readline()
    lines = lines.strip("\n")
    try:
        dict_all = eval(lines)
    except Exception as ex:
        end_time = time.time()
        print(start_time - end_time)
        print("空")
    for key in dict_all.keys():
        list_EXR = list()
        list_MNR = list()
        list_AD = list()
        list_ATR = list()
        list_RD = list()
        #EXR
        dict_all[key] = list(dict_all[key])
        for i in range(len(dict_all[key])):
            cursor.execute('select overall from review13 where reviewerID=\"' + dict_all[key][i] + '\"')
            rows = cursor.fetchall()
            sum = len(rows)
            cou = 0
            cc = 0
            for r in rows:
                cc += 1
                if r[0] == 1 or r[0] == 5:
                    cou += 1
            sum = cc
            # print(sum)
            ratio = cou / sum
            list_EXR.append(round(ratio, 4))
        line_EXR_dict[key] = list_EXR
        print(line_EXR_dict)
        #MNR
        for i in range(len(dict_all[key])):
            cursor.execute(
                'select count(*) from review13 where reviewerID=\"' + dict_all[key][i] + '\" group by unixReviewTime')
            rows = cursor.fetchall()
            # print(rows)
            num = len(rows)
            nor = []
            # 计算平均一天评论数
            sum = 0
            for r in rows:
                sum += r[0]
                nor.append(r[0])
            avgR = num / sum
            list_MNR.append(round(avgR, 4))
        line_MNR_dict[key] = list_MNR
        print(line_MNR_dict)
        #RD
        for i in range(len(dict_all[key])):
            cursor.execute('select overall,asin from review13 where reviewerID=\"' +  dict_all[key][i]  + '\"')
            rows = cursor.fetchall()
            num = len(rows)
            a = 0
            div = 0
            for r in rows:
                rat = r[0]
                asin = r[1]
                # 计算产品平均评分
                cursor.execute('select avg(overall) from review13 where asin=\"' + asin + '\"')
                lines = cursor.fetchall()
                avgp = lines[0][0]
                # print('平均评分:' + str(avgp))
                divsum = abs((rat - avgp))
                if divsum >= 0.5:
                    a += 1
                div = a / num
            list_RD.append(round(div, 4))
        line_RD_dict[key] = list_RD
        print(line_RD_dict)

        #ATR

        # set_l = list(set(dict_all[key]))
        grt = 0
        for i in range(len(dict_all[key])):
            cursor = con.cursor()
            cursor.execute('select count(*),count(distinct asin) from review13 where reviewerID=\"' +  dict_all[key][i]  + '\"')
            rows = cursor.fetchall()
            # print(rows[0][0], rows[0][1])
            rg = len(dict_all[key])
            vg = rows[0][0]
            pg = rows[0][1]
            grt = vg / (rg + pg)
        # grt = grt / len(set_l)
            list_ATR.append(round(grt,4))
        line_ATR_dict[key] = list_ATR
        print(line_ATR_dict)
        #AD
        for i in range(len(dict_all[key])):
            unixtime = []
            cursor_unixTime = con.cursor()
            cursor_unixTime.execute(
                'select unixReviewTime from review13 where reviewerID=\'' + dict_all[key][i] + '\'order by unixReviewTime desc')
            review_time = cursor_unixTime.fetchall()
            # print(review_time)
            for i in range(len(review_time)):
                unixtime.append(int(review_time[i][0]))
            ad = 1 - (max(unixtime) - min(unixtime)) / (86400000 * 365)
            list_AD.append(round(ad, 4))
        line_AD_dict[key] = list_AD
        print(line_AD_dict)

        list_AVG = list()
        for i in range(len(dict_all[key])):
            list_AVG.append(round((list_RD[i]+list_EXR[i]+list_ATR[i]+list_AD[i]+list_MNR[i]),4))
        print(list_AVG)
        dict_all_group = dict_all
        print("dict_all_group"+str(dict_all_group))
        num = 0
        for key in dict_all.keys():
            num = 0
            counter = 0
            group = []
            index_to_delete = []
            # 记录需要净化的dict_all_group中的元素的index
            for avg in list_AVG:
                if avg < 3:
                    index_to_delete.append(num)
                num += 1
            print("index_to_delete = ", index_to_delete)
            # 将需要净化的元素按照上一步记录的index删除掉
            for index in index_to_delete:
                index = index - counter
                dict_all_group[key].pop(index)
                counter += 1
        print("净化后dict_all_group" + str(dict_all_group))
        if len(dict_all_group[key]) != 0:
            fw.write(str(dict_all_group) + "\n")
            fw.flush()
        else:
            print("dict_all_group全部净化掉，不写入文件")

    if not lines:
        break
    for line in lines:
        pass
