import MySQLdb as mdb
import _mysql as mysql
import re

class custodies:

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

    def __connect():
        con = mdb.connect(host=self.__settings['host'], user=self.__settings['username'], passwd=self.__settings['password'], db=self.__settings['database'])
        return con

    def __sanitize(self,valuein):
        if type(valuein) == 'str':
            valueout = mysql.escape_string(valuein)
        else:
            valueout = valuein
        return valuein

    def add(self,inmateid,custodydate,custodytime,custodyclass):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO custodies(inmateid,custodydate,custodytime,custodyclass) VALUES(%s,%s,%s,%s)",(self.__sanitize(inmateid),self.__sanitize(custodydate),self.__sanitize(custodytime),self.__sanitize(custodyclass)))
            cur.close()
            newid = cur.lastrowid
        con.close()
        return newid

    def get(self,custodyid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM custodies WHERE custodyid = %s",(custodyid))
            row = cur.fetchone()
            cur.close()
        con.close()
        return row

    def getall(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM custodies")
            rows = cur.fetchall()
            cur.close()
        _custodies = []
        for row in rows:
            _custodies.append(row)
        con.close()
        return _custodies

    def delete(self,custodyid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM custodies WHERE custodyid = %s",(custodyid))
            cur.close()
        con.close()

    def update(self,custodyid,inmateid,custodydate,custodytime,custodyclass):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE custodies SET inmateid = %s,custodydate = %s,custodytime = %s,custodyclass = %s WHERE custodyid = %s",(self.__sanitize(inmateid),self.__sanitize(custodydate),self.__sanitize(custodytime),self.__sanitize(custodyclass),self.__sanitize(custodyid)))
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

