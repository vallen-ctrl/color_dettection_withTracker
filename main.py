import cv2
import numpy
import write
import time

def noting(x):
    pass

def main():
    isgreen = False
    detectGreen = False
    cap = cv2.VideoCapture(0);
    cv2.namedWindow("me")
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    cv2.createTrackbar("H_up", "me", 0, 255, noting)
    cv2.createTrackbar("S_up", "me", 0, 255, noting)
    cv2.createTrackbar("V_up", "me", 0, 255, noting)

    cv2.createTrackbar("H_low", "me", 0, 255, noting)
    cv2.createTrackbar("S_low", "me", 0, 255, noting)
    cv2.createTrackbar("V_low", "me", 0, 255, noting)

    [HSV_upper, HSV_lower]=write.loadCFG()

    cv2.setTrackbarPos("H_up", "me", HSV_upper[0])
    cv2.setTrackbarPos("S_up", "me", HSV_upper[1])
    cv2.setTrackbarPos("V_up", "me", HSV_upper[2])

    cv2.setTrackbarPos("H_low", "me", HSV_lower[0])
    cv2.setTrackbarPos("S_low", "me", HSV_lower[1])
    cv2.setTrackbarPos("V_low", "me", HSV_lower[2])
    b = 1;
    while True:
        ret, frame = cap.read()
        if not ret:
            print("kesalahan dalam membaca")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        h_up = cv2.getTrackbarPos("H_up", "me")
        s_up = cv2.getTrackbarPos("S_up", "me")
        v_up = cv2.getTrackbarPos("V_up", "me")

        h_low = cv2.getTrackbarPos("H_low", "me")
        s_low = cv2.getTrackbarPos("S_low", "me")
        v_low = cv2.getTrackbarPos("V_low", "me")

        hsv_upper = numpy.array([h_up,s_up, v_up])
        hsv_lower = numpy.array([h_up, s_low, v_low])

        mask = cv2.inRange(frame, hsv_lower, hsv_upper)
        result = cv2.bitwise_and(frame, frame, mask=mask);

        if cv2.countNonZero(mask) > 20:
            detectGreen = True;
            pass
        else:
            detectGreen = False
        
        if(detectGreen != isgreen):
            isgreen = detectGreen
            print(f"terdeteksi warna hijau: {isgreen}")
            b+=1
        cv2.imshow("me", frame);
        cv2.imshow("mask", mask);
        cv2.imshow("result", result);
        
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
        time.sleep(0.1)
    write.writeCFG([h_up,s_up,v_up], [h_low,s_low,v_low])
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()