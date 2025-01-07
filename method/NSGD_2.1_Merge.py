import linecache
import time


def jaccard_similarity(x,y):
    intersection_cardinality=len(set.intersection(*[set(x),set(y)]))
    union_cardinality=len(set.union(*[set(x),set(y)]))
    return intersection_cardinality/float(union_cardinality)
def getline(the_file_path, line_number):
  if line_number < 1:
    return ''
  for cur_line_number, line in enumerate(open(the_file_path, 'rU')):
    if cur_line_number == line_number-1:
      return line
  return ''
def findRepeat(readPath, writePath):
    lines_seen = set()
    outfiile = open(writePath, 'a+', encoding='utf-8')
    f = open(readPath, 'r', encoding='utf-8')
    sum = 0
    for line in f:
        if line not in lines_seen:
            sum += 1
            outfiile.write(line)
            lines_seen.add(line)
    print(sum)

def combine(frStr,fwStr):
    fr = open(frStr, "r")
    fw = open(fwStr, "w")
    jump = []
    num = 0
    while 1:
        num += 1
        lines = fr.readline()
        if not lines:
            break
        for line in lines:
            pass
    for i in range(1,num):
        dict_group_j = dict()
        dict_group_i = dict()
        fw_dict = dict()
        print(f"第{i}次循环开始，共{num}次循环")
        if i not in jump:
            the_line = linecache.getline(frStr, i)
            the_line = the_line.strip("\n")
            try:
                dict_group_i = eval(the_line)
            except:
                pass
            key_i = list(dict_group_i.keys())
            n = 0
            for j in range(1,num):
                if j == i:
                    continue
                the_line = linecache.getline(frStr, j)
                the_line = the_line.strip("\n")
                try:
                    dict_group_j = eval(the_line)
                except:
                    pass
                key_j = list(dict_group_j.keys())
                # print(key_i[0] , (key_j[0]))
                # 如果下面的if写了就n+1,就不写没改变的，如果没写就写源文件没有相似的群组。
                if key_i[0] == (key_j[0]) and jaccard_similarity(dict_group_i[key_i[0]],dict_group_j[key_j[0]]) >= 0.5 and jaccard_similarity(dict_group_i[key_i[0]], dict_group_j[key_j[0]]) != 1:
                    fw_dict[key_i[0]] = set(dict_group_i[key_i[0]] + dict_group_j[key_j[0]])
                    fw.write(str(fw_dict)+"\n")
                    print(str(fw_dict))
                    n = n + 1
                    jump.append(j)
            if n == 0:
                fw.write(str(dict_group_i) + "\n")
            fw.flush()
        else:

            print(f"跳过第{i}行")
    # and jaccard_similarity(dict_group_i[key_i[0]], dict_group_j[key_j[0]]) != 1
if __name__ == '__main__':
    start_time = time.time()
    frStr = "../output/Ymd_book_dict_BS_list_time.txt"
    fwStr = "../output/candidate groups merge.txt"
    fwStr_norepeat = "../output/candidate groups merge norepeat.txt"
    combine(frStr,fwStr)
    findRepeat(fwStr,fwStr_norepeat)
    end_time = time.time()
    print(end_time-start_time)