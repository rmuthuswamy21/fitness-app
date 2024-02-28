from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import datetime

coach = Blueprint('coach', __name__)

@coach.route('/selects', methods=['GET'])
def get_selects():
    cursor = db.get_db().cursor()

    cursor.execute('SELECT id, last_name, first_name FROM coach')

    json_data = []

    theData = cursor.fetchall()

    first_name = 2
    last_name = 1
    id = 0

    for row in theData:
        label = row[first_name] + ' ' + row[last_name]
        json_data.append({
            'label': label,
            'value': row[id],
         })

    print(theData[0][0])

    return jsonify(json_data)


# Get all the products from the database
@coach.route('/coach', methods=['GET'])
def get_coach():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT id, last_name, first_name, began_coaching, joined FROM coach')

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

@coach.route('/coach', methods=['POST'])
def add_new_coach():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # extracting the variable
    began_coaching = the_data['began_coaching']
    began_coaching = datetime.datetime.strptime(began_coaching, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d %H:%M:%S')
    
    last_name  = the_data['last_name']
    first_name = the_data['first_name']

    # Constructing the query
    query = "insert into coach (began_coaching, joined, last_name, first_name) values ('"
    query += began_coaching + "', "
    query += "current_timestamp(), '"
    query += last_name + "', '"
    query += first_name + "')"
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@coach.route('/coach/<id>', methods=['GET'])
def get_coach_id (id):

    query = 'SELECT * FROM coach WHERE id = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


@coach.route('/coach/<id>', methods=['PUT'])
def update_coach(id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    # extracting the variable
    began_coaching = the_data['began_coaching']
    began_coaching = datetime.datetime.strptime(began_coaching, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d %H:%M:%S')
    last_name  = the_data['last_name']
    first_name = the_data['first_name']

    # Constructing the query
    the_query = "UPDATE coach SET "
    the_query += "began_coaching = '" + began_coaching + "', "
    the_query += "last_name = '" + last_name + "', "
    the_query += "first_name = '" + first_name + "' "
    the_query += f"WHERE id = {id}"

    current_app.logger.info(the_query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()
    
    return 'Success!'
    

@coach.route('/coach/<id>', methods=['DELETE'])
def delete_coach(id):   
    # Constructing the query
    query = '''
    DELETE FROM coach
    WHERE id = ''' + str(id)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Deleted Coach!'
    


@coach.route('/coach/<id>/athlete', methods=['GET'])
def get_coach_athletes(id):

    query = f"SELECT last_name, first_name, id FROM athlete WHERE coach_id = {str(id)}"
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)
  
  
# setting an athlete's coach
@coach.route('/coach/<coachID>/athlete', methods=['POST', 'PUT'])
def add_coachs_athlete(coachID):

    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    athleteID = the_data['athleteID']

    # Constructing the query
    the_query = "UPDATE athlete SET "
    the_query += "coach_id = '" + coachID + "' "
    the_query += f"WHERE id = {athleteID}"

    current_app.logger.info(the_query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()
    
    return 'Success!'

@coach.route('/coach/<coachID>/athlete', methods=['DELETE'])
def delete_coachs_athlete(coachID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    athleteID = the_data['athleteID']

    # Constructing the query
    the_query = "UPDATE athlete SET "
    the_query += "coach_id = null "
    the_query += f"WHERE id = {athleteID} AND coach_id = {coachID}"

    current_app.logger.info(the_query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()
    
    return 'Success!'

