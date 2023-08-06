#!/usr/bin/env python3

import pymonetdb
print(pymonetdb.__path__)

conn = pymonetdb.connect(
	'foo', port=50000, host='127.0.0.1',
	# replysize=1,
)
conn.set_replysize(2)
cursor = conn.cursor()

query = "SELECT COUNT(*) FROM users WHERE ? = 0 OR ? = 0 OR ? = 0 OR ? = 0"

keywords = [
    # None,
    # "EXPLAIN",
    # "PLAN",
    # "TRACE",
    "PREPARE",
]

for kw in keywords:
    q = f"{kw} {query}" if kw else query
    print()
    print(f"EXECUTING: {q}")
    cursor.execute(q)
    for row in cursor.fetchall():
        print(row)