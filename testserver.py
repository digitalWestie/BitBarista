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

app = Flask(__name__)

@app.route("/")
def home():
  cost = request.args.get('cost')
  print cost
  return render_template('home.html', hello="STARTED")

if __name__ == "__main__":
  try:
    app.run(debug=True)
  except KeyboardInterrupt:
    print "Shutting down server"
  except Exception as error:
    print "Other error or exception occurred \n", str(error)
  finally: 
    print "Done."
