# import required modules
import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",password="")


show_db="SHOW DATABASES LIKE 'task_management' "

db="task_management"
create_db="CREATE DATABASE " f"{db}"
use_db="USE " f"{db}"

"""create table employees """
create_employee="CREATE TABLE `employees` (`id` int(11)  PRIMARY KEY  NOT NULL AUTO_INCREMENT,`employee_id` varchar(20) NOT NULL,`employee_password` text NOT NULL,`manager_id` int(11) DEFAULT NULL,`task_id` int(11) DEFAULT NULL,`status` tinyint(1) DEFAULT NULL COMMENT '0-pending,1-complete',`task_date` date DEFAULT NULL)"

"""create table clients """
create_client="CREATE TABLE `clients` (`id` int(11) PRIMARY KEY  NOT NULL AUTO_INCREMENT,`client_id` varchar(20) NOT NULL,`client_password` text NOT NULL,`date` datetime NOT NULL DEFAULT current_timestamp())"

"""create table managers """ 
create_manager="CREATE TABLE `managers` (`id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,`manager_id` int(20) NOT NULL,`manager_password` text NOT NULL,`department` varchar(20) NOT NULL,`date` date NOT NULL DEFAULT current_timestamp())"

"""create table tasks """
create_task="CREATE TABLE `tasks` (`id` int(11) PRIMARY KEY  NOT NULL AUTO_INCREMENT,`title` varchar(20) NOT NULL,`description` varchar(50) NOT NULL,`client_id` varchar(20) NOT NULL,`task_date` date NOT NULL DEFAULT current_timestamp(),`status` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'pending-0,complete-1')"
     
class Create_DataBase():
    @staticmethod
    def tables(show_db,create_db,create_employee,create_client):
        """create Databse """
        cursor = mydb.cursor()
        try:
            cursor.execute(show_db)
            rowcount = cursor.fetchall()
            mydb.commit()
            if len(rowcount)==0:
                cursor.execute(create_db)
                cursor.execute(use_db)
                cursor.execute(create_employee)
                cursor.execute(create_client)
                cursor.execute(create_manager)
                cursor.execute(create_task)
                mydb.commit()
                cursor.close()
            cursor.close()
            return True
        except Exception as err:
            print(err, "-- occurred during creating database_" f"{db}")
            return False

Create_DataBase.tables(show_db,create_db,create_employee,create_client)   
