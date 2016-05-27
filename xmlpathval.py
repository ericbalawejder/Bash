#!/usr/bin/env python

from lxml import etree
from optparse import OptionParser
import sys
import os.path

parser = OptionParser()

(opts, args) = parser.parse_args()

if len(args) != 1 and len(args) != 2:
    print "%s <XML file> [ <XPath expression> ]" % __file__
    sys.exit(1)
    
infile,expr = (args + [None])[:2]

if not os.path.isfile(infile):
    print "no such file: %s" % infile
    sys.exit(1)

try:
    dtdparser = etree.XMLParser(dtd_validation=True)
    doc = etree.parse(infile, parser=dtdparser)
except Exception as err:
    print '%s' % err
    sys.exit(1)
    
if len(args) == 1:
    sys.exit(0)

try:
    r = doc.xpath(expr)
except Exception as err:
    print '%s' % err
    sys.exit(1)

if isinstance(r,(str,int,float,bool)):
    print r
    sys.exit(0)

for node in r:
    if isinstance(node, etree._ElementStringResult):
        print node
    else:
        print "invalid path expression: %s" % expr
        sys.exit(1)

