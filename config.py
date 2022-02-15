import os


base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
	APP_URL = 'https://stv-telegram-bot.herokuapp.com/'
	TBOT_TOKEN = '5204604334:AAFql520pwgmjFoZqNuxUGUn-WFBBUL9b7c'

	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'STV_trafo.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
