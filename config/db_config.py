# import required modules
from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'task_management'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# initialize the MYSQL
mysql.init_app(app)