# -*- coding: utf-8 -*-
"""
Flask app factory class
"""
import os
import pathlib

from flask import Flask
from flask.cli import load_dotenv

# this lets alembic know about our models
from application.models import *

load_dotenv()

parent_dir = pathlib.Path(__file__).parent.parent.absolute()
digital_land_db_path = (
    f"file:{os.path.join(parent_dir, 'digital-land.sqlite3?mode=ro')}"
)
entity_stats_db_path = (
    f"file:{os.path.join(parent_dir, 'entity-stats.sqlite3?mode=ro')}"
)


def create_app(config_filename):
    """
    App factory function
    """
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 10

    register_blueprints(app)
    register_context_processors(app)
    register_templates(app)
    register_filters(app)
    register_extensions(app)
    register_commands(app)

    return app


def register_blueprints(app):
    """
    Import and register blueprints
    """

    from application.blueprints.base.views import base

    app.register_blueprint(base)

    from application.blueprints.dataset.views import dataset_bp

    app.register_blueprint(dataset_bp)

    from application.blueprints.publisher.views import publisher_pages

    app.register_blueprint(publisher_pages)

    from application.blueprints.ripa_test.views import ripa_test

    app.register_blueprint(ripa_test)


def register_context_processors(app):
    """
    Add template context variables and functions
    """

    def globals_context_processor():
        return {"assetPath": "/static", "staticPath": "https://digital-land.github.io"}

    app.context_processor(globals_context_processor)


def register_filters(app):
    from application.filters import (
        clean_int_filter,
        to_float_filter,
        days_since,
        split_filter,
        urlencode_filter,
        remove_query_param_filter,
        unhyphenate,
        pass_fail,
        date_time_format

    )

    app.add_template_filter(clean_int_filter, name="to_int")
    app.add_template_filter(to_float_filter, name="to_float")
    app.add_template_filter(days_since, name="days_since")
    app.add_template_filter(split_filter, name="split")
    app.add_template_filter(urlencode_filter, name="urlencode")
    app.add_template_filter(remove_query_param_filter, name="remove_query_param")
    app.add_template_filter(unhyphenate, name="unhyphenate")
    app.add_template_filter(pass_fail, name="pass_fail")
    app.add_template_filter(date_time_format, name="date_time_format")

    from digital_land_frontend.filters import commanum_filter, hex_to_rgb_string_filter

    app.add_template_filter(commanum_filter, name="commanum")
    app.add_template_filter(hex_to_rgb_string_filter, name="hex_to_rgb")


def register_extensions(app):
    """
    Import and register flask extensions and initialize with app object
    """

    from application.extensions import db, migrate

    db.init_app(app)
    migrate.init_app(app)


def register_templates(app):
    """
    Register templates from packages
    """
    from jinja2 import PackageLoader, PrefixLoader, ChoiceLoader

    multi_loader = ChoiceLoader(
        [
            app.jinja_loader,
            PrefixLoader(
                {
                    "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
                    "digital-land-frontend": PackageLoader("digital_land_frontend"),
                }
            ),
        ]
    )
    app.jinja_loader = multi_loader


def register_commands(app):

    from application.commands import data_test_cli

    app.cli.add_command(data_test_cli)
