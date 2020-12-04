from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.workout import Workout


class WorkoutListResource(Resource):

    def get(self):
        workouts = Workout.get_all_published()
        data = []

        for workout in workouts:
            data.append(workout.data)

        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()

        workout = Workout(name=json_data['name'],
                          length=json_data['length'],
                          directions=json_data['directions'],
                          body_part=json_data['body_part'],
                          user_id=current_user)

        workout.save()

        return workout.data(), HTTPStatus.CREATED


class WorkoutResource(Resource):
    @jwt_optional
    def get(self, workout_id):
        workout = Workout.get_by_id(workout_id=workout_id)

        if workout is None:
            return {'message': 'workout not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if workout.is_publish == False and workout_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return workout.data(), HTTPStatus.OK

    @jwt_required
    def put(self, workout_id):
        json_data = request.get_json()

        workout = Workout.get_by_id(workout_id=workout_id)
        if workout is None:
            return {'message': 'workout not found'}, HTTPStatus.NOT_FOUND

        workout.name = json_data['name']
        workout.length = json_data['length']
        workout.directions = json_data['directions']
        workout.body_part = json_data['body_part']

        workout.save()

        return workout.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, workout_id):
        workout = Workout.get_by_id(workout_id=workout_id)

        if workout is None:
            return {'message': 'Workout not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != workout.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        workout.delete()

        return {}, HTTPStatus.NO_CONTENT


class WorkoutPublishResource(Resource):
    @jwt_required
    def put(self, workout_id):

        workout = Workout.get_by_id(workout_id=workout_id)

        if workout is None:
            return {'message': 'Workout not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != workout.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        workout.is_publish = True
        workout.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, workout_id):

        workout = Workout.get_by_id(workout_id=workout_id)

        if workout is None:
            return {'message': 'Workout not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != workout.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        workout.is_publish = False
        workout.save()


