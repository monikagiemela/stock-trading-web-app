import os
import re

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, get_db_connection
from app.helpers import apology, login_required, lookup, usd, absolute


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    id = session.get("user_id")

    # Fetches available cash from table "users"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT cash FROM users WHERE id = (?)", (id,))
    cash_row = cur.fetchone()[0]
    cash = float(cash_row)
    
    # Fetches all open positions from table "transactions" and calculates total quantity of shares for each stock
    cur.execute(
                """SELECT symbol, name, SUM(quantity) AS shares, price 
                FROM transactions WHERE user_id = ? GROUP BY symbol""", (id,))
    open_positions = cur.fetchall()
    conn.close()

    # Dictionary of current prices for stocks in open positions - fetched from IEX API
    current_prices = {}

    # Total amount locked in open transactions
    locked = 0

    # Total current portfolio, i.e. available cash + total in open transactions
    total = cash

    for row in open_positions:
        symbol = row["symbol"]
        current_price = (lookup(symbol))["price"]
        current_prices[symbol] = current_price
        locked += current_price * row["shares"]
        total += locked

    return render_template("index.html", open_positions=open_positions, 
                            current_prices=current_prices, cash=cash, 
                            total=total, locked=locked)