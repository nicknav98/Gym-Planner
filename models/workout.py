from extensions import db

workout_list = []

def get_last_id():
    if workout_list:
        last_workout = workout_list[-1]
    else:
        return 1
    return last_workout.id + 1

class Workout:
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    length = db.Column(db.String(200))
    directions = db.Column(db.String(200))
    body_part = db.Column(db.String(200))
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default = db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default = db.func.now(), onupdate = db.func.now())

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))