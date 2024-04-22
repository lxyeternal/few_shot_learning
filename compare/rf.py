# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 14:35
# @Author  : blue
# @FileName: rf.py
# @Software: PyCharm


import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn import metrics


class RFModel:
    def __init__(self,train_data,train_label,test_data,test_label):
        self.train_data = train_data
        self.train_label = np.array(train_label)
        self.test_data = test_data
        self.test_label = np.array(test_label)


    def preprocess(self, dataset):
        # 定义空的二维np
        data_feature = list()
        for data_index in range(len(dataset)):
            float_list = [[float(val) for val in sub_list] for sub_list in dataset[data_index]]
            mean = np.mean(float_list, axis=0)
            data_feature.append(mean)
        return data_feature


    def rf_alg(self):
        self.train_data = np.array(self.preprocess(self.train_data))
        self.test_data = np.array(self.preprocess(self.test_data))
        rf_model = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                                          max_depth=None, max_features='auto', max_leaf_nodes=None,
                                          min_samples_leaf=1, min_samples_split=2,
                                          min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=1,
                                          oob_score=False, random_state=None, verbose=0,
                                          warm_start=False)

        print("[INFO] Successfully initialize a RF model !")
        print("[INFO] Training the model…… ")
        #   进行模型训练
        rf_model.fit(self.train_data, self.train_label)
        print("[INFO] Model training completed !")
        # 保存训练好的模型，下次使用时直接加载就可以了
        model_path = 'Model/mult_rf.pkl'
        joblib.dump(rf_model, model_path)
        print("[INFO] Model has been saved !")
        #   进行测试数据的预测
        rf_predictions = rf_model.predict(self.test_data)
        #   给出每一个标签的预测概率
        rf_probs = rf_model.predict_proba(self.test_data)[:, 1]
        #   计算模型的准确率
        rf_acc = metrics.accuracy_score(rf_predictions, self.test_label)
        rf_confusion_matrix = metrics.confusion_matrix(self.test_label, rf_predictions, labels=None, sample_weight=None)
        print("confusion metrix:\n", rf_confusion_matrix)
        print("overall accuracy: %f" % (rf_acc))
        print(rf_predictions)
        print(rf_probs)

        # label_list = ['0','1','2','3','4']
        # rf_classification_rep = classification_report(self.test_label, rf_predictions, target_names=label_list)
        # print("classification report: \n", rf_classification_rep)