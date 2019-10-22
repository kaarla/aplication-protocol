#!/usr/bin/env python
#Equipo Rocket
#Karla S. Garcia Alcantara
#Oscar Herrera Ortiz
import re
import sys
from math import log
from math import modf
from random import randint
from random import randrange

PACKET_SIZE = 1024
LINE_END = {'linux2':'\r\n','win32':'\n'}[sys.platform]

def getAsByte(value, n = 1): #Yeah sure, 'cause all msjs are send as string
    if(type(value)is list):
        val = ""
        for v in value:
            byte = '00000000' #fake byte            
            if(type(v) is tuple):
                byte *= v[1]
                v = v[0]
            val += byte[:len(byte) - len(v)] + v
        return val
    byte = '00000000' #fake byte
    byte *= n    
    return byte[:len(byte) - len(value)] + value


def getAsList(value):
    byteS = len(value) / 8
    values = []
    zeros = "^0+"
    for i in xrange(byteS):
        val = re.search(zeros, value[i * 8: (i + 1) * 8])
        if(val is not None):
            values.append(value[val.end () + i * 8: (i + 1) * 8])
        else:
            values.append(value[i * 8: (i + 1) * 8])
    return values

def getTrivia(exclude):
    data = [y.strip(LINE_END) for y in open('data/data.txt', 'r').readlines()]
    names = [x.split(',')[1] for x in data]
    if(exclude in names):
        names.remove(exclude)
    ch1 = names.pop(randrange(0, len(names)))
    ch2 = names.pop(randrange(0, len(names)))
    l = [ch1, ch2, exclude]
    l.sort()
    return l

def getRandomImage():
    try:
        data = [y.strip(LINE_END) for y in open('data/data.txt', 'r').readlines()]
        names = [x.split(',')[1] for x in data]
        withPicture = dict([[x.split(',')[1], (x.split(',')[0], x.split(',')[2])] for x in data if x.split(',')[2]])
        choice = withPicture.keys()[randrange(0, len(withPicture.keys()))]
        img = open('data/' + withPicture[choice][1], 'rb').read()
        return withPicture[choice][0], choice, img
    except:
        return None, None, None

def getPackets(v, size):
    v = v[::-1] #Needed for little endian
    l = len(v)
    if(l % size):
        parts = l / size        
        packets = [v[i:i + size] for i in xrange(0, parts * size, size)]
        packets.append(v[parts * size : ])
        return packets
    else:        
        return [v[i:i + size] for i in xrange(0, l, size)]

def joinPackets(packets):
    return ''.join(packets)[::-1]
