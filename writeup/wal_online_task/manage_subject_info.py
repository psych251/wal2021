import pandas as pd
import csv
import os
import sys
import datetime

# Methods to manage EXPID_subject_assignment_info.csv and EXPID_subject_worker_ids.csv inside experiment folder

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

def store_subject_info(expId, PROLIFIC_PID, tasksToComplete, STUDY_ID, SESSION_ID):
    if not os.path.exists(_thisDir + '/data/' + expId):
        os.makedirs(_thisDir + '/data/' + expId)
    # store subjectId and other relevant subject info, except PROLIFIC_PID
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_assignment_info.csv'
    if not os.path.exists(csvLocation):
        newSubjectId = expId + "_%04d" % (1,)
        currentTime = datetime.datetime.now()
        currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        newSubject = {'subjectId':newSubjectId, 'STUDY_ID':STUDY_ID, 'SESSION_ID':SESSION_ID, 'timestamp':currentTime}
        newSubject.update(tasksToComplete)
        new_df = pd.DataFrame(data=newSubject, index=[0])
    else:
        df = pd.read_csv(csvLocation)
        df2 = pd.read_csv(_thisDir + '/data/' + expId +'/' + expId + '_subject_worker_ids.csv')
        nSubjects = len(df2.index)
        newSubjectId = expId + "_%04d" % (nSubjects+1,)
        currentTime = datetime.datetime.now()
        currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        newSubject = {'subjectId':newSubjectId, 'STUDY_ID':STUDY_ID, 'SESSION_ID':SESSION_ID, 'timestamp':currentTime}
        newSubject.update(tasksToComplete)
        df2 = pd.DataFrame(data=newSubject, index=[0])
        new_df = pd.concat([df,df2], axis=0)
    new_df.to_csv(csvLocation,index=False)

    # store subjectId and PROLIFIC_PID
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_worker_ids.csv'
    newSubject = {'expId':expId, 'PROLIFIC_PID':PROLIFIC_PID, 'timestamp':currentTime}
    if not os.path.exists(csvLocation):
        new_df = pd.DataFrame(data=newSubject, index=[0])
    else:
        df = pd.read_csv(csvLocation)
        df2 = pd.DataFrame(data=newSubject, index=[0])
        new_df = pd.concat([df,df2], axis=0)
    new_df.to_csv(csvLocation,index=False)


def get_timestamp(expId, PROLIFIC_PID):
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_worker_ids.csv'
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)
        timestamps = df.loc[df['PROLIFIC_PID'] == PROLIFIC_PID]['timestamp'].values
        if len(timestamps) > 0:
            return timestamps[0]
        else:
            return False

# should assume subject did not participate before
def get_subjectId(expId, PROLIFIC_PID):
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_assignment_info.csv'
    csvWorkerIds = _thisDir + '/data/' + expId +'/' + expId + '_subject_worker_ids.csv'
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)
        timestamp = get_timestamp(expId, PROLIFIC_PID)
        if timestamp != False:
            subjectIds = df.loc[df['timestamp'] == timestamp]['subjectId'].values
            if len(subjectIds) > 0:
                if len(subjectIds) > 1: # same timestamp
                    df2 = pd.read_csv(csvWorkerIds)
                    PROLIFIC_PIDs = df2.loc[df2['timestamp'] == timestamp]['PROLIFIC_PID'].values
                    i = PROLIFIC_PIDs.tolist().index(PROLIFIC_PID)
                    return subjectIds[i]
                return subjectIds[0]
            else:
                return False
        else:
            return False
    else:
        return False

def get_PROLIFIC_PID(expId, subjectId):
    csvWorkerIds = _thisDir + '/data/' + expId +'/' + expId + '_subject_worker_ids.csv'
    csvSubjectIds = _thisDir + '/data/' + expId +'/' + expId + '_subject_assignment_info.csv'
    if os.path.exists(csvSubjectIds):
        df = pd.read_csv(csvSubjectIds)
        timestamps = df.loc[df['subjectId'] == subjectId]['timestamp'].values
        if len(timestamps) > 0:
            timestamp = timestamps[0]
            if os.path.exists(csvWorkerIds):
                df2 = pd.read_csv(csvWorkerIds)
                PROLIFIC_PIDs = df2.loc[df2['timestamp'] == timestamp]['PROLIFIC_PID'].values
                if len(PROLIFIC_PIDs) > 0:
                    if len(PROLIFIC_PIDs) > 1: # same timestamp
                        df2 = pd.read_csv(csvSubjectIds)
                        subjectIds = df2.loc[df2['timestamp'] == timestamp]['subjectId'].values
                        i = subjectIds.tolist().index(subjectId)
                        return PROLIFIC_PIDs[i]
                    return PROLIFIC_PIDs[0]
                else:
                    return False
        else:
            return False


def get_STUDY_ID(expId, subjectId):
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_assignment_info.csv'
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)
        STUDY_IDs = df.loc[df['subjectId'] == subjectId]['STUDY_ID'].values
        if len(STUDY_IDs) > 0:
            STUDY_ID = STUDY_IDs[0]
            return STUDY_ID
        else:
            return False # STUDY_ID doesn't exist
    else:
        return False

def PROLIFIC_PID_exists(expId, PROLIFIC_PID):
    csvWorkerIds = _thisDir + '/data/' + expId +'/' + expId + '_subject_worker_ids.csv'
    if os.path.exists(csvWorkerIds):
        df = pd.read_csv(csvWorkerIds)
        if PROLIFIC_PID in df['PROLIFIC_PID'].values:
            return True
    return False

def completed_task(expId, PROLIFIC_PID, task):
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_assignment_info.csv'
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)
        if PROLIFIC_PID_exists(expId, PROLIFIC_PID) and task in df.columns:
            subjectId = get_subjectId(expId, PROLIFIC_PID)
            completed = df.loc[df['subjectId'] == subjectId][task].values[0]
            if completed == True:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def completed_task_subject(expId, subjectId, task):
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_assignment_info.csv'
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)
        if task in df.columns:
            completed = df.loc[df['subjectId'] == subjectId][task].values[0]
            if completed == True:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def set_completed_task(expId, PROLIFIC_PID, task, boole):
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_assignment_info.csv'
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)
        if PROLIFIC_PID_exists(expId, PROLIFIC_PID):
            subjectId = get_subjectId(expId, PROLIFIC_PID)
            idx = df[df['subjectId'] == subjectId].index[0]
            df.loc[idx, task] = boole
            df.to_csv(csvLocation,index=False)

"""
name: name of note
"""
def get_worker_notes(expId, subjectId, name):
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_assignment_info.csv'
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)
        if name in df.columns:
            #print df.loc[df[subjectId] == subjectId][name].values
            values = df.loc[df['subjectId'] == subjectId][name].values
            if len(values) > 0:
                return values[0]
    return None

"""
name: name of note
value: value of note with the given name
"""
def add_worker_notes(expId, PROLIFIC_PID, name, value):
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_assignment_info.csv'
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)
        if PROLIFIC_PID_exists(expId, PROLIFIC_PID):
            subjectId = get_subjectId(expId, PROLIFIC_PID)
            idx = df[df['subjectId'] == subjectId].index[0]
            df.loc[idx, name] = value
            df.to_csv(csvLocation,index=False)

def store_feedback(expId, PROLIFIC_PID, feedback):
    csvLocation = _thisDir + '/data/' + expId +'/' + expId + '_subject_feedback.csv'
    if PROLIFIC_PID_exists(expId, PROLIFIC_PID):
        subjectId = get_subjectId(expId, PROLIFIC_PID)
        newData = {'expId':expId, 'subjectId':subjectId, 'feedback':feedback}
        if not os.path.exists(csvLocation):
            new_df = pd.DataFrame(data=newData, index=[0])
        else:
            df = pd.read_csv(csvLocation)
            df2 = pd.DataFrame(data=newData, index=[0])
            new_df = pd.concat([df,df2], axis=0)
        new_df.to_csv(csvLocation,index=False)

"""
Get information from csv in individual subject folders
name: name of note
"""
def get_subfile_worker_notes(expId, subjectId, name):
    subDir = os.path.join(_thisDir, 'data', expId, subjectId)
    csvLocation = os.path.join(subDir, subjectId+'_SubjectNotes.csv')
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)
        if name in df.columns:
            #print df.loc[df[subjectId] == subjectId][name].values
            values = df.loc[df['subjectId'] == subjectId][name].values
            if len(values) > 0:
                return values[0]
    return False


"""
Add information to csv in individual subject folders
name: name of note
value: value of note with the given name
"""
def add_subfile_worker_notes(expId, subjectId, name, value):
    subDir = os.path.join(_thisDir, 'data', expId, subjectId)
    if not os.path.exists(subDir):
        os.mkdir(subDir)
    csvLocation = os.path.join(subDir, subjectId+'_SubjectNotes.csv')
    df = pd.DataFrame()
    if os.path.exists(csvLocation):
        df = pd.read_csv(csvLocation)

    df = df.to_dict('list')
    df['subjectId'] = [subjectId]
    df[name] = [str(value)]
    df = pd.DataFrame.from_dict(df)
    df.to_csv(csvLocation,index=False)