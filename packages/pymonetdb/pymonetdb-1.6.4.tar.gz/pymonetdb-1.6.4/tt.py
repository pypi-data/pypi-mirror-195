#!/usr/bin/env python3

import pymonetdb
print(pymonetdb.__path__)

conn = pymonetdb.connect(
	'foo', port=50000, host='127.0.0.1', 
	replysize=4, binary=True,
)

cursor = conn.cursor()

q = """
SELECT value AS i, 'xyz"' || value AS t FROM sys.generate_series(0,10);
"""
cursor.execute(q)

# fetchall
cursor.execute(q)
print("fetchall")
rows = cursor.fetchall()
for row in rows:
	print(row)

# fetchone
print("fetchone")
cursor.execute(q)
while True:
	row = cursor.fetchone()
	if row:
		print(row)
	else:
		break

# fetchmany
print("fetchmany")
cursor.execute(q)
while True:
	rows = cursor.fetchmany(100)
	if rows:
		for row in rows:
			print(row)
	else:
		break
