import random
import string
import urllib
import os

def convert_request_to_mturk_args(request):
	[PROLIFIC_PID, STUDY_ID, SESSION_ID] = get_necessary_args(request.args)
	mturk_args={}
	mturk_args['PROLIFIC_PID'] = PROLIFIC_PID
	mturk_args['STUDY_ID'] = STUDY_ID
	mturk_args['SESSION_ID'] = SESSION_ID
	return mturk_args

def get_url(mturk_args,prefix,expId,route):
	arg_keys = ['PROLIFIC_PID','STUDY_ID','SESSION_ID']
	for key in arg_keys:
		if key not in mturk_args.keys():
			print("Missing key in mturk_args:", key)
			raise KeyError
	args='?'+urllib.urlencode(mturk_args)
	if prefix == None:
		link=os.path.join('https://calkins.psych.columbia.edu',expId,route+args)
	else:
		link=os.path.join('https://calkins.psych.columbia.edu',prefix,expId,route+args)
	return link

"""
Checks request.args has STUDY_ID, SESSION_ID, PROLIFIC_PID
"""
def contains_necessary_args(args):
	if 'PROLIFIC_PID' in args and 'STUDY_ID' in args and 'SESSION_ID' in args:
		return True
	else:
		return False

"""
Retrieve necessary args: STUDY_ID, SESSION_ID, PROLIFIC_PID
"""
def get_necessary_args(args):
	PROLIFIC_PID = args.get('PROLIFIC_PID')
	STUDY_ID = args.get('STUDY_ID')
	SESSION_ID = args.get('SESSION_ID')
	return [PROLIFIC_PID, STUDY_ID, SESSION_ID]

def get_completion_code():
	# from https://pythontips.com/2013/07/28/generating-a-random-string/
	return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])

