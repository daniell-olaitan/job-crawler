#!/usr/bin/env python3
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

from app.auth.auth_views import *
