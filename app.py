from flask import Flask
from flask_restful import Api

from resources.workout import WorkoutListResource, WorkoutResource, WorkoutPublishResource

app = Flask(__name__)
api = Api(app)

api.add_resource(WorkoutListResource, '/workouts')
api.add_resource(WorkoutResource, '/workouts/<int:workout_id>')
api.add_resource(WorkoutPublishResource, '/workouts/<int:workout_id>/publish')

if __name__ == '__main__':
    app.run(port=6000, debug=True)
