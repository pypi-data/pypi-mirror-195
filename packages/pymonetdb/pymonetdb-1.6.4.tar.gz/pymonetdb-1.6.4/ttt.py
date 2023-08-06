#!/usr/bin/env python3

import pymonetdb
print(pymonetdb.__path__)

conn = pymonetdb.connect('demo', port=50000, host='127.0.0.1')
conn.set_replysize(4)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS foo")
cursor.execute("CREATE TABLE foo(i INT)")

# Example 1:
q = """
SELECT value FROM sys.generate_series(0,5);
SELECT value from sys.generate_series(10,15);
"""
cursor.execute(q)
print(cursor.fetchall())

# Example 2:
cursor.execute("SELECT value FROM sys.generate_series(0,200); SELECT value from sys.generate_series(1000,1200)")
