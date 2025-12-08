from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

desk = Blueprint('desk', __name__)

# GET all users with optional filters
@desk.route('/users', methods=['GET'])
def get_all_users():
    cursor = db.get_db().cursor()
    
    acc_status = request.args.get('accStatus')
    name = request.args.get('name')
    
    query = 'SELECT userID, name, email, phoneNumber, accStatus FROM user WHERE 1=1'
    params = []
    
    if acc_status:
        query += ' AND accStatus = %s'
        params.append(acc_status)
    if name:
        query += ' AND name LIKE %s'
        params.append(f'%{name}%')
    
    query += ' ORDER BY name'
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST create a user
@desk.route('/users', methods=['POST'])
def create_user():
    data = request.json
    current_app.logger.info(f'Creating user: {data}')
    
    query = 'INSERT INTO user (userID, name, email, phoneNumber, accStatus) VALUES (%s, %s, %s, %s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['userID'], data['name'], data['email'], 
                          data['phoneNumber'], data.get('accStatus', 'active')))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'User created', 'id': data['userID']}))
    response.status_code = 201
    return response

# GET a specific user
@desk.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = db.get_db().cursor()
    query = 'SELECT userID, name, email, phoneNumber, accStatus FROM user WHERE userID = %s'
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    
    if not data:
        return jsonify({'error': 'User not found'}), 404
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# PUT update a user
@desk.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    current_app.logger.info(f'Updating user {user_id}: {data}')
    
    query = 'UPDATE user SET accStatus = %s WHERE userID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['accStatus'], user_id))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'User updated'}))
    response.status_code = 200
    return response

# DELETE a user
@desk.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM notification WHERE userID = %s', (user_id,))
    cursor.execute('DELETE FROM reward WHERE lostReportID IN (SELECT lostReportID FROM lost_item_report WHERE userID = %s)', (user_id,))
    cursor.execute('DELETE FROM lost_item_report WHERE userID = %s', (user_id,))
    cursor.execute('DELETE FROM found_item_report WHERE userID = %s', (user_id,))
    cursor.execute('DELETE FROM user WHERE userID = %s', (user_id,))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'User deleted'}))
    response.status_code = 200
    return response


# GET all inventory with filters
@desk.route('/inventory', methods=['GET'])
def get_all_inventory():
    cursor = db.get_db().cursor()
    
    manager_id = request.args.get('managerID')
    storage_location_id = request.args.get('storageLocationID')
    days_min = request.args.get('daysMin')
    
    query = '''
        SELECT fi.inventoryID, fi.dateReceived, fi.managerID, fi.itemID, fi.storageLocationID,
               i.description, i.status, i.daysInStorage,
               sl.shelfNumber,
               dm.name as managerName
        FROM found_item_inventory fi
        JOIN items i ON fi.itemID = i.itemID
        JOIN storage_location sl ON fi.storageLocationID = sl.storageLocationID
        JOIN desk_manager dm ON fi.managerID = dm.managerID
        WHERE 1=1
    '''
    params = []
    
    if manager_id:
        query += ' AND fi.managerID = %s'
        params.append(manager_id)
    if storage_location_id:
        query += ' AND fi.storageLocationID = %s'
        params.append(storage_location_id)
    if days_min:
        query += ' AND i.daysInStorage >= %s'
        params.append(days_min)
    
    query += ' ORDER BY fi.dateReceived DESC'
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST add to inventory
@desk.route('/inventory', methods=['POST'])
def create_inventory():
    data = request.json
    current_app.logger.info(f'Creating inventory record: {data}')
    
    query = '''
        INSERT INTO found_item_inventory (inventoryID, dateReceived, managerID, itemID, storageLocationID)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['inventoryID'], data['dateReceived'], data['managerID'],
                          data['itemID'], data['storageLocationID']))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Inventory record created'}))
    response.status_code = 201
    return response

# GET specific inventory item
@desk.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT fi.inventoryID, fi.dateReceived, fi.managerID, fi.itemID, fi.storageLocationID,
               i.description, i.status, i.daysInStorage,
               sl.shelfNumber,
               dm.name as managerName
        FROM found_item_inventory fi
        JOIN items i ON fi.itemID = i.itemID
        JOIN storage_location sl ON fi.storageLocationID = sl.storageLocationID
        JOIN desk_manager dm ON fi.managerID = dm.managerID
        WHERE fi.inventoryID = %s
    '''
    cursor.execute(query, (inventory_id,))
    data = cursor.fetchall()
    
    if not data:
        return jsonify({'error': 'Inventory item not found'}), 404
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# PUT update inventory location
@desk.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    data = request.json
    current_app.logger.info(f'Updating inventory {inventory_id}: {data}')
    
    query = 'UPDATE found_item_inventory SET storageLocationID = %s WHERE inventoryID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['storageLocationID'], inventory_id))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Inventory updated'}))
    response.status_code = 200
    return response

# DELETE from inventory
@desk.route('/inventory/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM found_item_inventory WHERE inventoryID = %s', (inventory_id,))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Inventory record deleted'}))
    response.status_code = 200
    return response


# GET all claims with filters
@desk.route('/claims', methods=['GET'])
def get_all_claims():
    cursor = db.get_db().cursor()
    
    manager_id = request.args.get('managerID')
    date_start = request.args.get('dateStart')
    date_end = request.args.get('dateEnd')
    
    query = '''
        SELECT cr.claimID, cr.claimDate, cr.claimerEmail, cr.itemID, cr.managerID,
               i.description as itemDescription,
               dm.name as managerName
        FROM claim_record cr
        JOIN items i ON cr.itemID = i.itemID
        JOIN desk_manager dm ON cr.managerID = dm.managerID
        WHERE 1=1
    '''
    params = []
    
    if manager_id:
        query += ' AND cr.managerID = %s'
        params.append(manager_id)
    if date_start:
        query += ' AND cr.claimDate >= %s'
        params.append(date_start)
    if date_end:
        query += ' AND cr.claimDate <= %s'
        params.append(date_end)
    
    query += ' ORDER BY cr.claimDate DESC'
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST create a claim
@desk.route('/claims', methods=['POST'])
def create_claim():
    data = request.json
    current_app.logger.info(f'Creating claim: {data}')
    
    query = '''
        INSERT INTO claim_record (claimID, claimDate, claimerEmail, itemID, managerID)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['claimID'], data['claimDate'], data['claimerEmail'],
                          data['itemID'], data['managerID']))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Claim created'}))
    response.status_code = 201
    return response

# GET specific claim
@desk.route('/claims/<int:claim_id>', methods=['GET'])
def get_claim(claim_id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT cr.claimID, cr.claimDate, cr.claimerEmail, cr.itemID, cr.managerID,
               i.description as itemDescription,
               dm.name as managerName
        FROM claim_record cr
        JOIN items i ON cr.itemID = i.itemID
        JOIN desk_manager dm ON cr.managerID = dm.managerID
        WHERE cr.claimID = %s
    '''
    cursor.execute(query, (claim_id,))
    data = cursor.fetchall()
    
    if not data:
        return jsonify({'error': 'Claim not found'}), 404
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# GET all items with filters
@desk.route('/items', methods=['GET'])
def get_all_items():
    cursor = db.get_db().cursor()
    
    category_id = request.args.get('categoryID')
    status = request.args.get('status')
    days_min = request.args.get('daysMin')
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
    if days_min:
        query += ' AND i.daysInStorage >= %s'
        params.append(days_min)
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

# GET specific item
@desk.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT i.itemID, i.description, i.status, i.dateFound, i.daysInStorage,
               i.categoryID, c.categoryName
        FROM items i
        LEFT JOIN category c ON i.categoryID = c.categoryID
        WHERE i.itemID = %s
    '''
    cursor.execute(query, (item_id,))
    data = cursor.fetchall()
    
    if not data:
        return jsonify({'error': 'Item not found'}), 404
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# PUT update item status
@desk.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    current_app.logger.info(f'Updating item {item_id}: {data}')
    
    query = 'UPDATE items SET status = %s WHERE itemID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['status'], item_id))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Item updated'}))
    response.status_code = 200
    return response

# DELETE item
@desk.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM found_item_report WHERE itemID = %s', (item_id,))
    cursor.execute('DELETE FROM found_item_inventory WHERE itemID = %s', (item_id,))
    cursor.execute('DELETE FROM claim_record WHERE itemID = %s', (item_id,))
    cursor.execute('DELETE FROM items WHERE itemID = %s', (item_id,))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Item deleted'}))
    response.status_code = 200
    return response


# GET all found reports with filters
@desk.route('/found-reports', methods=['GET'])
def get_all_found_reports():
    cursor = db.get_db().cursor()
    
    location_id = request.args.get('locationID')
    user_id = request.args.get('userID')
    date_start = request.args.get('dateStart')
    date_end = request.args.get('dateEnd')
    
    query = '''
        SELECT fr.foundReportID, fr.dateFound, fr.`condition`, fr.userID, 
               fr.locationID, fr.itemID,
               u.name as finderName, u.email, u.phoneNumber,
               l.lastSeenAt as location,
               i.description as itemDescription
        FROM found_item_report fr
        JOIN user u ON fr.userID = u.userID
        JOIN location l ON fr.locationID = l.locationID
        JOIN items i ON fr.itemID = i.itemID
        WHERE 1=1
    '''
    params = []
    
    if location_id:
        query += ' AND fr.locationID = %s'
        params.append(location_id)
    if user_id:
        query += ' AND fr.userID = %s'
        params.append(user_id)
    if date_start:
        query += ' AND fr.dateFound >= %s'
        params.append(date_start)
    if date_end:
        query += ' AND fr.dateFound <= %s'
        params.append(date_end)
    
    query += ' ORDER BY fr.dateFound DESC'
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# GET specific found report
@desk.route('/found-reports/<int:report_id>', methods=['GET'])
def get_found_report(report_id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT fr.foundReportID, fr.dateFound, fr.`condition`, fr.userID, 
               fr.locationID, fr.itemID,
               u.name as finderName, u.email, u.phoneNumber,
               l.lastSeenAt as location,
               i.description as itemDescription
        FROM found_item_report fr
        JOIN user u ON fr.userID = u.userID
        JOIN location l ON fr.locationID = l.locationID
        JOIN items i ON fr.itemID = i.itemID
        WHERE fr.foundReportID = %s
    '''
    cursor.execute(query, (report_id,))
    data = cursor.fetchall()
    
    if not data:
        return jsonify({'error': 'Found report not found'}), 404
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# GET all lost reports with filters
@desk.route('/lost-reports', methods=['GET'])
def get_all_lost_reports():
    cursor = db.get_db().cursor()
    
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
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# GET all storage locations
@desk.route('/storage-locations', methods=['GET'])
def get_storage_locations():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT storageLocationID, shelfNumber FROM storage_location ORDER BY shelfNumber')
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# GET all managers
@desk.route('/managers', methods=['GET'])
def get_all_managers():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT managerID, name, phoneNumber, email FROM desk_manager ORDER BY name')
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# GET specific manager
@desk.route('/managers/<int:manager_id>', methods=['GET'])
def get_manager(manager_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT managerID, name, phoneNumber, email FROM desk_manager WHERE managerID = %s', (manager_id,))
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# GET all categories
@desk.route('/categories', methods=['GET'])
def get_categories():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT categoryID, categoryName FROM category ORDER BY categoryName')
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# GET all locations
@desk.route('/locations', methods=['GET'])
def get_locations():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT locationID, lastSeenAt FROM location ORDER BY lastSeenAt')
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    return response