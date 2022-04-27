# source: https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
import cv2
import os

video_url = '/Users/kallifeinberg/Documents/Senior/Semester2/CS1430/cv_final_proj/data/video/10mvid2.mp4'
directory_name = '10mvid2'
sec = 0
frameRate = 0.1 # it will capture images every 0.5 seconds
count = 1

vidcap = cv2.VideoCapture(video_url)
os.mkdir("../data/images/" + directory_name)
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("../data/images/" + directory_name + "/" + str(count)+".jpg", image)     # save frame as JPG file
    return hasFrames

success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)