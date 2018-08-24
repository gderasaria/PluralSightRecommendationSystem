#A Temporary test file 
from similarusers import SimilarUsers

print("inside test")
sim = SimilarUsers(7487,True)
print("object created") 
sim.pre_process_data("data/raw/rawdata.db")
print("pre_processing done")
sim.recommendation(path = "" )