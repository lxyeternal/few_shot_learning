# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 14:35
# @Author  : blue
# @FileName: svm.py
# @Software: PyCharm


import joblib
import numpy as np
from sklearn import svm
from sklearn import metrics
from sklearn.multiclass import OneVsRestClassifier


class SVMModel:
    def __init__(self,train_data,train_label,test_data,test_label):
        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_label = test_label


    def svm_alg(self):
        random_state = np.random.RandomState(10)
        model = OneVsRestClassifier(
            svm.SVC(kernel='linear', max_iter=-1, random_state=random_state))  #  多项式核函数：poly    高斯核函数：rbf     sigmod核函数：sigmoid
        print("[INFO] Successfully initialize a SVM model !")
        print("[INFO] Training the model…… ")
        #   模型训练
        clt = model.fit(self.train_data,self.train_label)
        print("[INFO] Model training completed !")
        # 保存训练好的模型，下次使用时直接加载就可以了
        model_path = 'Model/mult_svm.pkl'
        joblib.dump(clt,model_path)
        print("[INFO] Model has been saved !")
        y_test_pred = clt.predict(self.test_data)
        ov_acc = metrics.accuracy_score(y_test_pred, self.test_label)
        print("overall accuracy: %f" % (ov_acc))