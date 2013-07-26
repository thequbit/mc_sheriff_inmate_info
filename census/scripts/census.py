import datetime

# Helper files
from getinmates import getinmates

# DB access layer 
from scraperruns import scraperruns
from inmates import inmates
from custodies import custodies
from judges import judges
from courts import courts
from arrestingagencies import arrestingagencies
from arresttypes import arresttypes
from charges import charges
from bookings import bookings



def main(DEBUG=False):
    print "Pulling inmates from the interwebs ..."

    theinmates,success = getinmates(DEBUG)
    if success:
        print "Imates pulled successfully, pushing to database."
    else:
        raise Exception("Something bad happened ... no inmates were pulled.")

    print "Pushing {0} inmates to the database ...".format(len(theinmates))

    i = inmates()
    for inmate in theinmates:
        name,mcid,sex,race,dob,custodydate,custodytime,custodyclass,bookings = inmate
        parts = name.split(',')
        first = parts[0]
        parts2 = parts[1].rsplit(' ',1)[0]
        last = parts[1]
        if len(parts2) != 0:
            last = parts2[0]
        middle = ""
        if len(parts2) == 2:
            middle = parts2[1]
        try:
            isodob = datetime.datetime.strptime(dob, '%m-%d-%Y').date().isoformat()
        except:
            print "name: {0}, dob: ".format(name,dob)
            raise Exception("error.")
        i.add(first,last,middle,mcid,sex,race,isodob)

main()
