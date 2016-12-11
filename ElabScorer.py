'''
ElabScorer: by Sethavidh Gertphol
Last update 11 Dec 2016
License: CC-BY-SA

1st version: take a saved HTML file and extract username/graded score for 
 each question. The HTML file is saved from Elab webpage.
 
'''
from bs4 import BeautifulSoup

file = open("591_set1_midterm_craps.html", "r", encoding="latin-1")
bsObj = BeautifulSoup(file.read())

stds = bsObj.findAll('a', {"class", "std_id"})
ps = bsObj.findAll('span', title="P = Pass, - = Fail, S = Incorrect Spacing, C = Incorrect Case")

