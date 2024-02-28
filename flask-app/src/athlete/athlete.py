from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import datetime

athlete = Blueprint('athlete', __name__)

# Get all customers from the DB
@athlete.route('/athlete', methods=['GET'])
def get_athlete():
    print("got here")
    cursor = db.get_db().cursor()
    cursor.execute('''select id, first_name, last_name, date_of_birth, joined,
                   goal_weight, weight, height, coach_id from athlete''')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
        print(str(row))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all customers from the DB
@athlete.route('/athlete', methods=['POST'])
def create_athlete():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    weight = the_data['weight']
    height = the_data['height']
    date_of_birth = the_data['date_of_birth']
    date_of_birth = datetime.datetime.strptime(date_of_birth, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d %H:%M:%S')
    last_name = the_data['last_name']
    first_name = the_data['first_name']
    goal_weight = the_data['goal_weight']
    coach_id = the_data['coach_id']

    
    # Constructing the query
    query = "insert into athlete (weight, height, date_of_birth, joined, last_name, first_name, goal_weight, coach_id) values ('"
    query += weight + "', '"
    query += height + "', '"
    query += date_of_birth + "', "
    query += "CURRENT_TIMESTAMP, " 
    query += "'" + last_name + "', '"
    query += first_name + "', '"
    query += goal_weight + "', '"
    query += str(coach_id) + "');"

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Added athlete!'



###########################################################

# Get customer detail for customer with particular userID
@athlete.route('/athlete/<id>', methods=['GET'])
def get_athlete_id(id):
    cursor = db.get_db().cursor()
    cursor.execute('select * from athlete where id = {0}'.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@athlete.route('/athlete/<id>', methods=['DELETE'])
def delete_athlete(id):

    # Constructing the query
    query = '''
    DELETE FROM athlete
    WHERE id = ''' + str(id)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Deleted Athlete!'

# Changes size, price, sugar level, and/or ice level of a drink in a given order
@athlete.route('/athlete/<id>', methods=['PUT'])
def update_athlete(id):
    the_data = request.json

    weight = the_data['weight']
    height = the_data['height']
    date_of_birth = the_data['date_of_birth']
    date_of_birth = datetime.datetime.strptime(date_of_birth, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d %H:%M:%S')
    last_name = the_data['last_name']
    first_name = the_data['first_name']
    goal_weight = the_data['goal_weight']
    coach_id = the_data['coach_id']

    current_app.logger.info(the_data)
    
    the_query = 'UPDATE athlete SET '
    the_query += "weight = '" + str(weight) + "', "
    the_query += "height = '" + str(height) + "', "
    the_query += "date_of_birth = '" + str(date_of_birth) + "', "
    the_query += "last_name = '" + last_name + "', "
    the_query += "first_name = '" + first_name + "', "
    the_query += "goal_weight = '" + str(goal_weight) + "', "
    the_query += "coach_id = '" + str(coach_id) + "' "
    the_query += "WHERE id = {0};".format(id)

    current_app.logger.info(the_query)
    
    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    return "Updated athlete!"

###########################################################

@athlete.route('/athlete/<id>/friends', methods=['GET'])
def get_athlete_friends(id):
    query = '''
    SELECT a.last_name, a.first_name, a.id
    FROM athlete a
    JOIN friends f ON a.id = f.athlete_id_1 OR a.id = f.athlete_id_2
    WHERE (f.athlete_id_1 = {0} OR f.athlete_id_2 = {0}) AND a.id != {0}'''.format(id)

    cursor = db.get_db().cursor()
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


@athlete.route('/athlete/<id>/friends', methods=['POST'])
def create_athlete_friend(id):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    athlete_id_2 = the_data['athlete_id_2']


    # Constructing the query
    query = 'insert into friends (athlete_id_1, athlete_id_2) values ("'
    query += str(id) + '", "'
    query += athlete_id_2 + '");'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'added friends for id {0}!'.format(id)


@athlete.route('/athlete/<id>/friends', methods=['DELETE'])
def delete_athlete_friend(id):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    athlete_id_2 = the_data['athlete_id_2']

    # Constructing the query
    query = f'delete from friends where athlete_id_1 = {id} AND athlete_id_2 = {athlete_id_2}'
    # query += str(id) + '", "'
    # query += athlete_id_2 + '");'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    # Constructing the query
    query = f'delete from friends where athlete_id_1 = {athlete_id_2} AND athlete_id_2 = {id}'
    # query += str(id) + '", "'
    # query += athlete_id_2 + '");'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return f'Deleted friend {athlete_id_2} for athlete {id}!'
