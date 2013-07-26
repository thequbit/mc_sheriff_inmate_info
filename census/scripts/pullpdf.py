import os
import re
import urllib
import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

def _downloadpdf(url):
    f = urlopen(url)
    filename = "./pdfs/{0}".format(os.path.basename(url))
    with open(filename, "wb") as local_file:
        local_file.write(f.read())
    return filename 

def _decodepdf(filename,DEBUG=False):
   
    pdfstr = ""
    if DEBUG:
        with open("rawfile.txt","r") as rawfile:
            pdfstr = rawfile.read()
    else:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

        fp = file(filename, 'rb')
        process_pdf(rsrcmgr, device, fp)
        fp.close()
        device.close()

        pdfstr = retstr.getvalue()
        retstr.close()
   
        with open("rawfile.txt","w") as rawfile:
            rawfile.write(pdfstr)
 
    labels = ['Book Dt:','Book Typ:','Cus Typ:','Bail:','Bond:','Court:','Judge:',
              'Exp Rls:','Arr Agy:','Arr Typ:','ROC:','Chg:','Indict:','Adj Dt:','Term:']
    
    for label in labels:
        pdfstr = pdfstr.replace(label,"\n{0} ".format(label))

    # preprocess to get rid of duplicate spaces and \n's
    pdfstr = re.sub(' +',' ',pdfstr)
    pdfstr = re.sub('\n+','\n',pdfstr)

    # handle current sentence going to next line 
    # (time from custody date/time + first three capital leters form sentence type)
    pdfstr = re.sub('([0-9]{4})(?: )?\n([A-Z]{3})','\\1 \\2',pdfstr)

    with open("rawfile2.txt","w") as rawfile:
        rawfile.write(pdfstr)

    # handle inmate ID not being on same line as inmate data
    # (in some casses mcid, sex, race, and dob can all be on different lines ...)
    pdfstr = re.sub('([0-9]{6})(?: )?(?:\n)?([A-Z])(?: )?(?:\n)?([A-Z])(?: )?(?:\n)?([0-9]{2}-[0-9]{2}-[0-9]{2})','\\1 \\2 \\3 \\4',pdfstr)
    
    with open("rawfile3.txt","w") as rawfile:
        rawfile.write(pdfstr)

    # remove page header
    pdfstr = re.sub('Current Census for Date: [0-9]{2}-[0-9]{2}-[0-9]{4}(?: )?(?:\n)?','',pdfstr)
    pdfstr = re.sub('Name(?: )?(?:\n)?Location(?: )?(?:\n)?','',pdfstr)
    pdfstr = re.sub('MCJ Sex Rce DOB(?: )?(?:\n)?','',pdfstr)
    pdfstr = re.sub('Custody(?: )?(?:\n)?Time(?: )?(?:\n)?Date(?: )?(?:\n)?Classification(?: )?(?:\n)?','',pdfstr)
    pdfstr = re.sub('Min(?: )?(?:\n)?Rel(?: )?(?:\n)?Date(?: )?(?:\n)?','',pdfstr)

    # remove page footers
    pdfstr = re.sub('Facility:(?: )?(?:\n)?','',pdfstr)
    pdfstr = re.sub('Page \d+ of \d+(?: )?(?:\n)?','',pdfstr) 
    pdfstr = re.sub('Printed:(?: )?\n([0-9]{2}-[0-9]{2}-[0-9]{4}) [0-9]{4}','',pdfstr)

    # page-to-page formating issue
    pdfstr = re.sub('\x0C(?: )?(?:\n)?','',pdfstr) 

    # Note: probably not nessisary
    # post-process to get rid of duplicate spaces and \n's
    pdfstr = re.sub(' +',' ',pdfstr)
    pdfstr = re.sub('\n+','\n',pdfstr)

    with open("rawfile4.txt","w") as rawfile:
        rawfile.write(pdfstr)

    return pdfstr,True

def pullpdf(url="http://www2.monroecounty.gov/sheriff-inmate",baseurl="http://www2.monroecounty.gov",linktext="Inmate Census"):
    DEBUG = True
    pdftext = ""
    success = False
    filename = ""
    if DEBUG:
        pdftext,success = _decodepdf(filename,DEBUG)
    else:
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html)
        atags = soup.find_all('a', href=True)
        for tag in atags:
            tagstr = None
            if tag.string != None:
                tagstr = tag.string.encode("utf8").lower()
                if tagstr.strip() == linktext.encode("utf8").lower().strip():
                    pdfurl = "{0}{1}".format(baseurl,tag['href'])
                    filename = _downloadpdf(pdfurl)
                    pdftext,success = _decodepdf(filename)
                    with open("pdftext.txt", "w") as txtfile:
                        txtfile.write(pdftext)
                    break
    return (pdftext,success)
