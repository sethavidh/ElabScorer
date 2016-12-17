'''
ElabScorer: by Sethavidh Gertphol
Last update 17 Dec 2016
License: CC-BY-SA

current version: 
- take a saved HTML file and extract username/graded score for each question.
- The HTML file is saved from Elab webpage.
- can combine results from several files, but still clumsy
- grade by scorer
- output table of id and scores

TODO: - better way to get filenames and problem names

'''
import os
import sys
from bs4 import BeautifulSoup

def readConf():
    try:
        conf_file = open('scorer.conf', 'r', encoding='utf-8')
    except:
        print('Cannot open scorer.conf file')
        sys.exit(1)
    problem_d = {}
    problem_order = []
    l_num = 0
    std_file = ''
    for line in conf_file.readlines():
        l_num += 1
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        ls = line.split(':')
        if ls[0] =='STD':
            std_file = ls[1]
            continue
        try:
            if ls[0] not in problem_order:
                problem_order.append(ls[0])
            if ls[0] in problem_d:
                problem_d[ls[0]].append(ls[1])
            else:
                problem_d[ls[0]] = [ls[1]]
        except:
            print('scorer.conf is in wrong format at line', l_num)
            sys.exit(2)
    
    if std_file == '' or os.path.isfile(std_file) == False:
        print("No student file")
        sys.exit(4)
    
    print('Student file is', std_file)
    print('Problem List:')
    max_name_len = max([len(x) for x in problem_order])
    for x in problem_order:
        fmt = '%'+'%d' % max_name_len + 's' 
        print(fmt % (x), end=': ')
        indent = max_name_len+2
        i = 0
        for y in problem_d[x]:
            if not os.path.isfile(y):
                print('No problem file: ', y)
                sys.exit(5)
            if i == 0: print(y)
            else: print(' ' * indent + '%s' % y)
            i += 1
    return std_file, problem_d, problem_order
        
def PCounter(s):
    return s.count('P')

def AllP(s):
    for x in s:
        if x != 'P': return 0
    return 1

def readAllStds(file):
    std_file = open(file, "r", encoding='utf-8')
    rec_list = std_file.readlines()
    all_std = []
    for rec in rec_list:
        item_list = rec.split(',')
        all_std.append((item_list[1], item_list[2]))
    return all_std

def extractStdScores(file, scorer=PCounter):
    file = open(file, "r", encoding="utf-8")
    bsObj = BeautifulSoup(file.read())
    std_list = bsObj.ul.findAll('li')
    std_table = []
    
    assignment = bsObj.find('div', id='content').b.nextSibling
    lab, problem = [x.strip() for x in assignment.split('>')]
    s = lab.split()
    lab = s[0] + ' ' + s[1]
    lab_set = s[2] + ' ' + s[3]
                     
    for li in std_list:
        std_name, std_id = li.find('a', class_='std_id').get_text().split('(')
        std_name = std_name.strip()
        std_id = std_id.strip(')')[1:]
        
        submit_ls = li.find('br').nextSibling.split()
        submit_time = submit_ls[2]
        for i in range(3,6):
            submit_time = submit_time + ' ' + submit_ls[i]
    
        submit_ip = submit_ls[7]
    
        res = li.find('span', title='P = Pass, - = Fail, S = Incorrect Spacing, C = Incorrect Case').get_text()
        res = res.strip().strip('[').strip(']')
        
        score = scorer(res)
        record = [std_id, std_name, submit_time, submit_ip,lab, lab_set, problem, res, score]
    
        std_table.append(record)
    
    return std_table

def insertScore(d, score_ls, problem_name):
    for rec in score_ls:
        d[rec[0]][problem_name] = rec[-1]

try:
    os.chdir(sys.argv[1])
except:
    print('Cannot change to directory', sys.argv[1])
    sys.exit(3)
    
std_file, problem_d, problem_order = readConf()
stds_ls = readAllStds(std_file)
all_score = {}
for std in stds_ls:
    all_score[std[0]] = {'name':std[1]}

for problem_name in problem_order:
    for file_name in problem_d[problem_name]:
        score_ls = extractStdScores(file_name)
        insertScore(all_score, score_ls, problem_name)

header = ['ID','Name','Total']
for problem_name in problem_order:
    header.append(problem_name)
    
out = [header]
for std, name in stds_ls:
    rec = [std,name]
    for problem_name in problem_order:
        try:
            rec.append(all_score[std][problem_name])
        except:
            rec.append('')
    total = 0
    for i in range(len(problem_order)):
        try:
            total += rec[2+i]
        except:
            pass
    rec.insert(2, total)
    out.append(rec)
    
out_file = open('all_problems.csv', 'w', encoding='utf-8')
for rec in out:
    for x in rec:
        print(x, end=',',file=out_file)
    print('', file=out_file)












