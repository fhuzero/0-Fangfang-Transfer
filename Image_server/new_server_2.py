import socket
from threading import Thread
import cv2
import time
import numpy as np
import os
import Queue as queue
import shutil
import struct
import socket
import time
import sys
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np
from numpy.random import normal as normal
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.animation as animation


TCP_IP = '192.168.0.182'
TCP_PORT = 6666
BUFFER_SIZE = 1024
time_interal = 0.1
num = -1

time_cam = np.zeros((4,8000))
time_leap = np.zeros(8000)
leap_data = np.zeros((8000,20))
time_4_queue = queue.Queue()

leap_count = 0
leap_count_save = 0

def calculate_bone_angle(dir):
    sin_angle=dir[2]
   
    angle=np.arcsin(sin_angle)
    angle2=angle*360/2/np.pi

    return angle2

def calculate_angle(dir1, dir2):
    Lx=1
    Ly=1
    cos_angle=dir1.dot(dir2)/(Lx*Ly)
   
    angle=np.arccos(cos_angle)
    angle2=angle*360/2/np.pi

    return angle2

def get_next_point(point,angle):
    next_point = np.zeros(3)
    next_point[0] = point[0]
    next_point[1] = point[1] + np.cos(angle)
    next_point[2] = point[2] + np.sin(angle)
    return next_point

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
        global num, init_time, time_cam, time_4_queue
        num = num + 1
        name = num
        os.mkdir('data_collected/images/'+str(name))
        os.mkdir('data_collected/images/'+str(name)+'_s')

        count = 0

        # while time.time()-init_time<60:
        #     tt = time.time()

        while True:
            length = recvall(self.sock,16)
            stringData = recvall(self.sock, int(length))
            
            data = np.fromstring(stringData, dtype='uint8')
            decimg=cv2.imdecode(data,1)
            # cv2.imshow('SERVER',decimg)
            cv2.imwrite('data_collected/images/'+str(name)+'/'+str(count)+'.jpg',decimg)
            time_sample = recvall(self.sock,32)
            time_sample = float(time_sample)
            time_cam[name][count] = time_sample
            # print(name, time_sample)
            if name == 3:
                time_4_queue.put(time_sample)
                # print(time_4_queue.qsize())
            # with open('data_collected/images/'+str(name)+'/'+"camera_timestamp.txt","a+") as f:
            #     f.write(str(time.time())+'\n')
            with open('data_collected/images/'+str(name)+'/'+"collect_timestamp.txt","a+") as f:
                f.write(str(time_sample)+'\n')
            timestamp = time.time()
            # print('already wrote: %d at name %s at time %s' % (count,str(name),str(timestamp)))
            count = count + 1
            if cv2.waitKey(10) == 27:
                break
# add buffer to other three cams and leap motion
def search_closest_time(time_piece, time_array):
    temp_time = 0
    delta_time = time_piece
    for i in range(len(time_array)):
        if abs(time_piece-time_array[i]) < 1:
            if abs(time_piece-time_array[i]) < delta_time:
                temp_time = time_array[i]
                delta_time = abs(time_piece-time_array[i])
                result_num = i
    # print('*'*20)
    # print(temp_time, result_num)
    if temp_time == 0:
        result_num = 0
    return (temp_time, result_num)


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print ("Initialized")

    def on_connect(self, controller):
        print ("Connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print ("Disconnected")

    def on_exit(self, controller):
        print ("Exited")

    def on_frame(self, controller):
        global flag, leap_data, time_leap, leap_count, leap_count_save
        
        frame = controller.frame()
        leap_now_time = time.time()
        all_angle = np.zeros((5,4))
        
        # print ("Frame id: %d, timestamp: %d" % (
        #       frame.id, frame.timestamp))

        # Get hands
        for hand in frame.hands:
            
            handType = "Left hand" if hand.is_left else "Right hand"
            normal = hand.palm_normal
            direction = hand.direction
            arm = hand.arm
            all_angle = np.zeros((5,4))
            finger_num = 0
            for finger in hand.fingers:
                direction_array = np.zeros((4,3))            
                for b in range(0, 4):
                    bone = finger.bone(b)                 
                    dir_str = str(bone.direction)
                    xinterim = np.array(dir_str[1:-1].split(', '))                 
                    xinterim = np.asfarray(xinterim,float)                   
                    direction_array[b] = xinterim
                
                dir_angle_array = np.zeros(4)
                dir_angle_array[0] = calculate_bone_angle(direction_array[0])
                for dir_id in range(3):
                    dir_angle_array[dir_id+1] = calculate_angle(direction_array[dir_id],direction_array[dir_id+1])
                # print("     angle: a1: %f, a2: %f, a3: %f, a4: %f" % (dir_angle_array[0], dir_angle_array[1], dir_angle_array[2], dir_angle_array[3]))
                all_angle[finger_num] = dir_angle_array
                finger_num = finger_num + 1
            all_angle_value = all_angle.flatten()
            all_angle = str(all_angle_value).replace('\n', '')[1:-1]
            if leap_count % 3 == 0:
                leap_data[leap_count_save] = all_angle_value
                time_leap[leap_count_save] = leap_now_time
         
                with open("data_collected/images/leap_raw_data.txt","a+") as f:
                    f.write(all_angle+'\n')
                with open("data_collected/images/leap_raw_time.txt","a+") as f:
                    # f.write(str(time_leap[leap_count_save])+'\n')
                    f.write(str(leap_count)+'\t'+str(leap_count_save)+'\t'+str(time_leap[leap_count_save])+'\n')
                leap_count_save = leap_count_save + 1
            leap_count = leap_count + 1
  
def leap_thread():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        controller.remove_listener(listener)
   
        

def sync_camera_leap(time_cam, time_4_queue, time_leap, leap_data):

    count_pic = 0
    count_any = -1
    while True:
        print(time_4_queue.qsize())
        if (time_4_queue.qsize()) != 0:
            print(time_4_queue.qsize())
            count_any = count_any + 1
            time_piece = time_4_queue.get()
            print(time_piece)
            temp_time = np.zeros(4)
            result_num = np.zeros(4)
    
            temp_time[3] = time_piece
            result_num[3] = count_any
            for cam_num in range(3):
                (temp_time[cam_num], result_num[cam_num]) = search_closest_time(time_piece, time_cam[cam_num])
                if temp_time[cam_num] == 0:
                    break
            (temp_time_leap, index_leap) = search_closest_time(time_piece, time_leap)

            if (np.count_nonzero(temp_time) == 4 and temp_time_leap != 0):
                with open("data_collected/images/leap_sync_data.txt","a+") as f:
                    f.write(str(leap_data[index_leap]).replace('\n', '')[1:-1]+'\n')
                with open("data_collected/images/leap_sync_time.txt","a+") as f:
                    f.write(str(temp_time_leap)+'\n')
                for i in range(4):
                    shutil.copyfile('data_collected/images/'+str(i)+'/'+str(int(result_num[i]))+'.jpg','data_collected/images/'+str(i)+'_s/'+str(int(count_pic))+'.jpg')
                    with open('data_collected/images/'+str(i)+'_s/'+"camera_timestamp_closed.txt","a+") as f:
                        f.write(str(temp_time[i])+'\n')
                count_pic = count_pic + 1


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

thread_sync = Thread(target=sync_camera_leap, args=(time_cam, time_4_queue, time_leap, leap_data))
threads.append(thread_sync)

thread_leap = Thread(target=leap_thread, args=())
threads.append(thread_leap)
thread_leap.start()

client_num = 0

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    client_num = client_num + 1
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)
    if client_num == 4:
        thread_sync.start()
        
    cv2.destroyAllWindows()

for t in threads:
    t.join()