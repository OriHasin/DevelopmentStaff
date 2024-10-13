from pymongo import MongoClient
from flask import Flask, request
from datetime import datetime, timedelta

app = Flask(__name__)
collection = None


def get_top_spenders(last_n_days=30, limit=10):
    global collection
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["commerce"]
    collection = db["products"]

    # Calculate the date 30 days ago from today
    thirty_days_ago = datetime.now() - timedelta(days=last_n_days)

    # Define the aggregation pipeline
    pipeline = [
        {
            "$match": {  # all the document from the previous 30 days
                "timestamp": {"$gte": thirty_days_ago}
            }
        },
        {
            "$group": {  # group all the document and perform aggregation with sum total amount per user
                "_id": "$user_id",
                "total_amount": {"$sum": "$amount"}
            }
        },
        {
            "$sort": {"total_amount": -1}  # sort the total_amount on descending order
        },
        {
            "$limit": limit  # limit to retrieve the largest 10 results
        }
    ]

    # Execute the aggregation pipeline
    results = collection.aggregate(pipeline)
    return results


def add_products():
    data = request.json
    new_data = {'user_id': data["user_id"],
                'product_id': data["product_id"],
                'amount': data['amount'],
                'timestamp': datetime.strptime(data['timestamp'], '%Y-%m-%d')}

    result = collection.insert_one(new_data)

    if result.inserted_id:
        return "Inserted data successfully!", 200
    return "Error while insert data", 500




if __name__ == '__main__':
    app.add_url_rule('/add', 'add_products', add_products, methods=['POST'])
    # app.run(debug=True)                   # run that to add new data into MongoDB

    results = get_top_spenders()
    for document in results:
        print(document)
