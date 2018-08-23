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
		self.user_id = int(user_id)
		self.train_mode = train_mode
		if train_mode:	
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
		self.scoring.interests_score(user_interests)
		self.scoring.assessment_score(user_assessment_scores)
		
		return

	def recommendation(self):
		#print("inside")
		with open('../data/processed/course_scoring_dict.pickle', 'rb') as file:
			#print("opened file")
			course_scoring_dict = pickle.load(file)
			#print("completed loading") 

		with open('../data/processed/interests_scoring_dict.pickle', 'rb') as file:
			interests_scoring_dict = pickle.load(file)

		with open('../data/processed/assessment_scoring_dict.pickle', 'rb') as file:
			assessment_scoring_dict = pickle.load(file)		

		if self.user_id in assessment_scoring_dict:
			similar_users_dict = { str(user_id) : score for user_id,score  in assessment_scoring_dict[self.user_id][:5]} 
			#print(assessment_scoring_dict[self.user_id][:5])
			return assessment_scoring_dict[self.user_id][:5]	

		elif self.user_id in course_scoring_dict:
			#print("user_id exists")
			similar_users_dict = { str(user_id) : score for user_id,score  in course_scoring_dict[self.user_id][:5]} 
			#print(course_scoring_dict[self.user_id][:5])
			return course_scoring_dict[self.user_id][:5]
			print("done")
		else: 
			similar_users_dict = { str(user_id) : score for user_id,score  in interests_scoring_dict[self.user_id][:5]} 
			#print(interests_scoring_dict[self.user_id][:5])
			return interests_scoring_dict[self.user_id][:5]
		
		return 



