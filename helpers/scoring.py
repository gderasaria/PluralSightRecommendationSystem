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
		
		U,S,Vt = svds(data_frame, k = 800)
		U = pairwise_distances(U, metric='cosine')
		U = pd.DataFrame(U, index = data_frame.index,\
						  columns = data_frame.index)
		return U 

	def get_co_ocurrence(self,dataframe,H):

		co_occurence_data = dataframe.dot(dataframe.T) # Compute co-occurence of courses amongst users
		offset = 10**-10       	
		co_occurence_data  =  co_occurence_data/H
		co_occurence_data[co_occurence_data > 1]  = 1 
		co_occurence_data[co_occurence_data  == 0] = offset #Adding offset to avoiding dividing by zero 

		return co_occurence_data 

	def assessment_score(data_frame):
				
		pass

	def interests_score(user_interests):
		
		pass

	def course_score(self,user_course_views):
		
		user_course_views = pd.pivot_table(user_course_views, index= "user_handle",\
                        				   columns = "course_id" ,\
                        				   values="view_time_seconds", aggfunc = len)
		user_course_views = user_course_views.replace(np.nan,0)
		user_course_views[user_course_views != 0 ] = 1

		#Run svd on the user_course matrix to get a user similarity matrix
		user_similarity = self.perform_svd(user_course_views,800)
		course_co_occurence = self.get_co_ocurrence(user_course_views,6)
		user_similarity = user_similarity.div(course_co_occurence)	
		course_scoring_dict = {}
		for index,row in zip(user_similarity.index, user_similarity.iterrows()): 
			course_scoring_dict[index] = []
			for idx,i in zip(user_similarity.index,row[1]):
				if index != idx :
					course_scoring_dict[index].append((idx,i))
			course_scoring_dict[index] = sorted(course_scoring_dict[index], key= itemgetter(1))
			course_scoring_dict[index] = course_scoring_dict[index][:100]
 	
 		#conn  = sqlite3.connect("../data/processed/course_scoring_dict.sqlite")
 		#c = conn.cursor()
		with open("../data/processed/course_scoring_dict.pickle",'wb') as file:
			pickle.dump(course_scoring_dict,file, protocol = pickle.HIGHEST_PROTOCOL)
 


