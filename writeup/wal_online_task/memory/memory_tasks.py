import random
from flask import Flask, render_template, request, session, Blueprint
from flask import redirect, url_for
import json
import pandas as pd
import time
from .utils import *
from store_data import *
from manage_subject_info import *

expId = 'MEM'

memory_tasks = Blueprint('memory_tasks', __name__, url_prefix='/MEM')

_thisDir = os.path.dirname(os.path.abspath(__file__))
_parentDir = os.path.abspath(os.path.join(_thisDir, os.pardir))
dataDir = _parentDir + '/data/'

expTasksToComplete = {'completedEncoding': False}


@memory_tasks.route("/", methods=["GET", "POST"])
def consent_form():
    if request.method == "GET":
        return render_template('memory/consent_form.html')
    else:
        if contains_necessary_args(request.args):
            # worker accepted HIT
            [PROLIFIC_PID, STUDY_ID, SESSION_ID] = get_necessary_args(request.args)
            if not PROLIFIC_PID_exists(expId, PROLIFIC_PID):
                store_subject_info(expId, PROLIFIC_PID, expTasksToComplete, STUDY_ID, SESSION_ID)
        else:
            # in testing - will create random worker ID and assignment ID
            PROLIFIC_PID = 'testWorker' + str(random.randint(1000, 10000))
            STUDY_ID = 'testAssignment' + str(random.randint(10000, 100000))
            SESSION_ID = 'testHIT' + str(random.randint(10000, 100000))
            store_subject_info(expId, PROLIFIC_PID, expTasksToComplete, STUDY_ID, SESSION_ID)
        return redirect(
            url_for('.mem_dep',
                    expId=expId, PROLIFIC_PID=PROLIFIC_PID, STUDY_ID=STUDY_ID, SESSION_ID=SESSION_ID))


# memory-dependent tasks: encoding, distractor (number parity), retrieval
@memory_tasks.route("/mem_dep", methods=["GET", "POST"])
def mem_dep():
    containsAllProlificArgs = contains_necessary_args(request.args)
    if containsAllProlificArgs:
        [PROLIFIC_PID, STUDY_ID, SESSION_ID] = get_necessary_args(request.args)
    if request.method == "GET" and containsAllProlificArgs:  # GET request
        subjectId = get_subjectId(expId, PROLIFIC_PID)
        filePath = dataDir + expId + '/' + subjectId + '/'
        encoding_trials, retrieval_trials = generate_encoding_and_retrieval_trials(n_trials_per_block=8)
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        encoding_trials.to_csv(os.path.join(filePath, subjectId + '_CueImagePairings.csv'))
        retrieval_trials.to_csv(os.path.join(filePath, subjectId + '_RetrievalTrialList.csv'))

        imgs = list(encoding_trials['img'].values)

        encoding_trials = encoding_trials.to_dict('records')
        retrieval_trials = retrieval_trials.to_dict('records')

        return render_template('memory/mem_dependent.html',
                               encoding_trials=encoding_trials,
                               retrieval_trials=retrieval_trials,
                               imgs=imgs)

    elif containsAllProlificArgs:  # POST request
        subjectId = get_subjectId(expId, PROLIFIC_PID)
        expResults = json.loads(request.form['experimentResults'])
        filePath = dataDir + expId + '/' + subjectId + '/'
        add_subfile_worker_notes(expId, subjectId, 'completedMemoryTask', True)
        results_to_csv(expId, subjectId, filePath, 'MemoryResults.csv', expResults, {})
        return redirect(
            url_for('.questionnaire', expId=expId, PROLIFIC_PID=PROLIFIC_PID, STUDY_ID=STUDY_ID, SESSION_ID=SESSION_ID))
    return redirect(url_for('unauthorized_error'))


@memory_tasks.route("/vis", methods=["GET", "POST"])
def consent_form_vis():
    if request.method == "GET":
        return render_template('memory/consent_form.html')
    else:
        if contains_necessary_args(request.args):
            # worker accepted HIT
            [PROLIFIC_PID, STUDY_ID, SESSION_ID] = get_necessary_args(request.args)
            if not PROLIFIC_PID_exists(expId, PROLIFIC_PID):
                store_subject_info(expId, PROLIFIC_PID, expTasksToComplete, STUDY_ID, SESSION_ID)
        else:
            # in testing - will create random worker ID and assignment ID
            PROLIFIC_PID = 'testWorker' + str(random.randint(1000, 10000))
            STUDY_ID = 'testAssignment' + str(random.randint(10000, 100000))
            SESSION_ID = 'testHIT' + str(random.randint(10000, 100000))
            store_subject_info(expId, PROLIFIC_PID, expTasksToComplete, STUDY_ID, SESSION_ID)
        return redirect(
            url_for('.visual',
                    expId=expId, PROLIFIC_PID=PROLIFIC_PID, STUDY_ID=STUDY_ID, SESSION_ID=SESSION_ID))

@memory_tasks.route("/visual", methods=["GET", "POST"])
def visual():
    containsAllProlificArgs = contains_necessary_args(request.args)
    if containsAllProlificArgs:
        [PROLIFIC_PID, STUDY_ID, SESSION_ID] = get_necessary_args(request.args)
    if request.method == "GET" and containsAllProlificArgs:  # GET request
        trials = generate_visual_trials()
        imgs = list(trials['img'].values)
        trials = trials.to_dict('records')
        return render_template('memory/visual.html', trials=trials, imgs=imgs)
    elif containsAllProlificArgs:  # POST request
        subjectId = get_subjectId(expId, PROLIFIC_PID)
        expResults = json.loads(request.form['experimentResults'])
        interactData = json.loads(request.form['interactionData'])
        filePath = dataDir + expId + '/' + subjectId + '/'
        add_subfile_worker_notes(expId, subjectId, 'completedVisualTask', True)
        results_to_csv(expId, subjectId, filePath, 'VisualResults.csv', expResults, {})
        results_to_csv(expId, subjectId, filePath, 'VisualTaskInteractionData.csv', interactData, {})
        return redirect(
            url_for('.questionnaire', expId=expId, PROLIFIC_PID=PROLIFIC_PID, STUDY_ID=STUDY_ID, SESSION_ID=SESSION_ID))
    return redirect(url_for('unauthorized_error'))


@memory_tasks.route("/qs", methods=["GET", "POST"])
def questionnaire():
    info = get_demographicq()
    instructions = 'Please answer each question as accurately as possible.'
    containsAllProlificArgs = contains_necessary_args(request.args)
    if containsAllProlificArgs:
        [PROLIFIC_PID, STUDY_ID, SESSION_ID] = get_necessary_args(request.args)
    if request.method == "GET" and containsAllProlificArgs:
        widthPercent = 10
        return render_template('demographicq.html', info=info, instructions=instructions,
                               widthPercent=widthPercent)
    elif containsAllProlificArgs:  # in request.method == "POST"
        subjectId = get_subjectId(expId, PROLIFIC_PID)
        q_and_a = []  # list of dictionaries where questions are keys and answers are values
        nQuestions = len(info)
        for i in range(0, nQuestions):
            tmp = {'QuestionNum': i + 1, 'Question': request.form['q' + str(i + 1)]}
            if 'a' + str(i + 1) in request.form:
                tmp['Answer'] = request.form['a' + str(i + 1)]  # set keys and values in dictionary
            else:
                tmp['Answer'] = ''
            q_and_a.append(tmp)

        tmp = {'QuestionNum': len(q_and_a) + 1, 'Question': 'Feedback', 'Answer': request.form['feedback']}
        q_and_a.append(tmp)

        filePath = dataDir + expId + '/' + subjectId + '/'

        add_subfile_worker_notes(expId, subjectId, 'completedDemoQ', True)
        results_to_csv(expId, subjectId, filePath, 'DemographicQuestionnaire.csv', q_and_a, {})

        return redirect(
            url_for('thank_you', expId=expId, PROLIFIC_PID=PROLIFIC_PID, STUDY_ID=STUDY_ID, SESSION_ID=SESSION_ID))
    else:
        return redirect(url_for('unauthorized_error'))