#!/usr/bin/env python
#
# maketoc.py
#
# Assumes that we have reached an end of the book if
# either (or both) special "next" or "prev" tags are
# missing.
#
# Uses contents of first <h1> tag to construct
# section names.
#
# Without artificial pauses, the PubMed Central server
# will notice how quickly you're accessing book sections
# and block your IP address. To avoid this, maketoc.py
# will pause for a given number of seconds before
# sending each server request. Since this script need
# only be run once to build the book section link list,
# I suggest using a large pause time, e.g. 5 seconds,
# and letting it run in the background.
#
# Note that the IP block is only temporary;
# I estimate my address was blocked for about 20 minutes.
#
# The default pause time is 5 seconds.
# 
#
# NOTES: - This code uses non-standard documentation
#          and probably other styles... and is generally
#          non-optimized. Please update!
#
#        - Most exceptions and errors are treated
#          as fatal (i.e. no recovery is attempted).
#
#
# Scott Livingston <slivingston  caltech.edu>
# 7 March 2010
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
import time


# Currently disallow use as a module
if __name__ != '__main__':
    print 'Use as a module not supported.'
    exit(1)


if len(sys.argv) < 3:
    print 'Usage: %s base_url seed [output] [seconds to sleep]' % sys.argv[0]
    exit(1)

if len(sys.argv) > 3:
    out_fname = sys.argv[3]
else:
    out_fname = 'toc.html'
if len(sys.argv) > 4:
    pause_dur = int(sys.argv[4])
    if pause_dur < 0:
        print 'Pause duration must be non-negative.'
        exit(1)
else:
    pause_dur = 5 # In seconds

# Extract server hostname and base_path from base_url
servname = sys.argv[1]
if servname[0:7] == 'http://':
    servname = servname[7:]
k = servname.find('/')
if k == -1:
    # There must be at least one slash;
    # given base_url is probably wrong.
    print 'Invalid base url: %s\n' % sys.argv[1]
    exit(-1)
base_path = servname[k:] # Path to file or section
servname = servname[0:k]

# Attempt to start http session and open seed page
try:
    conn = httplib.HTTPConnection( servname )
except:
    print 'Failed to connect to server at %s' % servname
    exit(-1)

# Build list of links, step to first section,
# then to last section, and connect the parts.
sec_list = [] # Each entry is a 2-tuple: ( part value, section title )
found_prev = True # ...to permit initial entry into loop
current_part = sys.argv[2] # Seed the process
while found_prev:
    time.sleep( pause_dur )
    conn.request( 'GET', base_path + current_part )
    resp = conn.getresponse()
    if resp.status != 200: # File found? Other errors?
        print 'Error while reading part %s.' % current_part
        print 'Received msg: %d (%s)' % (resp.status, resp.reason)
        break
    fsrc = resp.read()
    prev_re = re.compile( '<p\s+class\s*=\s*["\']prev main["\']\s*>\s*<a\s+href\s*=\s*["\']br.fcgi[^"\']*part=(\w*)["\']' )
    prev_part = prev_re.findall( fsrc )
    if len(prev_part) == 0:
        found_prev = False
   
    # Try to construct section title (currently a naive approach)
    k_end = fsrc.find( '</h1' )
    k_start = fsrc.rfind( '>', 1, k_end )
    sec_list.append( (current_part, fsrc[k_start+1:k_end].lstrip().rstrip()) )
    
    if len(prev_part) == 0:
        found_prev = False
    else:
        current_part = prev_part[0]

# ...and now build final list with sections moving forward through book (in order)
sec_list.reverse() # Sections in sequential order
current_part = sys.argv[2]
# First step forward once since we already marked the part
# for the seed earlier in our section list.
time.sleep( pause_dur )
conn.request( 'GET', base_path + current_part )
resp = conn.getresponse()
if resp.status != 200: # File found? Other errors?
    print 'Error while reading part %s.' % current_part
    print 'Received msg: %d (%s)' % (resp.status, resp.reason)
    found_next = False
else:
    fsrc = resp.read()
    next_re = re.compile( '<p\s+class\s*=\s*["\']next main["\']\s*>\s*<a\s+href\s*=\s*["\']br.fcgi[^"\']*part=(\w*)["\']' )
    next_part = next_re.findall( fsrc )
    if len(next_part) != 0:
        current_part = next_part[0]
        found_next = True
    else:
        found_next = False

while found_next:
    time.sleep( pause_dur )
    conn.request( 'GET', base_path + current_part )
    resp = conn.getresponse()
    if resp.status != 200: # File found? Other errors?
        print 'Error while reading part %s.' % current_part
        print 'Received msg: %d (%s)' % (resp.status, resp.reason)
        break
    fsrc = resp.read()
    next_re = re.compile( '<p\s+class\s*=\s*["\']next main["\']\s*>\s*<a\s+href\s*=\s*["\']br.fcgi[^"\']*part=(\w*)["\']' )
    next_part = next_re.findall( fsrc )

    # Try to construct section title (currently a naive approach)
    k_end = fsrc.find( '</h1' )
    k_start = fsrc.rfind( '>', 1, k_end )
    sec_list.append( (current_part, fsrc[k_start+1:k_end].lstrip().rstrip()) )
    if len(next_part) == 0:
        break

    current_part = next_part[0]

conn.close()

# Dump result to an XHTML file.
f = open( out_fname, 'w' )
f.write( '<!DOCTYPE html\n  PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n\n<head></head>\n\n<body>\n' )
for sec in sec_list:
    sec_link = 'http://' + servname + base_path + sec[0]
    f.write( '<a href="' + sec_link + '">' + sec[0] + ': ' + sec[1] + '</a><br />\n' )
f.write( '</body>\n\n</html>\n' )    
f.close()
