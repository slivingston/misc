#!/usr/bin/env python
#
# pullpdfs.py
#
# Because this script generates a list of URLs for the found pdf
# files, it may be used to download all files in succession by
# wget. For example, suppose you wish to download all PDF files at
# http://foobar.net/secret/files.html
#
# ./pullpdfs.py foobar.net secret/files.html | wget -i -
#
#
# NOTES: - This code uses non-standard documentation
#          and probably other styles... and is generally
#          non-optimized. Please update!
#
# Scott Livingston  <slivingston@caltech.edu>
# March, April, August 2010.
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import httplib
import re


# Currently disallow use as a module
if __name__ != '__main__':
    print 'Use as a module not supported.'
    exit(1)


if len(sys.argv) < 3:
    print 'Usage: %s server file' % sys.argv[0]
    exit(1)

# Detect and strip leading "http://" if present
if sys.argv[1].find( 'http://' ) == 0:
    servname = sys.argv[1][7:]
else:
    servname = sys.argv[1]

# Add leading slash if necessary to file path
if sys.argv[2][0] != '/':
    fpath = '/' + sys.argv[2]
else:
    fpath = sys.argv[2]

conn = httplib.HTTPConnection( servname )
conn.request( 'GET', fpath )
r1 = conn.getresponse()
if r1.status != 200: # File found? Other errors?
    print 'Exit code: %d' % r1.status
    print '      msg: %s' % r1.reason
    conn.close()
    exit(-1)

fsrc = r1.read()
conn.close()
pdf_pattern = re.compile( '<\s*a[^<>]*href\s*=\s*["\']([^"\']*.pdf)["\'][^<>]*>', flags=re.IGNORECASE )
pdf_links = pdf_pattern.findall( fsrc )

lowest_slash = fpath.rfind('/')
base_path = 'http://' + servname + fpath[:lowest_slash+1]

for lnk in pdf_links:
    if lnk[:7] == 'http://':
        print lnk
    else:
        print base_path + lnk
