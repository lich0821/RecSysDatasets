# @Time   : 2020/9/18
# @Author : Shanlei Mu
# @Email  : slmu@ruc.edu.cn


import os
import re
import bz2
import csv
import time
import json
import operator
import numpy as np
import pandas as pd

from datetime import datetime
from tqdm import tqdm

from src.base_dataset import BaseDataset


class ML1MDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(ML1MDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'ml-1m'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings.dat')
        self.item_file = os.path.join(self.input_path, 'movies.dat')
        self.user_file = os.path.join(self.input_path, 'users.dat')
        self.sep = '::'

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

    def load_inter_data(self):
        return pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')


class ML10MDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(ML10MDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'ml-10m'

        # input_path
        self.inter_file = os.path.join(self.input_path, 'ratings.dat')
        self.item_file = os.path.join(self.input_path, 'movies.dat')

        self.sep = '::'

        # output_path
        output_files = self.get_output_files()
        self.output_inter_file = output_files[0]
        self.output_item_file = output_files[1]

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'movie_name:token_seq',
                            2: 'type:token_seq'}

    def load_inter_data(self):
        return pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')

    def load_item_data(self):
        origin_data = pd.read_csv(self.item_file, delimiter=self.sep, header=None, engine='python')
        processed_data = origin_data
        for i in range(origin_data.shape[0]):
            split_type = origin_data.iloc[i, 2].split('|')
            type_str = ' '.join(split_type)
            processed_data.iloc[i, 2] = type_str
        return processed_data


class AVAZUDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AVAZUDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'avazu'

        # input path
        self.inter_file = os.path.join(self.input_path, 'train')

        self.sep = ','

        # output path
        output_file = self.get_output_files()
        self.output_inter_file = output_file[0]

        # selected feature fields
        self.inter_fields = {0: 'item_id:token',
                             1: 'label:float',
                             2: 'timestamp:float',
                             3: 'C1:token',
                             4: 'banner_pos:float',
                             5: 'site_id:token',
                             6: 'site_domain:token',
                             7: 'site_category:token',
                             8: 'app_id:token',
                             9: 'app_domain:token',
                             10: 'app_category:token',
                             11: 'device_id:token',
                             12: 'device_ip:token',
                             13: 'device_model:token',
                             14: 'device_type:token',
                             15: 'device_conn_type:token',
                             16: 'C14:token',
                             17: 'C15:token',
                             18: 'C16:token',
                             19: 'C17:token',
                             20: 'C18:token',
                             21: 'C19:token',
                             22: 'C20:token',
                             23: 'C21:token'}

    def load_inter_data(self):
        table = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        # remove head line
        return table.iloc[1:]


class ADULTDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(ADULTDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'adult'

        # input path
        self.inter_file = os.path.join(self.input_path, 'adult.data')

        self.sep = ', '

        # output path
        output_file = self.get_output_files()
        self.output_inter_file = output_file[0]

        # selected feature fields
        self.inter_fields = {0: 'age:float',
                             1: 'work_class:token',
                             2: 'final_weight:float',
                             3: 'education:token',
                             4: 'education_num:float',
                             5: 'marital_status:token',
                             6: 'occupation:token',
                             7: 'relationship:token',
                             8: 'race:token',
                             9: 'sex:token',
                             10: 'capital_gain:float',
                             11: 'capital_loss:float',
                             12: 'hours_per_week:float',
                             13: 'native_country:token_seq',
                             14: 'label:float'}

    def load_inter_data(self):
        table = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        for i in range(table.shape[0]):
            table.iloc[i, 14] = 1 if table.iloc[i, 14] == ">50K" else 0
            table.iloc[i, 13] = table.iloc[i, 13].replace('-', ' ')
        return table


class TMALLDataset(BaseDataset):
    def __init__(self, input_path, output_path, repeat=True):
        super(TMALLDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'tmall'
        self.repeat = repeat
        if self.repeat:
            postfix = '-sums'
        else:
            postfix = ''
        self.buy_dataset_name = self.dataset_name + '-buy' + postfix
        self.click_dataset_name = self.dataset_name + '-click' + postfix

        # input path
        self.inter_file = os.path.join(self.input_path, 'ijcai2016_taobao.csv')

        self.sep = ','

        # output path
        self.output_inter_file = self.get_output_paths()

        # selected feature fields
        if self.repeat:
            self.inter_fields = {0: 'user_id:token',
                                 1: 'seller_id:token',
                                 2: 'item_id:token',
                                 3: 'category_id:token',
                                 4: 'timestamp:float',
                                 5: 'interactions:float'}
        else:
            self.inter_fields = {0: 'user_id:token',
                                 1: 'seller_id:token',
                                 2: 'item_id:token',
                                 3: 'category_id:token',
                                 4: 'timestamp:float'}

    def get_output_paths(self):
        buy_output_path = os.path.join(self.output_path, self.buy_dataset_name)
        click_output_path = os.path.join(self.output_path, self.click_dataset_name)

        if not os.path.isdir(buy_output_path):
            os.makedirs(buy_output_path)
        if not os.path.isdir(click_output_path):
            os.makedirs(click_output_path)

        buy_inter_file = os.path.join(buy_output_path, self.buy_dataset_name + '.inter')
        click_inter_file = os.path.join(click_output_path, self.click_dataset_name + '.inter')
        output_inter_file = (click_inter_file, buy_inter_file)

        return output_inter_file

    def load_inter_data(self):
        click_table, buy_table = [], []
        f = '%Y%m%d'
        with open(self.inter_file, encoding='utf-8') as fp:
            lines = fp.readlines()[1:]
            for line in tqdm(lines):
                words = line.strip().split(self.sep)
                time = int(datetime.strptime(words[5], f).timestamp())
                words[5] = str(time)
                label = words.pop(4)
                if label == '0':
                    click_table.append(words)
                else:
                    buy_table.append(words)
        return click_table, buy_table

    def convert_inter(self):
        try:
            click_table, buy_table = self.load_inter_data()
            click_output_path, buy_output_path = self.output_inter_file
            if self.repeat:
                click_dict, buy_dict = self.merge_repeat(click_table, buy_table)
                # write -click file
                with open(click_output_path, 'w') as cf:
                    cf.write('\t'.join([self.inter_fields[i] for i in range(len(self.inter_fields))]) + '\n')
                    for k, v in tqdm(click_dict.items()):
                        cf.write('\t'.join([str(item) for item in list(k) + v]) + '\n')
                # write -buy file
                with open(buy_output_path, 'w') as bf:
                    bf.write('\t'.join([self.inter_fields[i] for i in range(len(self.inter_fields))]) + '\n')
                    for k, v in tqdm(buy_dict.items()):
                        bf.write('\t'.join([str(item) for item in list(k) + v]) + '\n')
            else:
                # write -click file
                with open(click_output_path, 'w') as cf:
                    cf.write('\t'.join([self.inter_fields[i] for i in range(len(self.inter_fields))]) + '\n')
                    for line in tqdm(click_table):
                        cf.write('\t'.join(line) + '\n')
                # write -buy file
                with open(buy_output_path, 'w') as bf:
                    bf.write('\t'.join([self.inter_fields[i] for i in range(len(self.inter_fields))]) + '\n')
                    for line in tqdm(buy_table):
                        bf.write('\t'.join(line) + '\n')
        except NotImplementedError:
            print('This dataset can\'t be converted to inter file\n')

    def merge_repeat(self, click_table, buy_table):
        click_dict, buy_dict = {}, {}
        for line in click_table:
            key = tuple(line[:-1])
            time = line[-1]
            if key in click_dict:
                click_dict[key][0] = time
                click_dict[key][1] += 1
            else:
                click_dict[key] = [time, 1]
        for line in buy_table:
            key = tuple(line[:-1])
            time = line[-1]
            if key in buy_dict:
                buy_dict[key][0] = time
                buy_dict[key][1] += 1
            else:
                buy_dict[key] = [time, 1]
        return click_dict, buy_dict


class NETFLIXDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(NETFLIXDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'netflix'

        # input pathgit
        self.inter_file = os.path.join(self.input_path, 'netflix_data')

        self.sep = ','

        # output path
        output_file = self.get_output_files()
        self.output_inter_file = output_file[0]

        # selected feature fields
        self.inter_fields = {0: 'item_id:token',
                             1: 'user_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        # preprocess raw data file
        raw_file_list = ['combined_data_1.txt', 'combined_data_2.txt', 'combined_data_3.txt', 'combined_data_4.txt']
        raw_path_list = [os.path.join(self.input_path, raw_file) for raw_file in raw_file_list]
        lines_list = [open(raw_path, encoding='utf-8').read().strip().split('\n') for raw_path in raw_path_list]
        time_format = '%Y-%m-%d'
        with open(self.inter_file, 'w') as fp:
            for lines in lines_list:
                i = 0
                while i < len(lines):
                    u_id = lines[i].replace(':', ',')
                    i += 1
                    while i < len(lines) and lines[i][-1] != ':':
                        words = lines[i].strip().split(',')
                        words[-1] = str(int(datetime.strptime(words[-1], time_format).timestamp()))
                        fp.write(u_id + ','.join(words) + '\n')
                        i += 1

    def load_inter_data(self):
        return pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')


class CRITEODataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(CRITEODataset, self).__init__(input_path, output_path)
        self.dataset_name = 'criteo'

        # input_path
        self.input_file = os.path.join(self.input_path, 'train.txt')
        self.sep = '\t'

        # output_path
        self.output_file = os.path.join(output_path, 'criteo.inter')

        # selected feature fields
        self.fields = {0: 'label:token'}
        for i in range(1, 14):
            self.fields[i] = "I" + str(i) + ":float"
        for i in range(14, 40):
            self.fields[i] = "C" + str(i - 13) + ":token"

    def convert_inter(self):
        # convert
        fin = open(self.input_file, "r")
        fout = open(self.output_file, "w")
        fout.write('\t'.join([self.fields.get(i) for i in self.fields.keys()]) + '\n')

        # Get file rows 
        lines_count = 0
        for _ in fin:
            lines_count += 1
        fin.seek(0, 0)

        # lines_count = 45850617
        for j in tqdm(range(lines_count)):
            line = fin.readline()
            line_list = line.split('\t')
            for i in range(1, 14):
                if line_list[i] != "":
                    line_list[i] = float(line_list[i])
            fout.write('\t'.join([str(line_list[i])
                                  for i in range(len(line_list))]))
        fin.close()
        fout.close()


class FOURSQUAREDataset(BaseDataset):
    def __init__(self, input_path, output_path, merge_repeat=True):
        super(FOURSQUAREDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'foursquare'
        self.merge_repeat = merge_repeat

        # input file
        # self.input_file_NYC="../raw_data/foursquare/formytest.csv"
        self.input_file_NYC = os.path.join(self.input_path, "dataset_TSMC2014_NYC.csv")
        self.input_file_TKY = os.path.join(self.input_path, "dataset_TSMC2014_TKY.csv")

        # output file
        # self.output_file_NYC = os.path.join(output_path, 'formytest.inter')
        self.output_file_NYC = os.path.join(output_path, 'foursquare_NYC.inter')
        self.output_file_TKY = os.path.join(output_path, 'foursquare_TKY.inter')

        # selected feature fields
        self.fields = {0: 'user_id:token',
                       1: 'venue_id:token',
                       2: 'venue_category_id:token',
                       3: 'venue_category_name:str',
                       4: 'latitude:float',
                       5: 'longitude:float',
                       6: 'timezone_offset:float',
                       7: 'timestamp:str',
                       8: 'click_times:float'}

    def utc_to_timestamp(self, utc_time):
        # change utc-time to timestamp
        timeArray = time.strptime(utc_time, "%a %b %d %H:%M:%S %z %Y")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def click_count_process(self, data_without_count, info_len=2):
        result = pd.DataFrame(columns=data_without_count.columns)
        result['click_times'] = ''

        # use dict to recard
        n_dict = {}
        info_dict = {}

        # change to list
        data_list = data_without_count.values.tolist()

        for i in tqdm(range(len(data_without_count))):
            user_item_tp = tuple(data_list[i][:info_len])
            if user_item_tp not in info_dict:
                n_dict[user_item_tp] = 1
                info_dict[user_item_tp] = tuple(data_list[i][info_len:])
            elif info_dict.get(user_item_tp)[-1] < data_list[i][-1]:
                n_dict[user_item_tp] = n_dict[user_item_tp] + 1
                info_dict[user_item_tp] = tuple(data_list[i][info_len:])

        for key, value in tqdm(info_dict.items()):
            key_list = list(key)
            key_list.extend(info_dict[key])
            key_list.append(n_dict[key])
            result.loc[len(result)] = key_list

        return result

    def convert_inter(self):
        # load data
        data_NYC = pd.read_csv(self.input_file_NYC, header=0, engine='python')
        data_TKY = pd.read_csv(self.input_file_TKY, header=0, engine='python')

        # print(1)
        # data process
        fout_NYC = open(self.output_file_NYC, "w")
        fout_TKY = open(self.output_file_TKY, "w")
        fout_NYC.write('\t'.join([self.fields.get(i) for i in self.fields.keys()]) + '\n')
        fout_TKY.write('\t'.join([self.fields.get(i) for i in self.fields.keys()]) + '\n')

        # utc time to timestamp
        data_NYC.iloc[:, -1] = [self.utc_to_timestamp(x[-1]) for x in data_NYC.values.tolist()]
        data_TKY.iloc[:, -1] = [self.utc_to_timestamp(x[-1]) for x in data_TKY.values.tolist()]

        # count
        if self.merge_repeat == True:
            data_NYC = self.click_count_process(data_NYC)
            data_TKY = self.click_count_process(data_TKY)

        for i in tqdm(range(data_NYC.shape[0])):
            fout_NYC.write('\t'.join([str(data_NYC.iloc[i, j])
                                      for j in range(data_NYC.shape[1])]) + '\n')
        fout_NYC.close()
        print("The NYC part of Dataset FOURSQUARE has finished.")

        for i in tqdm(range(data_TKY.shape[0])):
            fout_TKY.write('\t'.join([str(data_TKY.iloc[i, j])
                                      for j in range(data_TKY.shape[1])]) + '\n')
        fout_TKY.close()
        print("The TKY part of Dataset FOURSQUARE has finished.")


class DIGINETICADataset(BaseDataset):
    def __init__(self, input_path, output_path, merge_repeat=True):
        super(DIGINETICADataset, self).__init__(input_path, output_path)
        self.dataset_name = 'DIGINETICA'
        self.merge_repeat = merge_repeat
        # 'item' part
        self.fields_item = {0: 'item_id:token',
                            1: 'item_priceLog2:float',
                            2: 'item_name:token',
                            3: 'item_category:token'}

        self.input_file_prod = os.path.join(self.input_path, "products.csv")
        self.input_file_prod_cate = os.path.join(self.input_path, "product-categories.csv")
        self.output_file_prod = os.path.join(self.output_path, 'diginetica.item')

        # 'inter' part
        if self.merge_repeat == True:
            self.fields_inter = {0: 'session_id:token',
                                 1: 'item_id:token',
                                 2: 'timestamp:float',
                                 3: 'repeat_times:float'}
        else:
            self.fields_inter = {0: 'session_id:token',
                                 1: 'item_id:token',
                                 2: 'timestamp:float'}
        self.input_file_item_views = os.path.join(self.input_path, "train-item-views.csv")
        self.output_file_inter = os.path.join(self.output_path, 'diginetica.inter')

    def item_process(self):
        cate_dict = {}
        data_prod_cate_list = self.data_prod_cate.values.tolist()
        for i in tqdm(range(len(data_prod_cate_list))):
            cate_dict[data_prod_cate_list[i][0]] = data_prod_cate_list[i][1]
        return cate_dict

    def convert_item(self):
        # item part
        self.data_prod_cate = pd.read_csv(self.input_file_prod_cate, delimiter=';', header=0, engine='python')
        cate_dict = self.item_process()

        fin = open(self.input_file_prod, 'r')
        fout_prod = open(self.output_file_prod, "w")
        fout_prod.write('\t'.join([self.fields_item.get(i) for i in self.fields_item.keys()]) + '\n')

        # Get file rows 
        lines_count = 0
        for _ in fin:
            lines_count += 1
        fin.seek(0, 0)
        fin.readline()

        for j in tqdm(range(lines_count)):
            line = fin.readline()[:-1]
            line_list = line.split(';')
            if line_list[0] == "":
                continue
            line_list.append(cate_dict[int(line_list[0])])
            fout_prod.write('\t'.join([str(line_list[i])
                                       for i in range(len(line_list))]) + '\n')
        fin.close()
        fout_prod.close()
        print("The 'item' part of dataset DIGINETICA has finished.")

    def convert_inter(self):
        # the part of 'item'
        self.convert_item()

        with open(self.input_file_item_views, "r") as f:
            reader = csv.DictReader(f, delimiter=';')
            sess_clicks = {}
            sess_date = {}
            ctr = 0
            curid = -1
            curdate = None
            for data in reader:
                sessid = data['sessionId']
                if curdate and not curid == sessid:
                    date = ''
                    date = time.mktime(time.strptime(curdate, '%Y-%m-%d'))
                    sess_date[curid] = date
                curid = sessid
                item = data['itemId'], int(data['timeframe'])
                curdate = ''
                curdate = data['eventdate']
                if sessid in sess_clicks:
                    sess_clicks[sessid] += [item]
                else:
                    sess_clicks[sessid] = [item]
                ctr += 1
            date = ''
            date = time.mktime(time.strptime(curdate, '%Y-%m-%d'))
            for i in list(sess_clicks):
                sorted_clicks = sorted(sess_clicks[i], key=operator.itemgetter(0))
                sess_clicks[i] = [c for c in sorted_clicks]
            sess_date[curid] = date

        # Filter out length 1 sessions
        for s in list(sess_clicks):
            if len(sess_clicks[s]) == 1:
                del sess_clicks[s]
                del sess_date[s]

        # Count number of times each item appears
        iid_counts = {}
        for s in sess_clicks:
            seq = sess_clicks[s]
            for iid in seq:
                if iid[0] in iid_counts:
                    iid_counts[iid[0]] += 1
                else:
                    iid_counts[iid[0]] = 1
        #
        for s in list(sess_clicks):
            curseq = sess_clicks[s]
            filseq = list(filter(lambda i: iid_counts[i[0]] >= 5, curseq))
            if len(filseq) < 2:
                del sess_clicks[s]
                del sess_date[s]
            else:
                sess_clicks[s] = filseq

        fout = open(self.output_file_inter, "w")
        fout.write('\t'.join([self.fields_inter.get(i) for i in self.fields_inter.keys()]) + '\n')

        if self.merge_repeat == True:
            count = 1
            for key, value in tqdm(sess_clicks.items()):
                #    print(key, value)\
                count = 1
                inter_pre = [key, value[0][0]]
                for i in range(1, len(value)):
                    line = [key, value[i][0]]
                    if (line == inter_pre):
                        count = count + 1
                    else:
                        inter_pre.append(int(sess_date[key]) + int(value[i - 1][1]))
                        inter_pre.append(count)
                        fout.write('\t'.join([str(inter_pre[i])
                                              for i in range(len(inter_pre))]) + '\n')
                        count = 1
                    inter_pre = [key, value[i][0]]

                inter_pre.append(int(sess_date[key]) + int(value[len(value) - 1][1]))
                inter_pre.append(count)
                fout.write('\t'.join([str(inter_pre[i])
                                      for i in range(len(inter_pre))]) + '\n')
        else:
            # divide
            for key, value in tqdm(sess_clicks.items()):
                for i in range(0, len(value)):
                    line = [key, value[i][0]]
                    line.append(int(sess_date[key]) + int(value[i][1]))
                    fout.write('\t'.join([str(line[i])
                                          for i in range(len(line))]) + '\n')
        fout.close()
        print("The 'inter' part of dataset DIGINETICA has finished.")
        print("The process of dataset DIGINETICA has finished.")


class ANIMEDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(ANIMEDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'anime'

        # input file
        self.inter_file = os.path.join(self.input_path, 'rating.csv')
        self.item_file = os.path.join(self.input_path, 'anime.csv')

        self.sep = ','

        # output file
        output_files = self.get_output_files()
        self.output_inter_file = output_files[0]
        self.output_item_file = output_files[1]

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float'}
        self.item_fields = {0: 'item_id:token',
                            1: 'name:token_seq',
                            2: 'genre:token_seq',
                            3: 'type:token',
                            4: 'episodes:float',
                            5: 'avg_rating:float',
                            6: 'members:float'}

    def load_inter_data(self):
        return pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python').iloc[1:, :]

    def load_item_data(self):
        origin_data = pd.read_csv(self.item_file, delimiter=self.sep, header=None, engine='python').iloc[1:, :]
        processed_data = origin_data
        for i in range(origin_data.shape[0]):
            try:
                split_type = origin_data.iloc[i, 2].split(', ')
                type_str = ' '.join(split_type)
            except:
                type_str = ''
            processed_data.iloc[i, 2] = type_str
        processed_data = processed_data.where((processed_data.applymap(lambda x: True if str(x) != 'nan' else False)),
                                              '')
        return processed_data


class EPINIONSDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(EPINIONSDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'epinions'

        # input file
        self.inter_file = os.path.join(self.input_path, 'epinions.json')

        self.sep = ', '

        # output file
        output_files = self.get_output_files()
        self.output_inter_file = output_files[0]

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float',
                             4: 'price:float'}

    def load_inter_data(self):
        dict_all_data = {}
        cnt = 0
        with open(self.inter_file, 'r') as f:
            line = f.readline()
            while True:
                if not line:
                    break
                dict_line = eval(line)
                del dict_line['review']
                dict_all_data[cnt] = dict_line
                cnt += 1
                line = f.readline()

        order = ['user', 'item', 'stars', 'time', 'paid']
        data = pd.DataFrame(dict_all_data).T[order]
        return data


class GOWALLADataset(BaseDataset):
    def __init__(self, input_path, output_path, merge_repeat=False):
        super(GOWALLADataset, self).__init__(input_path, output_path)
        self.dataset_name = 'gowalla'
        self.merge_repeat = merge_repeat  # merge repeat interactions if 'repeat' is True

        # input file
        self.inter_file = os.path.join(self.input_path, 'loc-gowalla_totalCheckins.txt')

        self.sep = '\t'

        # output file
        output_files = self.get_output_files()
        self.output_inter_file = output_files[0]

        # selected feature fields
        if self.merge_repeat == True:
            self.inter_fields = {0: 'user_id:token',
                                 1: 'item_id:token',
                                 2: 'timestamp:float',
                                 3: 'latitude:float',
                                 4: 'longitude:float',
                                 5: 'num_repeat:float'}
        else:
            self.inter_fields = {0: 'user_id:token',
                                 1: 'item_id:token',
                                 2: 'timestamp:float',
                                 3: 'latitude:float',
                                 4: 'longitude:float'}

    def load_inter_data(self):
        if self.merge_repeat == True:
            processed_data = self.merge_repeat_lines()
        else:
            origin_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
            order = [0, 4, 1, 2, 3]
            origin_data = origin_data[order]
            processed_data = origin_data
            processed_data[1] = origin_data[1].apply(lambda x: time.mktime(time.strptime(x, '%Y-%m-%dT%H:%M:%SZ')))
        return processed_data

    def merge_repeat_lines(self):
        cnt_row = 0
        all_user = {}
        a_user = {}
        pre_userid = '0'
        with open(self.inter_file, 'r') as f:
            line = f.readline()
            while True:
                if not line:
                    for key, value in a_user[pre_userid].items():
                        all_user[cnt_row] = [pre_userid, key, value[0], value[1], value[2], value[3]]
                        cnt_row += 1
                    pre_userid = userid
                    break
                line = line.strip().split('\t')
                userid, timestamp, lati, longi, itemid = line[0], line[1], line[2], line[3], line[4]
                timestamp = time.mktime(time.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ'))
                if userid not in a_user.keys():
                    a_user[userid] = {}
                if itemid not in a_user[userid].keys():
                    a_user[userid][itemid] = [timestamp, lati, longi, 1]
                else:
                    a_user[userid][itemid][3] += 1

                if userid != pre_userid:
                    for key, value in a_user[pre_userid].items():
                        all_user[cnt_row] = [pre_userid, key, value[0], value[1], value[2], value[3]]
                        cnt_row += 1
                    pre_userid = userid
                line = f.readline()
        order = [0, 1, 2, 3, 4, 5]
        processed_data = pd.DataFrame(all_user).T[order]
        return processed_data


class LFM1bDataset(BaseDataset):
    def __init__(self, input_path, output_path, item_type='tracks', merge_repeat=True):
        super(LFM1bDataset, self).__init__(input_path, output_path)
        self.input_path = input_path
        self.output_path = output_path

        self.merge_repeat = merge_repeat  # merge repeat interactions if 'merge_repeat' is True
        self.item_type = item_type  # artists, albums, tracks
        self.dataset_name = 'lfm1b-' + self.item_type

        # input file
        self.inter_file = os.path.join(self.input_path, 'LFM-1b_LEs.txt')
        self.item_file = os.path.join(self.input_path, 'LFM-1b_' + self.item_type + '.txt')
        self.user_file = os.path.join(self.input_path, 'LFM-1b_users.txt')
        self.user_file_add = os.path.join(self.input_path, 'LFM-1b_users_additional.txt')

        self.sep = '\t'

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        if self.merge_repeat == True:
            self.inter_fields = {0: 'user_id:token',
                                 1: self.item_type + '_id:token',
                                 2: 'timestamp:float',
                                 3: 'num_repeat:float'
                                 }
        else:
            self.inter_fields = {0: 'user_id:token',
                                 1: self.item_type + '_id:token',
                                 2: 'timestamp:float'
                                 }

        if self.item_type == 'artists':
            self.item_fields = {0: self.item_type + '_id:token',
                                1: 'name:token_seq'
                                }
        else:
            self.item_fields = {0: self.item_type + '_id:token',
                                1: 'name:token_seq',
                                2: 'artists_id:token'
                                }

        self.user_fields = {0: 'user_id:token',
                            1: 'country:token',
                            2: 'age:float',
                            3: 'gender:token',
                            4: 'playcount:float',
                            5: 'registered_timestamp:float',
                            6: 'novelty_artist_avg_month:float',
                            7: 'novelty_artist_avg_6months:float',
                            8: 'novelty_artist_avg_year:float',
                            9: 'mainstreaminess_avg_month:float',
                            10: 'mainstreaminess_avg_6months:float',
                            11: 'mainstreaminess_avg_year:float',
                            12: 'mainstreaminess_global:float',
                            13: 'cnt_listeningevents:float',
                            14: 'cnt_distinct_tracks:float',
                            15: 'cnt_distinct_artists:float',
                            16: 'cnt_listeningevents_per_week:float',
                            17: 'relative_le_per_weekday1:float',
                            18: 'relative_le_per_weekday2:float',
                            19: 'relative_le_per_weekday3:float',
                            20: 'relative_le_per_weekday4:float',
                            21: 'relative_le_per_weekday5:float',
                            22: 'relative_le_per_weekday6:float',
                            23: 'relative_le_per_weekday7:float',
                            24: 'relative le per hour0:float',
                            25: 'relative le per hour1:float',
                            26: 'relative le per hour2:float',
                            27: 'relative le per hour3:float',
                            28: 'relative le per hour4:float',
                            29: 'relative le per hour5:float',
                            30: 'relative le per hour6:float',
                            31: 'relative le per hour7:float',
                            32: 'relative le per hour8:float',
                            33: 'relative le per hour9:float',
                            34: 'relative le per hour10:float',
                            35: 'relative le per hour11:float',
                            36: 'relative le per hour12:float',
                            37: 'relative le per hour13:float',
                            38: 'relative le per hour14:float',
                            39: 'relative le per hour15:float',
                            40: 'relative le per hour16:float',
                            41: 'relative le per hour17:float',
                            42: 'relative le per hour18:float',
                            43: 'relative le per hour19:float',
                            44: 'relative le per hour20:float',
                            45: 'relative le per hour21:float',
                            46: 'relative le per hour22:float',
                            47: 'relative le per hour23:float'
                            }

    def convert_inter(self):
        fout = open(self.output_inter_file, 'w')
        for i in range(len(self.inter_fields)):
            v = self.inter_fields[i]
            fout.write(v) if i == 0 else fout.write('\t' + v)
        fout.write('\n')

        if self.repeat == True:
            self.merge_repeat_lines(fout)
        else:
            with open(self.inter_file, 'r') as f:
                line = f.readline()
                while True:
                    if not line:
                        break

                    line = line.strip().split('\t')
                    userid, artistid, albumid, trackid, timestamp = line[0], line[1], line[2], line[3], line[4]
                    if self.item_type == 'artists':
                        itemid = artistid
                    elif self.item_type == 'albums':
                        itemid = albumid
                    else:
                        itemid = trackid
                    fout.write(str(userid) + '\t' + str(itemid) + '\t' + str(timestamp) + '\n')
                    line = f.readline()

        print(self.output_inter_file + ' is done!')
        fout.close()

    def convert_item(self):
        fout = open(self.output_item_file, 'w')
        for i in range(len(self.item_fields)):
            v = self.item_fields[i]
            fout.write(v) if i == 0 else fout.write('\t' + v)
        fout.write('\n')

        cnt_row = 0
        dict_all_items = {}
        with open(self.item_file, 'r') as f:
            line = f.readline()
            while True:
                if not line:
                    break
                fout.write(line)
                line = f.readline()
        print(self.output_item_file + ' is done!')
        fout.close()

    def convert_user(self):
        fout = open(self.output_user_file, 'w')
        for i in range(len(self.user_fields)):
            v = self.user_fields[i]
            fout.write(v) if i == 0 else fout.write('\t' + v)
        fout.write('\n')

        with open(self.user_file, 'r') as f1:
            with open(self.user_file_add, 'r') as f2:
                line1 = f1.readline()
                line2 = f2.readline()
                line1 = f1.readline()
                line2 = f2.readline()
                while True:
                    if not line1 or not line2:
                        break
                    line1 = line1.strip()
                    line2 = line2.strip().replace('?', '')
                    fout.write(line1 + '\t' + line2 + '\n')
                    line1 = f1.readline()
                    line2 = f2.readline()
        print(self.output_user_file + ' is done!')
        fout.close()

    def merge_repeat_lines(self, fout):
        a_user = {}
        pre_userid = '31435741'
        user_order = []
        with open(self.inter_file, 'r') as f:
            line = f.readline()
            while True:
                if not line:
                    if pre_userid not in user_order:
                        user_order.append(pre_userid)
                    for userid in user_order:
                        for key, value in a_user[userid].items():
                            fout.write(
                                str(userid) + '\t' + str(key) + '\t' + str(value[0]) + '\t' + str(value[1]) + '\n')
                    break
                line = line.strip().split('\t')
                userid, artistid, albumid, trackid, timestamp = line[0], line[1], line[2], line[3], line[4]
                if self.item_type == 'artists':
                    itemid = artistid
                elif self.item_type == 'albums':
                    itemid = albumid
                else:
                    itemid = trackid

                if userid not in a_user.keys():
                    a_user[userid] = {}
                if itemid not in a_user[userid].keys():
                    a_user[userid][itemid] = [timestamp, 1]
                else:
                    a_user[userid][itemid][1] += 1

                if userid != pre_userid:
                    if pre_userid not in user_order:
                        user_order.append(pre_userid)
                    pre_userid = userid
                line = f.readline()


class PHISHINGWEBDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(PHISHINGWEBDataset, self).__init__(input_path, output_path)
        self.input_path = input_path
        self.output_path = output_path

        self.dataset_name = 'phishing-website'

        # input file
        self.inter_file = os.path.join(self.input_path, 'Training Dataset.arff')

        self.sep = ','

        # output file
        self.output_inter_file = self.get_output_files()[0]

        self.inter_fields = {0: 'label:float',
                             1: 'AB1:float',
                             2: 'AB2:float',
                             3: 'AB3:float',
                             4: 'AB4:float',
                             5: 'AB5:float',
                             6: 'AB6:float',
                             7: 'AB7:float',
                             8: 'AB8:float',
                             9: 'AB9:float',
                             10: 'AB10:float',
                             11: 'AB11:float',
                             12: 'AB12:float',
                             13: 'A1:float',
                             14: 'A2:float',
                             15: 'A3:float',
                             16: 'A4:float',
                             17: 'A5:float',
                             18: 'A6:float',
                             19: 'HJ1:float',
                             20: 'HJ2:float',
                             21: 'HJ3:float',
                             22: 'HJ4:float',
                             23: 'HJ5:float',
                             24: 'D1:float',
                             25: 'D2:float',
                             26: 'D3:float',
                             27: 'D4:float',
                             28: 'D5:float',
                             29: 'D6:float',
                             30: 'D7:float'
                             }

    def convert_inter(self):
        fout = open(self.output_inter_file, 'w')
        for i in range(len(self.inter_fields)):
            v = self.inter_fields[i]
            fout.write(v) if i == 0 else fout.write('\t' + v)
        fout.write('\n')

        with open(self.inter_file, 'r') as f:
            line = f.readline()
            while True:
                if not line:
                    break

                if line == '\n' or line[0] == '@':
                    line = f.readline()
                    continue
                line = line.strip().split(',')
                fout.write(str(line[-1]))
                for i in range(len(line) - 1):
                    fout.write('\t' + str(line[i]))
                fout.write('\n')
                line = f.readline()
        fout.close()


class BOOKCROSSINGDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(BOOKCROSSINGDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'book-crossing'

        # input file
        self.inter_file = os.path.join(self.input_path, 'BX-Book-Ratings.csv')
        self.user_file = os.path.join(self.input_path, 'BX-Users.csv')
        self.item_file = os.path.join(self.input_path, 'BX-Books.csv')
        self.sep = ';'
        # print(self.input_file)

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float'}

        self.user_fields = {0: 'user_id:token',
                            1: 'location:token_seq',
                            2: 'age:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'book_title:token_seq',
                            2: 'book_author:token_seq',
                            3: 'publication_year:float',
                            4: 'publisher:token_seq'}

    def load_inter_data(self):
        processed_list = []
        with open(self.inter_file, 'r', encoding='cp1252') as f:
            for each_line in f.readlines():
                split_line = each_line[:-1].split(';')
                split_line = [item[1:-1] for item in split_line]
                processed_list.append(split_line)

            column_list = processed_list[0]
            processed_list.pop(0)
            data = pd.DataFrame(processed_list, columns=column_list)
        return data

    def load_item_data(self):
        pattern = re.compile(r'(?<=");(?=")')
        processed_list = []
        with open(self.item_file, 'r', encoding='cp1252') as f:
            for each_line in f.readlines():
                split_line = pattern.split(each_line[:-1])
                split_line = [item[1:-1] for item in split_line]
                processed_list.append(split_line)

            column_list = processed_list[0]
            processed_list.pop(0)
            data = pd.DataFrame(processed_list, columns=column_list)
        return data

    def load_user_data(self):
        pattern = re.compile(r'NULL|".*?(?<!\\)"', re.S)
        with open(self.user_file, 'r', encoding='cp1252') as f:
            content = pattern.findall(f.read())
            content = [s[1:-1] if s != 'NULL' else None for s in content]
            processed_list = list(np.array(content).reshape((-1, 3)))
            column_list = processed_list[0]
            processed_list.pop(0)
            data = pd.DataFrame(processed_list, columns=column_list)
        return data

    def convert_user(self):
        try:
            input_user_data = self.load_user_data()
            self.book_convert(input_user_data, self.user_fields, self.output_user_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to user file\n')

    def book_convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.user_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')


class IPINYOUDataset(BaseDataset):
    def __init__(self, input_path, output_path, repeat=True):
        super(IPINYOUDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'ipinyou'
        self.repeat = repeat
        self.record_id = 1
        if self.repeat:
            postfix = '-sums'
        else:
            postfix = ''
        self.view_dataset_name = self.dataset_name + '-view' + postfix
        self.click_dataset_name = self.dataset_name + '-click' + postfix

        self.sep = '\t'

        # input path list
        days_2nd = ['201306%02d' % day for day in range(6, 13)]
        days_3rd = ['201310%02d' % day for day in range(19, 28)]
        self.input_view_files = [os.path.join(self.input_path, 'training2nd/imp.%s.txt.bz2' % s) for s in days_2nd] + \
                                [os.path.join(self.input_path, 'training3rd/imp.%s.txt.bz2' % s) for s in days_3rd]

        self.input_click_files = [os.path.join(self.input_path, 'training2nd/clk.%s.txt.bz2' % s) for s in days_2nd] + \
                                 [os.path.join(self.input_path, 'training3rd/clk.%s.txt.bz2' % s) for s in days_3rd]

        # decompress bz2 file
        for filepath in self.input_view_files + self.input_click_files:
            new_filepath = filepath[:-4]
            # avoid decompressing the file having been decompressed
            if os.path.exists(new_filepath):
                continue
            with open(new_filepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
                for data in iter(lambda: file.read(100 * 1024), b''):
                    new_file.write(data)

        self.input_view_files = [file[:-4] for file in self.input_view_files]
        self.input_click_files = [file[:-4] for file in self.input_click_files]

        # output path
        output_file = self.get_output_paths()
        self.output_inter_file = output_file[0]
        self.output_item_file = output_file[1]
        self.output_user_file = output_file[2]

        # selected feature fields
        if self.repeat:
            self.inter_fields = {0: 'user_id:token',
                                 1: 'item_id:token',
                                 2: 'season:token',
                                 3: 'region_id:token',
                                 4: 'city_id:token',
                                 5: 'interactions:float'}
        else:
            self.inter_fields = {0: 'user_id:token',
                                 1: 'item_id:token',
                                 2: 'season:token',
                                 3: 'region_id:token',
                                 4: 'city_id:token'}

        self.item_fields = {0: 'item_id:token',
                            1: 'season:token',
                            2: 'slot_width:float',
                            3: 'slot_height:float',
                            4: 'slot_price:float',
                            5: 'category_id:token'}

        self.user_fields = {0: 'user_id:token',
                            1: 'user_profile:token_seq'}

    def load_inter_data(self):
        total_clk_output, total_imp_output = {}, {}
        # Process view and click inter files
        for imp, clk in zip(self.input_view_files, self.input_click_files):
            clk_output, imp_output = self.load_inter_file(imp, clk)
            total_clk_output.update(clk_output)
            total_imp_output.update(imp_output)
        return total_imp_output, total_clk_output

    def load_item_data(self):
        total_item_data = set()
        for imp in self.input_view_files:
            total_item_data |= self.load_item_file(imp)
        return total_item_data

    def load_user_data(self):
        total_user_data = set()
        for imp in self.input_view_files:
            total_user_data |= self.load_user_file(imp)
        return total_user_data

    def load_inter_file(self, input_imp_file, input_clk_file):
        imp_lines = open(input_imp_file, encoding='utf-8').readlines()
        clk_lines = open(input_clk_file, encoding='utf-8').readlines()
        if input_imp_file[-8:-6] == '06':
            season = '2'
        else:
            season = '3'

        clk_output = {}
        for line in clk_lines:
            words = line.strip().split(self.sep)
            if len(words) != 24:
                continue
            if self.repeat:
                k = [words[3], words[18], words[6], words[7], words[12]]
            else:
                k = [words[3], words[18], words[6], words[7], self.record_id]
                self.record_id += 1
            k.insert(2, season)
            k = tuple(k)
            if k in clk_output:
                clk_output[k] += 1
            else:
                clk_output[k] = 1

        imp_output = {}
        for line in imp_lines:
            words = line.strip().split(self.sep)
            if len(words) != 24:
                continue
            if self.repeat:
                k = [words[3], words[18], words[6], words[7], words[12]]
            else:
                k = [words[3], words[18], words[6], words[7], self.record_id]
                self.record_id += 1
            k.insert(2, season)
            k = tuple(k)
            if k in imp_output:
                imp_output[k] += 1
            else:
                imp_output[k] = 1
        return clk_output, imp_output

    def load_item_file(self, input_imp_file):
        if input_imp_file[-8:-6] == '06':
            season = '2'
        else:
            season = '3'
        imp_lines = open(input_imp_file, encoding='utf-8').readlines()
        item_output = set()
        index = [18, 13, 14, 20, 22, 12]
        for line in imp_lines:
            words = line.strip().split(self.sep)
            if len(words) != 24:
                continue
            filed_list = [words[i] for i in index]
            filed_list.insert(1, season)
            item_output.add(tuple(filed_list))
        return item_output

    def load_user_file(self, input_imp_file):
        imp_lines = open(input_imp_file, encoding='utf-8').readlines()
        user_output = set()
        for line in imp_lines:
            words = line.strip().split(self.sep)
            if len(words) != 24:
                continue
            user_output.add((words[3], words[23]))
        return user_output

    def get_output_paths(self):
        view_output_path = os.path.join(self.output_path, self.view_dataset_name)
        click_output_path = os.path.join(self.output_path, self.click_dataset_name)

        if not os.path.isdir(view_output_path):
            os.makedirs(view_output_path)
        if not os.path.isdir(click_output_path):
            os.makedirs(click_output_path)

        view_inter_file = os.path.join(view_output_path, self.view_dataset_name + '.inter')
        click_inter_file = os.path.join(click_output_path, self.click_dataset_name + '.inter')
        output_inter_file = (view_inter_file, click_inter_file)

        view_item_file = os.path.join(view_output_path, self.view_dataset_name + '.item')
        click_item_file = os.path.join(click_output_path, self.click_dataset_name + '.item')
        output_item_file = (view_item_file, click_item_file)

        view_user_file = os.path.join(view_output_path, self.view_dataset_name + '.user')
        click_user_file = os.path.join(click_output_path, self.click_dataset_name + '.user')
        output_user_file = (view_user_file, click_user_file)

        return output_inter_file, output_item_file, output_user_file

    def convert_inter(self):
        try:
            view_inter, click_inter = self.load_inter_data()
            view_file, click_file = self.output_inter_file
            with open(view_file, 'w') as fp:
                fp.write('\t'.join([self.inter_fields[i] for i in range(len(self.inter_fields))]) + '\n')
                for k, v in tqdm(view_inter.items()):
                    k = k[:-1]
                    if self.repeat:
                        fp.write('\t'.join([str(item) for item in list(k) + [v]]) + '\n')
                    else:
                        fp.write('\t'.join([str(item) for item in list(k)]) + '\n')
            with open(click_file, 'w') as fp:
                fp.write('\t'.join([self.inter_fields[i] for i in range(len(self.inter_fields))]) + '\n')
                for k, v in tqdm(click_inter.items()):
                    k = k[:-1]
                    if self.repeat:
                        fp.write('\t'.join([str(item) for item in list(k) + [v]]) + '\n')
                    else:
                        fp.write('\t'.join([str(item) for item in list(k)]) + '\n')
        except NotImplementedError:
            print('This dataset can\'t be converted to inter file\n')

    def convert_item(self):
        try:
            item_data = self.load_item_data()
            view_file, click_file = self.output_item_file
            with open(view_file, 'w') as vf, open(click_file, 'w') as cf:
                title = '\t'.join([self.item_fields[i] for i in range(len(self.item_fields))]) + '\n'
                vf.write(title)
                cf.write(title)
                for item in tqdm(item_data):
                    item = item[:-1]
                    record = '\t'.join([str(field) for field in item]) + '\n'
                    vf.write(record)
                    cf.write(record)
        except NotImplementedError:
            print('This dataset can\'t be converted to inter file\n')

    def convert_user(self):
        try:
            user_data = self.load_user_data()
            view_file, click_file = self.output_user_file
            with open(view_file, 'w') as vf, open(click_file, 'w') as cf:
                title = '\t'.join([self.user_fields[i] for i in range(len(self.user_fields))]) + '\n'
                vf.write(title)
                cf.write(title)
                for user in tqdm(user_data):
                    record = '\t'.join([user[0], user[1].replace(',', ' ')]) + '\n'
                    vf.write(record)
                    cf.write(record)
        except NotImplementedError:
            print('This dataset can\'t be converted to inter file\n')


class STEAMDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(STEAMDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'steam'

        # input file
        self.inter_file = os.path.join(self.input_path, 'steam_new.json')
        self.item_file = os.path.join(self.input_path, 'steam_games.json')
        #        self.sep = '::'

        # output file
        self.output_inter_file, self.output_item_file, _ = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: "user_id:token",
                             1: "play_hours:float",
                             2: "products:token",
                             3: "product_id:token",
                             4: "page_order:float",
                             5: "timestamp:float",
                             6: "early_access:bool",
                             7: "page:float",
                             8: "found_funny:string",
                             9: "compensation:string"}

        self.item_fields = {0: "app_name:token",
                            1: "developer:token",
                            2: "early_access:bool",
                            3: "genres:token_seq",
                            4: "id:token",
                            5: "metascore:float",
                            6: "price:float",
                            7: "publisher:token",
                            8: "timestamp:float",
                            9: "sentiment:token",
                            10: "specs:token_seq",
                            11: "tags:token_seq",
                            12: "title:token"}

    def convert_inter(self):
        fout = open(self.output_inter_file, "w")
        fout.write('\t'.join([self.inter_fields.get(i) for i in self.inter_fields.keys()]) + '\n')

        fin = open(self.inter_file, "r")
        head = ["hours",
                "products",
                "product_id",
                "page_order",
                "date",
                "early_access",
                "page",
                "found_funny",
                "compensation",
                "user_id"]
        user_dict = {}
        prod_count = 0
        cur_user_id = 0
        error_count = 0

        lines_count = 0
        for _ in fin:
            lines_count += 1
        fin.seek(0, 0)
        fin.readline()

        for i in tqdm(range(lines_count)):
            line = fin.readline()
            if line == "":
                continue
            # delete 'text' and 'username' becase there are so many things that hart to deal with
            text_pos = line.find("u'text':")
            user_pos = line.find("u'username':")
            text_next_pos = 100000
            user_next_pos = text_pos
            for j in range(len(head)):
                pattern = "u'" + head[j] + "':"
                new_text_next_pos = line.find(pattern)
                new_user_next_pos = new_text_next_pos
                if new_text_next_pos > text_pos and new_text_next_pos < text_next_pos:
                    text_next_pos = new_text_next_pos
                if new_user_next_pos > user_pos and new_user_next_pos < user_next_pos:
                    user_next_pos = new_user_next_pos

            user_name = line[user_pos + 15: user_next_pos - 3]
            line = line[:user_pos] + line[user_next_pos:text_pos] + line[text_next_pos:]
            line = re.sub("u\"", "u\'", line)
            line = re.sub("u'", "\"", line)
            line = re.sub("': ", "\": ", line)
            line = re.sub("', ", "\", ", line)
            line = re.sub("False", "false", line)
            line = re.sub("True", "true", line)
            line = re.sub(r"\\", "-", line)  # JSONDecodeError: Invalid \escape

            try:
                line_dict = json.loads(line)
            except:
                error_count = error_count + 1
                print(i, "error")
                continue

            if int(line_dict["product_id"]) > prod_count:
                prod_count = int(line_dict["product_id"])

            timeArray = time.strptime(line_dict["date"], "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray))
            line_dict["date"] = timeStamp
            if user_name not in user_dict:
                user_dict[user_name] = cur_user_id
                cur_user_id = cur_user_id + 1
            user_id = user_dict[user_name]

            data_line = [user_id]
            for j in range(9):
                if head[j] in line_dict:
                    data_line.append(line_dict[head[j]])
                else:
                    data_line.append("")

            fout.write('\t'.join([str(data_line[i])
                                  for i in range(len(data_line))]) + '\n')

        fin.close()
        fout.close()
        print("There are ", error_count, " error data.")
        #        print("There are ", lines_count, " lines.")
        #        print("There are ", prod_count, " products.")
        #        print("There are ", cur_user_id, " users.")
        print("The Dataset STEAM has finished.")

    def convert_item(self):
        fout = open(self.output_item_file, "w")
        fout.write('\t'.join([self.item_fields.get(i) for i in self.item_fields.keys()]) + '\n')

        fin = open(self.item_file, "r")
        head = ["app_name",
                "developer",
                "early_access",
                "genres",
                "id",
                "metascore",
                "price",
                "publisher",
                "release_date",
                "sentiment",
                "specs",
                "tags",
                "title",
                "reviews_url",  # ignore finally
                "url",  # ignore finally
                "discount_price"  # ignore finally
                ]

        error_count = 0

        lines_count = 0
        for _ in fin:
            lines_count += 1
        fin.seek(0, 0)
        fin.readline()

        def get_data(line, head, i):
            pattern = "u'" + head[i] + "':"
            pos = line.find(pattern)
            if pos == -1:
                return ""
            next_pos = len(line)
            for j in range(len(head)):
                pattern = "u'" + head[j] + "':"
                new_pos = line.find(pattern)
                if new_pos > pos and new_pos < next_pos:
                    next_pos = new_pos
            data = line[pos: next_pos]
            if next_pos == len(line):
                line = line[:pos - 2]
            else:
                line = line[:pos] + line[next_pos:]
            return data

        for i in tqdm(range(lines_count)):
            line = fin.readline()
            if line == "":
                continue
            for j in range(13):
                data = get_data(line, head, j)
                deli_idx = data.find(":")
                data = data[deli_idx + 2: -2]
                data = re.sub("u\'", "", data)
                data = re.sub("\'", "", data)
                if head[j] == "release_date":
                    try:
                        timeArray = time.strptime(data, "%Y-%m-%d")
                        data = int(time.mktime(timeArray))
                    except:
                        data = ""
                fout.write(str(data))

                if j != 12:
                    fout.write('\t')
            fout.write('\n')

        fin.close()
        fout.close()
        print("There are ", error_count, " error data.")
        #        print("There are ", lines_count, " lines.")
        print("The item part of Dataset STEAM has finished.")


class PINTERESTDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(PINTERESTDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'pinterest'

        # input path
        self.inter_file = os.path.join(self.input_path, 'pinterest-20.train.rating')

        self.sep = '\t'

        # output path
        output_file = self.get_output_files()
        self.output_inter_file = output_file[0]

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token'}

    def load_inter_data(self):
        return pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')


class JESTERDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(JESTERDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'jester'
        #
        #        # input file
        self.input_file_1 = os.path.join(input_path, 'jester-data-1.xls')
        self.input_file_2 = os.path.join(input_path, 'jester-data-2.xls')
        self.input_file_3 = os.path.join(input_path, 'jester-data-3.xls')

        #
        #        # output file
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        self.output_file = os.path.join(output_path, 'jester.inter')
        #
        #        # selected feature fields
        inter_fields = {0: 'user_id:token',
                        1: 'item_id:token',
                        2: 'rating:float'}

    def convert_inter(self):
        data1 = pd.read_excel(self.input_file_1, header=None).values.tolist()
        data2 = pd.read_excel(self.input_file_2, header=None).values.tolist()
        data3 = pd.read_excel(self.input_file_3, header=None).values.tolist()
        data = [data1, data2, data3]

        fout = open(self.output_file, "w")
        fout.write('\t'.join([self.inter_fields.get(i) for i in self.inter_fields.keys()]) + '\n')

        cur_user_id = 0
        inter_count = 0
        data_i = 1
        for data_test in data:
            for i in tqdm(range(len(data_test))):
                inter_count = inter_count + data_test[i][0]
                for j in range(1, len(data_test[0])):
                    #        print(i, j)
                    if data_test[i][j] != 99:
                        # user_id = cur_user_id
                        # item_id = j - 1
                        # rating = data_test[i][j]
                        fout.write('\t'.join([str(cur_user_id), str(j - 1), str(data_test[i][j])]) + '\n')
                cur_user_id = cur_user_id + 1
            print("The ", data_i, " part of Dataset JESTER has finished.")
            data_i = data_i + 1

        print("There are ", inter_count, " interactions.")
        print("The process of Dataset JESTER has finished.")
        fout.close()


class DOUBANDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(DOUBANDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'steam'
        #
        #        # input file
        self.input_file = os.path.join(input_path, 'DMSC.csv')

        if not os.path.isdir(output_path):
            os.makedirs(output_path)

        #        # output file
        self.output_file = os.path.join(output_path, 'douban.inter')
        #
        #        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float',
                             4: 'likes_num:float'}

    #

    def convert_inter(self):
        data = pd.read_csv(self.input_file, header=0).values.tolist()

        fout = open(self.output_file, "w")
        fout.write('\t'.join([self.inter_fields.get(i) for i in self.inter_fields.keys()]) + '\n')

        user_count = 0
        user_dict = {}
        item_count = 0
        item_dict = {}
        inter_count = len(data)

        for i in tqdm(range(inter_count)):
            if data[i][5] not in user_dict:
                user_dict[data[i][5]] = user_count
                user_id = user_count
                user_count = user_count + 1
            else:
                user_id = user_dict[data[i][5]]

            if data[i][1] not in item_dict:
                item_dict[data[i][1]] = item_count
                item_id = item_count
                item_count = item_count + 1
            else:
                item_id = item_dict[data[i][1]]

            rating = data[i][7]

            timeArray = time.strptime(data[i][6], "%Y-%m-%d")
            timestamp = int(time.mktime(timeArray))

            like_num = data[i][9]
            fout.write('\t'.join([str(user_id), str(item_id), str(rating), str(timestamp), str(like_num)]) + '\n')

        fout.close()
        print("There are ", user_count, " users.")
        print("There are ", item_count, " items.")
        print("There are ", inter_count, " interactions.")
        print("The process of Dataset DOUBAN has finished.")


class KDD2010BridgeAlgebra2006Dataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(KDD2010BridgeAlgebra2006Dataset, self).__init__(input_path, output_path)
        self.dataset_name = 'KDD2010-bridge-algebra2006_2007'

        # input file
        self.train_inter_file = os.path.join(self.input_path, 'algebra_2006_2007_train.txt')
        self.master_inter_file = os.path.join(self.input_path, 'algebra_2006_2007_master.txt')

        self.sep = '\t'

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'raw:float',
                             1: 'student_id:token',
                             2: 'problem_hierarchy:token_seq',
                             3: 'problem_step_name:token',
                             4: 'problem_view:float',
                             5: 'step_start_time:float',
                             6: 'first_transaction_time:float',
                             7: 'correct_transcation_time:float',
                             8: 'step_end_time:float',
                             9: 'step_duration:float',
                             10: 'correct_step_duration:float',
                             11: 'error_step_duration:float',
                             12: 'correct_first_attempt:float',
                             13: 'incorrects:float',
                             14: 'hints:float',
                             15: 'corrects:float',
                             16: 'kc:token_seq',
                             17: 'opportunity:token_seq'}

    def load_inter_data(self):
        train_inter_data = pd.read_csv(self.train_inter_file, delimiter=self.sep, engine='python')
        master_inter_data = pd.read_csv(self.master_inter_file, delimiter=self.sep, engine='python')
        all_data = pd.concat([train_inter_data, master_inter_data], ignore_index=True)
        time_convert_data = all_data
        for each_field in tqdm(all_data.columns):
            if each_field.endswith('Time'):
                this_field = []
                for i in tqdm(range(all_data.shape[0])):
                    if pd.isnull(all_data[each_field][i]):
                        this_field.append(all_data[each_field][i])
                        continue
                    d = datetime.strptime(str(all_data[each_field][i]), "%Y-%m-%d %H:%M:%S.0")
                    time_str = time.mktime(d.timetuple())
                    this_field.append(time_str)
                time_convert_data[each_field] = pd.Series(this_field)

        sorted_by_row_data = time_convert_data.sort_values(by='Row', ascending=True)
        finished_data = sorted_by_row_data.drop(columns=['Problem Name', 'Step Name'])
        problem_step_name = []
        for i in tqdm(range(time_convert_data.shape[0])):
            new_name = time_convert_data.iloc[i, 3] + '<' + time_convert_data.iloc[i, 5]
            problem_step_name.append(new_name)
        finished_data.insert(3, 'problem_step_name', pd.Series(problem_step_name))
        return finished_data

    def convert_inter(self):
        try:
            input_inter_data = self.load_inter_data()
            self.kdd_convert(input_inter_data, self.inter_fields, self.output_inter_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to inter file\n')

    def kdd_convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.inter_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')


class KDD2010BRIDGEALGEBRA2008Dataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(KDD2010BRIDGEALGEBRA2008Dataset, self).__init__(input_path, output_path)
        self.dataset_name = 'KDD2010-bridge-birdge-algebra2008_2009'

        # input file
        self.train_inter_file = os.path.join(self.input_path, 'algebra_2008_2009_train.txt')

        self.sep = '\t'

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'raw:float',
                             1: 'student_id:token',
                             2: 'problem_hierarchy:token_seq',
                             3: 'problem_step_name:token',
                             4: 'problem_view:float',
                             5: 'step_start_time:float',
                             6: 'first_transaction_time:float',
                             7: 'correct_transcation_time:float',
                             8: 'step_end_time:float',
                             9: 'step_duration:float',
                             10: 'correct_step_duration:float',
                             11: 'error_step_duration:float',
                             12: 'correct_first_attempt:float',
                             13: 'incorrects:float',
                             14: 'hints:float',
                             15: 'corrects:float',
                             16: 'kc:token_seq',
                             17: 'opportunity:token_seq'}

    def load_inter_data(self):
        train_inter_data = pd.read_csv(self.train_inter_file, delimiter=self.sep, engine='python')

        time_convert_data = train_inter_data
        for each_field in tqdm(train_inter_data.columns):
            print(each_field, type(each_field))
            if each_field.endswith('Time'):
                this_field = []
                for i in tqdm(range(train_inter_data.shape[0])):
                    if pd.isnull(train_inter_data[each_field][i]):
                        this_field.append(train_inter_data[each_field][i])
                        continue
                    d = datetime.strptime(str(train_inter_data[each_field][i]), "%Y-%m-%d %H:%M:%S.0")
                    time_str = time.mktime(d.timetuple())
                    this_field.append(time_str)
                # print(all_data[each_field][i])
                time_convert_data[each_field] = pd.Series(this_field)

        sorted_by_row_data = time_convert_data.sort_values(by='Row', ascending=True)
        finished_data = sorted_by_row_data.drop(columns=['Problem Name', 'Step Name'])
        problem_step_name = []
        for i in tqdm(range(time_convert_data.shape[0])):
            new_name = time_convert_data.iloc[i, 3] + '<' + time_convert_data.iloc[i, 5]
            problem_step_name.append(new_name)
        finished_data.insert(3, 'problem_step_name', pd.Series(problem_step_name))
        return finished_data

    def convert_inter(self):
        try:
            input_inter_data = self.load_inter_data()
            self.kdd_convert(input_inter_data, self.inter_fields, self.output_inter_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to inter file\n')

    def kdd_convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.inter_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')


class KDD2010BridgeBridgeToAlgebra2006Dataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(KDD2010BridgeBridgeToAlgebra2006Dataset, self).__init__(input_path, output_path)
        self.dataset_name = 'KDD2010-bridge-bridge-to-algebra2006_2007'

        # input file
        self.train_inter_file = os.path.join(self.input_path, 'bridge_to_algebra_2006_2007_train.txt')
        self.master_inter_file = os.path.join(self.input_path, 'bridge_to_algebra_2006_2007_master.txt')

        self.sep = '\t'

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'raw:float',
                             1: 'student_id:token',
                             2: 'problem_hierarchy:token_seq',
                             3: 'problem_step_name:token',
                             4: 'problem_view:float',
                             5: 'step_start_time:float',
                             6: 'first_transaction_time:float',
                             7: 'correct_transcation_time:float',
                             8: 'step_end_time:float',
                             9: 'step_duration:float',
                             10: 'correct_step_duration:float',
                             11: 'error_step_duration:float',
                             12: 'correct_first_attempt:float',
                             13: 'incorrects:float',
                             14: 'hints:float',
                             15: 'corrects:float',
                             16: 'kc:token_seq',
                             17: 'opportunity:token_seq'}

    def load_inter_data(self):
        train_inter_data = pd.read_csv(self.train_inter_file, delimiter=self.sep, engine='python')
        master_inter_data = pd.read_csv(self.master_inter_file, delimiter=self.sep, engine='python')
        all_data = pd.concat([train_inter_data, master_inter_data], ignore_index=True)
        time_convert_data = all_data
        for each_field in tqdm(all_data.columns):
            if each_field.endswith('Time'):
                this_field = []
                for i in tqdm(range(all_data.shape[0])):
                    if pd.isnull(all_data[each_field][i]):
                        this_field.append(all_data[each_field][i])
                        continue
                    d = datetime.strptime(str(all_data[each_field][i]), "%Y-%m-%d %H:%M:%S.0")
                    time_str = time.mktime(d.timetuple())
                    this_field.append(time_str)
                time_convert_data[each_field] = pd.Series(this_field)

        sorted_by_row_data = time_convert_data.sort_values(by='Row', ascending=True)
        finished_data = sorted_by_row_data.drop(columns=['Problem Name', 'Step Name'])
        problem_step_name = []
        for i in tqdm(range(time_convert_data.shape[0])):
            new_name = time_convert_data.iloc[i, 3] + '<' + time_convert_data.iloc[i, 5]
            problem_step_name.append(new_name)
        finished_data.insert(3, 'problem_step_name', pd.Series(problem_step_name))
        return finished_data

    def convert_inter(self):
        try:
            input_inter_data = self.load_inter_data()
            self.kdd_convert(input_inter_data, self.inter_fields, self.output_inter_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to inter file\n')

    def kdd_convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.inter_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')


class AmazonAppsForAndroidDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonAppsForAndroidDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Apps_for_Android'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Apps_for_Android.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Apps_for_Android.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'categories:token_seq',
                            3: 'sales_type:token',
                            4: 'sales_rank:float',
                            5: 'price:float'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            categories = origin_data.iloc[i, 2]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            salesRank = origin_data.iloc[i, 3]
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(3, 'sales_type', pd.Series(sales_type))
        finished_data.insert(4, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(2, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:

            input_item_data = self.load_item_data()

            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonBeautyDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonBeautyDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Beauty'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Beauty.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Beauty.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'title:token',
                            4: 'sales_type:token',
                            5: 'sales_rank:float',
                            6: 'categories:token_seq',
                            7: 'price:float',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            categories = origin_data.iloc[i, 5]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            salesRank = origin_data.iloc[i, 4]
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])

        finished_data.insert(4, 'sales_type', pd.Series(sales_type))
        finished_data.insert(5, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(6, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:

            input_item_data = self.load_item_data()

            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonToolsAndHomeImprovementDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonToolsAndHomeImprovementDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Tools_and_Home_Improvement'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Tools_and_Home_Improvement.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Tools_and_Home_Improvement.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'categories:token_seq',
                            3: 'title:token',
                            5: 'price:float',
                            6: 'brand:token',
                            8: 'sales_type:token',
                            9: 'sales_rank:float'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 8]
            categories = origin_data.iloc[i, 2]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(2, 'categories', pd.Series(new_categories))
        finished_data.insert(8, 'sales_type', pd.Series(sales_type))
        finished_data.insert(9, 'sales_rank', pd.Series(sales_rank))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:

            input_item_data = self.load_item_data()

            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonBooksDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonBooksDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Books'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Books.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Books.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'sales_type:token',
                            2: 'sales_rank:float',
                            4: 'categories:token_seq',
                            5: 'title:token',
                            7: 'price:float',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 1]
            categories = origin_data.iloc[i, 3]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(1, 'sales_type', pd.Series(sales_type))
        finished_data.insert(2, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(4, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonInstantVideoDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonInstantVideoDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Instant_Video'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Amazon_Instant_Video.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Amazon_Instant_Video.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'categories:token_seq',
                            2: 'price:float'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        new_categories = []
        finished_data = origin_data.drop(columns=['categories'])
        for i in tqdm(range(origin_data.shape[0])):
            categories = origin_data.iloc[i, 1]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])

        finished_data.insert(1, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonDigitalMusicDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonDigitalMusicDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Digital_Music'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Digital_Music.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Digital_Music.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'title:token',
                            2: 'price:float',
                            5: 'sales_type:token',
                            6: 'sales_rank:float',
                            7: 'categories:token_seq',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 5]
            categories = origin_data.iloc[i, 6]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(5, 'sales_type', pd.Series(sales_type))
        finished_data.insert(6, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(7, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonMoviesAndTVDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonMoviesAndTVDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Movies_and_TV'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Movies_and_TV.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Movies_and_TV.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'categories:token_seq',
                            3: 'title:token',
                            4: 'price:float',
                            5: 'sales_type:token',
                            6: 'sales_rank:float',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 5]
            categories = origin_data.iloc[i, 1]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(1, 'categories', pd.Series(new_categories))
        finished_data.insert(5, 'sales_type', pd.Series(sales_type))
        finished_data.insert(6, 'sales_rank', pd.Series(sales_rank))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonAutomotiveDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonAutomotiveDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Automotive'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Automotive.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Automotive.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'categories:token_seq',
                            3: 'title:token',
                            4: 'price:float',
                            6: 'brand:token',
                            8: 'sales_type:token',
                            9: 'sales_rank:float'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 8]

            categories = origin_data.iloc[i, 1]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])

            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(1, 'categories', pd.Series(new_categories))
        finished_data.insert(8, 'sales_type', pd.Series(sales_type))
        finished_data.insert(9, 'sales_rank', pd.Series(sales_rank))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonBabyDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonBabyDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Baby'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Baby.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Baby.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'categories:token_seq',
                            3: 'title:token',
                            4: 'price:float',
                            6: 'brand:token',
                            8: 'sales_type:token',
                            9: 'sales_rank:float'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 8]
            categories = origin_data.iloc[i, 1]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(1, 'categories', pd.Series(new_categories))
        finished_data.insert(8, 'sales_type', pd.Series(sales_type))
        finished_data.insert(9, 'sales_rank', pd.Series(sales_rank))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonClothingShoesAndJewelryDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonClothingShoesAndJewelryDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Clothing_Shoes_and_Jewelry'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Clothing_Shoes_and_Jewelry.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Clothing_Shoes_and_Jewelry.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'title:token',
                            3: 'price:float',
                            4: 'sales_type:token',
                            5: 'sales_rank:float',
                            7: 'brand:token',
                            8: 'categories:token_seq'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 4]
            categories = origin_data.iloc[i, 7]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(4, 'sales_type', pd.Series(sales_type))
        finished_data.insert(5, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(8, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonCellPhonesAndAccessoriesDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonCellPhonesAndAccessoriesDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Cell_Phones_and_Accessories'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Cell_Phones_and_Accessories.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Cell_Phones_and_Accessories.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'title:token',
                            3: 'price:float',
                            4: 'sales_type:token',
                            5: 'sales_rank:float',
                            7: 'brand:token',
                            8: 'categories:token_seq'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 4]
            categories = origin_data.iloc[i, 7]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(4, 'sales_type', pd.Series(sales_type))
        finished_data.insert(5, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(8, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonPatioLawnAndGardenDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonPatioLawnAndGardenDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Patio_Lawn_and_Garden'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Patio_Lawn_and_Garden.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Patio_Lawn_and_Garden.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'title:token',
                            5: 'sales_type:token',
                            6: 'sales_rank:float',
                            7: 'categories:token_seq',
                            8: 'price:float',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 5]
            categories = origin_data.iloc[i, 6]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(5, 'sales_type', pd.Series(sales_type))
        finished_data.insert(6, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(7, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonKindleStoreDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonKindleStoreDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Kindle_Store'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Kindle_Store.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Kindle_Store.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'price:float',
                            5: 'categories:token_seq',
                            6: 'title:token',
                            7: 'sales_type:token',
                            8: 'sales_rank:float',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 7]
            categories = origin_data.iloc[i, 5]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(5, 'categories', pd.Series(new_categories))
        finished_data.insert(7, 'sales_type', pd.Series(sales_type))
        finished_data.insert(8, 'sales_rank', pd.Series(sales_rank))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonHomeAndKitchenDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonHomeAndKitchenDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Home_and_Kitchen'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Home_and_Kitchen.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Home_and_Kitchen.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'sales_type:token',
                            2: 'sales_rank:float',
                            4: 'categories:token_seq',
                            5: 'title:token',
                            8: 'price:float',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 1]
            categories = origin_data.iloc[i, 3]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(1, 'sales_type', pd.Series(sales_type))
        finished_data.insert(2, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(4, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonGroceryAndGourmetFoodDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonGroceryAndGourmetFoodDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Grocery_and_Gourmet_Food'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Grocery_and_Gourmet_Food.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Grocery_and_Gourmet_Food.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'title:token',
                            5: 'sales_type:token',
                            6: 'sales_rank:float',
                            7: 'categories:token_seq',
                            8: 'price:float',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 5]
            categories = origin_data.iloc[i, 6]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(5, 'sales_type', pd.Series(sales_type))
        finished_data.insert(6, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(7, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonHealthAndPersonalCareDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonHealthAndPersonalCareDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Health_and_Personal_Care'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Health_and_Personal_Care.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Health_and_Personal_Care.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'title:token',
                            5: 'sales_type:token',
                            6: 'sales_rank:float',
                            7: 'categories:token_seq',
                            8: 'price:float',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 5]
            categories = origin_data.iloc[i, 6]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(5, 'sales_type', pd.Series(sales_type))
        finished_data.insert(6, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(7, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonPetSuppliesDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonPetSuppliesDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Pet_Supplies'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Pet_Supplies.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Pet_Supplies.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'title:token',
                            3: 'price:float',
                            4: 'sales_type:token',
                            5: 'sales_rank:float',
                            7: 'brand:token',
                            8: 'categories:token_seq'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 4]
            categories = origin_data.iloc[i, 7]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(4, 'sales_type', pd.Series(sales_type))
        finished_data.insert(5, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(8, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonSportsAndOutdoorsDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonSportsAndOutdoorsDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Sports_and_Outdoors'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Sports_and_Outdoors.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Sports_and_Outdoors.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'title:token',
                            2: 'price:float',
                            5: 'brand:token',
                            6: 'categories:token_seq',
                            7: 'sales_type:token',
                            8: 'sales_rank:float'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 7]
            categories = origin_data.iloc[i, 6]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(6, 'categories', pd.Series(new_categories))
        finished_data.insert(7, 'sales_type', pd.Series(sales_type))
        finished_data.insert(8, 'sales_rank', pd.Series(sales_rank))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonToysAndGamesDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonToysAndGamesDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Toys_and_Games'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Toys_and_Games.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Toys_and_Games.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'title:token',
                            3: 'price:float',
                            4: 'sales_type:token',
                            5: 'sales_rank:float',
                            7: 'brand:token',
                            8: 'categories:token_seq'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 4]
            categories = origin_data.iloc[i, 7]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(4, 'sales_type', pd.Series(sales_type))
        finished_data.insert(5, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(8, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonElectronicsDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonElectronicsDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Electronics'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Electronics.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Electronics.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            3: 'categories:token_seq',
                            4: 'title:token',
                            5: 'price:float',
                            6: 'sales_type:token',
                            7: 'sales_rank:float',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 6]
            categories = origin_data.iloc[i, 3]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(3, 'categories', pd.Series(new_categories))
        finished_data.insert(6, 'sales_type', pd.Series(sales_type))
        finished_data.insert(7, 'sales_rank', pd.Series(sales_rank))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonOfficeProductsDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonOfficeProductsDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Office_Products'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Office_Products.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Office_Products.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'price:float',
                            5: 'sales_type:token',
                            6: 'sales_rank:float',
                            7: 'categories:token_seq',
                            8: 'title:token',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 5]
            categories = origin_data.iloc[i, 6]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(5, 'sales_type', pd.Series(sales_type))
        finished_data.insert(6, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(7, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonVideoGamesDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonVideoGamesDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Video_Games'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Video_Games.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Video_Games.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            2: 'price:float',
                            5: 'sales_type:token',
                            6: 'sales_rank:float',
                            7: 'categories:token_seq',
                            8: 'title:token',
                            9: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 5]
            categories = origin_data.iloc[i, 6]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(5, 'sales_type', pd.Series(sales_type))
        finished_data.insert(6, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(7, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class AmazonMusicalInstrumentsDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(AmazonMusicalInstrumentsDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'Amazon_Musical_Instruments'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ratings_Musical_Instruments.csv')
        self.item_file = os.path.join(self.input_path, 'meta_Musical_Instruments.json')

        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'user_id:token',
                             1: 'item_id:token',
                             2: 'rating:float',
                             3: 'timestamp:float'}

        self.item_fields = {0: 'item_id:token',
                            1: 'title:token',
                            2: 'price:float',
                            4: 'sales_type:token',
                            5: 'sales_rank:float',
                            6: 'categories:token_seq',
                            8: 'brand:token'}

    def count_num(self, data):
        user_set = set()
        item_set = set()
        for i in tqdm(range(data.shape[0])):
            user_id = data.iloc[i, 0]
            item_id = data.iloc[i, 1]
            if user_id not in user_set:
                user_set.add(user_id)

            if item_id not in item_set:
                item_set.add(item_id)
        user_num = len(user_set)
        item_num = len(item_set)
        sparsity = 1 - (data.shape[0] / (user_num * item_num))
        print(user_num, item_num, data.shape[0], sparsity)

    def load_inter_data(self):
        inter_data = pd.read_csv(self.inter_file, delimiter=self.sep, header=None, engine='python')
        self.count_num(inter_data)
        return inter_data

    def load_item_data(self):
        origin_data = self.getDF(self.item_file)
        sales_type = []
        sales_rank = []
        new_categories = []
        finished_data = origin_data.drop(columns=['salesRank', 'categories'])
        for i in tqdm(range(origin_data.shape[0])):
            salesRank = origin_data.iloc[i, 4]
            categories = origin_data.iloc[i, 5]
            categories_set = set()
            for j in range(len(categories)):
                for k in range(len(categories[j])):
                    categories_set.add(categories[j][k])
            new_categories.append(str(categories_set)[1:-1])
            if pd.isnull(salesRank):
                sales_type.append(None)
                sales_rank.append(None)
            else:
                for key in salesRank:
                    sales_type.append(key)
                    sales_rank.append(salesRank[key])
        finished_data.insert(4, 'sales_type', pd.Series(sales_type))
        finished_data.insert(5, 'sales_rank', pd.Series(sales_rank))
        finished_data.insert(6, 'categories', pd.Series(new_categories))
        return finished_data

    def convert(self, input_data, selected_fields, output_file):
        output_data = pd.DataFrame()
        for column in selected_fields:
            output_data[self.item_fields[column]] = input_data.iloc[:, column]
        output_data.to_csv(output_file, index=0, header=1, sep='\t')

    def convert_item(self):
        try:
            # self.load_inter_data()
            input_item_data = self.load_item_data()
            # print(input_item_data)
            self.convert(input_item_data, self.item_fields, self.output_item_file)
        except NotImplementedError:
            print('This dataset can\'t be converted to item file\n')


class YELPDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(YELPDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'yelp'

        # input file
        self.inter_file = os.path.join(self.input_path, 'yelp_academic_dataset_review.json')
        self.item_file = os.path.join(self.input_path, 'yelp_academic_dataset_business.json')
        self.user_file = os.path.join(self.input_path, 'yelp_academic_dataset_user.json')

        # output_file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'review_id:token',
                             1: 'user_id:token',
                             2: 'business_id:token',
                             3: 'stars:float',
                             4: 'useful:float',
                             5: 'funny:float',
                             6: 'cool:float',
                             8: 'date:float'}

        self.item_fields = {0: 'business_id:token',
                            1: 'name:token_seq',
                            2: 'address:token_seq',
                            3: 'city:token_seq',
                            4: 'state:token',
                            5: 'postal_code:token',
                            6: 'latitude:float',
                            7: 'longitude:float',
                            8: 'stars:float',
                            9: 'review_count:float',
                            10: 'is_open:float',
                            12: 'categories:token_seq'}

        self.user_fields = {0: 'user_id:token',
                            1: 'name:token',
                            2: 'review_count:float',
                            3: 'yelping_since:float',
                            4: 'useful:float',
                            5: 'funny:float',
                            6: 'cool:float',
                            7: 'elite:token',
                            9: 'fans:float',
                            10: 'average_stars:float',
                            11: 'compliment_hot:float',
                            12: 'compliment_more:float',
                            13: 'compliment_profile:float',
                            14: 'compliment_cute:float',
                            15: 'compliment_list:float',
                            16: 'compliment_note:float',
                            17: 'compliment_plain:float',
                            18: 'compliment_cool:float',
                            19: 'compliment_funny:float',
                            20: 'compliment_writer:float',
                            21: 'compliment_photos:float'}

    def load_item_data(self):
        return pd.read_json(self.item_file, lines=True)

    def convert_inter(self):
        fin = open(self.inter_file, "r")
        fout = open(self.output_inter_file, "w")

        lines_count = 0
        for _ in fin:
            lines_count += 1
        fin.seek(0, 0)

        fout.write('\t'.join([self.inter_fields[column] for column in self.inter_fields.keys()]) + '\n')

        for i in tqdm(range(lines_count)):
            line = fin.readline()
            line_dict = json.loads(line)
            line_dict['date'] = int(time.mktime(time.strptime(line_dict['date'], "%Y-%m-%d %H:%M:%S")))
            fout.write('\t'.join([str(line_dict[self.inter_fields[key][0:self.inter_fields[key].find(":")]]) for key in
                                  self.inter_fields.keys()]) + '\n')

        fin.close()
        fout.close()

    def convert_user(self):
        fin = open(self.user_file, "r")
        fout = open(self.output_user_file, "w")

        lines_count = 0
        for _ in fin:
            lines_count += 1
        fin.seek(0, 0)

        fout.write('\t'.join([self.user_fields[column] for column in self.user_fields.keys()]) + '\n')

        for i in tqdm(range(lines_count)):
            line = fin.readline()
            line_dict = json.loads(line)
            line_dict['yelping_since'] = int(
                time.mktime(time.strptime(line_dict['yelping_since'], "%Y-%m-%d %H:%M:%S")))
            fout.write('\t'.join([str(line_dict[self.user_fields[key][0:self.user_fields[key].find(":")]]) for key in
                                  self.user_fields.keys()]) + '\n')

        fin.close()
        fout.close()


class LASTFMDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(LASTFMDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'lastfm'

        # input file
        self.item_file = os.path.join(self.input_path, 'artists.dat')
        self.tag_file = os.path.join(self.input_path, 'tags.dat')
        self.inter_file1 = os.path.join(self.input_path, 'user_artists.dat')
        self.inter_file2 = os.path.join(self.input_path, 'user_taggedartists-timestamps.dat')
        self.sep = "\t"

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.item_fields = {0: 'id:token',
                            1: 'name:token',
                            2: 'url:token',
                            3: 'picture_url:token'}
        self.inter_fields = {0: 'user_id:token',
                             1: 'artist_id:token',
                             2: 'weight:float',
                             3: 'tag_value:token_seq'}

    def load_item_data(self):
        return pd.read_csv(self.item_file, delimiter=self.sep, engine='python', quoting=3)

    def load_inter_data(self):
        # read the tags
        tags = {}
        fin = open(self.tag_file, "r", encoding='cp1252')
        next(fin)
        for line in fin:
            line = line.strip()
            line_list = line.split('\t')
            tags[line_list[0]] = line_list[1]

        origin_data1 = pd.read_csv(self.inter_file1, delimiter=self.sep, engine='python')
        origin_data2 = pd.read_csv(self.inter_file2, delimiter=self.sep, engine='python')
        origin_data1['tag_id'] = ''
        index = 0

        origin_data2 = pd.merge(origin_data2, origin_data1, how='inner')
        for i in tqdm(range(origin_data2.shape[0])):
            while not (origin_data2.iloc[i, 0] == origin_data1.iloc[index, 0] and origin_data2.iloc[i, 1] ==
                       origin_data1.iloc[index, 1]):
                index += 1
            if origin_data1.iloc[index, 3] == '':
                origin_data1.iloc[index, 3] += tags[str(origin_data2.iloc[i, 2])]
            else:
                origin_data1.iloc[index, 3] += ',' + tags[str(origin_data2.iloc[i, 2])]
        return origin_data1


class YAHOOMUSICDataset(BaseDataset):
    def __init__(self, input_path, output_path):
        super(YAHOOMUSICDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'yahoo-music'

        # input file
        self.inter_file = os.path.join(self.input_path, 'ydata-ymusic-user-artist-ratings-v1_0.txt')
        self.item_file = os.path.join(self.input_path, 'ydata-ymusic-artist-names-v1_0.txt')
        self.sep = '\t'

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        self.inter_fields = {0: 'anonymous_user_id:token',
                             1: 'artist_id:token',
                             2: 'rating:float'}
        self.item_fields = {0: 'artist_id:token',
                            1: 'name:token'}

    def convert_inter(self):
        fin = open(self.inter_file, "r")
        fout = open(self.output_inter_file, "w")

        lines_count = 0
        for _ in fin:
            lines_count += 1
        fin.seek(0, 0)

        fout.write('\t'.join([self.inter_fields[column] for column in self.inter_fields.keys()]) + '\n')

        for i in tqdm(range(lines_count)):
            line = fin.readline()
            line_list = line.split('\t')
            fout.write('\t'.join([str(line_list[i]) for i in range(len(line_list))]))

        fin.close()
        fout.close()

    def convert_item(self):
        fin = open(self.item_file, "r", encoding='cp1252')
        fout = open(self.output_item_file, "w")

        lines_count = 0
        for _ in fin:
            lines_count += 1
        fin.seek(0, 0)

        fout.write('\t'.join([self.item_fields[column] for column in self.item_fields.keys()]) + '\n')

        for i in tqdm(range(lines_count)):
            line = fin.readline()
            line_list = line.split('\t')
            fout.write('\t'.join([str(line_list[i]) for i in range(len(line_list))]))

        fin.close()
        fout.close()


class YOOCHOOSEDataset(BaseDataset):
    def __init__(self, input_path, output_path, interaction_type, duplicate_removal):
        super(YOOCHOOSEDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'yoochoose'
        self.interaction_type = interaction_type
        assert self.interaction_type in ['click', 'buy'], 'interaction_type must be in [click, buy]'
        self.duplicate_removal = duplicate_removal

        self.sep = ','
        if self.duplicate_removal:
            if self.interaction_type == 'click':
                self.inter_fields = {0: 'session_id:token',
                                     1: 'item_id:token',
                                     3: 'count:float',
                                     4: 'timestamp:float'}
            elif self.interaction_type == 'buy':
                self.inter_fields = {0: 'session_id:token',
                                     1: 'item_id:token',
                                     2: 'count:float',
                                     3: 'timestamp:float'}
        else:
            if self.interaction_type == 'click':
                self.inter_fields = {0: 'session_id:token',
                                     1: 'timestamp:float',
                                     2: 'item_id:token',
                                     3: 'category:token'}
            elif self.interaction_type == 'buy':
                self.inter_fields = {0: 'session_id:token',
                                     1: 'timestamp:float',
                                     2: 'item_id:token',
                                     3: 'price:float',
                                     4: 'quantity:float'}
        if self.interaction_type == 'click':
            self.inter_file = os.path.join(self.input_path, 'yoochoose-clicks.dat')
            self.output_inter_file = os.path.join(self.output_path, 'yoochoose-clicks.inter')
        elif self.interaction_type == 'buy':
            self.inter_file = os.path.join(self.input_path, 'yoochoose-buys.dat')
            self.output_inter_file = os.path.join(self.output_path, 'yoochoose-buys.inter')

    def convert_inter(self):
        if self.duplicate_removal:
            fin = open(self.inter_file, "r")
            fout = open(self.output_inter_file, "w")

            lines_count = 0
            for _ in fin:
                lines_count += 1
            fin.seek(0, 0)

            fout.write('\t'.join([self.inter_fields[column] for column in self.inter_fields.keys()]) + '\n')

            current_list = []
            for i in tqdm(range(lines_count)):
                line = fin.readline()
                line_list = line.split(',')
                if i == 0:
                    current_list.append(line_list[0])
                    current_list.append(line_list[2])
                    current_list.append(1)
                    current_list.append(int(time.mktime(time.strptime(line_list[1][0:19], "%Y-%m-%dT%H:%M:%S"))))
                elif line_list[0] == current_list[0] and line_list[2] == current_list[1]:
                    current_list[2] += 1
                    current_list[3] = int(time.mktime(time.strptime(line_list[1][0:19], "%Y-%m-%dT%H:%M:%S")))
                else:
                    fout.write('\t'.join([str(current_list[i]) for i in range(len(current_list))]) + '\n')
                    current_list.clear()
                    current_list.append(line_list[0])
                    current_list.append(line_list[2])
                    current_list.append(1)
                    current_list.append(int(time.mktime(time.strptime(line_list[1][0:19], "%Y-%m-%dT%H:%M:%S"))))

            fout.write('\t'.join([str(current_list[i]) for i in range(len(current_list))]))
            fin.close()
            fout.close()

        else:
            fin = open(self.inter_file, "r")
            fout = open(self.output_inter_file, "w")

            lines_count = 0
            for _ in fin:
                lines_count += 1
            fin.seek(0, 0)

            fout.write('\t'.join([self.inter_fields[column] for column in self.inter_fields.keys()]) + '\n')

            for i in tqdm(range(lines_count)):
                line = fin.readline()
                line_list = line.split(',')
                line_list[1] = int(time.mktime(time.strptime(line_list[1][0:19], "%Y-%m-%dT%H:%M:%S")))
                fout.write('\t'.join([str(line_list[i]) for i in range(len(line_list))]))

            fin.close()
            fout.close()


class RETAILROCKETDataset(BaseDataset):
    def __init__(self, input_path, output_path, interaction_type, duplicate_removal):
        super(RETAILROCKETDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'retailrocket'
        self.interaction_type = interaction_type
        assert self.interaction_type in ['view', 'addtocart', 'transaction'], 'interaction_type must be in [view, addtocart, transaction]'
        self.duplicate_removal = duplicate_removal

        # input file
        self.inter_file = os.path.join(self.input_path, 'events.csv')
        self.item_file1 = os.path.join(self.input_path, 'item_properties_part1.csv')
        self.item_file2 = os.path.join(self.input_path, 'item_properties_part2.csv')
        self.sep = ','

        # output file
        if self.interaction_type == 'view':
            self.output_inter_file = os.path.join(self.output_path, 'retailrocket-view.inter')
        elif self.interaction_type == 'addtocart':
            self.output_inter_file = os.path.join(self.output_path, 'retailrocket-addtocart.inter')
        elif self.interaction_type == 'transaction':
            self.output_inter_file = os.path.join(self.output_path, 'retailrocket-transaction.inter')
        self.output_item_file = os.path.join(self.output_path, 'retailrocket.item')

        # selected feature fields
        if self.duplicate_removal:
            if self.interaction_type == 'view':
                self.inter_fields = {0: 'timestamp:float',
                                     1: 'visitor_id:token',
                                     2: 'item_id:token',
                                     3: 'count:float'}
            elif self.interaction_type == 'addtocart':
                self.inter_fields = {0: 'timestamp:float',
                                     1: 'visitor_id:token',
                                     2: 'item_id:token',
                                     3: 'count:float'}
            elif self.interaction_type == 'transaction':
                self.inter_fields = {0: 'timestamp:float',
                                     1: 'visitor_id:token',
                                     2: 'item_id:token',
                                     3: 'count:float'}
        else:
            if self.interaction_type == 'view':
                self.inter_fields = {0: 'timestamp:float',
                                     1: 'visitor_id:token',
                                     2: 'item_id:token'}
            elif self.interaction_type == 'addtocart':
                self.inter_fields = {0: 'timestamp:float',
                                     1: 'visitor_id:token',
                                     2: 'item_id:token'}
            elif self.interaction_type == 'transaction':
                self.inter_fields = {0: 'timestamp:float',
                                     1: 'visitor_id:token',
                                     2: 'item_id:token',
                                     3: 'transaction_id:token'}
        self.item_fields = {0: 'timestamp:float',
                            1: 'item_id:token',
                            2: 'property:token',
                            3: 'value:token_seq'}

    def convert_inter(self):
        if self.duplicate_removal:
            fin = open(self.inter_file, "r")
            fout = open(self.output_inter_file, "w")

            lines_count = 0
            for _ in fin:
                lines_count += 1
            fin.seek(0, 0)

            fout.write('\t'.join([self.inter_fields[column] for column in self.inter_fields.keys()]) + '\n')
            dic = {}

            for i in tqdm(range(lines_count)):
                if i == 0:
                    fin.readline()
                    continue
                line = fin.readline()
                line_list = line.split(',')
                key = (line_list[1], line_list[3])
                if line_list[2] == self.interaction_type:
                    if key not in dic:
                        dic[key] = (line_list[0], 1)
                    else:
                        if line_list[0] > dic[key][0]:
                            dic[key] = (line_list[0], dic[key][1] + 1)
                        else:
                            dic[key] = (dic[key][0], dic[key][1] + 1)

            for key in dic.keys():
                fout.write(dic[key][0] + '\t' + key[0] + '\t' + key[1] + '\t' + str(dic[key][1]) + '\n')

            fin.close()
            fout.close()
        else:
            fin = open(self.inter_file, "r")
            fout = open(self.output_inter_file, "w")

            lines_count = 0
            for _ in fin:
                lines_count += 1
            fin.seek(0, 0)

            fout.write('\t'.join([self.inter_fields[column] for column in self.inter_fields.keys()]) + '\n')

            for i in tqdm(range(lines_count)):
                if i == 0:
                    fin.readline()
                    continue
                line = fin.readline()
                line_list = line.split(',')
                if line_list[2] == self.interaction_type:
                    if self.interaction_type != 'transaction':
                        del line_list[4]
                    else: line_list[4] = line_list[4].strip()
                    del line_list[2]
                    fout.write('\t'.join([str(line_list[i]) for i in range(len(line_list))]) + '\n')

            fin.close()
            fout.close()

    def convert_item(self):
        fin1 = open(self.item_file1, "r")
        fin2 = open(self.item_file2, "r")
        fout = open(self.output_item_file, "w")

        lines_count1 = 0
        for _ in fin1:
            lines_count1 += 1
        fin1.seek(0, 0)

        lines_count2 = 0
        for _ in fin2:
            lines_count2 += 1
        fin2.seek(0, 0)

        fout.write('\t'.join([self.item_fields[column] for column in self.item_fields.keys()]) + '\n')

        for i in tqdm(range(lines_count1)):
            if i == 0:
                line = fin1.readline()
                continue
            line = fin1.readline()
            line_list = line.split(',')
            fout.write('\t'.join([str(line_list[i]) for i in range(len(line_list))]))

        for i in tqdm(range(lines_count2)):
            if i == 0:
                line = fin2.readline()
                continue
            line = fin2.readline()
            line_list = line.split(',')
            fout.write('\t'.join([str(line_list[i]) for i in range(len(line_list))]))

        fin1.close()
        fin2.close()
        fout.close()


class TAFENGDataset(BaseDataset):
    def __init__(self, input_path, output_path, duplicate_removal):
        super(TAFENGDataset, self).__init__(input_path, output_path)
        self.dataset_name = 'ta-feng'
        self.duplicate_removal = duplicate_removal

        # input file
        self.inter_file = os.path.join(self.input_path, 'ta_feng_all_months_merged.csv')
        self.sep = ','

        # output file
        self.output_inter_file, self.output_item_file, self.output_user_file = self.get_output_files()

        # selected feature fields
        if self.duplicate_removal:
            self.inter_fields = {0: 'transaction_date:float',
                                 1: 'customer_id:token',
                                 2: 'product_id:token',
                                 3: 'amount:float'}
        else:
            self.inter_fields = {0: 'transaction_date:float',
                                 1: 'customer_id:token',
                                 2: 'age_group:token',
                                 3: 'pin_code:token',
                                 4: 'product_subclass:token',
                                 5: 'product_id:token',
                                 6: 'amount:float',
                                 7: 'asset:float',
                                 8: 'sales_price:float'}

    def convert_inter(self):
        if self.duplicate_removal:
            fin = open(self.inter_file, "r")
            fout = open(self.output_inter_file, "w")

            lines_count = 0
            for _ in fin:
                lines_count += 1
            fin.seek(0, 0)
            fout.write('\t'.join([self.inter_fields[column] for column in self.inter_fields.keys()]) + '\n')

            dic = {}
            for i in tqdm(range(lines_count)):
                if i == 0:
                    fin.readline()
                    continue
                line = fin.readline()
                line_list = line.split(',')
                line_list[-1] = line_list[-1].strip()
                for j in range(len(line_list)):
                    line_list[j] = line_list[j][1:-1]
                line_list[0] = int(time.mktime(time.strptime(line_list[0], "%m/%d/%Y")))
                key = (line_list[1], line_list[5])
                if key not in dic:
                    dic[key] = (line_list[0], int(line_list[6]))
                else:
                    if line_list[0] > dic[key][0]:
                        dic[key] = (line_list[0], dic[key][1] + int(line_list[6]))
                    else:
                        dic[key] = (dic[key][0], dic[key][1] + int(line_list[6]))

            for key in dic.keys():
                fout.write(str(dic[key][0]) + '\t' + key[0] + '\t' + key[1] + '\t' + str(dic[key][1]) + '\n')

            fin.close()
            fout.close()
        else:
            fin = open(self.inter_file, "r")
            fout = open(self.output_inter_file, "w")

            lines_count = 0
            for _ in fin:
                lines_count += 1
            fin.seek(0, 0)

            fout.write('\t'.join([self.inter_fields[column] for column in self.inter_fields.keys()]) + '\n')

            for i in tqdm(range(lines_count)):
                if i == 0:
                    fin.readline()
                    continue
                line = fin.readline()
                line_list = line.split(',')
                line_list[-1] = line_list[-1].strip()
                for j in range(len(line_list)):
                    line_list[j] = line_list[j][1:-1]
                line_list[0] = int(time.mktime(time.strptime(line_list[0], "%m/%d/%Y")))
                fout.write('\t'.join([str(line_list[j]) for j in range(len(line_list))]) + '\n')

            fin.close()
            fout.close()
