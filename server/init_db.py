# DB init
import sqlite3
cx = sqlite3.connect("data.db")
cu = cx.cursor()

# log table
q = '''CREATE TABLE IF NOT EXISTS log (
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    lux NUMERIC,
    temperature NUMERIC,
    humidity NUMERIC,
    battery INTEGER,
    emergency INTEGER,
    trigger INTEGER,
    video TEXT
);'''
cu.execute(q)