# -*- coding: UTF-8 -*-
"""
@Project ：few_shot_learning 
@File    ：word2vec_model.py
@Author  ：honywen
@Date    ：2022/12/29 15:40 
@Software: PyCharm
"""

import os
import json
from gensim.models import word2vec


class Word2vecModel:
    def __init__(self):
        self.config_path = "config.json"
        with open(self.config_path, "r") as fr:
            self.config = json.load(fr)
        self.traindata = list()


    def load_data(self):
        for dir in ["../reviews/eval/", "../reviews/train/"]:
            files = os.listdir(dir)
            for file in files:
                print("loading file: ", os.path.join(dir, file))
                f = open(os.path.join(dir, file), 'r')
                token_lines = f.readlines()
                for token_line in token_lines:
                    token_line_split = token_line.strip().split("\t")[0].split(" ")
                    self.traindata.append(token_line_split)


    def trainvec(self):
        self.load_data()
        model = word2vec.Word2Vec(self.traindata,
                                  workers = self.config['workers'],
                                  vector_size = self.config['embedding_size'],
                                  min_count = self.config['min_count'],
                                  window = self.config['window'],
                                  sample = self.config['sample'])
        # model.save("word2vec.model")
        model.wv.save_word2vec_format(self.config['word2vec_model_path'], binary=False)


if __name__ == '__main__':
    word2vecmodel = Word2vecModel()
    word2vecmodel.trainvec()


