import socket
import cv2
import numpy
import time

address = ('192.168.0.182', 6666)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(address)

capture = cv2.VideoCapture(0)
ret, frame = capture.read()
time1 = time.time()
with open("camera_2_timestamp.txt","a+") as f:
    f.write(str(time1)+'\n')
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

flag = 0

while ret:
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    if flag == 1:
        sock.send( str(len(stringData)).ljust(16));
        sock.send( stringData );
    with open("camera_2_timestamp.txt","a+") as f:
        f.write(str(time1)+'\n')
    ret, frame = capture.read()
    time1 = time.time()
    
    #decimg=cv2.imdecode(data,1)
    #cv2.imshow('CLIENT',decimg)
    if cv2.waitKey(10) == 27:
        break
sock.close()
cv2.destroyAllWindows()



