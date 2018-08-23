import warnings
warnings.filterwarnings("ignore")

from models.similarusers import SimilarUsers

from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from flask_jwt import JWT, jwt_required, current_identity
from flask_bcrypt import Bcrypt

import json
import sys
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()
bcrypt = Bcrypt(app)

def authenticate(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return Users.query.filter_by(id=user_id).first

jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

# this will be handled with hashed credentials in full version
@auth.get_password
def get_password(username):
    print("username:", username)
    if username == "Gderasaria":
        return "12345"
    return None

@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


class ApiCall(Resource):
	""" API Call
		Sends json object containing suggested users
	"""

	decorators = [auth.login_required]

	def __init__(self):
		print(1)
		self.reqparser = reqparse.RequestParser()
		super(ApiCall, self).__init__()	

	def post(self):

		print ('Enter Post')

		args = self.reqparser.parse_args()

		jsonstring = request.data
		jsonobject = json.loads(jsonstring.decode("utf-8"))

		print (jsonobject)

		if  "UserHandle" in jsonobject:
			print ('Entered json object')
			userInfo = jsonobject["UserHandle"]
			simuser = SimilarUsers(userInfo, train_mode = False)
			user_dict = simuser.recommendation()
			print ('type of user_dict',type(user_dict))
			user_dict_fin = { str(i) : j  for i,j in user_dict}
		print(user_dict_fin)
		
		return user_dict_fin,200

try:
	api.add_resource(ApiCall,'/api/v1.0/recommend',endpoint='recommend')

except:
	api.add_resource(ApiCall,'api/v1.0/recommend',endpoint=b'recommend')
	
if __name__ == "__main__":
	import ssl as SSL
	context = SSL.create_default_context(SSL.Purpose.CLIENT_AUTH)
	context.load_cert_chain('cert.pem', 'key.pem')
	print("**Starting Server...")

	app.run(host='0.0.0.0',use_reloader=True,port=5000,ssl_context= context, debug=True)
	print(1)