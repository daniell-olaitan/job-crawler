#!/usr/bin/env python3
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/v1')
