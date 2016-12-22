# -*- coding: utf-8 -*-
"""
  scorer.py define functions used to grade Elab problems. Will be imported automatically.
  
Created on Wed Dec 21 14:54:32 2016

@author: akepooh
"""

def symbolScorer(s):
    if s.count('-') == 9 and s.endswith('P'): #no score if only last P
        return 0
    else:
        return s.count('P') + 0.75 * s.count('S')