#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 16:09:43 2017

@author: matthewyeozhiwei
"""

import os
import glob
import numpy as np 
import pandas as pd
import string
sp = string.punctuation
from PIL import Image
import math


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


def getdimensions(fpath):
    '''
    Gets the dimensions of every single picture from each folder.
    
    Parameters:
    ----------
    ffpath: the folder containing folders of each category
    
    Returns:
    -------
    pictureDimensions: the dataframe containing the picture's url, dimensions and original directory
    
    
    '''
    
    url = 'https://cfshopeesg-a.akamaihd.net/file/'
    picturelist = []
    dimensionslist = []
    destinlist = []
    for f in listdir_nohidden(fpath):
        picturelist.append((url + f.split('_')[1].replace('.jpg', '')))
        dimensionslist.append(str(Image.open(f, 'r').size))
        destinlist.append(f)
    pictureID = pd.DataFrame(picturelist)
    dimensionsID = pd.DataFrame(dimensionslist)
    destinID = pd.DataFrame(destinlist)
    pictureDimensions = pd.concat([pictureID, dimensionsID], axis=1, join_axes=[pictureID.index])
    pictureDimensions = pd.concat([pictureDimensions, destinID], axis = 1, join_axes = [pictureID.index])
    pictureDimensions.columns = ['PictureURL', 'Dimensions', 'Destination']
    return pictureDimensions


def change_data(csvpath, fpath):
    
    
    '''
    Cleans the data, by parsing through string results to convert into relevant integers, converting
    result coordinates into actual picture coordinates.
    
    Parameters:
    ----------
    
    path: the path to the .csv file obtained from Amazon Mechanical Turk
    
    fpath: same as ffpath. getDimensions function is called in this function.
    
    Returns:
    -------
    
    finalresults: returns the final cleaned .csv that will be eventually read by cropimages to crop the images
    and save them in a folder.
    
    
    '''
    
    
    temp = pd.read_csv(csvpath)
    
    ## change the submitted into rejected/approved to your need
    temp = temp[temp['AssignmentStatus'] == 'Submitted'].reset_index() ##// This depends on the situation
    
    
    results = temp[['index','Input.Pictures','Answer.annotation_data','WorkerId','HITId']]
    results.columns = ['oindex','PictureURL','Answers','WorkerId', 'HITid']
    
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
    results.columns = ['oindex','PictureURL','WorkerId','HITid', 'Answers']
    rows = []
    _ = results.apply(lambda row: [rows.append([row['oindex'],row['PictureURL'], row['WorkerId'],row['HITid'], nn[0:1], 
                                                nn[1:2], nn[2:3], nn[3:4],nn[4:5]]) 
                         for nn in row.Answers], axis=1)
    
    results2 = pd.DataFrame(rows, columns = ['oindex','PictureURL','WorkerId','HITid', 'x1', 'y1', 'width', 'height', 'Label'])
    results2['Label'] = results2['Label'].apply(lambda x: str(x[0]))
    results2['x1'] = results2['x1'].apply(lambda x: int(x[0]))
    results2['y1'] = results2['y1'].apply(lambda x: int(x[0]))
    results2['width'] = results2['width'].apply(lambda x: int(x[0]))
    results2['height'] = results2['height'].apply(lambda x: int(x[0]))
    results2['x2'] = results2['width'] + results2['x1']
    results2['y2'] = results2['height'] + results2['y1']

    dimensions = getdimensions(fpath)
    dimtemp = dimensions['Dimensions'].tolist()
    dimtemp = list(map(lambda t: ''.join([" " if c in sp else c for c in t]), dimtemp))
    dimtemp = list(map(lambda t: t.split(), dimtemp))
    dimensions = pd.concat([dimensions, pd.DataFrame(np.array(dimtemp))], axis = 1, join_axes = [dimensions.index])
    dimensions = dimensions.drop(['Dimensions'], axis = 1)
    dimensions.columns = ['PictureURL', 'destinID','actual_x', 'actual_y']
    results3 = pd.merge(results2, dimensions, how = 'inner', on = 'PictureURL')
    
    results3['Ratio'] = results3['actual_y'].apply(lambda x: int(x)/500)

    results3['x1'] = results3['x1'] * results3['Ratio'] 
    results3['y1'] = results3['y1'] * results3['Ratio'] 
    results3['x2'] = results3['x2'] * results3['Ratio']
    results3['y2'] = results3['y2'] * results3['Ratio']
    
    results3['x1'] = results3['x1'].apply(lambda x: math.ceil(x))
    results3['y1'] = results3['y1'].apply(lambda x: math.ceil(x)) 
    results3['x2'] = results3['x2'].apply(lambda x: math.ceil(x))
    results3['y2'] = results3['y2'].apply(lambda x: math.ceil(x))

    finalresults = results3.drop(['Ratio', 'actual_x', 'actual_y', 'width', 'height'], axis = 1)

    return finalresults


def removesimilar(results):
    
    '''
    This function rounds up the coordinates of the results. For instances where people crop the same image, almost 
    exactly the same, this function gets the index of all the unique instances.
    
    Parameters:
    ----------
    
    results: the final cleaned .csv results
    
    Returns:
    -------
    
    y: y is a temporary dataframe. its index values are important to subset the original dataframe results
        so that we can get the unique instances of the results!
        
    
    '''
    
    results['x1'] = results['x1'].apply(lambda x: round(x, -1 ))
    results['y1'] = results['y1'].apply(lambda x: round(x, -1 )) 
    results['x2'] = results['x2'].apply(lambda x: round(x, -1 ))
    results['y2'] = results['y2'].apply(lambda x: round(x, -1 ))
    y = results.drop(results[(results['x1'] == results['x2']) & (results['y1'] == results['y2'])].index.values, axis = 0)
    y = y.drop_duplicates(subset = ['x1', 'x2', 'y1', 'y2', 'PictureURL'])
    return y


def cropimages(path,fpath,savepath):
    
    '''
    This function is a combination of clean_data and getdimensions. Using the final .csv results,
    it crops and saves the bounding box cropped by the Amazon Turks.
    
    Parameters:
    ----------
    
    path: path is the path to the .csv file obtained from Amazon Mechanical Turk
    
    fpath: fpath is the path to the folder containing the folder categories that contain all the images from 
            the category
    
    spath: spath is the path in which you want to save the cropped images for reviewing
    
    Returns:
    -------
    
    results: depending on the situation, especially, if you are reviewing over a second/third round, you
            may have lesser pictures. as a result, saving over a new set of results is neccessary. 
    
    
    '''
    
    

    results = change_data(csvpath,fpath)

    duplicate = results.copy()
    dup = removesimilar(duplicate)
    results = results.ix[dup.index.values]
    results= results.reset_index()

    for n in range(0,len(results.index)):
        url = results.ix[n]['PictureURL']
        input_img = Image.open(str(results.ix[n]['destinID']))
        box = (int(results.ix[n]['x1']), int(results.ix[n]['y1']), 
               int(results.ix[n]['x2']), int(results.ix[n]['y2']))
        output_img = input_img.crop(box)
        ## File will be saved as (index)_name.png
        output_img.save(savepath + results.ix[n]['Label'] + '_' + 
                        str(results.ix[n]['oindex']) + '_' +
                        url.split('file/')[1].replace('.jpg','') + '_' +'.jpg')
        print(n)
    
    return results


url = 'https://cfshopeesg-a.akamaihd.net/file/'
fpath = '/Users/matthewyeozhiwei/Desktop/imageprep/categories/babycoat/pictures'
csvpath = '/Users/matthewyeozhiwei/Desktop/imageprep/categories/babycoat/results/amturk_5_raw.csv' 
savepath = '/Users/matthewyeozhiwei/Desktop/imageprep/categories/babycoat/cropped_5_submitted/'   


x = cropimages(csvpath, fpath, savepath)