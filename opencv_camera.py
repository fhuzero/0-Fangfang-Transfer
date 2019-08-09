import numpy as np
import cv2

cap0 = cv2.VideoCapture(1)
cap0.set(3,640)
cap0.set(4,480)

cap1 = cv2.VideoCapture(2)
cap1.set(3,640)
cap1.set(4,480)

cap2 = cv2.VideoCapture(3)
cap2.set(3,640)
cap2.set(4,480)

cap3 = cv2.VideoCapture(4)
cap3.set(3,640)
cap3.set(4,480)

count = 0

while(True):
    # Capture frame-by-frame
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()


    bgr0 = frame0
    bgr1 = frame1
    bgr2 = frame2
    bgr3 = frame3




    # Our operations on the frame come here
    gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)




    # Display the resulting frame
  
    cv2.imshow('frame0',bgr0)
    cv2.imshow('frame1',bgr1)
    cv2.imshow('frame2',bgr2)
    cv2.imshow('frame3',bgr3)


    # print('start')
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    k = cv2.waitKey(1)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
    elif k == ord('s'):
        # print('start save')
        cv2.imwrite("./test1_captured_images/gray/c_%d_v_1.jpg" % count,gray0)
        cv2.imwrite("./test1_captured_images/gray/c_%d_v_2.jpg" % count,gray1)
        cv2.imwrite("./test1_captured_images/gray/c_%d_v_3.jpg" % count,gray2)
        cv2.imwrite("./test1_captured_images/gray/c_%d_v_4.jpg" % count,gray3)


        cv2.imwrite("./test1_captured_images/bgr/c_%d_v_1.jpg" % count,bgr0)
        cv2.imwrite("./test1_captured_images/bgr/c_%d_v_2.jpg" % count,bgr1)
        cv2.imwrite("./test1_captured_images/bgr/c_%d_v_3.jpg" % count,bgr2)
        cv2.imwrite("./test1_captured_images/bgr/c_%d_v_4.jpg" % count,bgr3)

        count  = count + 1


# When everything done, release the capture
cap0.release()
cap1.release()
cap2.release()
cap3.release()


cv2.destroyAllWindows()

