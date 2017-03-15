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
import requests
import socket

app = Flask(__name__)

with open('config.json') as json_config:
  config = json.load(json_config)

offers = config["offers"]
root_url = "http://localhost:5000"
state_url = "http://localhost:5000/state/"

@app.route("/test/")
def test():
  download_home_blurb()
  home_blurb = read_home_blurb()
  return render_template('test.html', home_blurb=home_blurb)


@app.route("/state/")
def state():
  result = { overall: 'ready' }
  return jsonify(**result)


@app.route("/table")
def table():
  suppliers=suppliers_list()
  suppliers.pop(0)
  return render_template('table.html', suppliers=suppliers)


@app.route('/assets/<path:path>')
def send_asset(path):
  return send_from_directory('assets', path)


def suppliers_list():
  try:
    reader = csv.reader(open('suppliers.csv', 'r'))
    return list(reader)
  except Exception as error:
    print "Failed to read suppliers csv \n", str(error)
    return []


def download_home_blurb():  
  r = requests.get('https://raw.githubusercontent.com/digitalWestie/BitBarista/master/templates/home_blurb.html')
  if ((r.status_code == 200) and (len(r.text) > 0)):
    with open('templates/home_blurb.html', 'w') as f:
      f.write(r.text)
    return True
  else:
    return False

def read_home_blurb():
  try:
    return open('templates/home_blurb.html', 'r').read()
  except Exception as error:
    print "Failed to read home blurb", str(error)
    return None

if __name__ == "__main__":
  try:
    app.run(debug=True)
  except KeyboardInterrupt:
    print "Shutting down server"
  except Exception as error:
    print "Other error or exception occurred \n", str(error)
  finally: 
    print "Done."
