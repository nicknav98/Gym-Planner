from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.workouts import Workout, workout_list


class WorkoutListResource(Resource):
    def get(self):
        data = []
        for workout in workout_list:
            if workout.is_publish is True:
                data.append(workout.data)
        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()
        workouts = Workout(name=data['name'],
                           length=data['length'],
                           directions=data['directions'],
                           type=data['type'],
                           )
        workout_list.append(workouts)
        return workouts.data, HTTPStatus.CREATED


class WorkoutResource(Resource):
    def get(self, workouts_id):
        workouts = next((workouts for workouts in workout_list if workouts.id == workouts_id and
                         workouts.is_publish == True), None)
        if workouts is None:
            return {'message': 'workouts not found'}, HTTPStatus.NOT_FOUND
        return workouts.data, HTTPStatus.OK

    def put(self, workouts_id):
        data = request.get_json()
        workouts = next((workouts for workouts in workout_list if workouts.id == workouts_id), None)
        if workouts is None:
            return {'message': 'workouts not found'}, HTTPStatus.NOT_FOUND
        workouts.name = data['name']
        workouts.length = data['length']
        workouts.directions = data['directions']
        workouts.type = data['type']
        return workouts.data, HTTPStatus.OK


class WorkoutPublishResource(Resource):
    def put(self, workout_id):
        workouts = next((workouts for workouts in workout_list if workout_id == workout_id), None)
        if workouts is None:
            return {'message': 'workouts not found'}, HTTPStatus.NOT_FOUND
        workouts.is_publish = True
        return {}, HTTPStatus.NO_CONTENT
