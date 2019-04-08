import os
from flask import Flask, request
from flask import jsonify
import json
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import uuid

app = Flask(__name__)
load_dotenv()

app.config["FLASK_APP"] = os.getenv("FLASK_APP")
app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

db = SQLAlchemy(app)

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
  return result.id


if __name__ == '__main__':
  app.run()
