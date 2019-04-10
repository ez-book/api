import os
from flask import Flask, request
from flask import jsonify
import json
from flask import abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import uuid
import bookingapi

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()

app.config['CORS_HEADERS'] = ['Content-Type']
app.config["FLASK_APP"] = os.getenv("FLASK_APP")
app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

db = SQLAlchemy(app)

b = bookingapi.BookingAPI()

class Test_Person(db.Model):
  __tablename__ = 'test_person'

  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80))

  def __init__(self, name):
    self.name = name


class Itenary(db.Model):
  __tablename__ = 'itenary'
  id = db.Column(db.String(50), primary_key=True)
  url = db.Column(db.String(256))
  places = db.Column(db.String(256))
  def __init__(self, url, placesArr):
    self.url = url
    self.places = ",".join(placesArr)
    self.id = str(uuid.uuid3(uuid.NAMESPACE_URL, url))

  @staticmethod
  def get(id):
    return db.session.query(Itenary).filter(Itenary.id == id).all()

  @staticmethod
  def getByURL(url):
    id = str(uuid.uuid3(uuid.NAMESPACE_URL, url))
    return db.session.query(Itenary).filter(Itenary.id == id).all()


  def post(self):
    rows = self.get(self.id)
    if len(rows) > 0:
      return
    db.session.add(self)
    db.session.commit()




@app.route('/')
def hello():
  return 'Hello, ' + os.getenv("NAME") + '!'

@app.route('/name/<id>', methods=['GET'])
def get_name(id):
  # There's probably a better way to do this, but it's 2am and I just want this to work ...
  return db.session.query(Test_Person).filter(Test_Person.id == int(id, 10)).all()[0].name

@app.route('/itenary/<id>', methods=['GET'])
def get_itenary(id):
  data = Itenary.get(id)

  if len(data) == 0 :
    abort(400)

  return jsonify(
    url = data[0].url,
    id=data[0].id,
    places=data[0].places.split(','),
  )

@app.route('/itenary', methods=['GET'])
def get_itenary_url():
  url = request.args.get('url')
  data = Itenary.getByURL(url)

  if len(data) == 0:
    return jsonify(
      url=url,
    )
  return jsonify(
    url=data[0].url,
    id=data[0].id,
    places=data[0].places.split(','),
  )

@app.route('/itenary', methods=['POST'])
def post_itenary():
  data = request.data
  dataDict = json.loads(data)

  url = ''
  places = []
  if 'url' in dataDict:
    url = dataDict['url']
  else:
    return abort(400)
  if 'places' in dataDict:
    places = dataDict['places']
  result = Itenary(url, dataDict['places'])
  result.post()
  return jsonify(id=result.id)

@app.route('/city', methods=['GET'])
def get_city_id():
  name = request.args.get('name')
  return jsonify(b.get_city_id_by_city_name(name))

@app.route('/hotel/city', methods=['GET'])
def get_hotels_in_city():
  name = request.args.get('name')
  return jsonify(b.get_hotels_by_city_name(name))

@app.route('/hotel/city/available', methods=['GET'])
def get_available_hotels_in_city():
  checkin = request.args.get('checkin')
  checkout = request.args.get('checkout')
  name = request.args.get('name')
  room = request.args.get('room')
  return jsonify(b.get_availability_hotel(checkin, checkout, name, room))


if __name__ == '__main__':
  app.run()
