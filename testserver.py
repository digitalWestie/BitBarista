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

@app.route("/")
def home():
  cost = request.args.get('cost')
  print cost
  return render_template('home.html', hello="STARTED")

@app.route("/offers")
def offers():
  offer_list = config["offers"].items()
  return render_template('offers.html', state_url=state_url, offers=offer_list)


if __name__ == "__main__":
  try:
    app.run(debug=True)
  except KeyboardInterrupt:
    print "Shutting down server"
  except Exception as error:
    print "Other error or exception occurred \n", str(error)
  finally: 
    print "Done."
