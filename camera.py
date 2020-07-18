import cv2 as cv
from time import localtime, strftime

class Camera(object):
    CAPTURES_DIR = "static/captures/"
    RESIZE_RATIO = 1.0
    time = 0
    temp = ""
    def __init__(self):
        self.video = cv.VideoCapture(0)
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None

        if (Camera.RESIZE_RATIO != 1):
            frame = cv.resize(frame, None, fx=Camera.RESIZE_RATIO, \
                fy=Camera.RESIZE_RATIO) 
            print(frame)   
        return frame

    def get_feed(self):
        frame = self.get_frame()
        if frame is not None:
            ret, jpeg = cv.imencode('.jpg', frame)
            #print(jpeg.tobytes())
            return jpeg.tobytes()

    def capture(self):
        frame = self.get_frame()
        #print("Frame" + frame)
        timestamp = strftime('%Y-%m-%d %I:%M %p', localtime())
        time = timestamp
        filename = Camera.CAPTURES_DIR + timestamp +".jpg"
        temp = filename
        print("Filename:" + filename)
        if not cv.imwrite(filename, frame):
            raise RuntimeError("Unable to capture image "+timestamp)
        return timestamp

    def getPath():
        return temp
