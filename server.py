#!/usr/bin/env python
#Equipo Rocket
#Karla S. Garcia Alcantara
#Oscar Herrera Ortiz

import socket
import sys
import thread
from common import *

#All msjs are send as Big endian
def run(cn, addr): #cn stands for connection
    def killThread(cn):
        print "Cerrando la conexion"
        cn.close()
        thread.exit()

    print "------------ SERVER -----------------"
    print "IP del cliente: ", addr[0] 
    print "Pto del cliente:", addr[1]
    print "with thread", thread.get_ident()
    try:
        cr = cn.recv(8) # As for client response, 8 bits to recive only
    except:
        killThread(cn) #If client was suspended or the universe is destroyed
    if(cr is None): #If something weird happend
        killThread(cn)
    msj = getAsList(cr) #Recover the response as a list
    if(len(msj) == 0):
        killThread(cn)
    if(msj[0] != "10"): 
        killThread(cn)
        
    print "------------ CLIENT -----------------"
    print "Codigo recibido:" , msj[0]
    print "rxbytes:", len(msj)
 
    print "------------ SERVER -----------------"
    idp, name, img = getRandomImage() 
    if not name:
        print "No trivia avalible"
        killThread(cn) #In case there is no image or image database was modified by unknow sources
    print "Tamano de la imagen:",len(img),"bytes"
    trivia = getTrivia(name) 
    sr = ["20", str(idp), (str(len(img)), 4), (trivia[0], 15), (trivia[1], 15), (trivia[2], 15)]#As for server response
    msj = getAsByte(sr)
    print "Codigo enviado:", sr[0]
    print "txbytes =",len(getAsList(msj)),"(codigo 20)"    
    try:
        cn.send(msj) #Here should verify that send() == len(msj), if not, then do something about it
    except:
        killThread(cn)
        
    print "Enviando imagen ..."
    pktCount = 0
    pktByteCount = 0
    try:
        for pkt in getPackets(img, PACKET_SIZE):#Same as Paulitos program            
            pktByteCount += cn.send(pkt)
            pktCount += 1    
        img = None #Release memory from thread
        print "Paquetes enviados:", pktCount
        print "txbytes:", pktByteCount, "(imagen)"       
        cn.send("ok")
    except:
        killThread(cn)
    try:
        cr = cn.recv(24)
    except:
        killThread(cn)
    if(cr is None):
        killThread(cn)
    msj = getAsList(cr) #Recover the response as a list
    if(len(msj) == 0):
        killThread(cn)
    if(msj[0] != "11"): 
        killThread(cn)
    
    print "------------ CLIENT -----------------"
    print "Codigo recibido:" , msj[0]
    print "rxbytes:", len(msj)
    print "idPok:", msj[1] #This make no sense, but meh
    print "idResp:", msj[2]

    sr = ["21"]
    print "------------ SERVER -----------------"
    print "Respuesta",
    if(trivia.index(name) == int(msj[2]) - 1):
        sr.append('1')
        print "correcta"
    else:
        sr.append('')
        print "incorrecta"
    print "txbytes:", len(sr)    
    msj = getAsByte(sr)
    try:
        cn.send(msj) #Here should verify that send() == len(msj), if not, then do something about it
    except:
        print "Client lost"
        killThread(cn)
    killThread(cn)

def main(maxConnections):
    if(len(sys.argv) != 2):
        print "Usage: python server.py <SERVER PORT>"
        exit()
    try:
        PORT = int(sys.argv[-1])
        if(PORT > 9999 or PORT < 1000):
            sys.exit()
    except:
        print(sys.argv[-1] + " is not a valid port")
        sys.exit()
    HOST = '' 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error , msg:
        print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    s.listen(maxConnections)
#    print s.getsockname()
    while True:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        thread.start_new_thread(run ,(conn,addr,))
    s.close()

if __name__ == "__main__":
    main(10)
