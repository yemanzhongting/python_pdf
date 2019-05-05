# -*- coding: UTF-8 -*-
__author__ = 'zy'
__time__ = '2019/5/4 15:11'
import os
from pdfminer.image import ImageWriter
import argparse
import logging
import six
import sys
import pdfminer.settings
pdfminer.settings.STRICT = False
import pdfminer.high_level
import pdfminer.layout
from pdfminer.image import ImageWriter

def extract_text(files=[], outfile='-',
            _py2_no_more_posargs=None,  # Bloody Python2 needs a shim
            no_laparams=False, all_texts=None, detect_vertical=None, # LAParams
            word_margin=None, char_margin=None, line_margin=None, boxes_flow=None, # LAParams
            output_type='text', codec='utf-8', strip_control=False,
            maxpages=0, page_numbers=None, password="", scale=1.0, rotation=0,
            layoutmode='normal', output_dir=None, debug=False,
            disable_caching=False, **other):
    if _py2_no_more_posargs is not None:
        raise ValueError("Too many positional arguments passed.")
    if not files:
        raise ValueError("Must provide files to work upon!")

    # If any LAParams group arguments were passed, create an LAParams object and
    # populate with given args. Otherwise, set it to None.
    if not no_laparams:
        laparams = pdfminer.layout.LAParams()
        for param in ("all_texts", "detect_vertical", "word_margin", "char_margin", "line_margin", "boxes_flow"):
            paramv = locals().get(param, None)
            if paramv is not None:
                setattr(laparams, param, paramv)
    else:
        laparams = None

    imagewriter = None
    if output_dir:
        imagewriter = ImageWriter(output_dir)

    if output_type == "text" and outfile != "-":
        for override, alttype in (  (".htm", "html"),
                                    (".html", "html"),
                                    (".xml", "xml"),
                                    (".tag", "tag") ):
            if outfile.endswith(override):
                output_type = alttype

    if outfile == "-":
        outfp = sys.stdout
        if outfp.encoding is not None:
            codec = 'utf-8'
    else:
        outfp = open(outfile, "wb")


    for fname in files:
        with open(fname, "rb") as fp:
            pdfminer.high_level.extract_text_to_fp(fp, **locals())
    return outfp

def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.PDF':
                L.append(os.path.join(root, file))
    return L
    # 其中os.path.splitext()函数将路径拆分为文件名+扩展名

def file_txt(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
                L.append(os.path.join(root, file))
    return L
    # 其中os.path.splitext()函数将路径拆分为文件名+扩展名

import string

def str_count(str):
    '''找出字符串中的中英文、空格、数字、标点符号个数'''
    count_en = count_dg = count_sp = count_zh = count_pu = 0

    for s in str:
        # 英文
        if s in string.ascii_letters:
            count_en += 1
        # 数字
        elif s.isdigit():
            count_dg += 1
        # 空格
        elif s.isspace():
            count_sp += 1
        # 中文
        elif s.isalpha():
            count_zh += 1
        # 特殊字符
        else:
            count_pu += 1

    print('英文字符：', count_en)
    print('数字：', count_dg)
    print('空格：', count_sp)
    print('中文：', count_zh)
    print('特殊字符：', count_pu)

    return count_zh

def trans_text(file_dir):
    tmp=[]
    tmp.append(file_dir)
    extract_text(tmp, outfile=file_dir+'.txt')
    print(file_dir+'转化txt完成！')

if __name__=='__main__':
    file_dir=input('请输入pdf文件路径：')
    file_list=file_name(file_dir)

    #key_word=input('请输入检索关键词：')

    key_word = []  # 定义一个空列表
    str_ = input("请输入检索关键词，用空格隔开,否则会报错:")
    lst1 = str_.split(" ")  # lst1用来存储输入的字符串，用空格分割

    for k in lst1:
        if k!='':
            key_word.append(k)

    code=input('是否已经转化pdf为txt,已经转化输入1，未转化输入0，转化后txt文件存入pdf文件路径:')
    if int(code)==0:
        for i in file_list:
            print('##########################正在统计文件 '+i)
            print('正在转化，时间较长，请稍后')
            trans_text(i)
    if int(code)==1:
        print('即将开始处理：')

    file_txt_list=file_txt(file_dir)

    tmp_result =''

    for i in file_txt_list:
        with open (i,'r',encoding='utf-8') as f:
            content= f.read()
            result={}
            RD=0
            tmp_sum=0
            all_word = str_count(content)
            for j in key_word:
                if j in content:
                    tmp_result_=content.count(j)
                    print(i  +' 关键字 '+j+' RD是： ' + str(tmp_result_ / all_word * 100))
                    RD = RD + (tmp_result_ / all_word * 100)
                    tmp_sum=tmp_sum+tmp_result_

                    #tmp_result+=i +'\t'+'关键字'+key_word+'\t'+'次数'+'\t'+str(result[key_word])+'\t'+ 'RD是：'+'\t' + str(RD)+'\r\n'
                else:
                    print('未检索到关键词'+j+'进行下一个')
                    # tmp_result+=i +'未检索到关键词，进行下一个'+'\r\n'

            tmp_result = tmp_result+i + '\t' + str(RD) +'\t'+str(tmp_sum) +'\r\n'

        f.close()

    with open('result.txt','w+',encoding='utf-8') as f:
        f.write(tmp_result)
        f.close()







