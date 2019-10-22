#!/usr/bin/env python
#Equipo Rocket
#Karla S. Garcia Alcantara
#Oscar Herrera Ortiz
 
import socket
import sys
import subprocess
import os
from common import *
from time import sleep
s = None
def main():
    port = 9999
    try:
        host = sys.argv[1]
        if(len(sys.argv) > 2):
            port = sys.argv[2]
    except:
        print "Usage:\n\tpython client.py <Server IP> [<Echo Port>]"
        exit()    
    try:
        host = socket.gethostbyname( host )        
    except socket.gaierror:
        print "connect () failed: Network is unreachable"
        exit()
    try:
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        exit()     
    
    try: #Idk if needs port verification
        port = int(port)
        if(port > 9999 or port < 0):
            exit()
    except:
        print sys.argv[2], "is not a valid port"
        exit()
        
    try:
        s.connect((host , port)) 
    except:
        print "connect () failed: Connection refused"
        exit()

        
    print "------------ CLIENT -----------------"
    try:
        usrin = raw_input("Introduce codigo a enviar: ") #As for user input
    except:
        killClient("")
    if(usrin != "10"):
        killClient("Codigo invalido ... Cerrando la conexion")
    msj = getAsByte(usrin)
    print "txbytes:", len(getAsList(msj)) 
    try:
        s.send(msj)
    except:
        killClient("Server down")
    try:
        sr = s.recv(408) #As for server response, should only recive at most 51 bytes
    except:
        killClient("Server down")

    if(sr is None):
        killClient("No server response")
    msj = getAsList(sr)
    if(len(msj) != 51): #Should be 51 bytes recived,  otherwise the response is inconplet or CORRUPT!!!!!!!!
        killClient("Server response do not meet the required format")
    if(msj[0] != "20"):
        killClient("Invalid code response")
    print "------------ SERVER -----------------"
    print "Codigo recibido:", msj[0]
    print "rxbytes:", len(msj)
    print "Id Pokemon:", msj[1]
    print "Tamano imagen en bytes:", ''.join(msj[2:6]) #.join is used cause the response is divided as list, where each element is a byte, a fake byte
    print "Respuesta 1:", ''.join(msj[6:21])
    print "Respuesta 2:", ''.join(msj[21:36])
    print "Respuesta 3:", ''.join(msj[36:])
    print "Recibiendo imagen ..."
    #recive img
    img = []
    pktCount = 0
    try:
        while True:
            sr = s.recv(PACKET_SIZE) #Only recive image as packets at most of 1024
            if(sr != "ok"):
                if(sr[-2:] == "ok" and sys.platform == 'linux2'):  #Workaraound for linux
                    img.append(sr[:-2])
                    pktCount += 1
                    break
                img.append(sr)
                pktCount += 1
            else:            
                break             
        img = joinPackets(img)
    except:
        killClient("Server down")
    print "Paquetes recibidos:", pktCount
    print "Tamano de la imagen en bytes:", len(img)
    #if size of the recived image is the same as the one specified in the response
    print "Imagen recibida y guardada correctamente" #As 'pokemon.jpg'
    print "Abriendo imagen ..."
    openImage(img)
    sleep(1.0)
    print "------------ CLIENT -----------------"
    try:
        usrin = raw_input("Introduce numero de respuesta: ") #As for user input
    except:
        killClient("")

    try:
        usrin = int(float(usrin))        
        if(usrin < 1 or usrin > 3):
            raise ValueError('')
    except:
        killClient("La respuesta es incorrecta")
        
    cr = ["11", msj[1], str(usrin)]
    msj = getAsByte(cr) #Idk if u most return the same idPokemon from response, or the idPokemon of the pokemon we choose, but wth
    print "txbytes:", len(cr) #Idk the diference between tcbytes and rxbytes
    try:
        s.send(msj)
    except:
        killClient("Server down")
    try:
        sr = s.recv(16)
    except:
        killClient("Server down")
    if(sr is None):
        killClient("No server response")
    msj = getAsList(sr)
    if(len(msj) != 2):
        killClient("Server response do not meet the required format")
    if(msj[0] != "21"):
        killClient("Invalid code response")
    print "------------ SERVER -----------------"
    print "Codigo recibido:", msj[0]
    print "rxbytes:", len(msj)
    print "La respuesta es",
    if(msj[1]):
        print "correcta"
    else:
        print "incorrecta"
    killClient("Cerrando la conexion")

def killClient(msj):   
    print msj
    if(s is not None):
        s.close()
    exit()

def openImage(data):
    f = open("pokemon.jpg", "wb")
    f.write(data)
    f.close()
    imageViewerFromCommandLine = {'linux2':'eog',
                                  'win32':'explorer'}[sys.platform]
    subprocess.call([imageViewerFromCommandLine, 'pokemon.jpg'])
    
if __name__ == "__main__":
    main()
    
