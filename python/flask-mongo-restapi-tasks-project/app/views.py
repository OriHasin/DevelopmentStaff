from flask import Blueprint, request, jsonify
from .extensions import mongo

main = Blueprint("main", __name__)



def get_next_id():
    document = mongo.db.counters.find_one_and_update({"_id": "product_id"},
                                          {"$inc": {"sequence_value": 1}},
                                          return_document=True,
                                          upsert=True)

    return document["sequence_value"]

@main.route("/get", methods=["GET"])
def get_tasks():
    # Pagination for large data sets processing
    limit = int(request.args.get("limit", 10))
    page = int(request.args.get("page", 1))
    tasks = mongo.db.tasks.find().skip((page -1) * limit).limit(limit)

    tasks = list(tasks)
    for task in tasks:
        task["_id"] = str(task["_id"])

    return jsonify({"Your Tasks\n": list(tasks)}), 200


@main.route("/get/<id>", methods=["GET"])
def get_task_by_id(id):
    task = mongo.db.tasks.find_one_or_404({"id": id})
    task["_id"] = str(task["_id"])

    return jsonify({"Your Task:\n": task}), 200


@main.route("/add", methods=["POST"])
def add_task():
    data = request.json

    new_task = {"id": get_next_id(),
                "description": data["description"],
                "priority": data["priority"]}

    mongo.db.tasks.insert_one(new_task)
    new_task["_id"] = str(new_task["_id"])

    return jsonify({"Added Product Successfully!\n": new_task}), 201


@main.route("/update/<id>", methods=["PUT"])
def update_product_by_id(id):
    data = request.json
    result = mongo.db.tasks.update_one({"id": id}, {"$set": data})
    if result.updated_one:
        return f'Successfully update Product ID : {id}', 200
    return "Error in updating", 404


@main.route("/delete/<id>", methods=["DELETE"])
def delete_product_by_id(id):
    result = mongo.db.tasks.delete_one({"id": id})
    if result.deleted_one:
        return f'Successfully delete Product ID : {id}', 200
    return "Error in deleting", 404