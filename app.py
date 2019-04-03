import os
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

app.config["FLASK_APP"] = os.getenv("FLASK_APP")
app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")

@app.route('/')
def hello():
  return 'Hello, ' + os.getenv("NAME") + '!'

@app.route('/name', methods=['GET'])
def get_name():
  return os.getenv("NAME")

if __name__ == '__main__':
  app.run()
