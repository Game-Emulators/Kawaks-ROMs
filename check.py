#!/usr/bin/env python2
# coding=utf-8
# Yaowen Xu
# 2021年2月1日 15点49分
line_list = []

with open("./download.sh", 'r') as f:
    for line in f:
        if line in line_list:
            print("Duplicate: "+line)
            continue
        if "http" in line:
            line_list.append(line)

print("总行数：" + str(len(line_list)))
