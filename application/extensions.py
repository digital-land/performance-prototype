# -*- coding: utf-8 -*-
"""
Flask extensions instances, for access outside app.factory
"""

from govuk_jinja_components.flask_govuk_components import GovukComponents

govuk_components = GovukComponents()

from digital_land_frontend.flask_dl_components import DLComponents

dl_components = DLComponents()