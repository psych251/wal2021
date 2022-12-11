import os
import sys
import csv
import random
import pandas as pd
import numpy as np
import mturk_utils
import glob

from manage_subject_info import *

expId = 'MEM'

_thisDir = os.path.dirname(os.path.abspath(__file__))
_parentDir = os.path.abspath(os.path.join(_thisDir, os.pardir))
dataDir = _parentDir + '/data/'

"""
Checks request.args has STUDY_ID, SESSION_ID, turkSubmitTo, PROLIFIC_PID, live - all but live is passed by MTurk
live refers to whether HIT is live or in sandbox
"""


def contains_necessary_args(args):
    if 'PROLIFIC_PID' in args and 'STUDY_ID' in args and 'SESSION_ID' in args:
        return True
    else:
        return False


"""
Retrieve necessary args: STUDY_ID, SESSION_ID, turkSubmitTo, PROLIFIC_PID, live
"""


def get_necessary_args(args):
    PROLIFIC_PID = args.get('PROLIFIC_PID')
    STUDY_ID = args.get('STUDY_ID')
    SESSION_ID = args.get('SESSION_ID')
    return [PROLIFIC_PID, STUDY_ID, SESSION_ID]

n_encoding_trials = 96

def get_all_images():
    animate_photo_imgs = glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_bird/*.jpg')) + \
                         glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_insect/*.jpg')) + \
                         glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_mammal/*.jpg')) + \
                         glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_sea/*.jpg'))
    animate_photo_imgs = ['/' + '/'.join(img.split('/')[-4:]) for img in animate_photo_imgs]
    animate_photos_df = pd.DataFrame(animate_photo_imgs, columns=['img'])
    animate_photos_df['animacy'] = 'animate'
    animate_photos_df['style'] = 'photo'

    animate_drawing_imgs = glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_bird/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_insect/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_mammal/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_sea/*.jpg'))
    animate_drawing_imgs = ['/' + '/'.join(img.split('/')[-4:]) for img in animate_drawing_imgs]
    animate_drawing_df = pd.DataFrame(animate_drawing_imgs, columns=['img'])
    animate_drawing_df['animacy'] = 'animate'
    animate_drawing_df['style'] = 'drawing'

    inanimate_photo_imgs = glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_clothe/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_electronic/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_fruit/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_veggie/*.jpg'))
    inanimate_photo_imgs = ['/' + '/'.join(img.split('/')[-4:]) for img in inanimate_photo_imgs]
    inanimate_photos_df = pd.DataFrame(inanimate_photo_imgs, columns=['img'])
    inanimate_photos_df['animacy'] = 'inanimate'
    inanimate_photos_df['style'] = 'photo'

    inanimate_drawing_imgs = glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_clothe/*.jpg')) + \
                             glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_electronic/*.jpg')) + \
                             glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_fruit/*.jpg')) + \
                             glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_veggie/*.jpg'))
    inanimate_drawing_imgs = ['/' + '/'.join(img.split('/')[-4:]) for img in inanimate_drawing_imgs]
    inanimate_drawing_df = pd.DataFrame(inanimate_drawing_imgs, columns=['img'])
    inanimate_drawing_df['animacy'] = 'inanimate'
    inanimate_drawing_df['style'] = 'drawing'
    return animate_photos_df, animate_drawing_df, inanimate_photos_df, inanimate_drawing_df

def get_images():
    animate_photo_imgs = glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_bird/*.jpg')) + \
                         glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_insect/*.jpg')) + \
                         glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_mammal/*.jpg')) + \
                         glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_sea/*.jpg'))
    animate_photo_imgs = ['/' + '/'.join(img.split('/')[-4:]) for img in animate_photo_imgs]
    img_names = [img.split('/')[-1] for img in animate_photo_imgs]
    animate_photos_df = pd.DataFrame(animate_photo_imgs, columns=['img'])
    animate_photos_df['animacy'] = 'animate'
    animate_photos_df['style'] = 'photo'
    animate_photos_df['img_name'] = img_names
    animate_photos_df = animate_photos_df.sample(frac=0.5)

    animate_drawing_imgs = glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_bird/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_insect/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_mammal/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_sea/*.jpg'))
    animate_drawing_imgs = ['/' + '/'.join(img.split('/')[-4:]) for img in animate_drawing_imgs]
    img_names = [img.split('/')[-1] for img in animate_drawing_imgs]
    animate_drawing_df = pd.DataFrame(animate_drawing_imgs, columns=['img'])
    animate_drawing_df['animacy'] = 'animate'
    animate_drawing_df['style'] = 'drawing'
    animate_drawing_df['img_name'] = img_names
    animate_drawing_df = animate_drawing_df.loc[~animate_drawing_df['img_name'].isin(animate_photos_df['img_name'].values)]

    inanimate_photo_imgs = glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_clothe/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_electronic/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_fruit/*.jpg')) + \
                           glob.glob(os.path.join(_thisDir, '../static/object_pics/picture_veggie/*.jpg'))
    inanimate_photo_imgs = ['/' + '/'.join(img.split('/')[-4:]) for img in inanimate_photo_imgs]
    img_names = [img.split('/')[-1] for img in inanimate_photo_imgs]
    inanimate_photos_df = pd.DataFrame(inanimate_photo_imgs, columns=['img'])
    inanimate_photos_df['animacy'] = 'inanimate'
    inanimate_photos_df['style'] = 'photo'
    inanimate_photos_df['img_name'] = img_names
    inanimate_photos_df = inanimate_photos_df.sample(frac=0.5)

    inanimate_drawing_imgs = glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_clothe/*.jpg')) + \
                             glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_electronic/*.jpg')) + \
                             glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_fruit/*.jpg')) + \
                             glob.glob(os.path.join(_thisDir, '../static/object_pics/drawing_veggie/*.jpg'))
    inanimate_drawing_imgs = ['/' + '/'.join(img.split('/')[-4:]) for img in inanimate_drawing_imgs]
    img_names = [img.split('/')[-1] for img in inanimate_drawing_imgs]
    inanimate_drawing_df = pd.DataFrame(inanimate_drawing_imgs, columns=['img'])
    inanimate_drawing_df['animacy'] = 'inanimate'
    inanimate_drawing_df['style'] = 'drawing'
    inanimate_drawing_df['img_name'] = img_names
    inanimate_drawing_df = inanimate_drawing_df.loc[~inanimate_drawing_df['img_name'].isin(inanimate_photos_df['img_name'].values)]
    return animate_photos_df, animate_drawing_df, inanimate_photos_df, inanimate_drawing_df

def generate_encoding_and_retrieval_trials(n_trials_per_block):
    [animate_photos_df, animate_drawing_df, inanimate_photos_df, inanimate_drawing_df] = get_images()
    df = pd.concat([animate_photos_df, animate_drawing_df, inanimate_photos_df, inanimate_drawing_df])

    df = df.sample(n=n_encoding_trials)

    words = pd.read_csv(os.path.join(_thisDir, '../static/list_of_verbs.txt'), header=None)
    words.columns = ['verb']
    words['verb'] = words['verb'].str.lower()
    words = words.sample(frac=1)
    words = words.sample(n=n_encoding_trials)
    words.reset_index(inplace=True, drop=True)

    df['verb'] = words['verb'].values
    df = df.sample(frac=1)
    df.reset_index(inplace=True, drop=True)

    retrieval_trials = set_retrieval_trial_order(df, n_trials_per_block)
    retrieval_trials = retrieval_trials.merge(df, how="left", on="img")
    return df, retrieval_trials


# ensure that the repeated presentations of item are separated at least two trials apart
def set_retrieval_trial_order(encoding_trials_df, n_trials_per_block):
    full_retrieval_trial_df = pd.DataFrame()
    n_blocks = len(encoding_trials_df) / n_trials_per_block
    current_block_n = 0
    starting_trial_i = 0
    while current_block_n < n_blocks:
        current_block_df = encoding_trials_df.iloc[starting_trial_i:starting_trial_i + n_trials_per_block].copy()

        # first presentation of item
        current_block_items1 = list(current_block_df.sample(frac=1)['img'].values)
        # second presentation of item
        current_block_items2 = list(current_block_df.sample(frac=1)['img'].values)

        need_to_reshuffle = (current_block_items1[-1] == current_block_items2[0]) or (
                current_block_items1[-1] == current_block_items2[1]) or (
                                    current_block_items2[-1] == current_block_items1[0]) or (
                                    current_block_items2[-1] == current_block_items1[1])
        while need_to_reshuffle:
            current_block_items2 = list(current_block_df.sample(frac=1)['img'].values)

            need_to_reshuffle = (current_block_items1[-1] == current_block_items2[0]) or (
                    current_block_items1[-1] == current_block_items2[1]) or (
                                        current_block_items2[-1] == current_block_items1[0]) or (
                                        current_block_items2[-1] == current_block_items1[1])

        current_block_items1_df = pd.DataFrame(current_block_items1, columns=["img"])
        current_block_items2_df = pd.DataFrame(current_block_items2, columns=["img"])

        # randomly assign half to be asked perceptual question first, other half to semantic question first
        current_block_items1_df["instruction"] = "semantic"
        current_block_items2_df["instruction"] = "perceptual"
        percep_first_items = np.random.choice(a=current_block_items1, size=int(len(current_block_items1) / 2),
                                              replace=False)

        current_block_items1_df.loc[
            current_block_items1_df["img"].isin(percep_first_items), "instruction"] = "perceptual"
        current_block_items2_df.loc[current_block_items2_df["img"].isin(percep_first_items), "instruction"] = "semantic"

        current_block_retrieval_trial_df = pd.concat([current_block_items1_df, current_block_items2_df])
        current_block_retrieval_trial_df["block_n"] = current_block_n
        full_retrieval_trial_df = pd.concat([full_retrieval_trial_df, current_block_retrieval_trial_df])
        current_block_n += 1
        starting_trial_i += n_trials_per_block

    full_retrieval_trial_df.reset_index(inplace=True, drop=True)
    return full_retrieval_trial_df


def generate_visual_trials():
    [animate_photos_df, animate_drawing_df, inanimate_photos_df, inanimate_drawing_df] = get_all_images()
    df = pd.concat([animate_photos_df, animate_drawing_df, inanimate_photos_df, inanimate_drawing_df])
    animate_categories = ["bird", "insect", "mammal", "sea"]
    inanimate_categories = ["clothe", "electronic", "fruit", "veggie"]
    animate_photo_categories = np.random.choice(a=animate_categories, size=int(len(animate_categories)/2), replace=False)
    inanimate_photo_categories = np.random.choice(a=inanimate_categories, size=int(len(inanimate_categories)/2), replace=False)

    df_new = pd.DataFrame()
    for category in animate_categories:
        if category in animate_photo_categories:
            sub_df = df.loc[df['img'].str.contains("picture_"+category)]
            sub_df['animacy'] = 'animate'
            sub_df['style'] = 'photo'
            df_new = pd.concat([df_new, sub_df])
        else:
            sub_df = df.loc[df['img'].str.contains("drawing_" + category)]
            sub_df['animacy'] = 'animate'
            sub_df['style'] = 'drawing'
            df_new = pd.concat([df_new, sub_df])

    for category in inanimate_categories:
        if category in inanimate_photo_categories:
            sub_df = df.loc[df['img'].str.contains("picture_"+category)]
            sub_df['animacy'] = 'inanimate'
            sub_df['style'] = 'photo'
            df_new = pd.concat([df_new, sub_df])
        else:
            sub_df = df.loc[df['img'].str.contains("drawing_" + category)]
            sub_df['animacy'] = 'inanimate'
            sub_df['style'] = 'drawing'
            df_new = pd.concat([df_new, sub_df])

    df_new.reset_index(inplace=True, drop=True)

    df_new['instruction'] = 'semantic'
    percep_trials = np.random.choice(a=range(len(df_new)), size=int(len(df_new) / 2), replace=False)
    percep_trials.sort()
    df_new.loc[percep_trials, 'instruction'] = 'perceptual'

    df_new = df_new.sample(frac=1)
    #df_new = df_new.sample(n=n_encoding_trials)

    return df_new


def get_demographicq():
    info = pd.read_csv(_thisDir + '/DemographicQuestions.csv', delimiter=',', encoding="utf-8-sig")
    questions = info['Question']
    info = info.set_index('Question')
    new_info = []
    for j in range(0, len(questions)):
        q = questions[j]
        tmp = info.loc[q].values
        options = []
        for i in tmp:
            if (type(i) == str) or (type(i) == bytes):  # remove nan values
                options.append(i)
        new_info.append({q: options})
    return new_info