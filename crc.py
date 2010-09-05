#!/usr/bin/env python
#
#
# Scott Livingston
# Apr 2010.


import sys


def get_input():
    """Obtain list of bytes on which to perform CRC."""
    input = []
    if len(sys.argv) == 2: # Read from stdin
        try:
            for line in sys.stdin:
                input.append( (int(float.fromhex(line)) & 0xff) )
        except KeyboardInterrupt:
            input.pop() # Last input was the interrupt signal,
                        # which we don't want
            print input
    else: # Input given at command-line
        raw_input = int(float.fromhex(sys.argv[2]))
        while raw_input: # Break up into bytes (in little endian)
            input.append( raw_input & 0xff )
            raw_input = raw_input >> 8
    return input


if len(sys.argv) < 2 or len(sys.argv) > 3:
    print "Usage: %s type [$0xinput]" % sys.argv[0]
    print "\nAssumes little endian ordering.\nInput read as bytes from stdin if none given."
    exit(1)

try:
    mode = int(sys.argv[1])
except ValueError:
    print "Invalid CRC type."
    exit(1)

if mode == 7: # CRC7
    input = get_input()
    if input is None or len(input) == 0:
        print "No input was given."
        exit(0)
    
    result = [0,0]
    for byte in input:
        for bit_ind in range(8):
            result[0] = result[0] << 1
            result[1] = result[1] << 1
            result[0] |= 0x1 & (byte ^ (result[1]>>4))
            result[1] |= 0x1 & (result[0] ^ (result[0]>>3))
            result[0] &= 0x7
            result[1] &= 0xf
            byte = byte >> 1
    print "%d%d%d%d%d%d%d" % ( result[0]&0x1, (result[0]>>1)&0x1, (result[0]>>2)&0x1,
                               result[1]&0x1, (result[1]>>1)&0x1,
                               (result[1]>>2)&0x1, (result[1]>>3)&0x1)

elif mode == 16: # CRC16
    input = get_input()
    if input is None or len(input) == 0:
        print "No input was given."
        exit(0)

    result = [0,0,0]
    for byte in input:
        for bit_ind in range(8):
            result[0] = result[0] << 1
            result[1] = result[1] << 1
            result[2] = result[2] << 1
            result[0] |= 0x1 & (byte ^ (result[2]>>4))
            result[1] |= 0x1 & (result[0] ^ (result[0]>>5))
            result[2] |= 0x1 & (result[0] ^ (result[1]>>7))
            result[0] &= 0x1f
            result[1] &= 0x7f
            result[2] &= 0xf
            byte = byte >> 1

    result_output = result[0]
    result_output |= result[1]<<5
    result_output |= result[2]<<12
    print "0x%04X" % result_output
    
else:
    print "Unrecognized CRC type."
    exit(1)
