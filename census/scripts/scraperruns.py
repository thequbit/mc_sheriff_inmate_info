import MySQLdb as mdb
import _mysql as mysql
import re

class scraperruns:

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

    def add(self,rundt,newdatafound,success,filename,inmatecount,bookingscount,newinmates):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO scraperruns(rundt,newdatafound,success,filename,inmatecount,bookingscount,newinmates) VALUES(%s,%s,%s,%s,%s,%s,%s)",(self.__sanitize(rundt),self.__sanitize(newdatafound),self.__sanitize(success),self.__sanitize(filename),self.__sanitize(inmatecount),self.__sanitize(bookingscount),self.__sanitize(newinmates)))
            cur.close()
            newid = cur.lastrowid
        con.close()
        return newid

    def get(self,scraperrunid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM scraperruns WHERE scraperrunid = %s",(scraperrunid))
            row = cur.fetchone()
            cur.close()
        con.close()
        return row

    def getall(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM scraperruns")
            rows = cur.fetchall()
            cur.close()
        _scraperruns = []
        for row in rows:
            _scraperruns.append(row)
        con.close()
        return _scraperruns

    def delete(self,scraperrunid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM scraperruns WHERE scraperrunid = %s",(scraperrunid))
            cur.close()
        con.close()

    def update(self,scraperrunid,rundt,newdatafound,success,filename,inmatecount,bookingscount,newinmates):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE scraperruns SET rundt = %s,newdatafound = %s,success = %s,filename = %s,inmatecount = %s,bookingscount = %s,newinmates = %s WHERE scraperrunid = %s",(self.__sanitize(rundt),self.__sanitize(newdatafound),self.__sanitize(success),self.__sanitize(filename),self.__sanitize(inmatecount),self.__sanitize(bookingscount),self.__sanitize(newinmates),self.__sanitize(scraperrunid)))
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

