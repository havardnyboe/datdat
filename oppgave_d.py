import sqlite3
import datetime
from print_table import print_table

con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()
friday = 4


def is_weekend(date: datetime.datetime) -> bool:
    return date.weekday() > friday

def routesWithStations(a, b, dato: datetime.datetime):
    if is_weekend(dato): 
        weekend = "AND KjørerHelger = 1" 
    else: 
        weekend = ""
    cursor.execute("""
        SELECT  A.Jernbanestasjon, A.Avgangstid, B.Jernbanestasjon, B.Ankomsttid
        FROM StasjonerITabell A, StasjonerITabell B, Togrutetabell
        WHERE A.TogrutetabellID = B.TogrutetabellID
        AND A.Stasjonnummer < B.Stasjonnummer
        AND A.TogrutetabellID = Togrutetabell.ID
        AND B.TogrutetabellID = Togrutetabell.ID
        AND A.Jernbanestasjon LIKE ?
        AND B.Jernbanestasjon LIKE ?
        AND KjørerUkedager = 1
        AND A.Avgangstid >= ?
        """ +
        weekend +
        """
        ORDER BY A.Avgangstid ASC;
    """, (a+"%", b+"%", str(dato.time())))
    
    routes = cursor.fetchall()
    return routes


dag = input("Skriv inn dato (YYYY-MM-DD): ")
tid = input("Skriv inn tid (HH:MM): ")
if dag == "": dag = "2023-03-24"
if tid == "": tid = "00:00"
dato = datetime.datetime.strptime(dag.strip() + " " + tid.strip(), "%Y-%m-%d %H:%M")
imorgen = datetime.datetime.strptime(dag.strip(), "%Y-%m-%d") + datetime.timedelta(days=1)

start = input("Startstasjon: ")
stopp = input("Endestasjon: ")
strekninger = routesWithStations(start, stopp, dato)
strekninger_imorgen = routesWithStations(start, stopp, imorgen)

print(f"\nTabell for {dato.date()} kl. {dato.time()}")
if len(strekninger) > 0:
    print_table(strekninger, ["Startstasjon", "Avgang", "Sluttstasjon", "Ankomst"])
else:
    print("Ingen ruter for valgte tidspunkt.")

print(f"\nTabell for {imorgen.date()} kl. {imorgen.time()}")
if len(strekninger_imorgen) > 0:
    print_table(strekninger_imorgen, ["Startstasjon", "Avgang", "Sluttstasjon", "Ankomst"])
else:
    print("Ingen ruter for valgte tidspunkt.")

con.close()
