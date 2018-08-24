import pandas as pd 
import numpy as np 
import pickle 
from scipy.sparse.linalg import svds
from sklearn.metrics.pairwise import pairwise_distances
from operator import itemgetter

class Scoring:
	''' 
	Generates similarity score based on various features
	'''

	def perform_svd(self,data_frame,k):
		"""Performs svd on the user dataframe and returns user similarity matrix """
		U,S,Vt = svds(data_frame, k)
		U = pairwise_distances(U, metric='cosine')
		U = pd.DataFrame(U, index = data_frame.index,\
						  columns = data_frame.index)

		return U 

	def get_co_occurrence(self,dataframe,H):
		"""" Helper to get the coocurrence of users from the dataframe  """

		co_occurence_data = dataframe.dot(dataframe.T) # Compute co-occurence of courses amongst users
		offset = 10**-10       	
		co_occurence_data  =  co_occurence_data/H
		co_occurence_data[co_occurence_data > 1]  = 1 
		co_occurence_data[co_occurence_data  == 0] = offset #Adding offset to avoiding dividing by zero 

		return co_occurence_data 

	def generate_dict(self,dataframe):
		"""Takes in a similarity dataframe and returns a dictionary of top 100 users for each user id"""

		scoring_dict = {}
		for index,row in zip(dataframe.index, dataframe.iterrows()): 
			scoring_dict[index] = []
			for idx,i in zip(dataframe.index,row[1]):
				if index != idx :
					scoring_dict[index].append((idx,i))
			scoring_dict[index] = sorted(scoring_dict[index], key= itemgetter(1))
			scoring_dict[index] = scoring_dict[index][:100]

		return scoring_dict


	def assessment_score(self,user_assessment_data):
		"""
		Computes user similarity based on assessment scores 
		"""
		
		user_assessment = pd.pivot_table(user_assessment_data, index = "user_handle" , columns= "assessment_tag" ,\
                                                  values="user_assessment_score")
		user_assessment = user_assessment.apply(lambda x: x / np.sqrt(np.nansum(np.square(x))))
		user_assessment = user_assessment.replace(np.nan,0)

		offset = 0.005 #small offset to avoid dividing by zero
		user_assessment = self.perform_svd(user_assessment, k =50)

		#Get a co_occurence matrix to do a weighted similarity scoring. 
		temp_table = pd.pivot_table(user_assessment_data, index = "user_handle", columns = "assessment_tag" ,\
									  values = "user_assessment_date" ,  
									  aggfunc = len )
		co_occurence = temp_table.dot(temp_table.T)
		co_occurence = co_occurence.replace(np.nan,0)
		co_occurence[co_occurence > 1] = 1 
		co_occurence += offset

		user_assessment = user_assessment.div(co_occurence)

		assessment_scoring_dict = self.generate_dict(user_assessment)
		print("assessment_score done")

		with open("../models/data/processed/assessment_scoring_dict.pickle",'wb') as file:
			pickle.dump(assessment_scoring_dict, file, protocol = pickle.HIGHEST_PROTOCOL)


	def interests_score(self,user_interests):
		"""
		Computes user similarity based on user_interests
		"""
		
		user_interests = pd.pivot_table(user_interests,index = "user_handle",\
												  columns="interest_tag",values = "date_followed",aggfunc=len)
		user_interests = user_interests.replace(np.nan,0)
		user_interests[user_interests != 0 ] = 1
		
		#Run svd on the interests_course matrix to get a user similarity matrix
		user_similarity = self.perform_svd(user_interests,400)
		interests_co_occurence = self.get_co_occurrence(user_interests, 8)
		user_similarity = user_similarity.div(interests_co_occurence)	
		interests_scoring_dict = self.generate_dict(user_similarity)

		with open("../models/data/processed/interests_scoring_dict.pickle",'wb') as file:
			pickle.dump(interests_scoring_dict, file, protocol = pickle.HIGHEST_PROTOCOL)

	def course_score(self,user_course_views):
		
		""" 
		Computes user similarity based on course_interests
		"""
		
		user_course_views = pd.pivot_table(user_course_views, index= "user_handle",\
                        				   columns = "course_id" ,\
                        				   values="view_time_seconds", aggfunc = len)
		user_course_views = user_course_views.replace(np.nan,0)
		user_course_views[user_course_views != 0 ] = 1

		#Run svd on the user_course_views matrix to get a user similarity matrix
		user_similarity = self.perform_svd(user_course_views,800)
		course_co_occurence = self.get_co_occurrence(user_course_views,6)
		user_similarity = user_similarity.div(course_co_occurence)	
		course_scoring_dict = self.generate_dict(user_similarity)
		
		with open("../models/data/processed/course_scoring_dict.pickle",'wb') as file:
			pickle.dump(course_scoring_dict,file, protocol = pickle.HIGHEST_PROTOCOL)