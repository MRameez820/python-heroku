# Shamelessly copied from http://flask.pocoo.org/docs/quickstart/

from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

