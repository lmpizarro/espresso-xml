#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import division

import os
import sys
import pandas as pd

# fields:
#   nfi ekinc temph tempp  etot enthal econs econt vnhh xnhh0 vnhp xnhp0
# 
def parse_cp_output(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
   
    start = end = 0
    for i, l in enumerate(lines):

        if l.startswith('nfi',2):
            start = i

        if l.startswith('* Physical', 1):
            end = i


    if start > 0 and end > 0 and end > start:
        run_lines = lines[start:end]

    for i,l in enumerate(run_lines):
        if len(l) == 1:
            del run_lines[i]

    for i,l in enumerate(run_lines):
        if l.startswith('writing', 3):
            del run_lines[i]

    for i,l in enumerate(run_lines):
        if l.startswith('restart', 3):
            del run_lines[i]


    columns = []
    for r in run_lines[1:]:
        l = r.split()
        for i,e in enumerate(l):
            l[i] = float(e)
        columns.append(l)

    s = pd.DataFrame(columns, columns=run_lines[0].split())

    return s 


if __name__ == '__main__':
    s = parse_cp_output('si.cp.out')
    s.describe()
    s.to_excel('si.cp.xls')
