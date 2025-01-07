# -*- coding: utf-8 -*-


fr = open('../output/spammer groups_0.7.txt', 'r')
label = []
for line in fr:
    line = line.strip()
    label.append(int(line))
print(label)
break_count = 0
sum = 0
fw = open('../output/spammer groups_0.7_precision.txt', 'w')
for i in range(0, label.__len__()):
    sum = sum + label[i]
    ratio = sum / (i + 1)
    print(ratio)
    fw.write(str(ratio) + '\n')
    break_count += 1
    if break_count == 300:
        break
fr.close()
fw.close()
