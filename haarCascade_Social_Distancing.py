import cv2
import os
import math


person_cascade = cv2.CascadeClassifier(
os.path.join('haarcascade_fullbody.xml'))
cap = cv2.VideoCapture("VIRAT_S_010204_05_000856_000890.avi")
# the output will be written to output.avi
out = cv2.VideoWriter(
    'output_haar.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640, 360))
while True:
    r, frame = cap.read()
    if r:
        frame = cv2.resize(frame, (640, 360))  # Downscale to improve frame rate
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # Haar-cascade classifier needs a grayscale image
        rects = person_cascade.detectMultiScale(gray_frame)

        i = 0
        person_count = 0
        center = []
        original_cord = []
        for (x, y, w, h) in rects:
            center.append((int((x+(x+w))/2),int((y+(y+h))/2)))
            original_cord.append((x,y,w,h))
            cv2.circle(frame,(int((x+(x+w))/2),int((y+(y+h))/2)), 0, (0, 0, 255), -1)
            person_count = person_count + 1
            if i>0 :
                for j in range(1,person_count):
                    distance =math.sqrt(math.pow(center[i][0] - center[j-1][0], 2) + math.pow(center[i][1] -
                                                                                              center[j-1][1], 2) * 1.0)
                    print("distance",distance)
                    if (distance<50):
                        cv2.rectangle(frame, (original_cord[i][0], original_cord[i][1]),
                                      (original_cord[i][0] + original_cord[i][2], original_cord[i][1] + original_cord[i][3]),
                                      (0, 0, 255), 2)
                        cv2.rectangle(frame, (original_cord[j-1][0], original_cord[j-1][1]),
                                      (original_cord[j-1][0] + original_cord[j-1][2], original_cord[j-1][1] + original_cord[j-1][3]),
                                      (0, 0, 255), 2)
                        cv2.line(frame, center[i], center[j-1],(0, 0, 255), 1 )

            i = i +1
        # Write the output video
        out.write(frame.astype('uint8'))
        cv2.imshow("preview", frame)
    k = cv2.waitKey(1)
    if k & 0xFF == ord("q"):  # Exit condition
        break
# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window