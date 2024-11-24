from flask import Flask, request, jsonify
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce"
mongo = PyMongo(app)
products_counter = 0
projection = {'_id': 0, 'id': 1, 'name': 1, 'description': 1, 'price': 1, 'quantity': 1}


@app.route('/products')
def get_products():
    products_collection = mongo.db.products.find({}, projection)
    return list(products_collection)


@app.get('/products/<int:id>')
def get_products_by_id(id):
    products_collection = mongo.db.products.find_one_or_404({'id': id}, projection)
    return jsonify(products_collection)


@app.post('/products')
def add_product():
    global products_counter
    data = request.json
    products_counter += 1
    data["id"] = products_counter

    mongo.db.products.insert_one(data)
    return f"Added products successfully! \n product: {data}"

@app.put("/products/<int:id>")
def update_product(id):
    data = request.json
    document = mongo.db.products.update_one({'id' : id}, {'$set': data})
    return ""


@app.delete("/products/<int:id>")
def delete_product(id):
    mongo.db.products.delete_one({'id' : id})
    return ""



if __name__ == '__main__':
    app.run(debug=True)