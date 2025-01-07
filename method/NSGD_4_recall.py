# fr=open('Book_30_0_3/虚假群组/标签top_300.txt', 'r')
# label=[]
# for line in fr:
#     line=line.strip()
#     label.append(int(line))
# print(label)
#
# sum=0
# fw=open('Book_30_0_3/虚假群组/虚假群组标签精确度top_300.txt', 'w')
# for i in range(0,label.__len__()):
#     if label[i]==0:
#         sum=sum+1
#     ratio=sum/(i+1)
#     print(ratio)
#     fw.write(str(ratio)+'\n')
fr=open('../output/spammer_group_排序_0.7.txt', 'r')
label = []
for line in fr:
    line = line.strip()
    label.append(int(line))
print(label)

sum = sum(label)
count = 0
break_count = 0
fw=open('../output/spammer_group_排序_0.7_recall.txt', 'w')
for i in range(0, label.__len__()):
    count = count + label[i]
    ratio = count / sum
    print(ratio)
    fw.write(str(ratio) + '\n')
    break_count += 1
    if break_count == 300:
        break
fr.close()
fw.close()