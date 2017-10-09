from flask import Flask, abort, redirect
from flask import jsonify
from flask import render_template
from flask import send_from_directory
from flask import request
from subprocess import Popen, PIPE
import json
import urllib
import random
#import fake_board_reader as board_reader #board_reader on pi
import board_reader as board_reader
import qrcode as qrcode
import random
import csv
import datetime
import requests
import socket

app = Flask(__name__)

with open('config.json') as json_config:
  config = json.load(json_config)

with open('credentials.json') as json_credentials:
  credentials = json.load(json_credentials)

root_url = "http://localhost:5000"
state_url = "http://localhost:5000/state/"

def get_message(reason):
  if (reason == "refund"):
    return "Oops, something went wrong! Please claim a refund."
  elif (reason == "refill"):
    return "Thanks for the refill!"
  elif (reason == "water_refilled"):
    return "Thanks for the refill!"
  else:
    return "Thanks for that! Follow the steps to claim a payment or free coffee."

@app.route("/")
def home():
  home_blurb = read_home_blurb()
  return render_template('home.html', state_url=state_url, home_blurb=home_blurb)


@app.route("/table")
def table():
  suppliers=suppliers_list()
  suppliers.pop(0)
  return render_template('table.html', suppliers=suppliers)


@app.route("/start")
def start():
  offer_list = config["offers"].items()
  return render_template('offers.html', state_url=state_url, offers=offer_list)


@app.route('/assets/<path:path>')
def send_asset(path):
  return send_from_directory('assets', path)


@app.route('/water_request/')
def water_request():
  reward = "0.0002"
  
  abused = False
  history = action_history()
  if (len(history) > 0): 
    abused = (history[-1][1] == 'water_refilled' or history[-1][1] == 'water_abuse')
    save_action("water_abuse", None)
  
  return render_template('water_request.html', reward=reward, state_url=state_url, abused=abused)


@app.route('/state/')
def get_state():
  state = board_reader.read_state()
  if not is_connected():
    state["overall"] = 'disconnected'
    state["message"] = "BitBarista is not connected to internet, please check connectivity"
  return jsonify(**state)


@app.route('/qr/')
def get_qr():
  result = qrcode.start()
  print result
  return jsonify(**result)


@app.route('/choice/') #NB ONLY IN THE CASE OF A FREE COFFEE 
def choice():
  offer_list = config["offers"].items()
  
  message = None
  reason = request.args.get('reason')
  
  if reason:
    message = get_message(reason)

  return render_template('choice.html', state_url=state_url, offers=offer_list, message=message)


@app.route('/refill/')
def refill():
  return render_template('refill.html')


@app.route('/steamer/')
def steamer():
  return render_template('steamer.html', state_url=state_url)


@app.route('/empty_grinds/')
def empty_grinds():
  reward = "0.0002"
  return render_template('empty.html', state_url=state_url, reward=reward)


@app.route('/standby/')
def standby():
  return render_template('standby.html')


@app.route('/disconnected/')
def disconnected():
  return render_template('disconnected.html', state_url=state_url)


@app.route('/warmup/')
def warmup():
  global config
  if download_config():
    with open('config.json') as json_config:
      config = json.load(json_config)
  download_home_blurb()
  download_suppliers()
  return render_template('warmup.html')


@app.route('/sale/<offer>')
def sale(offer):
  state = board_reader.read_state() 
  if (state['overall'] == 'ready'):
    
    offer_details = config["offers"][offer]
    price = offer_details["price"]
    request = generate_request(price)

    if not request:
      print "\n Error: trouble generating request for offer"
      return redirect("/error/", code=302)
    
    request["URI"] = request["URI"]+'&label=BitBarista&message=offer_'+offer
    print "Making request for: "
    print request

    request_check_url = "http://localhost:5000/payment_request/"+request["address"]

    return render_template('sale.html', offer=offer, offer_details=offer_details, address=request["address"], price=price, qrdata=request["URI"], request_check_url=request_check_url)
  else:
    return redirect("/", code=302)


@app.route('/serve/<offer>')
def serve(offer):
  if (offer == "double"):
    button = "tazza2"
    servetime = 72
  else:
    button = "tazza1"
    servetime = 70
  
  cost = request.args.get('cost')
  if cost == None:
    cost = 0.0

  result = board_reader.press_button(button)
  
  if result:
    save_serving(offer, cost)
    servings = serving_counts()
    return render_template('serve.html', cost=cost, servetime=servetime, state_url=state_url, servings=servings.items(), total_servings=total_servings(servings))
  else:
    return redirect("/", code=302)


@app.route('/press_button/<button>')
def press_button(button=None):
  result = board_reader.press_button(button)
  return render_template('hello.html', result=result)


@app.route("/payment_request/<address>")
def payment_request(address):
  request = check_request(address)
  print request
  if request:
    if not is_connected():
      request['status'] = 'disconnected'
    return jsonify(**request)
  else: 
    abort(500)


@app.route("/pay/<address>/<amount>", methods = ['POST'])
def pay(address, amount):
  print "received pay request"
  if request.method == 'POST':
    r = send_payment(address, amount)
    #r=bool(random.getrandbits(1))
    return jsonify(**{ 'success': r })
  else:
    return redirect("/", code=302)


@app.route("/error/")
def error_page():
  return render_template('error.html', state_url=state_url)


@app.route("/help")
def help():
  return render_template('help.html')


@app.route("/claim/<amount>")
def claim(amount):
  reason = request.args.get('reason')
  message = get_message(reason)

  if (reason == "water_refilled"):
    save_action("water_refilled", None)

  return render_template('claim.html', amount=amount, message=message)


@app.route("/payout/<amount>")
def payout(amount):
  after_scan = request.args.get('after_scan')
  if (after_scan == None):
    after_scan = root_url
  else:
    after_scan = root_url+after_scan

  message = None
  if (request.args.get('type') == 'refund'):
    message = "Sorry we cannot serve coffee just now, please claim a refund!"

  return render_template('payout.html', amount=amount, after_scan=after_scan, message=message)


def check_request(address):
  p = Popen(['electrum', 'getrequest', address], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  output, err = p.communicate()
  if p.returncode == 0:
    return json.loads(output)
  else:
    return False


def send_payment(address, amount):
  print "Attempting to send payment to " + address + " for " + str(amount) + "BTC"
  p = Popen(['electrum', 'payto', address, str(amount), '-W', credentials["walletpass"]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  tx, err = p.communicate()
  
  if p.returncode == 0:
    print "Broadcasting txn\n", tx
    p = Popen(['electrum', 'broadcast', tx], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 0:
      return True
    else:
      return False
  else:
    print "Couldn't generate txn\n", err
    return False


def generate_request(amount):
  p = Popen(['electrum', 'addrequest', str(amount), '-m', 'Coffee Sale'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  output, err = p.communicate()
  if p.returncode == 0:
    return json.loads(output)
  else:
    return False


def daemon_status():
  p = Popen(['electrum', 'daemon', 'status'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  p.communicate()
  if (p.returncode == 0):
    return True
  else:
    return False


def bitbarista_history():
  p = Popen(['electrum', 'history'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  output, err = p.communicate()
  if (p.returncode == 0):
    return json.loads(output)
  else:
    return False


def action_history():
  try:
    reader = csv.reader(open('history.csv', 'r'))
    return list(reader)
  except Exception as error:
    print "Failed to read history csv \n", str(error)
    return []


def action_counts():
  counts = {}
  for action in action_history():
    if counts.has_key(action[1]):
      counts[action[1]] += 1
    else:
      counts[action[1]] = 1
  return counts


def serving_counts():
  counts = {}
  for key,val in action_counts().items():
    split = key.split(':')
    if (len(split) > 1):
      counts[split[1]] = val
  return counts


def total_servings(serving_counts):
  total = 0
  for key,val in serving_counts.items():
    total += val
  return total


def save_action(action, param):
  try:
    with open("history.csv", "a") as history:
      nextline = ""
      if len(action_history()) >= 1:
        nextline = "\n"
      history.write(nextline + str(datetime.datetime.now()) + "," + str(action) + "," + str(param))
    return True
  except Exception as error:
    print "Failed to write to history.csv \n", str(error)
    return False


def save_serving(offer, price):
  return save_action('served:'+offer, price)


def download_home_blurb():
  r = requests.get('https://raw.githubusercontent.com/digitalWestie/BitBarista/master/templates/home_blurb.html')
  if ((r.status_code == 200) and (len(r.text) > 0)):
    with open('templates/home_blurb.html', 'w') as f:
      f.write(r.text)
    return True
  else:
    return False


def download_config():
  r = requests.get('https://raw.githubusercontent.com/digitalWestie/BitBarista/master/config.json')
  if ((r.status_code == 200) and (len(r.text) > 0)):
    with open('config.json', 'w') as f:
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


def download_suppliers():
  r = requests.get('https://raw.githubusercontent.com/digitalWestie/BitBarista/master/suppliers.csv')
  if ((r.status_code == 200) and (len(r.text) > 0)):
    with open('suppliers.csv', 'w') as f:
      f.write(r.text)
    return True
  else:
    return False


def suppliers_list():
  try:
    reader = csv.reader(open('suppliers.csv', 'r'))
    return list(reader)
  except Exception as error:
    print "Failed to read suppliers csv \n", str(error)
    reader = csv.reader(open('backup_suppliers.csv', 'r'))
    return list(reader)


def is_connected():
  try:
    socket.create_connection(("www.google.com", 80))
    return True
  except:
    pass
  return False


if __name__ == "__main__":
  try:
    electrumStarted = daemon_status()
    if not electrumStarted:
      raise ValueError('Electrum daemon not started, please run: electrum daemon start')
    app.run(debug=True)
  except KeyboardInterrupt:
    print "Shutting down server"
  except Exception as error:
    print "Other error or exception occurred \n", str(error)
  finally: 
    board_reader.cleanup()
