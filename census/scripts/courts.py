import MySQLdb as mdb
import _mysql as mysql
import re

class courts:

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

    def add(self,shortname,fullname,description):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO courts(shortname,fullname,description) VALUES(%s,%s,%s)",(self.__sanitize(shortname),self.__sanitize(fullname),self.__sanitize(description)))
            cur.close()
            newid = cur.lastrowid
        con.close()
        return newid

    def get(self,courtid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM courts WHERE courtid = %s",(courtid))
            row = cur.fetchone()
            cur.close()
        con.close()
        return row

    def getall(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM courts")
            rows = cur.fetchall()
            cur.close()
        _courts = []
        for row in rows:
            _courts.append(row)
        con.close()
        return _courts

    def delete(self,courtid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM courts WHERE courtid = %s",(courtid))
            cur.close()
        con.close()

    def update(self,courtid,shortname,fullname,description):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE courts SET shortname = %s,fullname = %s,description = %s WHERE courtid = %s",(self.__sanitize(shortname),self.__sanitize(fullname),self.__sanitize(description),self.__sanitize(courtid)))
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

