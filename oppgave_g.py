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

def findAvailableBeds(togruteforekomst: int, delstrekninger: list):
    # 1. Finn alle senger på den aktuelle togruteforekomsten

    cursor.execute("""
        select Seng.VognID, Seng.Nummer, Seng.Kupenummer 
        from VognIOppsett 
        Inner join Vogn on VognIOppsett.vognid=vogn.id 
        inner join Togrute on togrute.vognoppsett=vognoppsettid 
        inner join togruteforekomst on togrute.id=togruteforekomst.togrute 
        inner join Seng on Seng.vognid=vogn.id 
        where togruteforekomst.id = ?;
    """, (togruteforekomst,))
    
    allBedsOnTogruteforekomst = cursor.fetchall()
    
    # 2. Finn alle salg av senger på alle delstrekninger på den aktuelle togruteforekomsten

    cursor.execute("""
        SELECT BillettTilStrekning.DelstrekningID, Billett.SengVogn, Billett.Sengnummer, Seng.Kupenummer
        FROM BillettTilStrekning
        INNER JOIN Billett ON BillettID=Billett.ID
        INNER JOIN Seng ON ((Billett.Sengnummer=Seng.Nummer) 
            AND (Billett.Sengvogn=Seng.VognID))
        WHERE Togruteforekomst = ?
        AND Billett.SengNummer NOT NULL;
    """, (togruteforekomst,))

    allBedSalesOnTogruteforekomst = cursor.fetchall()

    # 3. Finn kupeer der seng allerede er solgt
        # Alle solgte kupeer(kan inneholde duplikater) på minst en av de valgte delstrekningene:
    soldBedsOnDelstrekninger = set([bed[1:4] for bed in allBedSalesOnTogruteforekomst if (bed[0],) in delstrekninger])
    soldCompartments = set([bed[2] for bed in soldBedsOnDelstrekninger])

    # 4. Finn ledige senger også mtp kupeer
    allAvailableBeds = set(allBedsOnTogruteforekomst).difference(soldBedsOnDelstrekninger)
    availableBeds = [bed for bed in allAvailableBeds if bed[2] not in soldCompartments]

    return availableBeds
    

#Funksjon som finner alle ledige
def findAvailableSeats(togruteforekomst: int, delstrekninger: list): #Returnerer oversikt (liste?) over alle ledige seter
    # 1. Finn alle seter på den aktuelle togruteforekomsten

    cursor.execute("""
        select Sete.VognID, Sete.Nummer 
        from VognIOppsett 
        Inner join vogn on VognIOppsett.vognid=vogn.id 
        inner join togrute on togrute.vognoppsett=vognoppsettid 
        inner join togruteforekomst on togrute.id=togruteforekomst.togrute 
        inner join Sete on Sete.vognid=vogn.id 
        where togruteforekomst.id = ?;
    """, (togruteforekomst,))

    allSeatsOnTogruteforekomst = cursor.fetchall()

    # 2. Finn alle salg av seter på alle delstrekninger på den aktuelle togruteforekomsten
    
    cursor.execute("""
        SELECT BillettTilStrekning.DelstrekningID, Billett.Setevogn, Billett.Setenummer
        FROM BillettTilStrekning 
        INNER JOIN Billett ON BillettID=Billett.ID
        WHERE Togruteforekomst = ?
        AND Billett.Setenummer NOT NULL;
    """, (togruteforekomst,))
    allSeatSalesOnTogruteforekomst = cursor.fetchall()

    
    # 3. Velg ut de setene (ut av alle) som ikke er solgt for noen av de valgte delstrekningene

    # Alle solgte seter(kan inneholde duplikater) på minst en av de valgte delstrekningene:
    soldSeatsOnDelstrekninger = [seat[1:3] for seat in allSeatSalesOnTogruteforekomst if (seat[0],) in delstrekninger]
    
    # Unike solgte seter
    soldSeatsOnDelstrekninger = set(soldSeatsOnDelstrekninger)

    availableSeats = set(allSeatsOnTogruteforekomst).difference(soldSeatsOnDelstrekninger)

    return availableSeats


def chooseSeats(availableSeats, seatCount):
    chosenSeats = []
    availableSeats = sorted(list(availableSeats))
    for i in range(seatCount):
        print(f"Velg ett av de følgende setene ({i+1}/{seatCount}):")
        
        for index, seat in enumerate(availableSeats):
            print(f"#{index+1}: Vogn {seat[0]} - Sete {seat[1]}")
        
        chosenIndex = -1
        while chosenIndex < 1:
            try:
                chosenIndex = int(input("Velg: "))
            except ValueError:
                print("Ikke et gyldig tall!")
                continue

            if not 0 < chosenIndex < len(availableSeats):
                print("Ikke en gyldig valgmulighet!")
                chosenIndex = -1

        chosenSeat = availableSeats[chosenIndex-1]
        chosenSeats.append(chosenSeat)
        del(availableSeats[chosenIndex-1])

    return chosenSeats

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
        FROM Togrute 
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

    if plasstype == "1":
        cursor.execute("""
            INSERT INTO Billett (ID, Togruteforekomst, SeteVogn, SeteNummer, Kundeordrenummer) VALUES (?,?,?,?,?);
        """, (billettID, togruteforekomst, vognID, plassnummer, kundeordrenummer))
        con.commit()
        print(f"Billett til sete {plassnummer} i vogn {vognID} er nå kjøpt. God tur!")
        return billettID
    
    elif plasstype == "2":
        cursor.execute("""
            INSERT INTO Billett (ID, Togruteforekomst, SengVogn, SengNummer, Kundeordrenummer) VALUES (?,?,?,?,?);
        """, (billettID, togruteforekomst, vognID, plassnummer, kundeordrenummer))
        con.commit()
        print(f"Billett til seng {plassnummer} i vogn {vognID} er nå kjøpt. God tur!")
        return billettID
    else:
        print("Ugyldig billettype!")
        return


def ticketToDelstrekning(billettID, delstrekningID):
    cursor.execute("""
        INSERT INTO BillettTilStrekning (BillettID, DelstrekningID) VALUES (?, ?);
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

def findAllDelstrekningerInForekomst(togruteforekomst):
    cursor.execute("""
        Select Togrute.ID, Startstasjon, Endestasjon
        From Togrute
        INNER JOIN Togruteforekomst ON Togrute.ID=Togruteforekomst.Togrute
        WHERE Togruteforekomst.ID=?
    """, (togruteforekomst, ))
    stations = cursor.fetchone()
    routes = routesWithStations(stations[1], stations[2])
    for route in routes:
        if route[11] == togruteforekomst:
            startNum = route[2]
            endNum = route[7]
    return findStrekningerBetween(stations[0], startNum, endNum)


def orderTickets():
    route = selectRoute()
    togruteforekomst = route[11]

    harSittevogn, harSovevogn = findVogntyper(route[0])
    if harSittevogn and harSovevogn:
        print("Ønsker du sitteplass, velg #1. Ønsker du sengeplass, velg #2: ")
        plass = -1
        while plass not in ["1", "2"]:
            plass = input("#: ")
    elif harSittevogn and not harSovevogn:
        print("Det er kun sitteplasser tilgjengelig på denne strekningen.")
        plass = "1"
    elif harSovevogn and not harSittevogn:
        print("Det er kun sengeplasser tilgjengelig på denne strekningen.")
        plass = "2"

    plasstype = {"1": "sitte", "2": "senge"}
    if plass == "1": 
        strekninger = findStrekningerBetween(route[0], route[2], route[7])   
        availablePlass = findAvailableSeats(togruteforekomst, strekninger)
    elif plass == "2":
        strekninger = findAllDelstrekningerInForekomst(togruteforekomst)
        availablePlass = findAvailableBeds(togruteforekomst, strekninger)

    print(f"Det finnes {len(availablePlass)} ledige {plasstype[plass]}plasser på den valgte strekningen")

    numberOfSeats = -1
    while numberOfSeats < 1:
        try:
            numberOfSeats = int(input(f"Hvor mange {plasstype[plass]}plasser ønsker du? "))
        except ValueError:
            print("Ikke et gyldig tall!")
            continue
        if not 0 < numberOfSeats <= len(availablePlass):
            print("Ikke en gyldig valgmulighet!")
            numberOfSeats = -1

    
    chosenSeats = chooseSeats(availablePlass, numberOfSeats)
    

    ordrenummer = createKundeordre(getKunde(input("Logg inn: ")))
    # billettID = buyTicket(togruteforekomst, plass, 2, 3, ordrenummer)
    for seat in chosenSeats:
        billettID = buyTicket(togruteforekomst, plass, seat[0], seat[1], ordrenummer)
        for strekning in strekninger:
            ticketToDelstrekning(billettID, strekning[0])


orderTickets()
# print(findAvailableSeats(1, []))
con.close()
# getTogruteforekomster()
