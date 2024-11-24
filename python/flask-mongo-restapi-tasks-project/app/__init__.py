from flask import Flask, jsonify, request
from .extensions import mongo
from .views import main
def create_app(config_object):

    app = Flask(__name__)
    app.config.from_object(config_object)

    mongo.init_app(app)
    app.register_blueprint(main)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"Message" : "Resource Not Found!"}), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        message = {"Message": "An Error Occurred!",
                   "Error": str(error)}
        return jsonify(message), 500


    @app.before_request
    def before_request():
        print(f'Request arrived from ip: {request.remote_addr}, method: {request.method}, path: {request.path}')

    @app.after_request
    def after_request(response):
        print(f'Responding to request: {request.method} {request.path} with status code: {response.status_code}')
        return response

    return app