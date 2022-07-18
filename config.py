import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__)) #to get root directory folder
load_dotenv(os.path.join(basedir, '.env')) #load .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') #read .env file and get SECRET_KEY variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db') #database connection
    SQLALCHEMY_TRACK_MODIFICATIONS = False