from flask import Flask
from flask import jsonify
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import Flask,redirect
from subprocess import Popen, PIPE

import fake_board_reader #board_reader on pi

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
  state = fake_board_reader.read_state()
  return jsonify(**state)

#return redirect("http://www.example.com", code=302)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html', name=name)

@app.route("/test")
def testing():
  p = Popen(['electrum', 'getaddresshistory', '1AR9FJLYUb9cqojiuTwrD7awP18FfXJkoQ'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  output, err = p.communicate()
  rc = p.returncode
  return output

if __name__ == "__main__":
  app.run(debug=True)