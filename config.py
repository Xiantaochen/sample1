#encoding:utf-8
import os

DEBUG = True

SECRET_KEY  =  os.urandom(24)

HOSTNAME = "127.0.0.1"
PORT = '3306'
DATABASE = 'zlktqa_demo'
USERNAME = 'root'
PASSWORD = "302811"
DB_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False