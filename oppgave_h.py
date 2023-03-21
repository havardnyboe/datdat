import sqlite3 
con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()

def findFutureTrips(Navn):
    cursor.execute("""
    SELECT * DISTINCT FROM Kunde,Kundeordre,Billett 
    WHERE Kunde.Navn == Navn &&
    Kundeordre.Kunde == Kunde.Kundenummer && 
    Kundeordre.Ordrenummer == Billett.Kundeordrenummer
    """)