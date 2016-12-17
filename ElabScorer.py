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
from bs4 import BeautifulSoup

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
        
stds_ls = readAllStds("ALL-AB-Table 1.csv")
all_score = {}
for std in stds_ls:
    all_score[std[0]] = {'name':std[1]}

single_digit_s1 = extractStdScores("591_set1_midterm_singledigit.html")
single_digit_s2 = extractStdScores("591_set2_midterm_singledigit.html")
coin_s1 = extractStdScores("591_set1_midterm_coin.html")
coin_s2 = extractStdScores("591_set2_midterm_coin.html")
skyline_s1 = extractStdScores("591_set1_midterm_skyline.html")
skyline_s2 = extractStdScores("591_set2_midterm_skyline.html")
threefive_s1 = extractStdScores("591_set1_midterm_threefive.html")
threefive_s2 = extractStdScores("591_set2_midterm_threefive.html")
craps_s1 = extractStdScores("591_set1_midterm_craps.html")
craps_s2 = extractStdScores("591_set2_midterm_craps.html")

insertScore(all_score, single_digit_s1, 'Single_Digit')
insertScore(all_score, single_digit_s2, 'Single_Digit')
insertScore(all_score, coin_s1, 'Coin')
insertScore(all_score, coin_s2, 'Coin')
insertScore(all_score, skyline_s1, 'Skyline')
insertScore(all_score, skyline_s2, 'Skyline')
insertScore(all_score, threefive_s1, 'Three and Five')
insertScore(all_score, threefive_s2, 'Three and Five')
insertScore(all_score, craps_s1, 'Craps')
insertScore(all_score, craps_s2, 'Craps')

out = [['ID', 'Name','Total', 'Single_Digit','Coin','Skyline','Three and Five', 'Craps']]
for std, name in stds_ls:
    rec = [std, name]
    try:
        rec.append(all_score[std]['Single_Digit'])
    except:
        rec.append('')
    try:
        rec.append(all_score[std]['Coin'])
    except:
        rec.append('')    
    try:
        rec.append(all_score[std]['Skyline'])
    except:
        rec.append('')
    try:
        rec.append(all_score[std]['Three and Five'])
    except:
        rec.append('')
    try:
        rec.append(all_score[std]['Craps'])
    except:
        rec.append('')
    total = 0
    for i in range(1,6):
        try:
            total += rec[i]
        except:
            pass
    rec.insert(2, total)
    out.append(rec)
    
out_file = open('all_problems.csv', 'w', encoding='utf-8')
for rec in out:
    for x in rec:
        print(x, end=',',file=out_file)
    print('', file=out_file)












