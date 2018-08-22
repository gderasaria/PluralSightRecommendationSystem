import pandas as pd
import numpy as np 
from operator import itemgetter
import os 

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from helpers.scoring import Scoring

import sqlite3
import pickle

class SimilarUsers: 
	
	def __init__(self, user_id, train_mode):
		self.user_id = user_id
		self.train_mode = train_mode
		self.scoring = Scoring()


	def pre_process_data(self,file_path	):
		"""Loads data from sqlite database to pre-process the data and store it in sqlite format"""

		conn = sqlite3.connect(file_path)
		#course_tags = pd.read_sql("SELECT * FROM course_tags", conn)
		user_assessment_scores = pd.read_sql("SELECT * FROM user_assessment_scores", conn)
		user_course_views = pd.read_sql("SELECT * FROM user_course_views",conn)
		user_interests = pd.read_sql("SELECT * FROM user_interests",conn)
		conn.close()

		self.scoring.course_score(user_course_views)
		return

	def recommendation(self):
		#print("inside")
		with open('../data/processed/course_scoring_dict.pickle', 'rb') as handle:
			#print("opened file")
			course_scoring_dict = pickle.load(handle)
			#print("completed loading") 
		if self.user_id in course_scoring_dict:
			#print("user_id exists")
			print(course_scoring_dict[self.user_id][:5])
			#print("done")
		return 



