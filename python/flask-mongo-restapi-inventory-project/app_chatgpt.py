from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['inventory_db']
products_collection = db['products']

# GET all products
@app.route('/products', methods=['GET'])
def get_products():
    products = list(products_collection.find())
    for product in products:
        product['_id'] = str(product['_id'])  # Convert ObjectId to string
    return jsonify(products)

# GET a specific product
@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = products_collection.find_one({'_id': ObjectId(id)})
    if product:
        product['_id'] = str(product['_id'])
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

# POST a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = {
        'name': data['name'],
        'description': data['description'],
        'price': data['price'],
        'quantity': data['quantity']
    }
    result = products_collection.insert_one(new_product)
    new_product['_id'] = str(result.inserted_id)
    return jsonify(new_product), 201

# PUT update a product
@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    data = request.json
    updated_product = {
        'name': data['name'],
        'description': data['description'],
        'price': data['price'],
        'quantity': data['quantity']
    }
    result = products_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_product})
    if result.modified_count == 1:
        return jsonify({'message': 'Product updated'}), 200
    return jsonify({'error': 'Product not found or no changes made'}), 404

# DELETE a product
@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    result = products_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Product deleted'}), 200
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
