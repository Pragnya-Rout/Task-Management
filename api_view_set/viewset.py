
# import required modules
from flask import request,Response,jsonify,make_response,json
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from datetime import datetime
from flask_restful import  Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from blacklist import BLACKLIST
from models.db_model import DbModel

USER_LOGGED_OUT = "User <{}> successfully logged out."

class Operation:
    @staticmethod
    def validate_client_auth(client_id):
        """ validate authorized_client """
        try:
            res=DbModel.retrieve_data("clients","*","client_id='"+client_id+"'","")
            if len(res) != 0:
                return True, res[0]
            return False
        except Exception as err:
            print(err, '-- occurred during fetching client details')
            return False
    
    @staticmethod
    def validate_employee_auth(employee_id):
        """ validate authorized_employee"""
        try:
            res=DbModel.retrieve_data("employees","*","employee_id='"+employee_id+"'","")
            if len(res) != 0:
                return True, res[0]
            return False
        except Exception as err:
            print(err, '-- occurred during fetching employee details')
            return False
            
    @staticmethod
    def validate_manager_auth(manager_id):
        """ validate authorized_manager"""
        try:
            res=DbModel.retrieve_data("managers","*","manager_id='"+manager_id+"'","")
            if len(res) != 0:
                return True, res[0]
            return False
        except Exception as err:
            print(err, '-- occurred during fetching manager details')
            return False
          
class Login(Resource):
    @staticmethod
    def post():
        """
        Log in as a client or an employee or a manager;
        
        """
        try:
            if not ('id'  in request.headers and 'password' in request.headers and 'usertype' in request.headers):
                return {'authenticated': '0', 'message': 'Missing required header.'}
            _id,password,user_type = request.headers['id'],request.headers['password'],request.headers['usertype']
            if (_id.isspace()==True or _id == '')or(password.isspace()==True or password=='')or(user_type.isspace()==True or user_type==''):
                return {'message': 'Headers are missing'}, 401
            if user_type=="employee":
                emp_data=DbModel.retrieve_data("employees","*","employee_id='"+_id+"'","")
                if len(emp_data)==1:
                    emp_pass=emp_data[0]['employee_password']
                    if check_password_hash(emp_pass,password):
                        access_token = create_access_token(identity=_id, fresh=True)
                        refresh_token = create_refresh_token(_id)
                        return ({"emp_access_token": access_token, "emp_refresh_token": refresh_token},200,)
                    return {"message": 'password does not match'}, 401
                return {"message": 'invalid_empid'}, 401
            elif user_type=="client":
                client_data=DbModel.retrieve_data("clients","*","client_id='"+_id+"'","")
                if len(client_data)==1:
                    client_pass=client_data[0]['client_password']
                    if check_password_hash(client_pass,password):
                        access_token = create_access_token(identity=_id, fresh=True)
                        refresh_token = create_refresh_token(_id)
                        return ({"client_access_token": access_token, "client_refresh_token": refresh_token},200,)
                    return {"message": 'password does not match'}, 401
                return {"message": 'invalid_client'}, 401
            elif user_type=="manager":
                mngr_data=DbModel.retrieve_data("managers","*","manager_id='"+_id+"'","")
                if len(mngr_data)==1:
                    manager_pass=mngr_data[0]['manager_password']
                    if check_password_hash(manager_pass,password):
                        access_token = create_access_token(identity=_id, fresh=True)
                        refresh_token = create_refresh_token(_id)
                        return ({"manager_access_token": access_token, "manager_refresh_token": refresh_token},200,)
                    return {"message": 'password does not match'}, 401
                return {"message": 'invalid_manager'}, 401
            else:
                Response(status=401)
            return {"message": 'invalid_user_type'}, 401
        except Exception as err:
            print(err, '-- occurred while trying to login')
            return jsonify({"status": 0, "message": 'Something went wrong!'})

class Create_Clients(Resource):
    @staticmethod
    def post():
        """
        Creates a new Client  to create task;
        
        """
        parser = reqparse.RequestParser()
        parser.add_argument("client_id", type=str, required=True,help="client_id is required")
        parser.add_argument("password", type=str, required=True,help="password is required")
        arg_data = parser.parse_args()
        try:
            client_data=DbModel.retrieve_data("clients","*","client_id='"+arg_data['client_id']+"'","")
            if len(client_data)>0:
                return {"message": 'client_id already exists!'}, 401
            password_hash = generate_password_hash(arg_data['password'])
            values={"client_password":password_hash,"client_id":arg_data['client_id']}
            flag=DbModel.insert_Data("clients",values)
            if flag:
                return ({"message": f"Client{arg_data['client_id']} created successfully"},200,)
            return {"message": 'Client could not be created!'}, 401
        except Exception as err:
            print(err, '-- occurred while trying to create client')
            return jsonify({"status": 0, "message": 'Something went wrong!'})

class Create_Managers(Resource):
    @staticmethod
    def post():
        """
        Creates a new Manager  to assign task;
        
        """
        parser = reqparse.RequestParser()
        parser.add_argument("manager_id", type=str, required=True,help="manager_id is required")
        parser.add_argument("password", type=str, required=True,help="password is required")
        arg_data = parser.parse_args()
        try:
            mngr_data=DbModel.retrieve_data("managers","*","manager_id='"+arg_data['manager_id']+"'","")
            if len(mngr_data)>0:
                return {"message": 'manager_id already exists!'}, 401
            password_hash = generate_password_hash(arg_data['password'])
            values={"manager_password":password_hash,"manager_id":arg_data['manager_id']}
            flag=DbModel.insert_Data("managers",values)
            if flag:
                return ({"message": f"Manager_{arg_data['manager_id']} created successfully"},200,)
            return {"message": 'Manager could not be created!'}, 401
        except Exception as err:
            print(err, '-- occurred while trying to create manager')
            return jsonify({"status": 0, "message": 'Something went wrong!'})

class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

class Create_Edit_Task(Resource):
    @staticmethod
    @jwt_required
    def post():
        """
        Creates a new task;
        
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True,help="title is required")
        parser.add_argument("description", type=str, required=True,help="description is required")
        arg_data = parser.parse_args()
        try:  
            # check for missing headers
            if not ('client_id'  in request.headers):
                return {'authenticated': '0', 'message': 'Missing required header.'}
            client_id = request.headers['client_id']
            res=Operation.validate_client_auth(client_id)
            if res:
                values={"title":arg_data['title'],"description":arg_data['description'],"client_id":client_id}
                flag=DbModel.insert_Data("tasks",values)
                if flag:
                    return {"message": f"Task_{arg_data['title']} has been created successfully!"}, 201
                return jsonify({"status": 0, "message": "Task couldn't be created!"})
            return {'authenticated': '0', 'message': 'Invalid client.'}
        except Exception as err:
            print(err, '-- occurred while trying to create task')
            return {"status": 0, "message": "Something went wrong!"}
            
class Task_List(Resource):
    @staticmethod
    @jwt_required
    def get():
        """
        List of tasks ;
        
        """
        try:      
            # check for missing headers
            if not ('client_id'  in request.headers):
                return {'authenticated': '0', 'message': 'Missing required header.'}
            client_id = request.headers['client_id']
            res=Operation.validate_client_auth(client_id)
            if res:
                flag=DbModel.retrieve_data("tasks","*","client_id='"+client_id+"'","")
                if flag:
                    response = make_response(jsonify({'message': f"Task List of client_{client_id}", 'list': flag},200))
                    return response
                return jsonify({"status": 0, "message": "No task to show!"})
            return {'authenticated': '0', 'message': 'Invalid client.'}
        except Exception as err:
            print(err, '-- occurred while trying to show task details')
            return {"status": 0, "message": "Something went wrong!"}
            
class Edit_Task(Resource):
    @staticmethod
    @jwt_required
    def put():
        """
        Edit task ;
        
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True,help="title is required")
        parser.add_argument("description", type=str, required=True,help="description is required")
        parser.add_argument("task_id", type=str, required=True,help="task_id is required")
        arg_data = parser.parse_args()
        try:  
            # check for missing headers
            if not ('client_id'  in request.headers):
                return {'authenticated': '0', 'message': 'Missing required header.'}
            client_id = request.headers['client_id']
            res=Operation.validate_client_auth(client_id)
            if res:
                values={"title":arg_data['title'],"description":arg_data['description']}
                print(f"id={arg_data['task_id']}")
                flag=DbModel.update_data("tasks",values,f"id={arg_data['task_id']}")
                if flag:
                    return {"message": f"Task_{arg_data['title']} has been edited successfully!"}, 201
                return jsonify({"status": 0, "message": "Task couldn't be created!"})
            return {'authenticated': '0', 'message': 'Invalid client.'}
        except Exception as err:
            print(err, '-- occurred while trying to edit task')
            return {"status": 0, "message": "Something went wrong!"}

class Assign_Task(Resource):
    @staticmethod
    @jwt_required
    def put():
        """
        Manager assigns a task to employee;
        
        """
        parser = reqparse.RequestParser()
        parser.add_argument("employee_id", type=str, required=True,help="employee_id is required")
        parser.add_argument("task_id", type=str, required=True,help="task_id is required")
        arg_data = parser.parse_args()
        try:  
            # check for missing headers
            if not ('manager_id'  in request.headers):
                return {'authenticated': '0', 'message': 'Missing required header.'}
            manager_id = request.headers['manager_id']
            res=Operation.validate_manager_auth(manager_id)
            if res:
                now = datetime.now()
                current_date = now.strftime('%Y-%m-%d')
                values={
                        "task_id":arg_data['task_id'],
                        "manager_id":manager_id,
                        "status":"0",
                        "task_date":current_date
                        }
                flag=DbModel.update_data("employees",values,"employee_id='"+arg_data['employee_id']+"'")
                if flag:
                    return {"message": f"Task_{arg_data['task_id']} has been assigned to Employee_{arg_data['employee_id']} successfully!"}, 201
                return jsonify({"status": 0, "message": "Task couldn't be assigned!"})
            return {'authenticated': '0', 'message': 'Invalid manager.'}
        except Exception as err:
            print(err, '-- occurred while trying to assign task')
            return {"status": 0, "message": "Something went wrong!"}
            
class Delete_Task(Resource):
    @staticmethod
    @jwt_required
    def delete(task_id):
        """
        Manager delete a task ;
        
        """
        try:         
            # check for missing headers
            if not ('manager_id'  in request.headers):
                return {'authenticated': '0', 'message': 'Missing required header.'}
            manager_id = request.headers['manager_id']
            res=Operation.validate_manager_auth(manager_id)
            if res:
                flag=DbModel.delete("tasks","id='"+task_id+"'")
                if flag:
                    return {"message": f"Task_{task_id}  has been deleted successfully!"}, 201
                return jsonify({"status": 0, "message": "Task couldn't be deleted!"})
            return {'authenticated': '0', 'message': 'Invalid manager.'}
        except Exception as err:
            print(err, '-- occurred while trying to delete task')
            return {"status": 0, "message": "Something went wrong!"}
 
class Create_Employee(Resource):
    @staticmethod
    def post():
        """
        Creates a new Employee  to perform task;
        
        """
        parser = reqparse.RequestParser()
        parser.add_argument("employee_id", type=str, required=True,help="employee_id is required")
        parser.add_argument("password", type=str, required=True,help="password is required")
        arg_data = parser.parse_args()
        try:
            emp_data=DbModel.retrieve_data("employees","*","employee_id='"+arg_data['employee_id']+"'","")
            if len(emp_data)>0:
                return {"message": 'employee_id already exists!'}, 401
            password_hash = generate_password_hash(arg_data['password'])
            values={"employee_password":password_hash,"employee_id":arg_data['employee_id']}
            flag=DbModel.insert_Data("employees",values)
            if flag:
                return ({"message": f"Employee_{arg_data['employee_id']} created successfully"},200,)
                return {"message": 'Employee could not be created!'}, 401
        except Exception as err:
            print(err, '-- occurred while trying to create employee')
            return jsonify({"status": 0, "message": 'Something went wrong!'})

class Complete_Task(Resource):
    @staticmethod
    @jwt_required
    def put(task_id):
        """
        Complete  task;
        
        """
        try: 
            # check for missing headers
            if not ('employee_id'  in request.headers):
                return {'authenticated': '0', 'message': 'Missing required header.'}
            employee_id = request.headers['employee_id']
            res=Operation.validate_employee_auth(employee_id)
            if res:
                values={
                        "status":"1"
                        }
                flag=DbModel.update_data("tasks",values,"id='"+task_id+"'")
                if flag:
                    return {"message": f"Task_{task_id}  has been completed by Employee_{employee_id} successfully!"}, 201
                return jsonify({"status": 0, "message": "Task couldn't be completed!"})
            return {'authenticated': '0', 'message': 'Invalid employee.'}
        except Exception as err:
            print(err, '-- occurred while trying to complete task')
            return {"status": 0, "message": "Something went wrong!"}

class Logout(Resource):
    @classmethod
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200