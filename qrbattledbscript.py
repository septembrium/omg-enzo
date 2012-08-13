import sqlite3
con = sqlite3.connect('qrbattle.db')
con.execute("CREATE TABLE qrbattle (id INTEGER PRIMARY KEY, slug char(50) NOT
NULL, comp1 char(250) NOT NULL, comp2 char(250) NOT NULL, qr1 char(50) NOT
NULL, qr2 char(50) NOT NULL, points1 INTEGER, points2 INTEGER)")
con.commit()

