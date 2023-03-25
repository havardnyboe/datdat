import sqlite3
from deleteall import deleteall

deleteall()

con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()

cursor.executescript(open("schema.sql", "r").read())
cursor.executescript(open("oppgave_a.sql", "r").read())
cursor.executescript(open("oppgave_b.sql", "r").read())
cursor.executescript(open("oppgave_f.sql", "r").read())

con.close()