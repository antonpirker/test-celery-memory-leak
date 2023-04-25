# -*- coding: utf-8 -*-
"""Create an application instance."""
import os
from functools import partial

from my_flask_app.app import create_app

app = create_app()
