#!/usr/bin/env python3
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/v1/auth')
