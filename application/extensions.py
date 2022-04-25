# -*- coding: utf-8 -*-
"""
Flask extensions instances, for access outside app.factory
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db=db)
