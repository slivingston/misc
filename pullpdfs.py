#!/usr/bin/env python

# Copyright (c) 2010, Scott C. Livingston
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of Scott C. Livingston nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
