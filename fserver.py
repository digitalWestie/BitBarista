from flask import Flask
from flask import jsonify
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import Flask,redirect
from subprocess import Popen, PIPE

#import fake_board_reader as board_reader #board_reader on pi
import board_reader as board_reader 

app = Flask(__name__)

state_url = "http://localhost:5000/state"

@app.route("/")
def root():
  return render_template('root.html', state_url=state_url)

@app.route('/assets/<path:path>')
def send_asset(path):
  return send_from_directory('assets', path)

@app.route('/state/')
def get_state():
  state = board_reader.read_state()
  return jsonify(**state)

@app.route('/sell/<offer>')
def sell(offer="single"):
  state = board_reader.read_state()
  if (state['overall'] == 'ready'):
    return render_template('sale.html', offer=offer, address="xyz1232323", price="0.0001")
  else:
    return redirect("/", code=302)

@app.route('/pressbutton/<pin>')
def press_button(pin=None):
  result = board_reader.press_button(pin)
  return render_template('hello.html', result=result)

@app.route("/test")
def testing():
  p = Popen(['electrum', 'getaddresshistory', '1AR9FJLYUb9cqojiuTwrD7awP18FfXJkoQ'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  output, err = p.communicate()
  rc = p.returncode
  return output

if __name__ == "__main__":
  try:
    app.run(debug=True)
  except KeyboardInterrupt:  
    print "Shutting down server"
  except:
    print "Other error or exception occurred!"  
  finally: 
    board_reader.cleanup()
