
# fr = open("../output/Ymd_book_dict_BS_list_time", "r")
# fw = open("../output/Ymd_book_dict_BS_list_time_geq2.txt", "w")
while 1:
    dict_group = dict()
    lines = fr.readline()
    lines = lines.strip("\n")
    try:
        dict_group = eval(lines)
    except:
        pass
    for key in dict_group.keys():
        if len(dict_group[key]) >= 2:
            fw.write(str(dict_group)+"\n")
        fw.flush()
    if not lines:
        break
    for line in lines:
        pass
fw.close()
