# -*- coding: UTF-8 -*-
"""
@Project ：few_shot_learning 
@File    ：siamese_group.py
@Author  ：honywen
@Date    ：2022/12/30 13:51 
@Software: PyCharm
"""


import os
import math
import shutil
import random


def write_data(filename, data):
    f = open(filename, 'a+')
    f.write(data)


def read_normname_data():
    cwe_list = ['NORMAL', 'CWE780', 'CWE122', 'CWE762', 'CWE369', 'CWE457', 'CWE773', 'CWE675', 'CWE126', 'CWE78', 'CWE121', 'CWE416', 'CWE617', 'CWE459', 'CWE469', 'CWE36', 'CWE367', 'CWE259', 'CWE506', 'CWE476', 'CWE535', 'CWE327', 'CWE591', 'CWE253', 'CWE400', 'CWE761', 'CWE605', 'CWE789', 'CWE666', 'CWE123', 'CWE464', 'CWE195', 'CWE665', 'CWE685', 'CWE15', 'CWE223', 'CWE415', 'CWE534', 'CWE328', 'CWE680', 'CWE690', 'CWE190', 'CWE114', 'CWE319', 'CWE222', 'CWE510', 'CWE124', 'CWE475', 'CWE134', 'CWE681', 'CWE256', 'CWE426', 'CWE127', 'CWE325', 'CWE197', 'CWE775', 'CWE321', 'CWE226', 'CWE404', 'CWE23', 'CWE364', 'CWE758', 'CWE196', 'CWE90', 'CWE252', 'CWE401', 'CWE194', 'CWE427', 'CWE244', 'CWE590', 'CWE191', 'CWE688', 'CWE606', 'CWE467']
    cwe_num = [[0,0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    f = open("../data/mvd_uniques_normname.txt", 'r')
    contents = f.read()
    contents_split = contents.split("------------------------------")
    count = 0
    for content_split in contents_split:
        c_code = ''
        split_lines = content_split.strip().split("\n")
        for line_index in range(len(split_lines)):
            try:
                count = count + 1
                if (line_index != 0) and (line_index != 1):
                    code_line = split_lines[line_index]
                    c_code = c_code + ' ' + code_line.strip()
                code_index = split_lines[0]
                code_cwe_string = split_lines[1]
                if code_cwe_string.startswith("CWE"):
                    code_cwe = code_cwe_string.split("_")[0]
                    code_label = code_index.split(" ")[1]
                    if code_label == '0':
                        code_cwe = 'NORMAL'
                        code_cwe_index = cwe_list.index(code_cwe)
                        filename = '../data/siamese_data/alldata/' + code_cwe + '/' + str(count) + '.txt'
                        cwe_dir = '../data/siamese_data/alldata/' + code_cwe
                    else:
                        code_cwe_index = cwe_list.index(code_cwe)
                        filename = '../data/siamese_data/alldata/' + code_cwe + '/' + str(count) + '.txt'
                        cwe_dir = '../data/siamese_data/alldata/' + code_cwe
                    if os.path.exists(cwe_dir):
                        pass
                    else:
                        os.makedirs(cwe_dir)
                else:
                    continue
            except:
                continue
        if code_label == '0':
            cwe_num[0][0] = cwe_num[0][0] + 1
        else:
            cwe_num[code_cwe_index][1] = cwe_num[code_cwe_index][1] + 1

        write_data(filename, c_code + '\n')


    # for index in range(len(cwe_num)):
    #     if cwe_num[index][0] == 0 or cwe_num[index][1] == 0:
    #         cwe_filename = '../data/cwedata/' + cwe_list[index] + '.txt'
    #         os.remove(cwe_filename)
    print(cwe_num)

# read_normname_data()


def split_data():
    base_dir = "../data/siamese_data/"
    alldata_base_dir = base_dir + 'alldata/'
    filedirs = os.listdir(alldata_base_dir)
    for filedir in filedirs:
        txtfiles = os.listdir(os.path.join(alldata_base_dir, filedir))
        if len(txtfiles) < 5:
            continue
        train_num = math.ceil(len(txtfiles) * 0.8)
        train_files = random.sample(txtfiles, train_num)
        # eval_files = list(set(txtfiles).difference(set(train_files)))
        for txtfile in txtfiles:
            old_file_path = os.path.join(alldata_base_dir, filedir, txtfile)
            train_dir = os.path.join(base_dir, 'train', filedir)
            eval_dir = os.path.join(base_dir, 'eval', filedir)
            if txtfile in train_files:
                # 移动到train文件夹
                new_file_path = os.path.join(base_dir, 'train', filedir, txtfile)
                if not os.path.exists(train_dir):
                    os.makedirs(train_dir)
                shutil.copyfile(old_file_path, new_file_path)
            else:
                # 移动到eval文件夹
                new_file_path = os.path.join(base_dir, 'eval', filedir, txtfile)
                if not os.path.exists(eval_dir):
                    os.makedirs(eval_dir)
                shutil.copyfile(old_file_path, new_file_path)


split_data()