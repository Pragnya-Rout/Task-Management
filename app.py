# -*- coding: utf-8 -*-
"""
    Project Name        : Task Management
    Author              : Pragnya Priyadarsini Rout
    Date of Creation    : 09 JULY 2021
    Purpose             : As a part of recruitment process
    Description         : Creating api for Task Management.
    Version             : ver 0.0.1
"""


# import required modules
from flask import Flask,make_response,request,Response,jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Api
from blacklist import BLACKLIST
from models.create_db   import *
from api_view_set.viewset import *

app = Flask(__name__)

# JWT configurations
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # Enable Blacklist Feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access","refresh",]
app.config['SECRET_KEY'] = 'task_management'
api = Api(app)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

jwt = JWTManager(app)





# handle 404 (resource not found) error
@app.errorhandler(404)
def handle_404(e):
    return {'message': 'Requested page not available'}, 404


# handle 505 (internal server error) error
@app.errorhandler(500)
def handle_500(e):
    return {'message': 'Something went wrong'}, 500



@jwt.token_in_blacklist_loader
#A token_in_blacklist_callback must be provided via the '@token_in_blacklist_loader' if JWT_BLACKLIST_ENABLED is True
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


if __name__ == "__main__":
    # map the resources with URL path
    api.add_resource(Create_Employee, '/register-employee')
    api.add_resource(Create_Clients, '/register-client')
    api.add_resource(Create_Managers, '/register-manager')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/log-out')
    api.add_resource(TokenRefresh, '/refresh-token')
    api.add_resource(Create_Edit_Task, '/task-creations')
    api.add_resource(Edit_Task, '/edit-task')
    api.add_resource(Assign_Task, "/assigne-task")
    api.add_resource(Delete_Task, "/delete-task/<string:task_id>")
    api.add_resource(Complete_Task, "/complete-task/<string:task_id>")
    api.add_resource(Task_List, "/task-list")
    # start the flask app in production environment
    app.run(port=5555, debug=True)
