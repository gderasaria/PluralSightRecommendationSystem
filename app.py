import warnings
warnings.filterwarnings("ignore")

from models.similarusers import SimilarUsers

from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from flask_jwt import JWT, jwt_required, current_identity
from flask_bcrypt import Bcrypt
from flask_json  import json_response

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


@auth.get_password
def get_password(username):
    print("username:", username)
    if username == "Gderasaria":
        return "12345"
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


class ApiCall(Resource):
	""" API Call
		Sends json object containing suggested users
	"""

	decorators = [auth.login_required]

	def __init__(self):
		self.reqparser = reqparse.RequestParser()
		super(ApiCall, self).__init__()	

	def post(self):
		"""Return similar user with their similarity user to client as HTTP response
		"""
		args = self.reqparser.parse_args()

		jsonstring = request.data
		jsonobject = json.loads(jsonstring.decode("utf-8"))

		if  "UserHandle" in jsonobject:
			userInfo = jsonobject["UserHandle"]
			simuser = SimilarUsers(userInfo, train_mode = False)
			user_dict = simuser.recommendation(path="models/")
			#print ('type of user_dict',type(user_dict))
			user_dict_fin = { str(i) : j  for i,j in user_dict}
			#print(type(user_dict_fin))

		return jsonify(user_dict_fin)#,200

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

