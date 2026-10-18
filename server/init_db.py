# DB init
import sqlite3
cx = sqlite3.connect("data.db")
cu = cx.cursor()

# log table
q = '''CREATE TABLE log (
    timestamp TEXT NOT NULL DEFAULT datetime()
    lux NUMERIC
    temperature NUMERIC
    humidity NUMERIC
    battery INTEGER
    emergency INTEGER
    trigger INTEGER
    video TEXT
);'''
cu.execute(q)