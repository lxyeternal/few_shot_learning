# -*- coding: UTF-8 -*-
"""
@Project ：few_shot_learning 
@File    ：glove_model.py
@Author  ：honywen
@Date    ：2022/12/29 15:41 
@Software: PyCharm
"""

import os
import json
from glove import Glove
from glove import Corpus


class GloveModel:
    def __init__(self):
        self.config_path = "./config.json"
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
        corpus_model = Corpus()
        corpus_model.fit(self.traindata, window=self.config['window'])
        print('Dict size: %s' % len(corpus_model.dictionary))
        print('Collocations: %s' % corpus_model.matrix.nnz)
        glove = Glove(no_components = self.config['embedding_size'],
                      learning_rate = self.config['learning_rate'])  # no_components 维度，可以与word2vec一起使用。
        glove.fit(corpus_model.matrix,
                  epochs = self.config['epochs'],
                  no_threads = self.config['no_threads'],
                  verbose = True)
        glove.add_dictionary(corpus_model.dictionary)

        # # 3.glove模型保存与加载
        # corpus_model.save(self.config['glove_model_path'])
        # Save the GloVe model vectors to a text file
        with open(self.config['glove_model_path'], 'w', encoding='utf-8') as fw:
            for word, index in glove.dictionary.items():
                vector = ' '.join(map(str, glove.word_vectors[index]))
                fw.write(f"{word} {vector}\n")

        print('Vectors saved to glove_vectors.txt.')
        # corpus_model = Corpus.load('corpus.model')
        # 指定词条词向量
        print(glove.word_vectors[glove.dictionary['int']])


if __name__ == '__main__':
    glovemodel = GloveModel()
    glovemodel.trainvec()