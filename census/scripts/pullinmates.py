from pullpdf import pullpdf
import re

def _getlines(pdftext):
    lines = []
    for line in pdftext.split('\n'):
        line = line.strip()
        if line != "":
            lines.append(line)
    return lines

def _getinmates(pdftext):
    success = True
    try:
        indexes = []
        lines = _getlines(pdftext)
        for i in range(0,len(lines)):
            # see if it is a name in all caps
            if re.match("^[A-Z]*$", lines[i].replace(",","").replace(" ","").replace(".","").replace("-","")):
                indexes.append(i)
                #print "Inmate: {0}".format(lines[i])
        inmates = []
        for i in range(0,len(indexes)-1):
            inmatedata = []
            datarange = indexes[i+1]-indexes[i]-1
            for j in range(0,datarange):
                inmatedata.append(lines[indexes[i]+j])
            inmates.append((lines[indexes[i]],inmatedata))
    except:
        success = False
    return inmates,success

def pullinmates(pdftext):
    inmates = []
    inmates,success = _getinmates(pdftext)
    return inmates,success
