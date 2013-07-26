import MySQLdb as mdb
import _mysql as mysql
import re

class judges:

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

    def add(self,fullname,first,middle,last):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO judges(fullname,first,middle,last) VALUES(%s,%s,%s,%s)",(self.__sanitize(fullname),self.__sanitize(first),self.__sanitize(middle),self.__sanitize(last)))
            cur.close()
            newid = cur.lastrowid
        con.close()
        return newid

    def get(self,judgeid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM judges WHERE judgeid = %s",(judgeid))
            row = cur.fetchone()
            cur.close()
        con.close()
        return row

    def getall(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM judges")
            rows = cur.fetchall()
            cur.close()
        _judges = []
        for row in rows:
            _judges.append(row)
        con.close()
        return _judges

    def delete(self,judgeid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM judges WHERE judgeid = %s",(judgeid))
            cur.close()
        con.close()

    def update(self,judgeid,fullname,first,middle,last):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE judges SET fullname = %s,first = %s,middle = %s,last = %s WHERE judgeid = %s",(self.__sanitize(fullname),self.__sanitize(first),self.__sanitize(middle),self.__sanitize(last),self.__sanitize(judgeid)))
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

