import os
import re

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, get_db_connection
from app.helpers import apology, login_required, lookup, usd, absolute


@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    """Change user settings"""
    id = session.get("user_id")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT cash FROM users WHERE id = (?)", (
                id,))
    credit = float(cur.fetchone()["cash"])
    if request.method == "GET":
        return render_template("user.html", credit=credit)
    elif request.method == "POST":
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")
        amount = request.form.get("money")
        transaction = request.form.get("transaction")
        
        # If user entered a new password the following checks if user entered a valid format of a password
        if new_password:    
            if new_password != confirmation:
                return apology("Make sure that New Password and Confirmation match", 400)
            if len(new_password) < 8:
                return apology("Make sure your password is at lest 8 characters", 400)
        
            if not re.search("[0-9]", new_password):
                return apology("Make sure your password has a number in it", 400)
            if not re.search("[A-Z]", new_password):
                return apology("Make sure your password has a capital letter in it", 400)
            if not re.search("[a-z]", new_password):
                return apology("Make sure your password has a lower-case letter in it", 400)
            if not re.search("[!@#$%^&*()-_]", new_password):
                return apology("Make sure your password has a special sign in it", 400)

            # Updates database 
            cur.execute("UPDATE users SET hash = ? WHERE id = (?)", 
                        (generate_password_hash(
                        new_password, method='pbkdf2:sha256', salt_length=8), 
                        id))
            conn.commit()
            conn.close()

            flash("You have successfuly changed your password")
            return render_template("user.html")

        elif amount:
            # If user chose to deposit money
            if transaction == "deposit":
                credit += float(amount)
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("UPDATE users SET cash = ? WHERE id = (?)", (
                            credit, id))
                conn.commit()
                cur.execute("""INSERT INTO traffic (
                            trans, amount, user_id) VALUES (?, ?, ?)""", (
                            transaction, amount, id))
                conn.commit()
                conn.close()

                flash("You have successfuly deposited money to your account")
                return render_template("user.html", credit=credit)
            # If user chose to withdraw money
            elif transaction == "withdraw":
                credit -= float(amount)
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("UPDATE users SET cash = ? WHERE id = (?)", (
                            credit, id))
                conn.commit()
                cur.execute("""INSERT INTO traffic (trans, amount, user_id) 
                            VALUES (?, ?, ?)""", (transaction, amount, id))
                conn.commit()
                conn.close()

                flash("You have successfuly sent money to your bank account")
                return render_template("user.html", credit=credit)