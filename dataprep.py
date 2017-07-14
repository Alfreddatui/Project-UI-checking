#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 11:18:26 2017

@author: matthewyeozhiwei
"""

##

import os
import glob
import numpy as np 
import pandas as pd
import string
sp = string.punctuation


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


def uidataprep(csvpath, fpath):
        
    
    temp = pd.read_csv(csvpath)
    
    ## change the 'Submitted' into ''Rejected'/'Approved' to your need
    temp = temp[temp['AssignmentStatus'] == 'Submitted'].reset_index() 
    
    
    results = temp[['index','Input.Pictures','Answer.annotation_data','WorkerId','HITId','AssignmentId','Approve', 'Reject']]
    results.columns = ['oindex','PictureURL','Answers','WorkerId', 'HITid', 'AssignmentId', 'Approve', 'Reject']
    
    temp = results['Answers'].tolist()
    temp = list(map(lambda t: t[2:-2], temp))
    temp = list(map(lambda t: ''.join([" " if c in sp else c for c in t]), temp))
    temp = list(map(lambda t: t.split(), temp))
    temp2 = []
    
    for n in temp:
        temp1 = []
        for index in range(1,len(n),2):
            temp1.append(n[index])
        temp2.append(temp1)
    t2 = []
    for row in temp2:
        t = []
        for n in range(0, len(row), 5):
            t.append(row[n:n+5]) 
        t2.append(t)
        
    bboxresults = np.array(t2)
    bboxresults = pd.DataFrame(bboxresults)
    results = pd.concat([results, bboxresults], axis = 1, join_axes = [results.index])
    results = results.drop('Answers', axis = 1)
    
    results.columns = ['oindex','PictureURL','WorkerId','HITid', 'AssignmentId', 'Approve',  'Reject', 'Answers']
    rows = []
    _ = results.apply(lambda row: [rows.append([row['oindex'],row['PictureURL'], row['WorkerId'],row['HITid'],row['AssignmentId'],
                                                 row['Approve'], row['Reject'],nn[0:1],nn[1:2], nn[2:3], nn[3:4],nn[4:5]]) 
                         for nn in row.Answers], axis=1)
    
    results2 = pd.DataFrame(rows, columns = ['oindex','PictureURL','WorkerId','HITid', 'AssignmentId', 'Approve', 'Reject','x1', 'y1', 'width', 'height', 'Label'])
    results2['Label'] = results2['Label'].apply(lambda x: str(x[0]))
    results2['x1'] = results2['x1'].apply(lambda x: int(x[0]))
    results2['y1'] = results2['y1'].apply(lambda x: int(x[0]))
    results2['width'] = results2['width'].apply(lambda x: int(x[0]))
    results2['height'] = results2['height'].apply(lambda x: int(x[0]))
    
    picturelist = []
    destinlist = []
    
    for f in listdir_nohidden(fpath):
        picturelist.append((url + f.split('_')[1].replace('.jpg', '')))
        destinlist.append(f)
    pictureID = pd.DataFrame(picturelist)
    destinID = pd.DataFrame(destinlist)
    pictureDestination = pd.concat([pictureID, destinID], axis = 1, join_axes = [pictureID.index])
    pictureDestination.columns = ['PictureURL','Destination']

    results3 = pd.merge(results2, pictureDestination, how = 'inner', on = 'PictureURL')

    return results3


url = 'https://cfshopeesg-a.akamaihd.net/file/'
fpath = r'C:\Users\alfred.datui\Desktop\imageprep\categories\babycoat\pictures'
csvpath = r'C:\Users\alfred.datui\Desktop\imageprep\categories\babycoat\results\amturk_5_raw.csv'

results = uidataprep(csvpath, fpath)
results.to_csv(r'C:\Users\alfred.datui\Desktop\imageprep\categories\babycoat\results\amturk_5_submitted.csv')