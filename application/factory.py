# -*- coding: utf-8 -*-
"""
Flask app factory class
"""
import os

from flask import Flask, render_template, session
from flask.cli import load_dotenv

load_dotenv()


def create_app(config_filename):
    """
    App factory function
    """
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 10

    register_blueprints(app)
    register_context_processors(app)
    register_filters(app)
    register_extensions(app)

    return app


def register_blueprints(app):
    """
    Import and register blueprints
    """

    from application.blueprints.base.views import base

    app.register_blueprint(base)


def register_context_processors(app):
    """
    Add template context variables and functions
    """

    def base_context_processor():
        return {"asset_path": "/static/"}

    app.context_processor(base_context_processor)


def register_filters(app):
    from application.filters import (
        clean_int_filter,
        to_float_filter,
        days_since,
        split_filter,
    )

    app.add_template_filter(clean_int_filter, name="to_int")
    app.add_template_filter(to_float_filter, name="to_float")
    app.add_template_filter(days_since, name="days_since")
    app.add_template_filter(split_filter, name="split")

    from digital_land_frontend.filters import commanum

    app.add_template_filter(commanum)


def register_extensions(app):
    """
    Import and register flask extensions and initialize with app object
    """

    from application.assets import assets

    assets.init_app(app)

    from application.extensions import govuk_components

    govuk_components.init_app(app)

    from application.extensions import dl_components

    dl_components.init_app(app)
