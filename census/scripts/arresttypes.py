import MySQLdb as mdb
import _mysql as mysql
import re

class arresttypes:

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

    def add(self,fullname,description):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO arresttypes(fullname,description) VALUES(%s,%s)",(self.__sanitize(fullname),self.__sanitize(description)))
            cur.close()
            newid = cur.lastrowid
        con.close()
        return newid

    def get(self,arresttypeid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM arresttypes WHERE arresttypeid = %s",(arresttypeid))
            row = cur.fetchone()
            cur.close()
        con.close()
        return row

    def getall(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM arresttypes")
            rows = cur.fetchall()
            cur.close()
        _arresttypes = []
        for row in rows:
            _arresttypes.append(row)
        con.close()
        return _arresttypes

    def delete(self,arresttypeid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM arresttypes WHERE arresttypeid = %s",(arresttypeid))
            cur.close()
        con.close()

    def update(self,arresttypeid,fullname,description):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE arresttypes SET fullname = %s,description = %s WHERE arresttypeid = %s",(self.__sanitize(fullname),self.__sanitize(description),self.__sanitize(arresttypeid)))
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

