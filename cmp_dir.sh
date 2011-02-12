#!/bin/sh
#
# Compare all files in two paths, using the first as a reference.
# (i.e., files in the second path but not the first will go unnoticed.)
#
# Default behavior is to quit on first difference. Use -F flag to
# continue anyway.
#
#
# Scott Livingston  <slivingston@caltech.edu>
# 2011 Jan 15.

if [ -z $1 ] || [ -z $2 ]; then
        echo "Usage: $0 path0 path1 [-F]"
        exit 2
fi

PATH0=$1
PATH1=$2

if [[ $3 = "-F" ]]; then
        MARCH_ON=1
fi

FILE_LIST=`ls $PATH0`

echo Paths:
echo $PATH0
echo $PATH1
for f in $FILE_LIST; do
        if [ -d $PATH0/$f ]; then
                echo Ignoring directory $f.
                continue
        fi
        if [ -r $PATH0/$f ] && [ -r $PATH1/$f ]; then
                echo Comparing $f ...
                cmp $PATH0/$f $PATH1/$f || if [ -z $MARCH_ON ]; then exit -1; fi
        else
                echo $f does not exist or is unreadable!
                if [ -z $MARCH_ON ]; then
                        exit -1
                fi
        fi
done