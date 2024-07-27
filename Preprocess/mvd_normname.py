# -*- coding: utf-8 -*-
# @Time    : 2022/1/12 15:36
# @Author  : blue
# @FileName: mvd_normname.py
# @Software: PyCharm

from lexical.token_split import split_token
from variablename.mapping import mapping


#  对去重之后的mvd文件进行变量命名的替换
def mvd_normname():
    slice_file_path = '../data/mvd_uniques.txt'
    normname_slice_file_path = '../data/mvd_uniques_normname.txt'
    f = open(slice_file_path, 'r')
    allcodes = f.read()
    slice_code_list = list()
    normname_slice_code_list = list()
    slice_firstline_list = list()
    slice_secondline_list = list()
    allcodes_split = allcodes.split('------------------------------')
    allcodes_split = allcodes_split[:-1]
    for snippet in allcodes_split:
        tmp = ''
        code_lines = snippet.strip().split('\n')
        for line_index in range(len(code_lines)):
            if line_index == 0:
                slice_firstline_list.append(code_lines[line_index])
            elif line_index == 1:
                second_line_split = code_lines[line_index].split(" ")[1:-1]
                new_second_line = ""
                for code_token in second_line_split:
                    new_second_line = new_second_line + code_token + " "
                slice_secondline_list.append(new_second_line.strip())
            else:
                line_code = code_lines[line_index]
                line_code_split = line_code.split(" ")[:-1]
                new_line_code = ""
                for code_token in line_code_split:
                    new_line_code = new_line_code + code_token + " "
                tmp = tmp + new_line_code.strip() + '\n'
        tmp = tmp.strip()
        slice_code_list.append(tmp)


    for slice_code in slice_code_list:
        normname_snippet_code = ""
        snippet_code_token = list()
        slice_code_lines = slice_code.split("\n")
        for line in slice_code_lines:
            line = line.strip()
            all_token,all_token_list = split_token(line)
            snippet_code_token.append(all_token_list)
        list_code, list_func = mapping(snippet_code_token)
        for mapping_code_line in list_code:
            mapping_code_line = mapping_code_line.strip(" ") + '\n'
            normname_snippet_code = normname_snippet_code + mapping_code_line
        normname_snippet_code = normname_snippet_code.strip()
        normname_slice_code_list.append(normname_snippet_code)


    #  将重命名之后的代码片段写入文件
    fw = open(normname_slice_file_path, 'w')
    for index in range(len(slice_firstline_list)):
        fw.write(slice_firstline_list[index] + '\n')
        fw.write(slice_secondline_list[index] + '\n')
        fw.write(normname_slice_code_list[index] + '\n')
        fw.write('------------------------------\n')


mvd_normname()