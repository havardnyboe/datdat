from print_table import print_table
import sqlite3
con = sqlite3.connect("jernbanenett.db")
cursor = con.cursor()


def get_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return cursor.fetchall()


def deleteall():
    print_table(get_tables(), ["Tabeller"])

    if (input("Er du sikker på at du vil slette alle disse tabellene? (j/n): ").lower() == "j"):
        for table in get_tables():
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Databasen laget med alle tabeller :)")
    else:
        quit()
