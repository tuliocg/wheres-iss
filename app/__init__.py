__author__ = 'github/tuliocg'

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.config import config

enviroment = 'development'

app = Flask(__name__)
app.config.from_object(config[enviroment])
CORS(app)

db = SQLAlchemy(app)
from app.models import ISS
db.create_all()

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

from app import views
