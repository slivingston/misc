#!/usr/bin/python

# gArch.py - a simple Python script which gathers all emails from gmail
#   using POP3 and then places them into a TARed and GZIPed archive.
#
# NOTES: - if you desire ALL emails in your gmail account to be archived,
#   then select "Enable POP for all mail" under the tab "Forwarding and
#   POP/IMAP" of your gmail settings.
#
#
# Scott Livingston <slivingston@caltech.edu>. Copyright 2008.
#
# First released: 19 January 2008
# Updated: 29 August 2008
#  - Added looping to ensure all emails available are pulled from the server.
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.


import getpass, poplib, tarfile, os, sys, datetime, re


if len(sys.argv) > 2:
    print "Usage: gArch.py NAME\n\n\
Archive all mail retrieved from gmail through POP3. Output is an archive\n\
compressed using TAR and GZIP and name NAME.tar.gz. If no argument is given,\n\
then default name of USERNAME_gmail_archive-YYYYMMDD is used, where USERNAME\n\
is your gmail username and YYYYMMDD is the current date.\n\n\
Scott Livingston. Copyright 2008.\n\
This program is free software; it is released WITHOUT ANY WARRANY and under\n\
the GNU General Public License, version 3. See GPLv3.txt (distributed with\n\
this script) or visit http://www.gnu.org/licenses/gpl.html for exact terms.\n"
    exit()
elif len(sys.argv) == 2:
    # handle a help request
    if sys.argv[1] == 'help' or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print "Usage: gArch.py NAME\n\n\
Archive all mail retrieved from gmail through POP3. Output is an archive\n\
compressed using TAR and GZIP and name NAME.tar.gz. If no argument is given,\n\
then default name of USERNAME_gmail_archive-YYYYMMDD is used, where USERNAME\n\
is your gmail username and YYYYMMDD is the current date.\n\n\
Scott Livingston. Copyright 2008.\n\
This program is free software; it is released WITHOUT ANY WARRANY and under\n\
the GNU General Public License, version 3. See GPLv3.txt (distributed with\n\
this script) or visit http://www.gnu.org/licenses/gpl.html for exact terms.\n"
        exit()
    name = sys.argv[1]
else:
    name = "gmail_archive-" + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + str(datetime.date.today().day).zfill(2)

popServer = 'pop.gmail.com'
popPort = 995
ssl = True

try:
    if ssl:
        popCon = poplib.POP3_SSL(popServer, popPort)
    else:
        popCon = poplib.POP3(popServer, popPort)
except poplib.error_proto:
    print "init error: %s\n" % (poplib.error_proto)

#popCon.set_debuglevel(2) # 0 - none (default); 1 - moderate; 2 - high

print popCon.getwelcome()

user = raw_input('Email Address: ')
usrpasswd = getpass.getpass(); # storing password in memory like this is unsecure! (FIX THIS)

if len(sys.argv) == 1:
    name = str(user[:re.match('(\S+)@gmail.com',user).end(1)]) + '_' + name

popCon.user(user)
popCon.pass_(usrpasswd)

# attempt to open tar file using gzip compression
try:
    tgzFile = tarfile.open( name + ".tar.gz", 'w:gz' )
except ReadError:
    print "Error: failed to open " + name + ".tar.gz for writing.\n"

totalmsg = 0
mBoxStatus = popCon.stat()

eFileName = [] # initialize email filename list
while mBoxStatus[0] > 0:
    for i in range(len(popCon.list()[1])):
        eFileName.append(str(totalmsg+i+1) + '.email')
        tmpFile = file(eFileName[totalmsg+i],'wb')
        for j in popCon.retr(i+1)[1]:
            tmpFile.write(j + '\n')
        tmpFile.close()
        tgzFile.add(eFileName[totalmsg+i])
        print '.', # one dot printed per message

    popCon.quit()
    totalmsg = totalmsg + mBoxStatus[0]
    try:
        if ssl:
            popCon = poplib.POP3_SSL(popServer, popPort)
        else:
            popCon = poplib.POP3(popServer, popPort)
    except poplib.error_proto:
        print "init error: %s\n" % (poplib.error_proto)
        break
    popCon.user(user)
    popCon.pass_(usrpasswd)
    mBoxStatus = popCon.stat()
    

print '\nTotal messages retrieved: %d\n' % totalmsg
popCon.quit()
tgzFile.close()
for i in range(len(eFileName)):
    os.remove(eFileName[i])
