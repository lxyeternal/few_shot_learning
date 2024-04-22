# -*- coding: utf-8 -*-
# @Time    : 2023/3/11 21:20
# @Author  : blue
# @FileName: constructdata.py
# @Software: Vscode


import os
import json
import random
import numpy as np



class ConstructData:
    def __init__(self, nway, kshot) -> None:
        with open("config.json", "r") as fr:
            self.config = json.load(fr)
        self.word_vector_path = self.config['word_vector_path']
        self.cwedata_dir = "../data/cwedata/"
        self.nway = nway
        self.kshot = kshot
        self.train_sample = list()
        self.train_sample_vec = list()
        self.train_label = list()
        self.valid_sample = list()
        self.valid_sample_vec = list()
        self.valid_label = list()
        self.glove_vector = {}

    
    def read_txt(self, filename):
        fr = open(filename, "r")
        fr_content = fr.read().strip()
        content_split = fr_content.split("\n")
        train_sample = random.sample(content_split, self.kshot)
        valid_sample = [x for x in content_split if x not in train_sample]
        return train_sample, valid_sample


    def selectfile(self):
        cwefiles = os.listdir(self.cwedata_dir)
        random_files = random.sample(cwefiles, self.nway)
        files_fullpath = [os.path.join(self.cwedata_dir, filename) for filename in random_files]
        for filepath in files_fullpath:
            file_train_sample, file_valid_sample = self.read_txt(filepath)
            sample_count = len(file_train_sample) + len(file_valid_sample)
            self.train_sample = self.train_sample + file_train_sample
            self.valid_sample = self.valid_sample + file_valid_sample
            self.train_label = self.train_label + [files_fullpath.index(filepath)] * len(file_train_sample)
            self.valid_label = self.valid_label + [files_fullpath.index(filepath)] * len(file_valid_sample)


    def word_vec(self, sample_vocab):
        word_vectors = list()
        with open(self.word_vector_path, "r", encoding="utf8") as fr:
            for line in fr.readlines():
                line_list = line.strip().split(" ")
                self.glove_vector[line_list[0]] = line_list[1:]

        for i in range(1, len(sample_vocab)):
            if self.glove_vector.get(sample_vocab[i], None):
                word_vectors.append(self.glove_vector[sample_vocab[i]])
        return word_vectors
    

    def sample2vec(self):
        for sample in self.train_sample:
            sample_split = sample.split(" ")
            word_vectors = self.word_vec(sample_split)
            self.train_sample_vec.append(word_vectors)
        for sample in self.valid_sample:
            sample_split = sample.split(" ")
            word_vectors = self.word_vec(sample_split)
            self.valid_sample_vec.append(word_vectors)
        


# if __name__ == '__main__':
#     constructdata = ConstructData(3, 5)
#     constructdata.selectfile()
#     constructdata.sample2vec()


