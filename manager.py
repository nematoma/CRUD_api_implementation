from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__, template_folder='.')

client = MongoClient('mongodb://localhost:27017/')
db = client['api_manager']
apis_collection = db['apis']

@app.route('/')
def index():
    return render_template('interface.html')

@app.route('/apis', methods=['GET'])
def list_apis():
    apis = list(apis_collection.find())
    for api in apis:
        api['_id'] = str(api['_id'])  # Convert ObjectId to string
    return jsonify({'apis': apis})
@app.route('/apis.html')
def apis_page():
    return render_template('apis.html')

@app.route('/api', methods=['POST'])
def create_api():
    data = request.json
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid data format'}), 400
    
    api_id = apis_collection.insert_one(data).inserted_id
    return jsonify({'id': str(api_id), 'message': 'data created successfully'}), 201

@app.route('/update')
def update_api_form():
    return render_template('update.html')

@app.route('/api/<string:api_id>', methods=['PUT'])
def update_api(api_id):
    data = request.json
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid data format'}), 400
    
    result = apis_collection.update_one(
        {'_id': ObjectId(api_id)},
        {'$set': {
            'name': data['name'],
            'description': data['description']
        }}
    )
    
    if result.modified_count > 0:
        return jsonify({'message': 'data updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update data'}), 500

@app.route('/delete')
def delete_api_form():
    return render_template('delete.html')

@app.route('/api/<string:api_id>', methods=['DELETE'])
def delete_api(api_id):
    try:
        result = apis_collection.delete_one({'_id': ObjectId(api_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'data deleted successfully'}), 200
        else:
            return jsonify({'error': 'data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

