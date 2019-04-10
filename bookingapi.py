import json
import os

import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "https://distribution-xml.booking.com/2.4/json/"

USER = 'akoyya'
PW = 'randbopasswoed' #os.environ.get('BOOKING_PW')

class BookingAPI(object):
    def __init__(self):
        self.auth = HTTPBasicAuth(USER, PW)

    def _get_data(self, endpoint, params=None):
        try:
            url = "{}{}".format(BASE_URL, endpoint)
            params = params or {}
            r = requests.get(url, params=params, auth=self.auth)
            r.raise_for_status()
            return r.text
        except Exception as e:
            print("problem")
            print(e)
            return {}
    def get_autocomplete(self, cityName):
        endpoint = '/autocomplete'
        params = {'language': 'en'}
        params['text'] = cityName
        return json.loads(self._get_data(endpoint, params))

    def get_city_id_by_city_name(self, cityName):
        cityList = self.get_autocomplete(cityName)
        if 'result' not in cityList:
            return {}
        for item in cityList['result']:
            if 'city_name' not in item:
                continue
            if item['city_name'] != cityName:
                continue

            if 'city_ufi' in item:
                if item['city_ufi'] is None:
                    continue
                return item['city_ufi']
        return None

    def get_hotels_by_city_name(self, city_name):
        city_id = self.get_city_id_by_city_name(city_name)
        if city_id is None:
            return {}
        return self.get_hotels(city_id)

    def get_hotels(self, city_id):
        endpoint = '/hotels'
        params = {
            'city_ids': [city_id],
            'extras': 'hotel_description, hotel_info, hotel_photos, room_info, room_description, room_photos',
            'rows': 10,
        }
        hotels = self._get_data(endpoint, params)
        return json.loads(hotels)

    def get_availability_hotel(self, checkin, checkout, city_name, room):
        city_id = self.get_city_id_by_city_name(city_name)
        if city_id is None:
            return {}
        endpoint = '/hotelAvailability'
        params = {
            'checkin': checkin,
            'checkout': checkout,
            'city_ids': city_id,
            'extras': 'room_details,hotel_details,hotel_amenities',
            'room1': room
        }

        available_hotels = self._get_data(endpoint, params)
        return json.loads(available_hotels)

