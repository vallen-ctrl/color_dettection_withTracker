import cv2
import numpy
import write
import time
import urllib.request


def noting(x):
    pass

def main():
    url = "http://10.183.179.34/cam-mid.jpg"
    isgreen = False
    detectGreen = False

    cv2.namedWindow("me")

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
        imageRes = urllib.request.urlopen(url)
        image_np = numpy.array(bytearray(imageRes.read()), dtype=numpy.uint8)

        frame = cv2.imdecode(image_np, -1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        h_up = cv2.getTrackbarPos("H_up", "me")
        s_up = cv2.getTrackbarPos("S_up", "me")
        v_up = cv2.getTrackbarPos("V_up", "me")

        h_low = cv2.getTrackbarPos("H_low", "me")
        s_low = cv2.getTrackbarPos("S_low", "me")
        v_low = cv2.getTrackbarPos("V_low", "me")

        hsv_upper = numpy.array([h_up,s_up, v_up])
        hsv_lower = numpy.array([h_low, s_low, v_low])

        mask = cv2.inRange(frame, hsv_lower, hsv_upper)
        result = cv2.bitwise_and(frame, frame, mask=mask);

        if cv2.countNonZero(mask) >15:
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
    
    write.writeCFG([h_up,s_up,v_up], [h_low,s_low,v_low])
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()