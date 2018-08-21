# Code to access the endpoint for the project 
from flask import Flask


import sqlite3

# Create Flask object to run
app = Flask(__name__)

@app.route('/summary', methods = ["GET"])
def apicall():
	""" API Call

	Sends json object containing suggested users

	"""
	
	return   "In Development"

if __name__ == "__main__":
	print("**Starting Server...")
	
	# Run Server
	app.run()
