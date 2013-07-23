from pullpdf import pullpdf
from pullinmates import pullinmates
from parseinmates import parseinmates

def main():
    print "pulling todays census."
    #pdftext,success = pullpdf()
    success = True
    with open("pdftext.txt", "r") as _file:
        pdftext = _file.read()
    if success:
        print "pulling inmates from census data."
        _inmates,success = pullinmates(pdftext)
    if success:
        print "parsing inmate data."
        inmates,success = parseinmates(_inmates)
    if success:
        print "done."
    print "exit."
main()
