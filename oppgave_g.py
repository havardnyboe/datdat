import sqlite3
import re
import datetime
import uuid
from print_table import print_table

con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()
# Håndtere billettkjøp for de tre togrutene
# Billett kan være for: 3.april ELLER 4.april

def getKunde(email):
    cursor.execute("SELECT Kundenummer FROM Kunde WHERE ? LIKE Kunde.Epostadresse", (email, ))
    return cursor.fetchone()[0]

def isRegistered():
    email = input("Hvis du allerede er registrert bruker, skriv inn din mail. Hvis du ikke er registrert, må du gjøre det først.")
    if re.match("\w+@\w+\.\w+", email):
        return getKunde(email)
    else:
        return False
    
def totalBeds(togruteID):
    cursor.execute("""
        SELECT COUNT(Seng.Nummer)
            FROM VognIOppsett 
            INNER JOIN Vogn ON VognIOppsett.VognID = Vogn.ID
            INNER JOIN Vognoppsett ON VognIOppsett.VognoppsettID = Vognoppsett.ID
            INNER JOIN Togrute ON Togrute.Vognoppsett = Vognoppsett.id
            INNER JOIN Seng ON Seng.VognID = Vogn.ID
            WHERE Togrute.ID = ?;
    """,(togruteID,))
    return(cursor.fetchone()[0])


def totalSeats(togruteID):
    cursor.execute("""
        SELECT COUNT(Sete.Nummer)
            FROM VognIOppsett 
            INNER JOIN Vogn ON VognIOppsett.VognID = Vogn.ID
            INNER JOIN Vognoppsett ON VognIOppsett.VognoppsettID = Vognoppsett.ID
            INNER JOIN Togrute ON Togrute.Vognoppsett = Vognoppsett.id
            INNER JOIN Sete ON Sete.VognID = Vogn.ID
            WHERE Togrute.ID = ?;
    """,(togruteID,))
    return(cursor.fetchone()[0])


#Funksjon som lager alle billetter som er koblet mot alle seter
def ticketToSeatSetup(): #Returnerer map mellom sete og billett
    pass

#Funksjon som finner alle ledige
def findFreeTickets(Togruteforekomst): #Returnerer oversikt (liste?) over alle ledige seter
    cursor.execute("""
    SELECT ID, SengeNummer, SengeVogn, SeteNummer, SeteVogn FROM Billett WHERE Kundeordrenummer == NULL && Togruteforekomst == Billett.Togruteforekomst
    """)


#Funksjon som lar booke ett av de ledige
def bookASeat(togruteforekomst): #Tar inn setet man ønsker å booke
    antallBiletter = input("Hvor mange biletter ønsker du å kjøpe")
    for n in range (antallBiletter):
        billettID = input("Hva er ID på"+n+"'te billetten du ønsker å booke?")
        seteEllerSeng = input("Skal den være til et sete(1) eller en seng(2)")
        nummer = input("Hvilke sete/sengenummer")
        vognNummer = input("Hvilke vognnummer skal den tilhøre")
        Kundeordrenummer = str(uuid.uuid4())

        # if seteEllerSeng == 1:
        #     cursor.execute("""
        #         INSERT INTO Billett ("""+billettID+""","""+togruteforekomst+""", NULL, NULL, """+nummer+""","""+vognNummer+""","""+Kundeordrenummer""")""")
        # elif seteEllerSeng == 2:
        #     cursor.execute("""
        #         INSERT INTO Billett ("""+billettID+""","""+togruteforekomst+""","""+nummer+""","""+vognNummer+""", NULL, NULL"""+Kundeordrenummer""")""")

# def getTogruteforekomster():
#     start = input("Hvor ønsker du å reise fra? ")
#     end = input("Hvor ønsker du å reise til? ")
#     select_labels = "TRF.ID, TR.ID, DS.ID, TRF.Dato, SPR.Avgangstid, SPR.Ankomsttid, DS.Stasjon1, DS.Stasjon2"

#     cursor.execute("""
#         SELECT """ + select_labels + """
#         FROM Togruteforekomst as TRF 
#         INNER JOIN Togrute as TR ON TRF.Togrute = TR.ID
#         INNER JOIN StrekningPåRute as SPR ON TR.ID = SPR.TogruteID
#         INNER JOIN Delstrekning as DS ON SPR.DelstrekningID = DS.ID
#         WHERE DS.Stasjon1 LIKE ?
#         OR DS.Stasjon2 LIKE ?
#         GROUP BY TRF.ID HAVING COUNT(TRF.ID) = 1
#         ORDER BY TRF.Dato ASC
#         ;
#     """, (start + "%", end + "%"))

#     print_table(cursor.fetchall(), select_labels.split(", "))

def findStrekningerBetween(routeId, stationNumStart, stationNumEnd):
    strekninger = []
    for stationNum in range(stationNumStart, stationNumEnd):
        cursor.execute("""
        SELECT Delstrekning.* FROM Delstrekning, StasjonerITabell A, StasjonerITabell B
            WHERE (A.TogrutetabellID = ? AND B.TogrutetabellID = ?)
            AND (A.Stasjonnummer = ? AND B.Stasjonnummer = ?)
            AND (
                (A.Jernbanestasjon = Delstrekning.Stasjon1 AND B.Jernbanestasjon = Delstrekning.Stasjon2) OR
                (A.Jernbanestasjon = Delstrekning.Stasjon2 AND B.Jernbanestasjon = Delstrekning.Stasjon1)
            );
        """, (routeId, routeId, stationNum, stationNum+1))
        strekninger.append(cursor.fetchone())
    
    return strekninger

def routesWithStations(a, b):
    cursor.execute("""
        SELECT A.*, B.* FROM StasjonerITabell A, StasjonerITabell B
        WHERE A.TogrutetabellID = B.TogrutetabellID
        AND A.Stasjonnummer < B.Stasjonnummer
        AND A.Jernbanestasjon LIKE ?
        AND B.Jernbanestasjon LIKE ?;
    """, (a+"%", b+"%"))
    
    routes = cursor.fetchall()
    return routes

def orderTickets():
    start = input("Hvor ønsker du å reise fra? ")
    end = input("Hvor ønsker du å reise til? ")

    routes = routesWithStations(start, end)

    if len(routes) == 0:
        print("Vi har dessverre ingen aktive ruter på denne strekningen.")
        return
    
    elif len(routes) > 1:
        print("Vi har funnet flere mulige ruter. Vennligst velg:")
        for index,option in enumerate(routes):
            print(f"#{index+1}: Fra {option[1]} klokken {option[3]} -- Til {option[6]} klokken {option[8]}")
        
        select = input("#:")
        # TODO: Dangerous
        route = routes[int(select)-1]
    
    print("Du har valgt ruten:")
    print(route) #TODO: Prettyprint

    strekninger = findStrekningerBetween(route[0], route[2], route[7])
    print(strekninger)

orderTickets()

# getTogruteforekomster()

# for i in range(1, 4):
#     print("="*8+f"\nTogrute {i}")
#     print(f"{totalBeds(i)} Sengeplasser")
#     print(f"{totalSeats(i)} Seter\n")


# SELECT TogruteID, DS.Stasjon1, DS.Stasjon2 FROM StrekningPåRute AS SPR
# SELECT * FROM StrekningPåRute AS SPR
# INNER JOIN (
#     SELECT TR.ID TRID, Startstasjon, Endestasjon, SPR.Avgangstid, SPR.Ankomsttid, Stasjon1, Stasjon2 FROM Togrute as TR
#     INNER JOIN StrekningPåRute as SPR ON TRID = SPR.TogruteID
#     INNER JOIN Delstrekning as DS ON SPR.DelstrekningID = DS.ID
#     INNER JOIN Togrutetabell as TT ON TR.Togrutetabell = TT.ID
#     WHERE Stasjon1 LIKE "Steinkjer%"
#     OR Stasjon2 LIKE "fauske%") AS RES ON SPR.TogruteID = RES.TRID
# INNER JOIN Delstrekning as DS ON SPR.DelstrekningID = DS.ID;
