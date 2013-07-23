import re
from pprint import pprint

class Inmate:
    name = None
    number = None
    sex = None
    race = None
    dob = None
    custodydate = None
    custodytime = None
    custodyclass = None
    bookings = []
    
    def tostring(self):
        print "\tName: {0}".format(self.name)
        print "\tNumber: {0}".format(self.number)
        print "\tSex: {0}".format(self.sex)
        print "\tRace: {0}".format(self.race)
        print "\tDOB: {0}".format(self.dob)
        print "\tcust date: {0}".format(self.custodydate)
        print "\tcust time: {0}".format(self.custodytime)
        print "\tcust class: {0}".format(self.custodyclass)
        print ""

class Booking:
    bookdate = None
    booktype = None
    custodytype = None
    bail = None
    bond = None
    court = None
    judge = None
    arrestingagency = None
    arrestype = None
    roc = None
    charge = None
    indict = None
    adjusteddate = None
    term = None

def _checknone(dictionary):
    for item in dictionary:
        if item == None:
            return False
    return True

def parseinmates(rawinmates):
    success = True
    inmates = []
    for rawinmate in rawinmates:
        name,rawdata = rawinmate
        inmate = Inmate()
        #booking = None
        inmate.name = name
        #print "{0}".format(name)
        print "Working on '{0}'  ...".format(name)
        for data in rawdata:
            #print "Working on '{0}' ...".format(data)
            if re.match('[0-9]{6} [A-Z] [A-Z] [0-9]{2}-[0-9]{2}-[0-9]{4}',data):
                parts = data.split(' ')
                inmate.number = parts[0]
                inmate.sex = parts[1]
                inmate.race = parts[2]
                inmate.dob = parts[3]
            if re.match('[0-9]{2}-[0-9]{2}-[0-9]{4} [0-9]{4} [A-Z]{3}',data):
                parts = data.split(' ')
                inmate.custodydate = parts[0]
                inmate.custodytime = parts[1]
                inmate.custodyclass = " ".join(parts[2:])
            
            #if _checknone(inmate.__dict__):
            #   break
          
            #f _checknone(booking.__dict__):
            #   inmate.bookings.append(booking)
            #   booking = Booking()
        inmate.tostring()
        inmates.append(inmate)
    return inmates,success
