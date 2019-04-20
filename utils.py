
import re
from DBstructure import *

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
    with open(path , "r") as std:
        movies = std.readlines()
    new = []

    for m in movies:
        s = re.sub( ' +', ' ', m ).strip()
        if(len(s) > 1):
            t = clean_line(s)
            new.append(t + '\n')
    with open(path, 'w') as std:
        std.writelines(new)

def make_lists(dirt, found, not_dir, not_found):
    with open(not_dir , 'w+') as std:
        std.write(not_found)
    left = ''
    line = None
    with open(dirt , 'w+') as std:
        while line is None or line != '':
            line = std.readline()
            if not line in found:
                left += line
    with open(dirt , 'w+') as std:
        std.write(left)

def lazy():
    for g in sess.query(Game).all():
        yield g.name

a = lazy()

def run10():
    global a
    print('Funcion 1     ')
    for i in range(10):
        s = a.__next__()
        print(s)
    print('##############')
    print()

def run20():
    global a
    print('Funcion 2     ')
    for i in range(20):
        s = a.__next__()
        print(s)
    print('##############')
    print()

run10()
run20()