#!/usr/bin/python

# Copyright (c) 2008, Scott C. Livingston
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


# gArch.py - a simple Python script which gathers all emails from gmail
#   using POP3 and then places them into a TARed and GZIPed archive.
#
# NOTES: - if you desire ALL emails in your gmail account to be archived,
#   then select "Enable POP for all mail" under the tab "Forwarding and
#   POP/IMAP" of your gmail settings.
#
#
# Scott C. Livingston <slivingston@caltech.edu>. Copyright 2008.
#
# First released: 19 January 2008
# Updated: 29 August 2008
#  - Added looping to ensure all emails available are pulled from the server.


import getpass, poplib, tarfile, os, sys, datetime, re


if len(sys.argv) > 2:
    print "Usage: gArch.py NAME\n\n\
Archive all mail retrieved from gmail through POP3. Output is an archive\n\
compressed using TAR and GZIP and name NAME.tar.gz. If no argument is given,\n\
then default name of USERNAME_gmail_archive-YYYYMMDD is used, where USERNAME\n\
is your gmail username and YYYYMMDD is the current date.\n\n\
Scott C. Livingston. Copyright 2008.\n"
    exit()
elif len(sys.argv) == 2:
    # handle a help request
    if sys.argv[1] == 'help' or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print "Usage: gArch.py NAME\n\n\
Archive all mail retrieved from gmail through POP3. Output is an archive\n\
compressed using TAR and GZIP and name NAME.tar.gz. If no argument is given,\n\
then default name of USERNAME_gmail_archive-YYYYMMDD is used, where USERNAME\n\
is your gmail username and YYYYMMDD is the current date.\n\n\
Scott C. Livingston. Copyright 2008.\n"
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
