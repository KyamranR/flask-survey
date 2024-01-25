from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
import sys

print(sys.path)

app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = 'porsche'

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home():
    return 'Home Page'