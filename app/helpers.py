import os
from cv2 import DFT_REAL_OUTPUT
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

import pandas as pd


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """Decorate routes to require login."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""
    # Contact API
    try:
        API_KEY = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None

def end_day_lookup(symbol):
    print("end_day is running")
    
    try:
        API_KEY = os.environ.get("API_KEY") 
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/chart/20220508?token={API_KEY}"         
        response = requests.get(url)
        print(response)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    print(response.status_code)
    #df = pd.read_csv(response)
    
    #return df

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def absolute(quantity):
    """Format value as absolute"""
    if quantity < 0:
        return quantity * (-1)
    return quantity