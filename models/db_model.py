# import required modules
import pymysql
from config.db_config import mysql


class DbModel(): 
    @staticmethod
    def retrieve_data(table_name, fields, where_condition, order):
        """fetch data from tables """
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if fields:
            fields_value = fields
        else:
            fields_value = '*'
        qs_select = 'SELECT ' + fields_value + ' FROM ' + table_name
        if where_condition:
            qs_select = qs_select + ' WHERE ' + where_condition
        if order:
            qs_select = qs_select + ' ORDER BY ' +  order
        try:
            cursor.execute(qs_select)
            rowcount = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            return rowcount
        except Exception as err:
            print(err, '-- occurred during fetching data')
            return False

    @staticmethod
    def insert_Data(table_name, values):
        """insert/add data into tables """
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cols = values.keys()
        vals = values.values()
        strComma = "','"
        newVals = "'" + strComma.join(vals) + "'"
        qs_insert = "INSERT INTO %s (%s) VALUES(%s)" % (table_name, ",".join(cols), "" + newVals)
        try:
            cursor.execute(qs_insert)
            conn.commit()
            last_insert_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return True
        except Exception as err:
            print(err, '-- occurred during adding data')
            return False

    @staticmethod
    def delete(table_name, where_condition):
        """delete data from tables """
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        qs_delete = 'DELETE FROM ' + table_name
        if where_condition:
            qs_delete = qs_delete + ' WHERE ' + where_condition
        try:
            cursor.execute(qs_delete)
            conn.commit()
            cursor.close()
            conn.close()
            message = "success"
            response = {"message_type": 'success', "message_text": message}
            return response
        except Exception as err:
            print(err, '-- occurred during deleting data')
            return False

    @staticmethod
    def update_data(table_name, values, where_condition):
        """fetch edit/update into tables """
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        all_data = ''
        for key in values:
            if all_data:
                all_data = all_data + ", " + key + " = '" + values[key] + "'"
            else:
                all_data = all_data + key + " = '" + values[key] + "'"
        qs_update = "UPDATE " + table_name + " SET " + all_data + " WHERE " + where_condition
        try:
            cursor.execute(qs_update)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as err:
            print(err, '-- occurred during editing data')
            return False

  

