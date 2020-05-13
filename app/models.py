__author__ = 'github/tuliocg'

#default modules
from datetime import datetime
import requests
import os

#local modules
from app import db

class ISS(db.Model):
    _iss_api_url = 'http://api.open-notify.org/iss-now.json'
    _reversing_geo_api = {
        'base_url': 'https://api.mapbox.com/geocoding/v5/mapbox.places/',
        'return_type': '.json',
        'token_section': '?access_token='
    }
    _mapbox_token = os.environ.get('MAPBOX_TOKEN', 'NO KEY REGISTERED')

    __tablename__ = 'iss_fact'
    id_ = db.Column(db.Integer, primary_key=True)
    utc_timestamp = db.Column(db.Integer, nullable=False)
    utc_date = db.Column(db.String(25), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(50))
    country = db.Column(db.String(50))
    region = db.Column(db.String(50))
    utc_insert_date = db.Column(db.DateTime, default=datetime.utcnow)


    @staticmethod
    def get_wheres_iss():
        req = requests.get(ISS._iss_api_url)
        latitude = req.json()['iss_position']['latitude']
        longitude = req.json()['iss_position']['longitude']
        return latitude, longitude


    @staticmethod
    def revert_geocode(ltd, lng):
        '''
        Reverse lat and long to addres, country and region
        :param ltd -> float: latitude decimal
        :param lng -> float: longitude decimal
        :return -> dict: mapboxapi features or bobsponge addres
        '''
        req_url = '{baseurl}{lng},{ltd}{return_type}{token_section}{mapboxtoken}'.format(
            baseurl=ISS._reversing_geo_api['base_url'],
            lng=lng,
            ltd=ltd,
            return_type=ISS._reversing_geo_api['return_type'],
            token_section=ISS._reversing_geo_api['token_section'],
            mapboxtoken=ISS._mapbox_token
        )
        features = requests.get(req_url).json()['features']
        #print(features)
        index_country = index_region = index_address = None
        location_info = {}
        if not features:
            location_info['address'] = '124 Conch Dr.'
            location_info['region'] = 'Bikini Bottom'
            location_info['country'] = 'Under Water'
        else:
            for i in range(len(features)):
                placetype_neighborhood = features[i]['place_type'][0] == 'neighborhood'
                placetype_postcode = features[i]['place_type'][0] == 'postcode'
                placetype_locality = features[i]['place_type'][0] == 'locality'
                placetype_region = features[i]['place_type'][0] == 'region'
                placetype_country = features[i]['place_type'][0] == 'contry'
                if placetype_neighborhood or placetype_postcode or placetype_locality:
                    index_address = i
                elif placetype_region:
                    index_region = i
                elif placetype_country:
                    index_country = i
            if index_address is None:
                location_info['address'] = 'Not provided'
            else:
                location_info['address'] = features[index_address]['place_name']
            if index_region is None:
                location_info['region'] = 'Not provided'
            else:
                location_info['region'] = features[index_region]['place_name']
            if index_country is None:
                location_info['country'] = 'Not provided'
            else:
                location_info['country'] = features[index_country]['place_name']
        return location_info


    def __str__(self):
        return '<Current position: ltd {}, lng {}, address {}>'.format(
            self.latitude,
            self.longitude,
            self.address
        )
