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


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    id = session.get("user_id")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT cash FROM users WHERE id = (?)", (id,))
    user_credit = cur.fetchone()[0]
    
    if request.method == "GET":
        return render_template("buy.html", user_credit=user_credit)

    else:
        # Checkes if user enteres a valid symbol and fetches full name and price of the stock from IEX API
        symbol = request.form.get("symbol").lower()
        quote = lookup(symbol)
        if not symbol or not quote:
            return apology("Enter a valid stock symbol", 400)
        name = quote["name"]
        price = quote["price"]

        # Checks if user entered a valid number of shares
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Number of shares must be a positive integer", 400)

        if shares <= 0:
            return apology("Number of shares must be a positive integer", 400)

        # Checks if user has enough cash to buy shares
        if user_credit < shares * price:
            return apology("You can not afford this many shares", 400)

        # If all of the above conditions are fulfilled, amount of purchase is substracted from available cash
        user_credit -= shares * price

        # Updates database
        transaction = "buy"
        cur.execute("BEGIN TRANSACTION")
        try:
            cur.execute("UPDATE users SET cash = (?) WHERE id = (?)", 
                        (user_credit, id))
            cur.execute("""INSERT INTO transactions 
                        (symbol, name, quantity, price, user_id, trans) 
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (symbol, name, shares, price, id, transaction))     
            conn.commit()
        except DatabaseError:
            print("failed!")
            cur.execute("rollback")
  
        conn.close()

        flash("You have successfuly bought shares")
        return redirect("/")