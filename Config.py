class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{your_name}:{your_password}@localhost/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
