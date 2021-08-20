# -*- coding: utf-8 -*-

import os

from flask_assets import Bundle, Environment

from lib.sass_filter import LibSass

def static(*path):
    return os.path.join(os.path.dirname(__file__), 'static', *path)

libsass_output = LibSass(include_paths=[
    static('scss'),
    static('node_modules/govuk-frontend/')
])

css_govuk = Bundle(
  'scss/main.scss',
  filters=(libsass_output,),
  output='gen/css/main.css',
  depends=[
        'scss/**/*.scss',
        'node_modules/govuk-frontend/govuk/**/*.scss'
    ]
)

assets = Environment()

assets.register('css_govuk', css_govuk)

