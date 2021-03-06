__author__ = 'github/tuliocg'

import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#from app import config
from config import config

enviroment = os.environ.get('APP_SETTINGS')
print(enviroment)

app = Flask(__name__)
app.config.from_object(config[enviroment])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
from models import ISS

def insert_iss_position():
    ltd, lng = ISS.get_wheres_iss()
    location_info = ISS.revert_geocode(ltd, lng)
    utc_timestamp = datetime.utcnow()
    utc_date = utc_timestamp.strftime('%Y-%m-%d')
    config = {
        'utc_timestamp': utc_timestamp,
        'utc_date': utc_date,
        'latitude': ltd,
        'longitude': lng,
        'address': location_info['address'],
        'region': location_info['region'],
        'country': location_info['country']
    }
    iss = ISS(
        utc_timestamp=config['utc_timestamp'],
        utc_date=config['utc_date'],
        latitude=config['latitude'],
        longitude=config['longitude'],
        address=config['address'],
        country=config['country'],
        region=config['region']
    )
    db.session.add(iss)
    db.session.commit()

#route to teste uwsgi
@app.route('/', methods=['GET'])
def hello_wsgi():
    return "app entrypoint"

