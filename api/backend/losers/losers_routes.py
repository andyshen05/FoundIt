from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

losers = Blueprint('losers', __name__)


# GET all lost reports with filters
@losers.route('/lost-reports', methods=['GET'])
def get_all_lost_reports():
    cursor = db.get_db().cursor()
    
    # Get query parameters for filtering
    location_id = request.args.get('locationID')
    date_start = request.args.get('dateStart')
    date_end = request.args.get('dateEnd')
    user_id = request.args.get('userID')
    
    query = '''
        SELECT lr.lostReportID, lr.dateLost, lr.userID, lr.locationID,
               u.name as userName, u.email, u.phoneNumber,
               l.lastSeenAt as location
        FROM lost_item_report lr
        JOIN user u ON lr.userID = u.userID
        JOIN location l ON lr.locationID = l.locationID
        WHERE 1=1
    '''
    params = []
    
    if location_id:
        query += ' AND lr.locationID = %s'
        params.append(location_id)
    if date_start:
        query += ' AND lr.dateLost >= %s'
        params.append(date_start)
    if date_end:
        query += ' AND lr.dateLost <= %s'
        params.append(date_end)
    if user_id:
        query += ' AND lr.userID = %s'
        params.append(user_id)
    
    query += ' ORDER BY lr.dateLost DESC'
    
    current_app.logger.info(f'Executing query: {query} with params: {params}')
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST create a new lost report
@losers.route('/lost-reports', methods=['POST'])
def create_lost_report():
    data = request.json
    current_app.logger.info(f'Creating lost report: {data}')
    
    query = '''
        INSERT INTO lost_item_report (lostReportID, dateLost, userID, locationID)
        VALUES (%s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['lostReportID'], data['dateLost'], 
                          data['userID'], data['locationID']))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Lost report created successfully', 'id': data['lostReportID']}))
    response.status_code = 201
    return response

# GET a specific lost report
@losers.route('/lost-reports/<int:report_id>', methods=['GET'])
def get_lost_report(report_id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT lr.lostReportID, lr.dateLost, lr.userID, lr.locationID,
               u.name as userName, u.email, u.phoneNumber,
               l.lastSeenAt as location
        FROM lost_item_report lr
        JOIN user u ON lr.userID = u.userID
        JOIN location l ON lr.locationID = l.locationID
        WHERE lr.lostReportID = %s
    '''
    cursor.execute(query, (report_id,))
    data = cursor.fetchall()
    
    if not data:
        return jsonify({'error': 'Lost report not found'}), 404
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# PUT update a lost report
@losers.route('/lost-reports/<int:report_id>', methods=['PUT'])
def update_lost_report(report_id):
    data = request.json
    current_app.logger.info(f'Updating lost report {report_id}: {data}')
    
    query = '''
        UPDATE lost_item_report 
        SET dateLost = %s, locationID = %s
        WHERE lostReportID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['dateLost'], data['locationID'], report_id))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Lost report updated successfully'}))
    response.status_code = 200
    return response

# DELETE a lost report
@losers.route('/lost-reports/<int:report_id>', methods=['DELETE'])
def delete_lost_report(report_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM reward WHERE lostReportID = %s', (report_id,))
    cursor.execute('DELETE FROM lost_item_report WHERE lostReportID = %s', (report_id,))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Lost report deleted successfully'}))
    response.status_code = 200
    return response


# GET all rewards with filter by lostReportID
@losers.route('/rewards', methods=['GET'])
def get_all_rewards():
    cursor = db.get_db().cursor()
    
    lost_report_id = request.args.get('lostReportID')
    
    query = 'SELECT rewardID, rewardAmount, lostReportID FROM reward WHERE 1=1'
    params = []
    
    if lost_report_id:
        query += ' AND lostReportID = %s'
        params.append(lost_report_id)
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST create a reward
@losers.route('/rewards', methods=['POST'])
def create_reward():
    data = request.json
    current_app.logger.info(f'Creating reward: {data}')
    
    query = '''
        INSERT INTO reward (rewardID, rewardAmount, lostReportID)
        VALUES (%s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['rewardID'], data['rewardAmount'], data['lostReportID']))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Reward created successfully'}))
    response.status_code = 201
    return response

# GET a specific reward
@losers.route('/rewards/<int:reward_id>', methods=['GET'])
def get_reward(reward_id):
    cursor = db.get_db().cursor()
    query = 'SELECT rewardID, rewardAmount, lostReportID FROM reward WHERE rewardID = %s'
    cursor.execute(query, (reward_id,))
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# PUT update a reward
@losers.route('/rewards/<int:reward_id>', methods=['PUT'])
def update_reward(reward_id):
    data = request.json
    query = 'UPDATE reward SET rewardAmount = %s WHERE rewardID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['rewardAmount'], reward_id))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Reward updated successfully'}))
    response.status_code = 200
    return response

# DELETE a reward
@losers.route('/rewards/<int:reward_id>', methods=['DELETE'])
def delete_reward(reward_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM reward WHERE rewardID = %s', (reward_id,))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Reward deleted successfully'}))
    response.status_code = 200
    return response

# GET notifications for a user
@losers.route('/notifications/user/<int:user_id>', methods=['GET'])
def get_user_notifications(user_id):
    cursor = db.get_db().cursor()
    query = 'SELECT notificationID, message, userID FROM notification WHERE userID = %s ORDER BY notificationID DESC'
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST send a notification
@losers.route('/notifications', methods=['POST'])
def create_notification():
    data = request.json
    current_app.logger.info(f'Creating notification: {data}')
    
    query = 'INSERT INTO notification (notificationID, message, userID) VALUES (%s, %s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['notificationID'], data['message'], data['userID']))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Notification sent'}))
    response.status_code = 201
    return response

# DELETE a notification
@losers.route('/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM notification WHERE notificationID = %s', (notification_id,))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Notification deleted'}))
    response.status_code = 200
    return response


# GET all items with filters
@losers.route('/items', methods=['GET'])
def get_all_items():
    cursor = db.get_db().cursor()
    
    category_id = request.args.get('categoryID')
    status = request.args.get('status')
    date_start = request.args.get('dateStart')
    date_end = request.args.get('dateEnd')
    
    query = '''
        SELECT i.itemID, i.description, i.status, i.dateFound, i.daysInStorage,
               i.categoryID, c.categoryName
        FROM items i
        LEFT JOIN category c ON i.categoryID = c.categoryID
        WHERE 1=1
    '''
    params = []
    
    if category_id:
        query += ' AND i.categoryID = %s'
        params.append(category_id)
    if status:
        query += ' AND i.status = %s'
        params.append(status)
    if date_start:
        query += ' AND i.dateFound >= %s'
        params.append(date_start)
    if date_end:
        query += ' AND i.dateFound <= %s'
        params.append(date_end)
    
    query += ' ORDER BY i.dateFound DESC'
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# GET categories
@losers.route('/categories', methods=['GET'])
def get_categories():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT categoryID, categoryName FROM category ORDER BY categoryName')
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# GET locations
@losers.route('/locations', methods=['GET'])
def get_locations():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT locationID, lastSeenAt FROM location ORDER BY lastSeenAt')
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response