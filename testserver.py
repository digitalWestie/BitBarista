from flask import Flask, abort, redirect
from flask import jsonify
from flask import render_template
from flask import send_from_directory
from flask import request
from subprocess import Popen, PIPE
import json
import urllib
import random
import fake_board_reader as board_reader #board_reader on pi
import random
import csv
import datetime

app = Flask(__name__)

with open('config.json') as json_config:
  config = json.load(json_config)

offers = config["offers"]
root_url = "http://localhost:5000"
state_url = "http://localhost:5000/state/"

@app.route('/assets/<path:path>')
def send_asset(path):
  return send_from_directory('assets', path)

@app.route("/")
def home():
  cost = request.args.get('cost')
  print cost
  return render_template('home.html', hello="STARTED")

@app.route("/table")
def table():
  suppliers=suppliers_list()
  suppliers.pop(0)
  return render_template('table.html', suppliers=suppliers)

def suppliers_list():
  try:
    reader = csv.reader(open('suppliers.csv', 'r'))
    return list(reader)
  except Exception as error:
    print "Failed to read suppliers csv \n", str(error)
    return []


if __name__ == "__main__":
  try:
    app.run(debug=True)
  except KeyboardInterrupt:
    print "Shutting down server"
  except Exception as error:
    print "Other error or exception occurred \n", str(error)
  finally: 
    print "Done."
