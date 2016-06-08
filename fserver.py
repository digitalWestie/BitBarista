from flask import Flask, abort, redirect
from flask import jsonify
from flask import render_template
from flask import send_from_directory
from flask import request
from subprocess import Popen, PIPE
import json

import fake_board_reader as board_reader #board_reader on pi
#import board_reader as board_reader 

app = Flask(__name__)

with open('config.json') as json_config:
  config = json.load(json_config)

offers = config["offers"]

@app.route("/")
def root():
  state_url = "http://localhost:5000/state"
  return render_template('root.html', state_url=state_url, offers=offers)


@app.route('/assets/<path:path>')
def send_asset(path):
  return send_from_directory('assets', path)


@app.route('/state/')
def get_state():
  state = board_reader.read_state()
  return jsonify(**state)


@app.route('/sale/<offer>')
def sale(offer):
  state = board_reader.read_state() 
  if (state['overall'] == 'ready'):

    # TODO: WRITE JS TO POLL REQUEST CHECKER
    # AFTER X RETRIES REDIRECT "/" ?
    # TODO: WRITE PAGE FOR SERVING COFFEE
    
    request = generate_request(offers[offer])

    if not request:
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
  if (offer == "single"): 
    pin = 17
    #TAKES 45 SECONDS
  else:
    pin = 27
  result = board_reader.press_button(pin)
  if result:
    #TODO CHECK IT HAS SERVED OK
    return render_template('serve.html', result=result)
  else:
    return redirect("/", code=302)


@app.route('/pressbutton/<pin>')
def press_button(pin=None):
  result = board_reader.press_button(pin)
  return render_template('hello.html', result=result)


@app.route("/payment_request/<address>")
def payment_request(address):
  request = check_request(address)
  if request:
    return jsonify(**request)
  else: 
    abort(500)


@app.route("/pay/<address>")
def pay(address):
  result = send_payment(address, offers["single"])
  if result:
    return "Paid!"
  else:
    return redirect("/error", code=302)


@app.route("/error")
def error_page():
  return 'Oh uh, something went wrong! <a href="/">Please try again.</a>'


@app.route("/help")
def help():
  return render_template('help.html') 


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
  p = Popen(['electrum', 'addrequest', str(amount), '-m', 'Coffee Sale Test'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
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
