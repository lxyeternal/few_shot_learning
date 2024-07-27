# -*- coding: UTF-8 -*-
"""
@Project ：few_shot_learning 
@File    ：cwegroup.py
@Author  ：honywen
@Date    ：2022/12/29 20:24 
@Software: PyCharm
"""

import os
import sys
sys.path.append("/data1/gwb/few_shot_learning/")


def write_data(filename, data):
    f = open(filename, 'a+')
    f.write(data)

def read_uniques_data():
    cwe_list = ['CWE780', 'CWE122', 'CWE762', 'CWE369', 'CWE457', 'CWE773', 'CWE675', 'CWE126', 'CWE78', 'CWE121', 'CWE416', 'CWE617', 'CWE459', 'CWE469', 'CWE36', 'CWE367', 'CWE259', 'CWE506', 'CWE476', 'CWE535', 'CWE327', 'CWE591', 'CWE253', 'CWE400', 'CWE761', 'CWE605', 'CWE789', 'CWE666', 'CWE123', 'CWE464', 'CWE195', 'CWE665', 'CWE685', 'CWE15', 'CWE223', 'CWE415', 'CWE534', 'CWE328', 'CWE680', 'CWE690', 'CWE190', 'CWE114', 'CWE319', 'CWE222', 'CWE510', 'CWE124', 'CWE475', 'CWE134', 'CWE681', 'CWE256', 'CWE426', 'CWE127', 'CWE325', 'CWE197', 'CWE775', 'CWE321', 'CWE226', 'CWE404', 'CWE23', 'CWE364', 'CWE758', 'CWE196', 'CWE90', 'CWE252', 'CWE401', 'CWE194', 'CWE427', 'CWE244', 'CWE590', 'CWE191', 'CWE688', 'CWE606', 'CWE467']
    cwe_num = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    f = open("../data/mvd_uniques.txt", 'r')
    contents = f.read()
    contents_split = contents.split("------------------------------")
    for content_split in contents_split:
        c_code = ''
        split_lines = content_split.strip().split("\n")
        for line_index in range(len(split_lines)):
            try:
                if (line_index != 0) and (line_index != 1):
                    new_line = ''
                    code_line = split_lines[line_index].split(" ")
                    for i in range(len(code_line) - 1):
                        new_line = new_line + ' ' + code_line[i]
                    new_line = new_line.strip()
                    c_code = c_code + ' ' + new_line
                    c_code = c_code.strip()
                code_index = split_lines[0]
                code_cwe_string = split_lines[1].split(" ")[1]
                if code_cwe_string.startswith("CWE"):
                    code_cwe = code_cwe_string.split("_")[0]
                    code_label = code_index.split(" ")[1]
                    code_cwe_index = cwe_list.index(code_cwe)
                    filename = '../data/cwedata/' + code_cwe + '.txt'
                    if code_label == '0':
                        cwe_num[code_cwe_index][0] = cwe_num[code_cwe_index][0] + 1
                        code_label = '-1'
                    else:
                        cwe_num[code_cwe_index][1] = cwe_num[code_cwe_index][1] + 1
                        code_label = '1'
                else:
                    continue
            except:
                continue
        write_data(filename, c_code + '\t' + code_label + '\n')

    for index in range(len(cwe_num)):
        if cwe_num[index][0] == 0 or cwe_num[index][1] == 0:
            cwe_filename = '../data/cwedata/' + cwe_list[index] + '.txt'
            os.remove(cwe_filename)


def read_normname_data():
    cwe_list = ['CWE780', 'CWE122', 'CWE762', 'CWE369', 'CWE457', 'CWE773', 'CWE675', 'CWE126', 'CWE78', 'CWE121', 'CWE416', 'CWE617', 'CWE459', 'CWE469', 'CWE36', 'CWE367', 'CWE259', 'CWE506', 'CWE476', 'CWE535', 'CWE327', 'CWE591', 'CWE253', 'CWE400', 'CWE761', 'CWE605', 'CWE789', 'CWE666', 'CWE123', 'CWE464', 'CWE195', 'CWE665', 'CWE685', 'CWE15', 'CWE223', 'CWE415', 'CWE534', 'CWE328', 'CWE680', 'CWE690', 'CWE190', 'CWE114', 'CWE319', 'CWE222', 'CWE510', 'CWE124', 'CWE475', 'CWE134', 'CWE681', 'CWE256', 'CWE426', 'CWE127', 'CWE325', 'CWE197', 'CWE775', 'CWE321', 'CWE226', 'CWE404', 'CWE23', 'CWE364', 'CWE758', 'CWE196', 'CWE90', 'CWE252', 'CWE401', 'CWE194', 'CWE427', 'CWE244', 'CWE590', 'CWE191', 'CWE688', 'CWE606', 'CWE467']
    cwe_num = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    print(len(cwe_list))
    f = open("../data/mvd_uniques_normname.txt", 'r')
    contents = f.read()
    contents_split = contents.split("------------------------------")
    for content_split in contents_split:
        c_code = ''
        split_lines = content_split.strip().split("\n")
        for line_index in range(len(split_lines)):
            try:
                if (line_index != 0) and (line_index != 1):
                    code_line = split_lines[line_index].strip()
                    c_code = c_code + ' ' + code_line
                    c_code = c_code.strip()
                code_index = split_lines[0]
                code_cwe_string = split_lines[1]
                if code_cwe_string.startswith("CWE"):
                    code_cwe = code_cwe_string.split("_")[0]
                    code_label = code_index.split(" ")[1]
                    code_cwe_index = cwe_list.index(code_cwe)
                    filename = '../data/cwedata/' + code_cwe + '.txt'
                else:
                    continue
            except:
                continue
        if code_label == '0':
            cwe_num[code_cwe_index][0] = cwe_num[code_cwe_index][0] + 1
            code_label = '-1'
        else:
            cwe_num[code_cwe_index][1] = cwe_num[code_cwe_index][1] + 1
            code_label = '1'
        write_data(filename, c_code.replace('\t','') + '\t' + code_label + '\n')

    for index in range(len(cwe_num)):
        if cwe_num[index][0] < 10 or cwe_num[index][1] < 10:
            cwe_filename = '../data/cwedata/' + cwe_list[index] + '.txt'
            os.remove(cwe_filename)
    print(cwe_num)


# read_normname_data()

def CountData():
    cwefiles = os.listdir("/data1/gwb/few_shot_learning/data/cwedata/")
    data_nums = 0
    for cwefile in cwefiles:
        print(cwefile)
        f = open(os.path.join("/data1/gwb/few_shot_learning/data/cwedata/", cwefile), 'r')
        contents = f.read().strip()
        data_nums = data_nums + len(contents.split("\n"))
    print(data_nums)

# CountData()
