# -*- coding: utf-8 -*-
# @Time    : 2023/3/11 21:20
# @Author  : blue
# @FileName: constructdata.py
# @Software: Vscode


import os
import json
import random
import numpy as np
import re

class ConstructData:
    def __init__(self, nway, kshot) -> None:
        with open("config.json", "r") as fr:
            self.config = json.load(fr)
        self.word_vector_path = self.config['word_vector_path']
        self.cwedata_dir = "../all/"
        self.nway = nway
        self.kshot = kshot
        self.train_samples = []
        self.train_sample_vec = []
        self.train_labels = [1,1,1,1,1,-1,-1,-1,-1,-1] * 103
        self.valid_samples = []
        self.valid_sample_vec = []
        self.valid_labels = []
        self.glove_vector = {}

    def read_txt(self, filename):
        fr = open(filename, "r")
        samples = fr.readlines()
        fr.close()

        random.shuffle(samples)

        samples_1 = []
        samples_neg_1 = []
        valid_sample = []

        for sample in samples:
            # print(sample)
            match = re.match(r'^(.*)\s+(-?1)$', sample.strip())
            if match:
                text = match.group(1).strip()
                label = match.group(2)
                label = label.strip()
                text = text.strip()
                # print("label:", label)
                # print("text:", text)
                if label.endswith("-1"):
                    # print("label -1: ", label)
                    samples_neg_1.append(text)
                elif label.endswith("1"):
                    # print("label 1: ", label)
                    samples_1.append(text)
            else:
                # 如果无法匹配到文本和标签，可以根据实际需求进行处理
                print("find unmatched")
                pass


        train_sample_1 = random.sample(samples_1, min(int(self.kshot/2), len(samples_1)))
        train_sample_neg_1 = random.sample(samples_neg_1, min(int(self.kshot/2), len(samples_neg_1)))
        for sample in samples_1:
            if sample not in train_sample_1:
                valid_sample.append(sample)
                self.valid_labels.append(1)
        for sample in samples_neg_1:
            if sample not in train_sample_neg_1:
                valid_sample.append(sample)
                self.valid_labels.append(-1)

        return train_sample_1 + train_sample_neg_1, valid_sample
    

    def load_word2vec(self):
        # 读取词向量文件，建立词向量字典
        with open(self.word_vector_path, "r", encoding="utf8") as fr:
            for line in fr.readlines():
                line_list = line.strip().split(" ")
                word = line_list[0]
                vector = [float(val) for val in line_list[1:]]  # 将词向量转换为 float 数组
                self.glove_vector[word] = vector


    def selectfile(self):
        cwefiles = os.listdir(self.cwedata_dir)
        files_fullpath = [os.path.join(self.cwedata_dir, filename) for filename in cwefiles]

        for filepath in files_fullpath:
            file_train_samples, file_valid_samples = self.read_txt(filepath)
            self.train_samples.extend(file_train_samples)
            self.valid_samples.extend(file_valid_samples)

    
    def word_vec(self, sample_vocab):
        word_vectors = []
        embedding_size = 300  # 单词嵌入向量长度为300
        max_length = 200  # 最大长度设定为200
        # 对每个单词进行处理
        for word in sample_vocab[:max_length]:
            if word in self.glove_vector:
                word_vectors.append(self.glove_vector[word])
            else:
                # 如果词语不在词向量模型中，使用全零向量进行填充
                word_vectors.append([0.0] * embedding_size)
        # 如果长度不足 200，进行填充操作
        if len(word_vectors) < max_length:
            padding_vector = [0.0] * embedding_size
            word_vectors.extend([padding_vector] * (max_length - len(word_vectors)))
        return word_vectors
    

    def sample2vec(self):
        self.load_word2vec()
        # print("train sample:", self.train_samples)
        for sample in self.train_samples:
            sample_split = sample.split(" ")
            word_vectors = self.word_vec(sample_split)
            self.train_sample_vec.append(word_vectors)
        for sample in self.valid_samples:
            sample_split = sample.split(" ")
            word_vectors = self.word_vec(sample_split)
            self.valid_sample_vec.append(word_vectors)


        


