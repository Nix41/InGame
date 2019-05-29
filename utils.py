
import re
from DBstructure import *
import shutil
import os
from distutils.dir_util import copy_tree

def clean_line(A):
    B = ""
    x = 0
    bool = 0
    while 1:
        if x >= len(A):
            break
        if (A[x] == "[") or (A[x] == "(") or (A[x] == "{"):
            bool = 1
        else:
            if (bool == 1) and ((A[x] == "]") or (A[x] == ")") or (A[x] == "}")):
                x += 1
                if (x < len(A) and A[x] != "[") and (A[x] != "(") and (A[x] != "{"):
                    bool = 0
        if bool == 0 and x < len(A):
            B = B + A[x]
        x += 1
    bool = 0
    cnt = 0
    C = ""
    x = len(B) - 1
    if (B[len(B) - 1] == "B") and (B[len(B) - 2] == "M" or B[len(B) - 2] == "G"):
        while 1:
            if x == -1:
                break
            if cnt < 2:
                if B[x] == " ":
                    cnt += 1
            else:
                C = B[x] + C
            x -= 1
    else:
        C = B
     #(C)
    return C

def stupidshit(w, p):
    new = ''
    for i in range(p):
        new += w[i]
    for i in range(p+1,len(w)):
        new += w[i]
    return new

def clean(path):
    movies = []
    line = None
    with open(path , "r") as std:
        while line is None or line != '':
            try:
                line = std.readline()
                movies.append(line)
            except: Exception
    new = []
    for m in movies:
        s = re.sub( ' +', ' ', m ).strip()
        if(len(s) > 1):
            t = clean_line(s)
            new.append(t + '\n')
    with open(path, 'w') as std:
        std.writelines(new)

def make_lists(dirt, found, not_dir, not_found):
    with open(not_dir , 'a+') as std:
        std.write(not_found)
    left = ''
    line = None
    with open(dirt , 'r') as std:
        while line is None or line != '':
            line = std.readline()
            already = False
            for f in found:
                if f in line:
                    already = True
                    break
            if line == not_found:
                already = True
            if not (already):
                left += line
    with open(dirt , 'w+') as std:
        std.write(left)

def copy_to_client():
    print('Copiando los archivos')
    try:
        os.remove('SetupFiles/InGameClientEXE/server/yasmany')
    except: Exception
    try:
        shutil.rmtree('SetupFiles/InGameClientEXE/server/web/img/Work')
    except: Exception
    shutil.copyfile('yasmany', 'SetupFiles/InGameClientEXE/server/yasmany')
    shutil.copytree('web/img/Work', 'SetupFiles/InGameClientEXE/server/web/img/Work')


