import MySQLdb as mdb
import _mysql as mysql
import re

class bookings:

    __settings = {}
    __con = False

    def __init__(self):
        configfile = "sqlcreds.txt"
        f = open(configfile)
        for line in f:
            # skip comment lines
            m = re.search('^\s*#', line)
            if m:
                continue

            # parse key=value lines
            m = re.search('^(\w+)\s*=\s*(\S.*)$', line)
            if m is None:
                continue

            self.__settings[m.group(1)] = m.group(2)
        f.close()

    def __connect(self):
        con = mdb.connect(host=self.__settings['host'], user=self.__settings['username'], passwd=self.__settings['password'], db=self.__settings['database'])
        return con

    def __sanitize(self,valuein):
        if type(valuein) == 'str':
            valueout = mysql.escape_string(valuein)
        else:
            valueout = valuein
        return valuein

    def add(self,inmateid,censusdate,scraperrunid,bookdatetime,booktype,custodytype,bail,bond,court,courtid,expectedrelease,judge,judgeid,arrestingagency,arrestingagencyid,arresttype,roc,charge,chargeid,indict,adjusteddate,term):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO bookings(inmateid,censusdate,scraperrunid,bookdatetime,booktype,custodytype,bail,bond,court,courtid,expectedrelease,judge,judgeid,arrestingagency,arrestingagencyid,arresttype,roc,charge,chargeid,indict,adjusteddate,term) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.__sanitize(inmateid),self.__sanitize(censusdate),self.__sanitize(scraperrunid),self.__sanitize(bookdatetime),self.__sanitize(booktype),self.__sanitize(custodytype),self.__sanitize(bail),self.__sanitize(bond),self.__sanitize(court),self.__sanitize(courtid),self.__sanitize(expectedrelease),self.__sanitize(judge),self.__sanitize(judgeid),self.__sanitize(arrestingagency),self.__sanitize(arrestingagencyid),self.__sanitize(arresttype),self.__sanitize(roc),self.__sanitize(charge),self.__sanitize(chargeid),self.__sanitize(indict),self.__sanitize(adjusteddate),self.__sanitize(term)))
            cur.close()
            newid = cur.lastrowid
        con.close()
        return newid

    def get(self,bookingid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM bookings WHERE bookingid = %s",(bookingid))
            row = cur.fetchone()
            cur.close()
        con.close()
        return row

    def getall(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM bookings")
            rows = cur.fetchall()
            cur.close()
        _bookings = []
        for row in rows:
            _bookings.append(row)
        con.close()
        return _bookings

    def delete(self,bookingid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM bookings WHERE bookingid = %s",(bookingid))
            cur.close()
        con.close()

    def update(self,bookingid,inmateid,censusdate,scraperrunid,bookdatetime,booktype,custodytype,bail,bond,court,courtid,expectedrelease,judge,judgeid,arrestingagency,arrestingagencyid,arresttype,roc,charge,chargeid,indict,adjusteddate,term):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE bookings SET inmateid = %s,censusdate = %s,scraperrunid = %s,bookdatetime = %s,booktype = %s,custodytype = %s,bail = %s,bond = %s,court = %s,courtid = %s,expectedrelease = %s,judge = %s,judgeid = %s,arrestingagency = %s,arrestingagencyid = %s,arresttype = %s,roc = %s,charge = %s,chargeid = %s,indict = %s,adjusteddate = %s,term = %s WHERE bookingid = %s",(self.__sanitize(inmateid),self.__sanitize(censusdate),self.__sanitize(scraperrunid),self.__sanitize(bookdatetime),self.__sanitize(booktype),self.__sanitize(custodytype),self.__sanitize(bail),self.__sanitize(bond),self.__sanitize(court),self.__sanitize(courtid),self.__sanitize(expectedrelease),self.__sanitize(judge),self.__sanitize(judgeid),self.__sanitize(arrestingagency),self.__sanitize(arrestingagencyid),self.__sanitize(arresttype),self.__sanitize(roc),self.__sanitize(charge),self.__sanitize(chargeid),self.__sanitize(indict),self.__sanitize(adjusteddate),self.__sanitize(term),self.__sanitize(bookingid)))
            cur.close()
        con.close()

##### Application Specific Functions #####

#    def myfunc():
#        con = self.__connect()
#        with con:
#            cur = son.cursor()
#            cur.execute("")
#            row = cur.fetchone()
#            cur.close()
#        con.close()
#        return row

