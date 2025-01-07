import operator
import sys
import time

import numpy as np

start_time = time.time()
np.set_printoptions(suppress=True, threshold=sys.maxsize)
file = open('../output/book_dict.txt', 'r', encoding='gb18030', errors='ignore')
file_division_block = open('../output/Ymd_book_dict_BS.txt', 'w')
nodelist = dict()
nodelist = eval(file.read())
for key in list(nodelist.keys()):
    print(f"<<<<<<<< {key} begin >>>>>>>>>")
    nodelist_block = dict()
    truncation_j = []
    nodelist_division_block = list()
    print(nodelist[key])
    for j in range(0, len(nodelist[key]) - 1):
        if abs(nodelist[key][j + 1][1] - nodelist[key][j][1]) >= 0.002739 * 3:  # 0.001940是归一化时间之后的间隔一周的时间段。
            print(nodelist[key][j][1], nodelist[key][j + 1][1])
            truncation_j.append(j + 1)
    m = []  
    l = dict()
    m = np.split(nodelist[key], truncation_j)
    print(m)
    for i in range(len(m)):
        temp = []
        t = []
        n = []  
        for j in range(len(m[i])):
            temp.append(m[i][j][1])
            n.append(str(m[i][j][0])) 
        min_index, min_number = min(enumerate(temp), key=operator.itemgetter(1))
        max_index, max_number = max(enumerate(temp), key=operator.itemgetter(1))
        t.append(float(min_number))
        t.append(float(max_number))
        l[str(t)] = n
    print(f'{key}:{l}')
    file_division_block.write(str(l) + '\n')
file_division_block.close()
end_time = time.time()
print(end_time - start_time)


