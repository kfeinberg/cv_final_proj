# source: https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
import cv2

video_url = '/Users/kallifeinberg/Documents/Senior/Semester2/CS1430/cv_final_proj/data/video/vid1.mp4'
directory_name = '5mvid1'
sec = 0
frameRate = 1 # it will capture images every 0.5 seconds
count = 1

vidcap = cv2.VideoCapture(video_url)
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("../data/images/image" + directory_name + str(count)+".jpg", image)     # save frame as JPG file
    return hasFrames

success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)