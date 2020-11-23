from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.workout import Workout, workout_list

class WorkoutListResource(Resource):

    def get(self):

        data=[]

        for workout in workout_list:
            if workout.is_publish is True:
                data.append(workout.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        workout = Workout(name=data['name'],
                          length=data['length'],
                          directions=data['directions'],
                          body_part=data['body_part'])

        workout_list.append(workout)

        return workout.data, HTTPStatus.CREATED

class WorkoutResource(Resource):

    def get(self, workout_id):
        workout = next((workout for workout in workout_list if workout_id == workout_id and workout.is_publish == True), None)

        if workout is None:
            return{'message': 'workout not found'}, HTTPStatus.NOT_FOUND

        return workout.data, HTTPStatus.OK

    def put(self, workout_id):
        data = request.get_json()

        workout = next((workout for workout in workout_list if workout_id == workout_id), None)

        if workout is None:
            return{'message': 'workout not found'}, HTTPStatus.NOT_FOUND

        workout.name = data['name']
        workout.length = data['length']
        workout.directions = data['directions']
        workout.body_part = data['body_part']

        return workout.data, HTTPStatus.OK

class WorkoutPublishResource(Resource):

    def put(self, workout_id):
        workout = next((workout for workout in workout_list if workout_id == workout_id), None)

        if workout is None:
            return {'message': 'workout not found'}, HTTPStatus.NOT_FOUND

        workout.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, workout_id):
        workout = next((workout for workout in workout_list if workout_id == workout_id), None)

        if workout is None:
            return {'message': 'workout not found'}, HTTPStatus.NOT_FOUND

        workout.is_publish = False

        return {}, HTTPStatus.NO_CONTENT


