import re
from csv import reader

def splitEscaped(str, by, escapeChar):
    infile = [str]
    return reader(infile, delimiter=by, quotechar=escapeChar)

def removeComments(text):
    p = r'/\*[^*]*\*+([^/*][^*]*\*+)*/|("(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\'|.[^/"\'\\]*)'
    return ''.join(m.group(2) for m in re.finditer(p, text, re.M|re.S) if m.group(2))

def escapeAnnotations(text):
    return re.sub(r'(/\*@)(.*)(\*/)',r'@\2',text)
