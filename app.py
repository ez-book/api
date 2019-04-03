import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

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

@app.route('/')
def hello():
  return 'Hello, ' + os.getenv("NAME") + '!'

@app.route('/name/<id>', methods=['GET'])
def get_name(id):
  # There's probably a better way to do this, but it's 2am and I just want this to work ...
  return db.session.query(Test_Person).filter(Test_Person.id == int(id, 10)).all()[0].name

if __name__ == '__main__':
  app.run()
