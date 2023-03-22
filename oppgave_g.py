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
            INNER JOIN Vogn ON (VognIOppsett.VognID = Vogn.ID)
            INNER JOIN Vognoppsett ON (VognIOppsett.VognoppsettID = Vognoppsett.ID)
            INNER JOIN Togrute ON (Togrute.Vognoppsett = VognoppsettID)
            INNER JOIN Seng ON (Seng.VognID = Vogn.ID)
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


#Funksjon som finner alle ledige
def findAvailableSeats(togruteforekomst): #Returnerer oversikt (liste?) over alle ledige seter
    cursor.execute("""
        select * 
        from VognIOppsett 
        Inner join vogn on VognIOppsett.vognid=vogn.id 
        inner join togrute on togrute.vognoppsett=vognoppsettid 
        inner join togruteforekomst on togrute.id=togruteforekomst.togrute 
        inner join sete on sete.vognid=vogn.id 
        where togruteforekomst.id = ? AND (Sete.VognID AND Sete.Nummer) NOT IN (
            select Setenummer, Setevogn 
            from BillettTilStrekning 
            inner join billett on billettid=billett.id
            WHERE Togruteforekomst = ?
        );
    """, (togruteforekomst, togruteforekomst))

    cursor.execute("""
        select * 
        from VognIOppsett 
        Inner join vogn on VognIOppsett.vognid=vogn.id 
        inner join togrute on togrute.vognoppsett=vognoppsettid 
        inner join togruteforekomst on togrute.id=togruteforekomst.togrute 
        inner join sete on sete.vognid=vogn.id 
        where togruteforekomst.id = ? AND NOT EXISTS (
            select sete.*, billetttilstrekning.* 
            from BillettTilStrekning 
            inner join billett on billettid=billett.id
            WHERE Togruteforekomst = ?
            AND Sete.VognID = Setevogn
            AND Sete.Nummer = Setenummer
        );
    """, (togruteforekomst, togruteforekomst))


    cursor.execute("""
        select BillettTilStrekning.*, Togruteforekomst, Setenummer, Setevogn 
        from BillettTilStrekning 
        inner join billett on billettid=billett.id
        WHERE Togruteforekomst = ?;
    """, (togruteforekomst,))


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
        SELECT Delstrekning.ID FROM Delstrekning, StasjonerITabell A, StasjonerITabell B
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
    # cursor.execute("""
    #     SELECT A.*, B.* 
    #     FROM StasjonerITabell A, StasjonerITabell B
    #     WHERE A.TogrutetabellID = B.TogrutetabellID
    #     AND A.Stasjonnummer < B.Stasjonnummer
    #     AND A.Jernbanestasjon LIKE ?
    #     AND B.Jernbanestasjon LIKE ?;
    # """, (a+"%", b+"%"))
    cursor.execute("""
        SELECT A.*, B.*, Dato, TID
        FROM StasjonerITabell A, StasjonerITabell B
        INNER JOIN (SELECT Togruteforekomst.ID AS TID, Togruteforekomst.Dato, Togrutetabell 
            FROM Togrute INNER JOIN Togruteforekomst ON (Togrute.ID=Togruteforekomst.Togrute))
            ON A.TogrutetabellID=Togrutetabell
        WHERE A.TogrutetabellID = B.TogrutetabellID
        AND A.Stasjonnummer < B.Stasjonnummer
        AND A.Jernbanestasjon LIKE ?
        AND B.Jernbanestasjon LIKE ?
        ORDER BY Dato ASC, Avgangstid ASC;
    """, (a+"%", b+"%"))

    routes = cursor.fetchall()
    return routes

def findVogntyper(togrutetabell):
    cursor.execute("""
        SELECT Vogntype 
        From Togrute 
            INNER JOIN Togrutetabell ON (Togrutetabell=Togrutetabell.ID) 
            INNER JOIN (SELECT * From Vognoppsett 
            INNER JOIN VognIOppsett ON (Vognoppsett.ID=VognoppsettID) 
            INNER JOIN Vogn ON (VognID=Vogn.ID)) ON (Vognoppsett=VognoppsettID)
            WHERE Togrutetabell.ID LIKE ?;
    """, (togrutetabell,))
    types = cursor.fetchall()
    sittevogn = False
    sovevogn = False
    for type in types:
        if not sittevogn: sittevogn = type[0] == "SJ-sittevogn-1"
        if not sovevogn: sovevogn = type[0] == "SJ-sovevogn-1"

    return [sittevogn, sovevogn]

def createKundeordre(kundenummer):
    ordrenummer = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO Kundeordre VALUES (?, ?, ?);
    """, (ordrenummer, kundenummer, datetime.datetime.now()))
    con.commit()
    return ordrenummer


def buyTicket(togruteforekomst, plasstype, vognID, plassnummer, kundeordrenummer):
    billettID = str(uuid.uuid4())
    setevogn = plasstype == "1" if vognID else None
    setenummer = plasstype == "1" if plassnummer else None
    sengvogn = plasstype == "2" if vognID else None
    sengnummer = plasstype == "2" if plassnummer else None
    cursor.execute("""
        INSERT INTO Billett VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (billettID, togruteforekomst, sengnummer, sengvogn, setenummer, setevogn, kundeordrenummer))
    con.commit()
    return billettID

def ticketToDelstrekning(billettID, delstrekningID):
    cursor.execute("""
        INSERT INTO BillettTilStrekning VALUES (?, ?);
    """, (billettID, delstrekningID))
    con.commit()

def selectRoute():
    start = input("Hvor ønsker du å reise fra? ")
    end = input("Hvor ønsker du å reise til? ")

    routes = routesWithStations(start, end)

    if len(routes) == 0:
        print("Vi har dessverre ingen aktive ruter på denne strekningen.")
        return
    
    elif len(routes) > 1:
        print("Vi har funnet flere mulige ruter. Vennligst velg:")
        for index,option in enumerate(routes):
            print(f"#{index+1}: Dato {option[10]}: Fra {option[1]} Kl. {option[3]} -- Til {option[6]} klokken {option[8]}")
        
        select = input("#:")
        # TODO: Dangerous
        route = routes[int(select)-1]
    
    print("Du har valgt ruten:")
    print(f"Dato {option[10]}: Fra: {route[1]} Kl. {route[3]} -- Til {route[6]} Kl. {route[8]}")

    return route


def orderTickets():
    route = selectRoute()
    strekninger = findStrekningerBetween(route[0], route[2], route[7])
    togruteforekomst = route[11]

    vogntyper = findVogntyper(route[0])
    if vogntyper[0] and vogntyper[1]:
        print("Ønsker du sitteplass, velg #1. Ønsker du sengeplass, velg #2: ")
        plass = input("#: ")
    elif vogntyper[0] and (not vogntyper[1]):
        print("Det er kun sitteplasser tilgjengelig på denne strekningen.")
        plass = "1"
    elif (not vogntyper[0]) and vogntyper[1]:
        print("Det er kun sengeplasser tilgjengelig på denne strekningen.")
        plass = "2"

    plasstype = {"1": "sitte", "2": "senge"}
    numberOfSeats = input(f"Hvor mange {plasstype[plass]}plasser ønsker du? ")
    

    ordrenummer = createKundeordre(getKunde(input("Logg inn: ")))
    billettID = buyTicket(togruteforekomst, plass, 1, 3, ordrenummer)
    
    for strekning in strekninger:
        ticketToDelstrekning(billettID, strekning[0])
        
        
        



orderTickets()


con.close()

# getTogruteforekomster()

