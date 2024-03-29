import socket
import time
import sys
import RPi.GPIO as GPIO
#define host ip: Rpi's IP
HOST_IP = "192.168.1.5"
HOST_PORT = 8888
print("Starting socket: TCP...")
#1.create socket object:socket=socket.socket(family,type)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
host_addr = (HOST_IP, HOST_PORT)
#2.bind socket to addr:socket.bind(address)
socket_tcp.bind(host_addr)
#3.listen connection request:socket.listen(backlog)
socket_tcp.listen(1)
#4.waite for client:connection,address=socket.accept()
socket_con, (client_ip, client_port) = socket_tcp.accept()
print("Connection accepted from %s." %client_ip)
socket_con.send("Welcome to RPi TCP server!")
#5.handle
GPIO.setmode(GPIO.BCM)	##信号引脚模式定义，BCM模式
GPIO.setwarnings(False)

###主循环
while True:
    try:
        data=socket_con.recv(512)
        if len(data)>0:
            print("Received:%s"%data)
            if data=='stop':
			    print("stop...")
            elif data=='gogo':
			    print("gogo!!!")
            socket_con.send(data)
            time.sleep(1)
            continue
    except Exception:
            socket_tcp.close()
            sys.exit(1)