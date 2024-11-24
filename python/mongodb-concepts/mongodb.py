""" MongoDB core advanced concepts """

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client["my_custom_db_name"]
collection = db["my_custom_collection_name"]


""" Optimizing DB queries """

""" Indexes in MongoDB allow efficient querying by storing references to documents sorted by the indexed fields. 
Instead of scanning every document (collection scan) in each find() operation in O(n) time. 
MongoDB uses the index to quickly locate documents that match the query criteria in O(log n) by traversing a balanced tree which is sorted.
Internally, MongoDB uses B-trees to store and maintain these indexes, MongoDB traverses the B-tree to find the matching entries and then uses the pointers to fetch the relevant documents.
Keeping them balanced for optimal search, insert, and delete operations, that's why we need to manage them carefully with respect to write operations."""


collection.create_index(["myfield", 1])             # 1 for ascending order

collection.find({ "field": "value" }).explain()     # return a document that provides detailed information about how the database processes a query.
                                                    # including execution time, indexes used, stage of the query (collection scan, etc..). this will help us to understand how to optimize queries.

collection.find({}, {"field1": 1, "field2": 1})     # Projection, fetch necessary data, _id is always 1 by default.

collection.find().skip(10).limit(10)                # Pagination, is the process of dividing a large set of results into smaller, manageable chunks (pages), we will navigate each page sequentally.
def get_items_paginated():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    items = mongo.db.items.find().skip((page - 1) * limit).limit(limit)
    return jsonify([item for item in items]), 200



""" Aggregation Functions """

""" Aggregation Pipeline: A series of stages that transform and process documents. Each stage takes input from the 
 previous one, and the output of the last stage is the result.
 Stages:

$match: Filters documents by a condition (similar to find()).
$group: Groups documents by a specific field and allows performing operations like sum, avg, count.
$sort: Sorts documents based on a field.
$project: Reshapes documents to include or exclude fields, add computed fields.
$limit and $skip: Control pagination.
$lookup: Performs a join operation across collections. 

"""

result = collection.aggregate([
    {"$match": {"status": "active" } },               # Stage 1: Filter documents by status
    {"$group":
          {"_id": "$category",                         # Stage 2: Group by the 'category' field which the "_id" field will be their key.
           "total": {"$sum": 1 } } },                 # Create a 'total' field that counts each document
    {"$sort": {"total": -1 } }                        # Stage 3: Sort by count
])
