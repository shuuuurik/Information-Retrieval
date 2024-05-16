import os
import bisect
import math


class DatasetIterator:

    def __init__(self, dataset_path, *, wide_param=1000):
        self.corpora_path = dataset_path
        self.index_list = []
        self.index_list_size = []
        self.index_wide = wide_param
        self.limitation = None
        self.counter = 0

    def __next__(self):
        border = self.get_dataset_size()
        if self.limitation is not None:
            border = min(self.limitation, border)
        if self.counter < border:
            target = self.get_text_path_by_id(self.counter)
            self.counter += 1
            return target
        else:
            raise StopIteration
        
    def __iter__(self):
        return self

    def get_text_path_by_id(self, text_id):
        index = bisect.bisect_right(self.index_list_size, text_id)
        if index == 0:
            bias = 0
        else:
            bias = self.index_list_size[index - 1]
        second_index = text_id - bias
        return self.index_list[index][0] + "\\" + self.index_list[index][1][second_index // self.index_wide][
            second_index % self.index_wide]

    def build_index_list(self):
        absorbed_len = 0
        all_dirs = self.get_all_subdir()
        for cur_dir in all_dirs:
            cur_dir = self.corpora_path + "\\" + cur_dir
            all_cur_texts = self.get_all_txt(cur_dir)
            absorbed_len = absorbed_len + + len(all_cur_texts)
            self.index_list.append((cur_dir, self.build_index_cell(all_cur_texts)))
            self.index_list_size.append(absorbed_len)

    def build_index_cell(self, all_cur_texts):
        cur_list_cell = [None] * (math.ceil(len(all_cur_texts) / self.index_wide))
        for i in range(len(cur_list_cell)):
            cur_list_cell[i] = []
        for index, sample in enumerate(all_cur_texts):
            cur_list_cell[index // self.index_wide].append(sample)
        return cur_list_cell

    def get_all_subdir(self):
        return [d for d in os.listdir(self.corpora_path) if os.path.isdir(os.path.join(self.corpora_path, d))]

    @staticmethod
    def get_all_txt(path):
        return [file for file in os.listdir(path) if file.endswith(".txt")]

    def get_dataset_size(self):
        return self.index_list_size[-1]

    def set_start_iter(self, start):
        if isinstance(start, int) and start >= 0:
            self.counter = start

    def set_limitation(self, limit):
        if isinstance(limit, int) and limit > 0:
            self.limitation = min(limit, self.get_dataset_size())
