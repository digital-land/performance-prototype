import json

from flask import (
  render_template,
  Blueprint,
  current_app)


base = Blueprint('base', __name__)

@base.context_processor
def set_globals():
  return {
    "staticPath": "https://digital-land.github.io"
  }

def read_json_file(data_file_path):
  f = open(data_file_path,)
  data = json.load(f)
  f.close()
  return data


@base.route('/')
@base.route('/index')
def index():
  return render_template('index.html')
