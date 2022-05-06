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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Checks if username and password are entered correctly
        if not username:
            return apology("Must provide username", 400)
        elif not password:
            return apology("Must provide password", 400)
        elif not confirmation or password != confirmation:
            return apology("Password and password confirmation must be the same", 400)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = (?)", (username,))
        rows = rows = cur.fetchall()
        
        if len(rows) == 1:
            return apology("You are already registered", 400)

        # Updates database with new user data
        cur.execute("""INSERT INTO users (username, hash) 
                    VALUES (?, ?)""", (
                    username, 
                    generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)))
        conn.commit()
        conn.close()

        flash('You were successfully registered')
        return redirect("/login")

    else:
        return render_template("register.html")