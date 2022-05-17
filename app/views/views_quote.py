import os
import re

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, get_db_connection
from app.helpers import apology, login_required, lookup, end_day_lookup, usd, absolute

import pandas as pd
import matplotlib.pyplot as plt


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    id = session.get("user_id")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT cash FROM users WHERE id = (?)", (id,))
    rows = cur.fetchone() 
    user_credit = rows[0]
    conn.close()

    if request.method == "GET":
        return render_template("quote.html", user_credit=user_credit)

    else:
        # Checke if user enteres a valid symbol and fetch full name and price of the stock from IEX API
        symbol = request.form.get("symbol").lower()
        quote = lookup(symbol)
        if not symbol or not quote:
            return apology("Enter a valid stock symbol", 400)
        
        #end_day_lookup(symbol)
        return render_template("quoted.html", quote=quote, symbol=symbol, user_credit=user_credit)