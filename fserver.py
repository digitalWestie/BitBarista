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

app = Flask(__name__)

with open('config.json') as json_config:
  config = json.load(json_config)

offers = config["offers"]

root_url = "http://localhost:5000"
state_url = "http://localhost:5000/state/"

@app.route("/")
def home():
  return render_template('home.html', hello="STARTED")


@app.route("/table")
def table():
  return render_template('table.html')


@app.route("/start")
def start():
  return render_template('root.html', state_url=state_url, offers=offers)


@app.route('/assets/<path:path>')
def send_asset(path):
  return send_from_directory('assets', path)


@app.route('/water_request/')
def water_request():
  reward = "0.0006"
  return render_template('water_request.html', reward=reward, state_url=state_url)


@app.route('/state/')
def get_state():
  state = board_reader.read_state()
  return jsonify(**state)


@app.route('/qr/')
def get_qr():
  result = qrcode.start()
  print result
  return jsonify(**result)


@app.route('/choice/') #NB ONLY IN THE CASE OF A FREE COFFEE 
def choice():
  return render_template('choice.html', state_url=state_url)


@app.route('/refill/')
def refill():
  return render_template('refill.html')


@app.route('/empty_grinds/')
def empty_grinds():
  reward = "0.0006"
  return render_template('empty.html', state_url=state_url, reward=reward)


@app.route('/standby/')
def standby():
  return render_template('standby.html')


@app.route('/sale/<offer>')
def sale(offer):
  state = board_reader.read_state() 
  if (state['overall'] == 'ready'):
    
    request = generate_request(offers[offer])

    if not request:
      print "\n Error: trouble generating request for offer"
      return redirect("/error", code=302)
    
    request["URI"] = request["URI"]+'&label=BitBarista&message=offer_'+offer
    print "Making request for: "
    print request

    request_check_url = "http://localhost:5000/payment_request/"+request["address"]

    return render_template('sale.html', offer=offer, address=request["address"], price=offers[offer], qrdata=request["URI"], request_check_url=request_check_url)
  else:
    return redirect("/", code=302)


@app.route('/serve/<offer>')
def serve(offer):
  if (offer == "double"): 
    button = "tazza2"
    servetime = 60
  else:
    button = "tazza1"
    servetime = 45
  
  cost = request.args.get('cost')
  if cost == None:
    cost = 0.0

  result = board_reader.press_button(button)

  if result:
    return render_template('serve.html', cost=cost, servetime=servetime, state_url=state_url)
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


@app.route("/error")
def error_page():
  return 'Oh uh, something went wrong! <a href="/">Please try again.</a>'


@app.route("/help")
def help():
  return render_template('help.html')


@app.route("/claim/<amount>")
def claim(amount):
  reason = request.args.get('reason')
  if (reason == "refund"):
    message = "Oops, something went wrong! Follow the steps to claim a refund..."
  elif (reason == "refill"):
    message = "Thanks for the refill! Follow the steps to claim your payment."
  else:
    message = "Thanks for that! Follow the steps to claim your payment."
  return render_template('claim.html', amount=amount, message=message)


@app.route("/payout/<amount>")
def payout(amount):
  after_scan = request.args.get('after_scan')
  if (after_scan == None):
    after_scan = root_url
  else:
    after_scan = root_url+after_scan
  return render_template('payout.html', amount=amount, after_scan=after_scan)


def check_request(address):
  p = Popen(['electrum', 'getrequest', address], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  output, err = p.communicate()
  if p.returncode == 0:
    return json.loads(output)
  else:
    return False


def send_payment(address, amount):
  print "Attempting to send payment to " + address + " for " + str(amount) + "BTC"
  p = Popen(['electrum', 'payto', address, str(amount), '-W', config["walletpass"]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
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
