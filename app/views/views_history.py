import os
import re

import sqlite3
from sqlite3 import DatabaseError
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, get_db_connection
from app.helpers import apology, login_required, lookup, usd, absolute


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of transactions"""

    id = session.get("user_id")

    # Fetches available cash from table "users"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT cash FROM users WHERE id = (?)", (id,))
    cash_row = cur.fetchone()["cash"]
    user_credit = float(cash_row)
         
    # Fetches all open positions from table "transactions" as an offset of 
    # purchases and sales of each stock symbol
    cur.execute(
                """SELECT symbol, name, SUM(quantity) AS shares, price 
                FROM transactions WHERE user_id = (?) GROUP BY symbol""", (id,))
    open_positions = cur.fetchall()
        
    # Dictionary of current prices for stocks in open positions - fetched from IEX API
    current_prices = {}

    # Calculates total amount locked in open transactions
    locked = 0
    if len(open_positions) != 0:
        for row in open_positions:
            symbol = row["symbol"]
            current_price = (lookup(symbol))["price"]
            current_prices[symbol] = current_price
            locked += current_price * row["shares"]

    # Calculates total deposits
    cur.execute(
                """SELECT SUM(amount) AS deposits 
                FROM traffic WHERE user_id = (?) AND trans = (?)""", (
                id, "deposit"))
    deposits = cur.fetchall()
    total_deposits = 0
    if deposits[0]["deposits"] is not None:
        total_deposits += deposits[0]["deposits"]

    # Calculates total withdrawals
    cur.execute(
                """SELECT SUM(amount) AS withdrawals 
                FROM traffic WHERE user_id = (?) AND trans = (?)""", (
                id, "withdrawal"))
    withdrawals = cur.fetchall()
    total_withdrawals = 0
    if withdrawals[0]["withdrawals"] is not None:
        total_withdrawals += withdrawals[0]["withdrawals"]

    # Calculates total sales and purchases
    cur.execute(
                """SELECT symbol, name, quantity, price, time, trans 
                FROM transactions WHERE user_id = (?)""", (id,))
    user_transactions = cur.fetchall()
    total_sales = 0
    total_purchases = 0
    for transaction in user_transactions:
        if transaction["trans"] == "sell":
            total_sales += absolute(transaction["quantity"]) * transaction["price"]
        elif transaction["trans"] == "buy":
            total_purchases += absolute(transaction["quantity"]) * transaction["price"]

    # Fetches all open positions from table "transactions" and calculates total quantity of shares for each stock
    cur.execute(
                """SELECT symbol, name, SUM(quantity) AS shares, price 
                FROM transactions WHERE user_id = (?) GROUP BY symbol""", (
                id,))
    open_positions = cur.fetchall()
    conn.close()

    # Dictionary of current prices for stocks in open positions - fetched from IEX API
    current_prices = {}

    # Total amount locked in open transactions
    locked = 0

    # Total current portfolio, i.e. available cash + total in open transactions
    total = user_credit

    for row in open_positions:
        symbol = row["symbol"]
        current_price = (lookup(symbol))["price"]
        current_prices[symbol] = current_price
        locked += current_price * row["shares"]
        total += locked

    # Calulates total gain relative to cash available at the registration
    gain = (user_credit + total_withdrawals - total_deposits + locked) - 10000

    return render_template("history.html", user_transactions=user_transactions,
                         user_credit=user_credit, gain=gain, 
                         total_deposits=total_deposits, 
                         total_withdrawals=total_withdrawals, locked=locked)