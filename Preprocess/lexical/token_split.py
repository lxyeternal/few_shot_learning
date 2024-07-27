# -*- coding: utf-8 -*-
import string

letters = string.ascii_letters + "_"
# 空白字符
blank = " \n\r\t"
# 保留字数组
reserved_words = ["char", "int", "if", "else", "var", "return", "break", "do", 'long', 'short','unsigned','signed','const','volatile','enum','struct','union','sizeof','main','void'
                  "while", 'switch','goto',"for", "double", "float", "short", "scanf", "case", "void",'continue','break','default','typedef','auto','register','extern','static']
# 符号表
signs = {"=": 27, "<=": 28, "<>": 29, "<": 30, ">=": 31, ">": 32, "+": 33, "-": 34, 
         "*": 35, "==": 53, "/": 36, "//": 37, ":": 38, ";": 39, "(": 40, ")": 41,
         "{": 42, "}": 43, "[": 44, "]": 45, "\"": 46, ",": 47, "'": 48, "!=": 49,
         "&": 50, "&&": 51, "||": 52, "|": 54, "%": 55, "?": 56, "::":57,"->":58,'++':59,'--':60,"^":62,"!":63,"<<":64,">>":65,"~":66,
         "+=":67,"-=":68,"*=":69,"/=":70,"%=":71,"<<=":72,">>=":73,"&=":74,"^=":75,"|=":76,"%s":77,"%f":78,"%d":79,"%c":80,"\\n":81,"\\0":82,"\\r":83,"\\t":84}



def output_token(_str):
    # 输出函数
    try: # 尝试是否能通过数字形式输出，如果能s即为常数，否则为字符
        print(f"{int(_str)}\t26")
    except ValueError:
        if _str in reserved_words: # 判断是否为保留字
            print(f"{_str}\t{reserved_words.index(_str) + 1} 保留字")
            word = ""
        elif _str in signs: # 判断是否为符号
            print(f"{_str}\t{signs[_str]}")
        else: # 否则为标识符
            print(f"{_str}\t25 标识符")
            word = ""


#   将代码段分割为单个的token
def split_token(code):
    all_token = ''
    all_token_list = []
    for line in code.split("\n"): # 按行迭代
        word = "" # 类似缓冲区的作用
        flag = False # 标记是否为123这类常数
        _pass = False # 标记是否跳过这一个字符
        for index, letter in enumerate(line):
            if _pass: # 判断是否跳过当前字符
                _pass = False
                continue
            if letter in string.digits: # 判断当前是否为数字
                flag = not bool(word) # 如果word里没有字符，而当前又读到了数字，那么就打上标记
                word += letter # 将字符加入缓冲区
                continue
            elif letter in letters: # 判断当前是否为字母
                if flag: # 如果打过了标记， 而此时读到了字母，标识符是不能以数字开头的，所以分开
                    # output_token(word) # 输出数字
                    all_token = all_token + ' ' + word
                    all_token_list.append(word)
                    word = "" # 清空缓冲区
                    flag = False # 取消标记
                word += letter # 将当前的字母加入缓冲区
                continue
            else: # 此时当前字符既不是数字也不是字母，为符号或空白字符
                if word: # 判断缓冲区内是否有字符，有则输出
                    # output_token(word)
                    all_token = all_token + ' ' + word
                    all_token_list.append(word)
                    word = ""
                if letter in blank: # 如果当前为空白字符（空格、回车）则跳过
                    continue
                if line[index:index + 2] == "//": # 处理掉注释
                    break # 直接break，跳出行迭代
                # 判断当前字符是否为最后一个以及和下一个字符能否组成一组符号
                if index != len(line) - 1 and line[index:index + 2] in signs:
                    # output_token(line[index:index + 2]) # 输出组合的字符
                    all_token = all_token + ' ' + line[index:index + 2]
                    all_token_list.append(line[index:index + 2])
                    _pass = True # 跳过下一个字符
                else: # 输出单个字符
                    # output_token(letter)
                    all_token = all_token + ' ' + letter
                    all_token_list.append(letter)
                word = "" # 清空缓冲区
        all_token_list.append(word)
        all_token = all_token + ' ' + word
    return all_token,all_token_list



#   将单行代码分割为单个的token
def attribute_token(code):
    code = [code]
    all_token = ''
    for line in code: # 按行迭代
        word = "" # 类似缓冲区的作用
        flag = False # 标记是否为123这类常数
        _pass = False # 标记是否跳过这一个字符
        for index, letter in enumerate(line):
            if _pass: # 判断是否跳过当前字符
                _pass = False
                continue
            if letter in string.digits: # 判断当前是否为数字
                flag = not bool(word) # 如果word里没有字符，而当前又读到了数字，那么就打上标记
                word += letter # 将字符加入缓冲区
                continue
            elif letter in letters: # 判断当前是否为字母
                if flag: # 如果打过了标记， 而此时读到了字母，标识符是不能以数字开头的，所以分开
                    # output_token(word) # 输出数字
                    all_token = all_token + ' ' + word
                    word = "" # 清空缓冲区
                    flag = False # 取消标记
                word += letter # 将当前的字母加入缓冲区
                continue
            else: # 此时当前字符既不是数字也不是字母，为符号或空白字符
                if word: # 判断缓冲区内是否有字符，有则输出
                    # output_token(word)
                    all_token = all_token + ' ' + word
                    word = ""
                if letter in blank: # 如果当前为空白字符（空格、回车）则跳过
                    continue
                if letter == " ": # 如果当前为空白字符（空格、回车）则跳过
                    continue
                if line[index:index + 2] == "//": # 处理掉注释
                    break # 直接break，跳出行迭代
                # 判断当前字符是否为最后一个以及和下一个字符能否组成一组符号
                if index != len(line) - 1 and line[index:index + 2] in signs:
                    # output_token(line[index:index + 2]) # 输出组合的字符
                    all_token = all_token + ' ' + line[index:index + 2]
                    _pass = True # 跳过下一个字符
                else: # 输出单个字符
                    # output_token(letter)
                    all_token = all_token + ' ' + letter
                word = "" # 清空缓冲区
        all_token = all_token + ' ' + word
    return all_token