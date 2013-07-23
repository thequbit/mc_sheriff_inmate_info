from pullpdf import pullpdf
from pullinmates import pullinmates
from parseinmates import parseinmates

import sqlite3 as lite

def main(DEBUG=False):
    print "pulling todays census."
    if DEBUG == True:
        success = True
        with open("pdftext.txt", "r") as _file:
            pdftext = _file.read()
    else:
        pdftext,success = pullpdf()
    if success:
        print "pulling inmates from census data."
        _inmates,success = pullinmates(pdftext)
    if success:
        print "parsing booking information for {0} inmates ...".format(len(_inmates))
        inmates,success = parseinmates(_inmates)
    if success:
        print "{0} inmates processed successfully.".format(len(inmates))
    if success:
        print "Creating SQLite3 database ..."
        con = lite.connect('inmates.db')

        with con:
            cur = con.cursor()

            q = "PRAGMA foreign_keys = ON"
            cur.execute(q)

            q = ("CREATE TABLE inmates("
            "inmateid INTEGER PRIMARY KEY, "
            "name TEXT, "
            "number INTEGER, "
            "sex TEXT, "
            "race TEXT, "
            "dob TEXT, "
            "custodydate TEXT, "
            "custodytime TEXT, "
            "custodyclass TEXT"
            ")")
            cur.execute(q)
    
            q = ("CREATE TABLE bookings("
            "bookingid INTEGER PRIMARY KEY, "
            "inmateid INTEGER, "
            "bookdate TEXT, "
            "booktype TEXT, "
            "custodytype TEXT, "
            "bail TEXT, "
            "bond TEXT, "
            "court TEXT, "
            "judge TEXT, "
            "arrestingagency TEXT, "
            "arrestype TEXT, "
            "roc TEXT, "
            "charge TEXT, "
            "indict TEXT, "
            "adjusteddate TEXT, "
            "term TEXT, "
            "FOREIGN KEY(inmateid) REFERENCES inmates(inmateid)"
            ")")
            cur.execute(q)
    
            print "Saving inmate data to SQLite3 database ..."
    
            inmatecount = 0
            bookingcount = 0
    
            for inmate in inmates:
                name,number,sex,race,dob,custodydate,custodytime,custodyclass,bookings = inmate
    
                q = ("INSERT INTO inmates("
                "name,"
                "number,"
                "sex,"
                "race,"
                "dob,"
                "custodydate,"
                "custodytime,"
                "custodyclass"
                ") "
                "VALUES(?,?,?,?,?,?,?,?)")
                cur.execute(q,(name,number,sex,race,dob,custodydate,custodytime,custodyclass))
    
                q = "SELECT last_insert_rowid()"
                cur.execute(q)
                inmateid, = cur.fetchone()
    
                for booking in bookings:
                    bookdate,booktype,custodytype,bail,bond,court,judge,arrestingagency,arresttype,roc,charge,indict,adjusteddate,term = booking
                    q = ("INSERT INTO bookings("
                    "inmateid,"
                    "bookdate,"
                    "booktype,"
                    "custodytype,"
                    "bail,"
                    "bond,"
                    "court,"
                    "judge,"
                    "arrestingagency,"
                    "arrestype,"
                    "roc,"
                    "charge,"
                    "indict,"
                    "adjusteddate,"
                    "term"
                    ") "
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
                    cur.execute(q,(inmateid,bookdate,booktype,custodytype,bail,bond,court,judge,arrestingagency,arresttype,roc,charge,indict,adjusteddate,term))
                    bookingcount += 1
                inmatecount += 1
        print "Added {0} inmates and {1} bookings to the SQLite3 database.".format(inmatecount,bookingcount)
    print "Exiting."

main()
