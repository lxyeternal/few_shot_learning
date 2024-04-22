# -*- coding: utf-8 -*-
# @Time    : 2023/3/11 22:40
# @Author  : blue
# @FileName: cmpmain.py
# @Software: Vscode

import sys
sys.path.append("/data1/gwb/few_shot_learning/")

from compare.constructdata import ConstructData
from compare.rf import RFModel
from compare.cnn import CNNModel
from compare.gru import GRUModel

class CmpMain:
    def __init__(self, nway, kshot) -> None:
        self.nway = nway
        self.kshot = kshot
        constructdata = ConstructData(nway, kshot)
        constructdata.selectfile()
        constructdata.sample2vec()
        self.train_sample_vec = constructdata.train_sample_vec
        self.train_label = constructdata.train_label
        self.valid_sample_vec = constructdata.valid_sample_vec
        self.valid_label = constructdata.valid_label


    def start(self):

        # rfmodel = RFModel(self.train_sample_vec, self.train_label, self.valid_sample_vec, self.valid_label)
        # rfmodel.rf_alg()

        cnnmodel = CNNModel(self.train_sample_vec, self.train_label, self.valid_sample_vec, self.valid_label, self.nway)
        cnnmodel.cnn_alg()

        # grumodel = GRUModel(self.train_sample_vec, self.train_label, self.valid_sample_vec, self.valid_label, self.nway)
        # grumodel.gru_alg()



if __name__ == '__main__':
    cmpmain = CmpMain(2, 5)
    cmpmain.start()