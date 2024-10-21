#!/usr/bin/env python3
from flask import Blueprint

user_views = Blueprint('user_views', __name__)

from app.user.user_views import *
