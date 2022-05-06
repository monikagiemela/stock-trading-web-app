import os
import re

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from app.helpers import apology, login_required, lookup, usd, absolute

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filters
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["absolute"] = absolute

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create a database connection
def get_db_connection():
    conn = sqlite3.connect("finance.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

from app import models

from app.views.views_index import index
from app.views.views_buy import buy 
from app.views.views_history import history 
from app.views.views_login import login
from app.views.views_logout import logout
from app.views.views_quote import quote
from app.views.views_quoted import quoted
from app.views.views_register import register
from app.views.views_sell import sell
from app.views.views_user import user