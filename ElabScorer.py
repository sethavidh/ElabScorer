'''
ElabScorer: by Sethavidh Gertphol
Last update 14 Dec 2016
License: CC-BY-SA

1st version: take a saved HTML file and extract username/graded score for 
 each question. The HTML file is saved from Elab webpage.
 
'''
from bs4 import BeautifulSoup

file = open("591_set1_midterm_singledigit.html", "r", encoding="utf-8")
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
    std_id = std_id.strip(')')
    
    submit_ls = li.find('br').nextSibling.split()
    submit_time = submit_ls[2]
    for i in range(3,6):
        submit_time = submit_time + ' ' + submit_ls[i]

    submit_ip = submit_ls[7]

    res = li.find('span', title='P = Pass, - = Fail, S = Incorrect Spacing, C = Incorrect Case').get_text()
    res = res.strip().strip('[').strip(']')
    
    score = res.count('P')
    record = [std_id, std_name, submit_time, submit_ip,lab, lab_set, problem, res, score]

    std_table.append(record)

for x in std_table:
    print(x)