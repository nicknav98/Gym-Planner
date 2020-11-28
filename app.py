from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from Config import Config
from extensions import db
from models.user import User
from resources.workout import WorkoutListResource, WorkoutResource, WorkoutPublishResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    api = Api(app)

    api.add_resource(WorkoutListResource, '/workouts')
    api.add_resource(WorkoutResource, '/workouts/<int:workout_id>')
    api.add_resource(WorkoutPublishResource, '/workouts/<int:workout_id>/publish')

if __name__ == '__main__':
    app = create_app()
    app.run(port=6000, debug=True)
