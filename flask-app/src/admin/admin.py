from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import flask


admin = Blueprint('admin', __name__)

# Returns a list of all admin with last name, first name, and id attributes
@admin.route('/admin', methods=['GET', 'POST'])
def get_all_admin():
    if flask.request.method == 'GET':
        cursor = db.get_db().cursor()
        query = '''
            SELECT id, first, last, admin_perms FROM admin
        '''
        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))
        the_response = make_response(jsonify(json_data))
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
        return the_response
    elif flask.request.method == 'POST':
        # collecting data from the request object 
        the_data = request.json
        current_app.logger.info(the_data)

        '''
            CREATE TABLE admin (
                first varchar(40),
                last varchar(40),
                email varchar(50) NOT NULL,
                admin_perms CHAR,
                id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL
            );
        '''
        #extracting the variable
        first = the_data['first']
        last = the_data['last']
        email = the_data['email']
        admin_perms = the_data['admin_perms']

        # Constructing the query
        query = "insert into admin (first, last, email, admin_perms) values ('"
        query += first + "', '"
        query += last + "', '"
        query += email + "', '"
        query += admin_perms + "')"
        current_app.logger.info(query)

        # executing and committing the insert statement 
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        
        return 'Success!'

# Get customer detail for customer with particular userID
@admin.route('/admin/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_admin_by_id(id):
    if flask.request.method == 'GET':
        cursor = db.get_db().cursor()
        cursor.execute('select * from admin where id = {0}'.format(id))
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))
        the_response = make_response(jsonify(json_data))
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
        return the_response
    elif flask.request.method == 'PUT':
        the_data = request.json
        current_app.logger.info(the_data)
        
        # extracting the variable
        first = the_data['first']
        last = the_data['last']
        email = the_data['email']
        admin_perms = the_data['admin_perms']
        

        # Constructing the query
        query = "UPDATE admin SET "
        query += "first = '" + first + "', "
        query += "last = '" + last + "', "
        query += "email = '" + email + "', "
        query += "admin_perms = '" + admin_perms + "' "
        query += f"WHERE id = {id}"
        current_app.logger.info(query)

        # executing and committing the insert statement 
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        
        return 'Success!'
    elif flask.request.method == 'DELETE':
        # Constructing the query
        query = '''
        DELETE FROM admin
        WHERE id = ''' + str(id)


        # executing and committing the insert statement 
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        return 'Deleted Admin!'