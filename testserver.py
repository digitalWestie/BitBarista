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

@app.route("/test/")
def test():
  home_text='''<p>Currently serving <span class="input">Name</span> 
  coffee supplied by <span class="input_u">Producer</span> 
  harvested on   <span class="input_u">Dec 2016</span>
  purchased at <span class="input">&#163;20.00</span>/kg -   price change in relation to: previous year <span class="input_u">+0.34%</span>, previous month <span class="input_u">-0.001%</span></p>  <p>Supply purchased on <span class="input_u">6 Mar 2017</span>. Paid for by <span class="input">61</span> previous BitBarista customers, who chose the highest rated in terms of 
  <span class="input_u">Low Environmental Impact.</span></p>'''
  
  return render_template('test.html', home_text=home_text)


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


if __name__ == "__main__":
  try:
    app.run(debug=True)
  except KeyboardInterrupt:
    print "Shutting down server"
  except Exception as error:
    print "Other error or exception occurred \n", str(error)
  finally: 
    print "Done."
