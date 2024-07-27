# -*- coding: UTF-8 -*-
"""
@Project ：few_shot_learning 
@File    ：curve_chart.py
@Author  ：honywen
@Date    ：2023/1/8 22:26 
@Software: PyCharm
"""


import time
import heapq
import itertools
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import auc
from mpl_toolkits.axes_grid1 import host_subplot
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


def model_evaluation(test_real_label, test_pred_label):
    sklearn_accuracy = accuracy_score(test_real_label, test_pred_label)
    sklearn_precision = precision_score(test_real_label, test_pred_label, average='weighted')
    sklearn_recall = recall_score(test_real_label, test_pred_label, average='weighted')
    sklearn_f1 = f1_score(test_real_label, test_pred_label, average='weighted')
    print(sklearn_accuracy, sklearn_precision, sklearn_recall, sklearn_f1)


def get_confusion_matrix(test_real_label, test_pred_label, labels):
    conf_matrix = confusion_matrix(test_real_label, test_pred_label, labels)
    return conf_matrix


def draw_roc(test_real_label, pred_prob_list):
    fpr_keras, tpr_keras, thresholds_keras = metrics.roc_curve(test_real_label,
                                                               np.array(pred_prob_list)[:, 1])
    auc_keras = auc(fpr_keras, tpr_keras)
    plt.xlim([0.0, 1.02])
    plt.ylim([0.0, 1.02])

    plt.plot(fpr_keras, tpr_keras, label=' (auc = {:.4f})'.format(auc_keras))
    plt.title('ROC curve')
    plt.xlabel('True Positive Rate')
    plt.ylabel('False Positive Rate')
    plt.legend(loc='lower right')
    plt.grid()
    plt.savefig('roc.jpg')
    plt.show()


def draw_trainaccloss(loss_list, acc_list):
    host = host_subplot(111)  # row=1 col=1 first pic
    plt.subplots_adjust(right=0.8)  # ajust the right boundary of the plot window
    par1 = host.twinx()

    # set labels
    host.set_xlabel("task")
    host.set_ylabel("train loss")
    par1.set_ylabel("train accuracy")

    # plot curves
    p1, = host.plot(range(len(loss_list)), loss_list, label="loss")
    p2, = par1.plot(range(len(acc_list)), acc_list, label="accuracy")

    host.legend(loc=5)

    # set label color
    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())

    plt.grid()
    plt.draw()
    plt.savefig('/data1/gwb/few_shot_learning/visualization/new_trainaccloss.jpg')
    plt.show()


def draw_validaccloss(valid_loss_list, valid_acc_list):
    host = host_subplot(111)  # row=1 col=1 first pic
    plt.subplots_adjust(right=0.8)  # ajust the right boundary of the plot window
    par1 = host.twinx()

    # set labels
    host.set_xlabel("steps")
    host.set_ylabel("validation loss")
    par1.set_ylabel("validation accuracy")

    # plot curves
    p1, = host.plot(range(len(valid_loss_list)), valid_loss_list, label="loss")
    p2, = par1.plot(range(len(valid_acc_list)), valid_acc_list, label="accuracy")

    host.legend(loc=5)

    # set label color
    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())

    plt.grid()
    plt.draw()
    plt.show()
    plt.savefig('/data1/gwb/few_shot_learning/visualization/new_valaccloss.jpg')


def plot_confusion_matrix(classes, cm, normalized=True, title='Confusion matrix', cmap=plt.cm.Blues):
    if normalized:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("precent")
        np.set_printoptions(formatter={
            'float': '{: 0.2f}'.format})
        print(cm)
    else:
        print('number')
        print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    plt.ylim(len(classes) - 0.5, -0.5)
    fmt = '.2f' if normalized else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    ticks = time.time()
    plt.savefig('confusion_matrix.jpg')
    plt.show()
    plt.clf()


def parse_loss_acc_eval_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    loss_values = []
    acc_values = []
    for line in lines:
        if line.startswith("eval:"):
            parts = line.strip().split(',')
            loss = float(parts[1].split(':')[1].strip())
            acc = float(parts[2].split(':')[1].strip())
            loss_values.append(loss)
            acc_values.append(acc)

    return loss_values, acc_values


def parse_loss_acc_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    epoch_loss_values = []
    epoch_acc_values = []
    current_epoch_loss_values = []
    current_epoch_acc_values = []

    for i, line in enumerate(lines):
        if line.startswith("train: step:"):
            parts = line.strip().split(',')
            loss = float(parts[1].split(':')[1].strip())
            acc = float(parts[2].split(':')[1].strip())
            current_epoch_loss_values.append(loss)
            current_epoch_acc_values.append(acc)
        elif line.startswith("----- Epoch") or i == len(lines) - 1:  # 在遇到新的Epoch或到达文件末尾时处理
            if current_epoch_loss_values and current_epoch_acc_values:
                avg_loss = sum(current_epoch_loss_values) / len(current_epoch_loss_values)
                avg_acc = sum(current_epoch_acc_values) / len(current_epoch_acc_values)
                epoch_loss_values.append(avg_loss)
                epoch_acc_values.append(avg_acc)
                current_epoch_loss_values = []
                current_epoch_acc_values = []
    return epoch_loss_values, epoch_acc_values