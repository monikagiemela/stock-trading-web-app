import os
import re

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, get_db_connection
from app.helpers import apology, login_required, lookup, usd, absolute


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    id = session.get("user_id")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT cash FROM users WHERE id = (?)", (id,))
    user_credit = cur.fetchall()
    user_credit = user_credit[0]["cash"]
    cur.execute("""SELECT symbol, name, SUM(quantity) AS shares 
                FROM transactions WHERE user_id = (?) 
                GROUP BY symbol""", (id,))
    stocks = cur.fetchall()
    conn.close()

    if request.method == "GET":
        list_of_stocks = []
        for stock in stocks:
            if stock["shares"] > 0:
                list_of_stocks.append(stock["symbol"])
        return render_template("sell.html", user_credit=user_credit, list_of_stocks=list_of_stocks)

    else:
        # Checkes if user chose a symbol and fetches full name and price of the stock from IEX API
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not symbol or not quote:
            return apology("Enter a valid stock symbol", 403)
        name = quote["name"]
        price = quote["price"]

        # Checks if user entered a valid number of shares
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Number of shares must be a positive integer", 400)
        if shares <= 0:
            return apology("Number of shares must be a positive integer", 400)

        # Checks if user owns enough shares
        if len(stocks) < 1:
            return apology("You don't have this stock in your portfolio", 400)
        elif stocks[0]["shares"] < shares:
            return apology(f"You have only { stocks[0]['shares'] } shares in your portfolio", 400)

        # If all of the conditions are fulfilled, database is updated
        transaction = "sell"
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""UPDATE users SET cash = ? WHERE id = (?)""", 
                    user_credit + (price * shares), (id))
        conn.commit()
        cur.execute("""INSERT INTO transactions (
                    symbol, name, quantity, price, user_id, trans) 
                    VALUES (?, ?, ?, ?, ?, ?)""", (
                    symbol, name, -(shares), price, id, transaction))
        conn.commit()
        conn.close()

        flash("You have successfully sold shares")
        return redirect("/")