from pullpdf import pullpdf
from pullinmates import pullinmates
from parseinmates import parseinmates

def getinmates(DEBUG=False):
    inmates = []
    sucess = False
    if DEBUG == True:
        success = True
        with open("pdftext.txt", "r") as _file:
            pdftext = _file.read()
    else:
        pdftext,success = pullpdf()
    if success:
        _inmates,success = pullinmates(pdftext)
    if success:
        inmates,success = parseinmates(_inmates)
    return inmates
