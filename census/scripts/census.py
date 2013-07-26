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
        parts = name.replace('.','').split(',')
        last = parts[0].strip()
        if parts[1].rsplit(' ',1)[0] == "":
            first = parts[1].strip()
            middle = ""
        else:
            # take off middle
            first = parts[1][:-2].strip()
            middle = parts[1][-1:]
        
        try:
            isodob = datetime.datetime.strptime(dob, '%m-%d-%Y').date().isoformat()
        except:
            print "name: {0}, dob: ".format(name,dob)
            raise Exception("error.")
        
        i.add(first,last,middle,mcid,sex,race,isodob)
        #print "name = {0}, first = {1}, last = {2}, middle = {3}".format(name,first,last,middle)
        #raise Exception("you shall not pass.")
main()
