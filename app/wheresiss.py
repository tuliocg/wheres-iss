import os
import requests
from datetime import datetime

class ISS():
    _iss_api_url = 'http://api.open-notify.org/iss-now.json'
    _reversing_geo_api = {
        'base_url': 'https://api.mapbox.com/geocoding/v5/mapbox.places/',
        'return_type': '.json',
        'token_section': '?access_token='
    }
    _mapbox_token = os.environ.get('MAPBOX_TOKEN', 'NO KEY REGISTERED')


    def __init__(self, config):
        self.utc_timestamp = config['utc_timestamp']
        self.utc_date = config['utc_date']
        self.latitude = config['latitude']
        self.longitude = config['longitude']
        self.country = config['country']
        self.region = config['region']
        self.address = config['address']


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


if __name__ == '__main__':
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
    iss = ISS(config)
    print(iss)
