import sqlite3
import datetime
from print_table import print_table

con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()
friday = 4


def is_weekend(date: datetime.datetime) -> bool:
    return date.weekday() > friday


def get_route_between_station_by_date(startstation: str, stopstation: str, timestamp: datetime.datetime, weekend: bool):
    weekend_query = ""
    parameter_bindings: list = [startstation + "%", stopstation + "%"]
    if weekend:
        weekend_query = "AND KjørerHelger LIKE ?"
        parameter_bindings.append(weekend)

    cursor.execute(f"""
    SELECT Startstasjon, Endestasjon, SPR.Avgangstid, SPR.Ankomsttid, Stasjon1, Stasjon2 FROM Togrute as TR
    INNER JOIN StrekningPåRute as SPR ON TR.ID = SPR.TogruteID
    INNER JOIN Delstrekning as DS ON SPR.DelstrekningID = DS.ID
    INNER JOIN Togrutetabell as TT ON TR.Togrutetabell = TT.ID
    WHERE Startstasjon LIKE ?
    AND Endestasjon LIKE ?""" + weekend_query + ";", tuple(parameter_bindings))

    print_table(cursor.fetchall(), ["Startstasjon", "Endestasjon",
                "Avgangstid", "Ankomsttid", "Stasjon1", "Stasjon2"])


dag = input("Skriv inn dato (YYYY-MM-DD): ")
tid = input("Skriv inn tid (HH:MM): ")
if dag == "": dag = "1970-01-01"
if tid == "": tid = "00:00"
dato = datetime.datetime.strptime(dag.strip() + " " + tid.strip(), "%Y-%m-%d %H:%M")
neste_dato = dato + datetime.timedelta(days=1)

start = input("Startstasjon: ")
stopp = input("Endestasjon: ")

print(f"\nTabell for {dato.date()}")
get_route_between_station_by_date(start, stopp, dato, is_weekend(dato))
print(f"\nTabell for {neste_dato.date()}")
get_route_between_station_by_date(start, stopp, neste_dato, is_weekend(neste_dato))

con.close()
