import sqlite3
con = sqlite3.connect('qrcube.db')

con.execute("""
CREATE TABLE QRCode (
    id INTEGER PRIMARY KEY,
    author_id INTEGER,
    content char(500),
    eclevel INTEGER,
    qrtypenumber INTEGER,
    filename char(250),
    alttag char(500),
    titletag char(500),
    creation_date DATE
    )
""")

con.execute("""
CREATE TABLE Question(
    id INTEGER PRIMARY KEY,
    author_id INTEGER,
    slug char(250),
    type char(50),
    question char(500),
    views INTEGER,
    creation_date DATE
    )
""")

con.execute("""
CREATE TABLE QRCodeAnswers(
    id INTEGER PRIMARY KEY,
    question_id INTEGER,
    qrcode_id INTEGER,
    answer char(500),
    correct BOOLEAN,
    scanhits INTEGER,
    slug char(250)
    )
""")

con.execute("""
CREATE TABLE Scans(
    id INTEGER PRIMARY KEY,
    qrcode_id INTEGER,
    scan_date DATE
    )
""")

con.commit()

