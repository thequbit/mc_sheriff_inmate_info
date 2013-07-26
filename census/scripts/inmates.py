import MySQLdb as mdb
import _mysql as mysql
import re

class inmates:

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

    def add(self,first,last,middle,mcid,sex,race,dob):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO inmates(first,last,middle,mcid,sex,race,dob) VALUES(%s,%s,%s,%s,%s,%s,%s)",(self.__sanitize(first),self.__sanitize(last),self.__sanitize(middle),self.__sanitize(mcid),self.__sanitize(sex),self.__sanitize(race),self.__sanitize(dob)))
            cur.close()
            newid = cur.lastrowid
        con.close()
        return newid

    def get(self,inmateid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM inmates WHERE inmateid = %s",(inmateid))
            row = cur.fetchone()
            cur.close()
        con.close()
        return row

    def getall(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM inmates")
            rows = cur.fetchall()
            cur.close()
        _inmates = []
        for row in rows:
            _inmates.append(row)
        con.close()
        return _inmates

    def delete(self,inmateid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM inmates WHERE inmateid = %s",(inmateid))
            cur.close()
        con.close()

    def update(self,inmateid,first,last,middle,mcid,sex,race,dob):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE inmates SET first = %s,last = %s,middle = %s,mcid = %s,sex = %s,race = %s,dob = %s WHERE inmateid = %s",(self.__sanitize(first),self.__sanitize(last),self.__sanitize(middle),self.__sanitize(mcid),self.__sanitize(sex),self.__sanitize(race),self.__sanitize(dob),self.__sanitize(inmateid)))
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

