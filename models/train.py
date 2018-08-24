#A Temporary test file 
from similarusers import SimilarUsers

print("inside test")
sim = SimilarUsers(7487,True)
print("object created") 
sim.pre_process_data("data/raw/rawdata.db")
print("pre_processing done")
<<<<<<< HEAD
sim.recommendation(path = "" )
=======
sim.recommendation()
>>>>>>> 32a51e01875cf613d48fce7c03727e9e2d3f95f5
