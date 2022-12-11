import os
import sys
import csv
import pandas as pd
import datetime

_thisDir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(_thisDir)

# file name will be appended after "<subjectID>_". It must have ".csv" at the end
# info should be a dictionary of information you would like added to 
def results_to_csv(expID, subjectID, filePath, fileName, expResults, info):
    df = pd.DataFrame(expResults)
    for item in info:
        df[item] = info[item]
    currentTime = datetime.datetime.now()
    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    df['exp'] = expID
    df['subjectId'] = subjectID
    df['date'] = currentTime
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    df.to_csv(filePath + subjectID + '_' + fileName, index=False, encoding='utf-8')


def append_results_to_csv(expID, subjectID, filePath, fileName, expResults, info):
    df = pd.DataFrame(expResults)
    for item in info:
        df[item] = info[item]
    currentTime = datetime.datetime.now()
    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    df['exp'] = expID
    df['subjectId'] = subjectID
    df['date'] = currentTime
    path = filePath + subjectID + '_' + fileName
    if os.path.exists(filePath):
        origDf = pd.read_csv(path)
        origDf = pd.concat([origDf, df])
        origDf.reset_index(inplace=True)
        origDf['trialN'] = origDf.index.values
        origDf.reset_index(drop=True)
        origDf.to_csv(path, index=False, encoding='utf-8')


def append_results_to_csv_ignore_index(expID, subjectID, filePath, fileName, expResults, info):
    df = pd.DataFrame(expResults)
    for item in info:
        df[item] = info[item]
    currentTime = datetime.datetime.now()
    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    df['exp'] = expID
    df['subjectId'] = subjectID
    df['date'] = currentTime
    path = filePath + subjectID + '_' + fileName
    if os.path.exists(filePath):
        origDf = pd.read_csv(path)
        # origDf = pd.concat([origDf,df], sort=False)
        origDf = pd.concat([origDf, df])
        origDf.reset_index(inplace=True, drop=True)
        origDf['trialN'] = origDf.index.values
        origDf.to_csv(path, index=False, encoding='utf-8')
