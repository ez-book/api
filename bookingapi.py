import json
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()

BASE_URL = "https://distribution-xml.booking.com/2.4/json/"

USER = os.getenv("BOOKING_USER")
PW = os.getenv("BOOKING_PW")

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
        except Exception as exp:
            print(exp)
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
        return self.get_hotels(city_id, [])

    def get_hotels(self, city_id, hotel_ids):
        endpoint = '/hotels'
        params = {
            'extras': 'hotel_description, hotel_info, hotel_photos, room_info, room_description, room_photos',
        }

        if len(hotel_ids) > 0 :
            params['hotel_ids'] = hotel_ids
            params['extras'] = 'hotel_photos, room_photos'
        else:
            params['city_ids'] = [city_id]
            params['rows'] = 10

        hotels = self._get_data(endpoint, params)
        return json.loads(hotels)

    def extract_hotel_ids(self, available_hotels):
        hotel_ids = []

        if 'result' not in available_hotels:
            return hotel_ids
        hotel_list = available_hotels['result']

        for hotel_info in hotel_list:
            if 'hotel_id' in hotel_info and hotel_info['hotel_id'] is not None:
                hotel_ids.append(hotel_info['hotel_id'])
        print(hotel_ids)
        return hotel_ids

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
            'room1': room,
            'rows': 10
        }
        available_hotels = self._get_data(endpoint, params)
        available_hotels_info = json.loads(available_hotels)

        hotel_info = self.get_hotels(city_id, self.extract_hotel_ids(json.loads(available_hotels)))

        if 'result' not in hotel_info:
            return available_hotels_info

        extra_hotel_info = {}
        for item in hotel_info['result']:
            if 'hotel_id' not in item or 'room_data' not in item or 'hotel_data' not in item:
                continue
            extra_hotel_info[item['hotel_id']] = {}
            extra_hotel_info[item['hotel_id']]['room_data'] = item['room_data']
            extra_hotel_info[item['hotel_id']]['hotel_data'] = item['hotel_data']

        if 'result' not in available_hotels_info:
            return available_hotels_info

        available_hotels_info_data = available_hotels_info['result']

        available_hotels_info_data_new = []
        for item in available_hotels_info_data:
            if 'hotel_id' not in item:
                available_hotels_info_data_new.append(item)
                continue
            if item['hotel_id'] not in extra_hotel_info:
                available_hotels_info_data_new.append(item)
                continue
            item['room_data'] = extra_hotel_info[item['hotel_id']]['room_data']
            item['hotel_data'] = extra_hotel_info[item['hotel_id']]['hotel_data']
            available_hotels_info_data_new.append(item)

        available_hotels_info['result'] = available_hotels_info_data_new
        return available_hotels_info

