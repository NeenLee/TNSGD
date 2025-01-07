fr = open('../output/spammer groups_0.7_precision.txt', 'r')
lp = []
for line in fr:
    line = line.strip()
    lp.append(float(line))
print(lp)

fr = open('../output/spammer groups_0.7_recall.txt', 'r')
lr = []
for line in fr:
    line = line.strip()
    lr.append(float(line))
print(lr)

fw = open('../output/spammer groups_0.7_F1.txt', 'w')
for i in range(0, lp.__len__()):
    if 2 * lp[i] * lr[i] == 0:
        f1 = 0
    else:
        f1 = 2 * lp[i] * lr[i] / (lp[i] + lr[i])
    print(f1)
    fw.write(str(f1) + '\n')
fw.close()
