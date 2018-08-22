#A Temporary test file 
from similarusers import SimilarUsers


sim = SimilarUsers(7,True) 
sim.pre_process_data("../data/raw/rawdata.db")
sim.recommendation()