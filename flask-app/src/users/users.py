from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import datetime

user = Blueprint('user', __name__)

# Get all the products from the database
@user.route('/user', methods=['GET'])
def get_user():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT id, weight, height, date_of_birth, joined, last_name, first_name, goal_weight FROM user')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@user.route('/user', methods=['POST'])
def add_new_user():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # extracting the variable
    weight = the_data['weight']
    height = the_data['height']
    date_of_birth = the_data['date_of_birth']
    date_of_birth = datetime.datetime.strptime(date_of_birth, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d %H:%M:%S')
    joined = the_data['joined']
    joined = datetime.datetime.strptime(joined, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d %H:%M:%S')
    last_name = the_data['last_name']
    first_name = the_data['first_name']
    goal_weight = the_data['goal_weight']

    # Constructing the query
    query = "insert into user (weight, height, date_of_birth, joined, last_name, first_name, goal_weight) values ('"
    query += weight + "', '"
    query += height + "', '"
    query += date_of_birth + "', '"
    query += joined + "', '"
    query += last_name + "', '"
    query += first_name + "', '"
    query += goal_weight + "');"    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@user.route('/user/<id>', methods=['GET'])
def get_user_id (id):

    query = 'SELECT * FROM user WHERE id = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

@user.route('/user/<userID>', methods=['PUT'])
def update_user(userID):
    the_data = request.json
    current_app.logger.info(the_data)
    
    # extracting the variable
    weight = the_data['weight']
    height = the_data['height']
    date_of_birth = the_data['date_of_birth']
    date_of_birth = datetime.datetime.strptime(date_of_birth, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d %H:%M:%S')
    joined = the_data['joined']
    joined = datetime.datetime.strptime(joined, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d %H:%M:%S')
    last_name  = the_data['last_name']
    first_name = the_data['first_name']
    goal_weight = the_data['goal_weight']
    

    # Constructing the query
    query = "UPDATE user SET "
    query += "weight = '" + weight + "', "
    query += "height = '" + height + "', "
    query += "date_of_birth = '" + date_of_birth + "', "
    query += "joined = '" + joined + "', "
    query += "last_name = '" + last_name + "', "
    query += "first_name = '" + first_name + "', "
    query += "goal_weight = '" + goal_weight + "' "
    query += f"WHERE id = {userID}"
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
    

@user.route('/user/<id>', methods=['DELETE'])
def delete_user(id):   
    query = 'delete from user where id = ' + str(id)
    
    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return "Successfully deleted user!"
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    