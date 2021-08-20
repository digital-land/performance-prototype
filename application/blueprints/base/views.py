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


@base.route('/performance')
def performance():
  return render_template('performance.html')


@base.route('/dataset/<dataset_name>/performance')
def dataset_performance(dataset_name):
  return render_template('dataset/performance.html', name=dataset_name)


@base.route('/organisation/<organisation>/performance')
def organisation_performance(organisation):
  return render_template('organisation/performance.html', organisation=organisation)


@base.route('/resource/<resource>/performance')
def resource_performance(resource):
  return render_template('resource/performance.html', resource=resource)
