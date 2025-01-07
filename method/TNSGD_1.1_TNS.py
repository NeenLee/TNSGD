import json

from torch.utils.data import Dataset 
import numpy as np
import sys
import random


class TNS(Dataset):

    def __init__(self, file_path, neg_size, hist_len, directed=False, transform=None):
    
        self.neg_size = neg_size
        self.hist_len = hist_len
        self.directed = directed
        self.transform = transform
        self.max_d_time = -sys.maxsize  
        
        self.NEG_SAMPLING_POWER = 0.75
        self.neg_table_size = int(1e3)
        self.node2hist = dict() 
        self.node_set = set()  
        
        self.degrees = dict()
        with open(file_path, 'r') as infile:
            for line in infile:
                parts = line.split()
         
                s_node = str(parts[0]) # source node
                t_node = str(parts[1])# target node
                d_time = float(parts[2])  
                self.node_set.update([s_node, t_node])
                if s_node not in self.node2hist:
                    self.node2hist[s_node] = list()
                self.node2hist[s_node].append((t_node, d_time))

                if not directed:               
                    if t_node not in self.node2hist:                
                        self.node2hist[t_node] = list()             
                    self.node2hist[t_node].append((s_node, d_time)) 
                
                if d_time > self.max_d_time:    
                    self.max_d_time = d_time

                if s_node not in self.degrees:  #dict={key1:value1,key2:value2}
                    self.degrees[s_node] = 0   
                if t_node not in self.degrees:  
                    self.degrees[t_node] = 0   
                self.degrees[s_node] += 1       
                self.degrees[t_node] += 1

        self.node_dim = len(self.node_set)      
        print(self.node_dim)
        print(">>>>>>>>>>>>>>>>")
        self.data_size = 0                      
        for s in self.node2hist:                
            hist = self.node2hist[s]            
            hist = sorted(hist, key=lambda x: x[1])
            self.node2hist[s] = hist            
            self.data_size += len(self.node2hist[s])

        # self.idx2source_id = np.zeros((self.data_size,), dtype=np.int32)
        # self.idx2target_id = np.zeros((self.data_size,), dtype=np.int32)
        s = np.dtype('U4', align=True)
        self.idx2source_id = np.zeros((self.data_size,),dtype=s)  
        self.idx2target_id = np.zeros((self.data_size,),dtype=s)
        idx = 0

    
        for s_node in self.node2hist:          
            for t_idx in range(len(self.node2hist[s_node])):
                self.idx2source_id[idx] = s_node
                self.idx2target_id[idx] = t_idx
                idx += 1

        self.neg_table = np.zeros((self.neg_table_size,))
        # a = self.init_neg_table()
        # l_key=['A24Z79OS5VQA7Y','A1LST4I72EIH9P','A1NBZBMP1UKQSQ','A1GUNBQDH7YE86','A1LYFI8TUCB1QX','A1JI83RLITTQST','A1EQGFZPJ4V24X','A1JLU5H1CCENWX','A1MU8E76C6HXW4','A1NJHOGKZZRAX8','A1B7DR0K0VCMM','A1098Z3D7ENJ2F','A1K7TUXGIPEB6T','A1JRQ2J7QYHM2S','A17F3JQAMH2L1U','A29HGTDKDXB7T8','A142FJF6Z56NYP','A1B9WI8TVGG0O','A1MXWIY7A5V3CZ','A1LEQYV3H572Y1','A1PYPC0SGTL8PV','A10WE4JQOHF6H2','A12F1OPZ17YHBS','A2F6N60Z96CAJI','A1CGAU176MRXGD','A1GQAKL9CGQLP1','A1JIZ2Y8VG90AI','A16BI2XOSTGBBC','A14P4UH613ZFQZ','A1J0CB2ZMZK13O']
        l = dict()
        l = self.node2hist
        with open("dataset/book_dict.txt", "w",encoding='gb18030',errors="ignore") as f:
            for key in list(l.keys()):
                l_30 = dict()
                if len(l[key]) < 10 :
                    # print(key,len(nodelist[key]))
                    del l[key]
                # if key in l_key :
                #     l_30[key]=l[key]
                # if l_30!={}:
                #     f.write(str(l_30)+"\n")
            f.write(str(l))
        f.close()
        # ///使用l[key]内的值找出来需要的


    def get_node_dim(self):
        return self.node_dim
    def get_max_d_time(self):
        return self.max_d_time

    def init_neg_table(self):
        tot_sum, cur_sum, por = 0., 0., 0.
        n_id = 0
        for k in range(self.node_dim):
            tot_sum += np.power(self.degrees[k], self.NEG_SAMPLING_POWER)
        for k in range(self.neg_table_size):
            if (k + 1.) / self.neg_table_size > por:
                cur_sum += np.power(self.degrees[n_id], self.NEG_SAMPLING_POWER)
                por = cur_sum / tot_sum
                n_id += 1
            self.neg_table[k] = n_id - 1
            return self.neg_table





    def __len__(self):
        return self.data_size

    def __getitem__(self, idx):
        s_node = self.idx2source_id[idx]
        t_idx = self.idx2target_id[idx]
        t_node = self.node2hist[s_node][t_idx][0]
        t_time = self.node2hist[s_node][t_idx][1]
        if t_idx - self.hist_len < 0:
            hist = self.node2hist[s_node][0:t_idx]

        else:
            hist = self.node2hist[s_node][t_idx - self.hist_len:t_idx]

        hist_nodes = [h[0] for h in hist]
        hist_times = [h[1] for h in hist]

        np_h_nodes = np.zeros((self.hist_len,))
        np_h_nodes[:len(hist_nodes)] = hist_nodes
        np_h_times = np.zeros((self.hist_len,))
        np_h_times[:len(hist_times)] = hist_times
        np_h_masks = np.zeros((self.hist_len,))
        np_h_masks[:len(hist_nodes)] = 1.

        neg_nodes = self.negative_sampling()
        
        sample = {
            'source_node': s_node,
            'target_node': t_node,
            'target_time': t_time,
            'history_nodes': np_h_nodes,
            'history_times': np_h_times,
            'history_masks': np_h_masks,
            'neg_nodes': neg_nodes,
        }
        if self.transform:
            sample = self.transform(sample)

        return sample


    def negative_sampling(self):
        rand_idx = np.random.randint(0, self.neg_table_size, (self.neg_size,))
        sampled_nodes = self.neg_table[rand_idx]
        print("++++++++++++++++++++++++++++++++++++++")
        # print(self.node2hist)
        return sampled_nodes


if __name__ == '__main__':
    data = TNS(file_path='dataset/book10.txt', neg_size=None, hist_len=None, directed=False)
    # l = list(data)
    # with open("book_30_0_dict_time.txt", "w") as f:  # neg_size=10
    #     for line in l:
    #         f.write(str(line) + '\n')
    #     f.close()