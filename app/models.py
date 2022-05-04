import os
import re

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from app import app, get_db_connection


conn = get_db_connection()
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER, 
            username TEXT NOT NULL, 
            hash TEXT NOT NULL, 
            cash NUMERIC NOT NULL DEFAULT 10000.00, 
            PRIMARY KEY(id))""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER,
            symbol TEXT NOT NULL,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price NUMERIC NOT NULL,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            trans TEXT NOT NULL,
            PRIMARY KEY(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
            )""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS traffic (
    id INTEGER,
    trans TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
conn.commit()
conn.close()