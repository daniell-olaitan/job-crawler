#!/usr/bin/env python3
from flask import Blueprint

job_views = Blueprint('job_views', __name__)

from app.job.job_views import *
