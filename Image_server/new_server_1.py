import socket
from threading import Thread
from socketserver import ThreadingMixIn
import cv2
import time
import numpy
import os

TCP_IP = '192.168.0.182'
TCP_PORT = 6666
BUFFER_SIZE = 1024
time_interal = 0.1
num = 0

def recvall(socksock, countcount):
    buf = b''
    while countcount:
        newbuf = socksock.recv(countcount)
        if not newbuf: return None
        buf += newbuf
        countcount -= len(newbuf)
    return buf

init_time = time.time()

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print (" New thread started for "+ip+":"+str(port))
    def run(self):
        global num, init_time
        num = num + 1
        name = num
        os.mkdir('data_collected/images/'+str(name))
        count = 0

        while time.time()-init_time<60:
            tt = time.time()

        t1 = time.time()
        while True:
            t2 = time.time()
            if t2-t1>time_interal:
                # self.sock.send(b'start')
                time_sample = recvall(self.sock,32)
                length = recvall(self.sock,16)
                stringData = recvall(self.sock, int(length))
                data = numpy.fromstring(stringData, dtype='uint8')
                decimg=cv2.imdecode(data,1)
                # cv2.imshow('SERVER',decimg)
                cv2.imwrite('data_collected/images/'+str(name)+'/'+str(count)+'.jpg',decimg)
                with open('data_collected/images/'+str(name)+'/'+"camera_timestamp.txt","a+") as f:
                    f.write(str(time.time())+'\n')
                with open('data_collected/images/'+str(name)+'/'+"collect_timestamp.txt","a+") as f:
                    f.write(str(time_sample)+'\n')
                timestamp = time.time()
                print('already wrote: %d at port %s at time %s' % (count,str(port),str(timestamp)))
                count = count + 1
                t1 = t2
                if cv2.waitKey(10) == 27:
                    break
      

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)
    cv2.destroyAllWindows()

for t in threads:
    t.join()