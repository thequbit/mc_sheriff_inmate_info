import re
from pprint import pprint

def _checknone(_tuple):
    if None in _tuple:
        return False
    return True

def _nones15():
    return None,None,None,None,None,None,None,None,None,None,None,None,None,None,None

def _nones7():
    return None,None,None,None,None,None,None

def parseinmates(rawinmates):
    success = True
    inmates = []
    for rawinmate in rawinmates:
        name,rawdata = rawinmate
        number,sex,race,dob,custodydate,custodytime,custodyclass = _nones7() 
        for data in rawdata:
            #print "Working on '{0}' ...".format(data)
            if re.match('([0-9]{6}) [A-Z] [A-Z] ([0-9]{2})-([0-9]{2})-([0-9]{4})',data):
                #print "here."
                parts = data.split(' ')
                number = parts[0]
                sex = parts[1]
                race = parts[2]
                dob = parts[3]
            if re.match('[0-9]{2}-[0-9]{2}-[0-9]{4} [0-9]{4} [A-Z]{3}',data):
                #print "here2"
                parts = data.split(' ')
                custodydate = parts[0]
                custodytime = parts[1]
                custodyclass = " ".join(parts[2:])
 
            inmate = (name,number,sex,race,dob,custodydate,custodytime,custodyclass)

            if _checknone(inmate):
                bookings = []
                bookdate,booktype,custodytype,bail,bond,court,expectedrelease,judge,arrestingagency,arresttype,roc,charge,indict,adjusteddate,term = _nones15()
                for _data in rawdata:
                    if re.match('Book Dt:',_data):
                        bookdate = _data.split(':')[1].strip()
                    if re.match('Book Typ:',_data):
                        booktype = _data.split(':')[1].strip()
                    if re.match('Cus Typ:',_data):
                        custodytype = _data.split(':')[1].strip()
                    if re.match('Bail:',_data):
                        bail = _data.split(':')[1].strip()
                    if re.match('Bond:',_data):
                        bond = _data.split(':')[1].strip()
                    if re.match('Court:',_data):
                        court = _data.split(':')[1].strip()
                    if re.match('Exp Rel:',_data):
                        expectedrelease = _data.split(':')[1].strip()
                    if re.match('Judge:',_data):
                        judge = _data.split(':')[1].strip()
                    if re.match('Arr Agy:',_data):
                        arrestingagency = _data.split(':')[1].strip()
                    if re.match('Arr Typ',_data):
                        arresttype = _data.split(':')[1].strip()
                    if re.match('ROC:',_data):
                        roc = _data.split(':')[1].strip()
                    if re.match('Chg:',_data):
                        charge = _data.split(':')[1].strip()
                    if re.match('Indict:',_data):
                        indict = _data.split(':')[1].strip()
                    if re.match('Adj Dt:',_data):
                        adjusteddate = _data.split(':')[1].strip()
                    if re.match('Term:',_data):
                        term = _data.split(':')[1].strip()
                    booking = (bookdate,booktype,custodytype,bail,bond,court,judge,arrestingagency,
                               arresttype,roc,charge,indict,adjusteddate,term)
                    if _checknone(booking):
                        bookings.append(booking)
                        bookdate,booktype,custodytype,bail,bond,court,expectedrelease,judge,arrestingagency,arresttype,roc,charge,indict,adjusteddate,term = _nones15()

                break
        inmate = (name,number,sex,race,dob,custodydate,custodytime,custodyclass,bookings)
        inmates.append(inmate)
        inmate = None
    return inmates,success
