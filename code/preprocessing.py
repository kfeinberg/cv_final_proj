# source: https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
import cv2
import os

frameRate = 0.05 # it will capture images every 0.05 seconds
directory = '/Users/kallifeinberg/Documents/Senior/Semester2/CS1430/cv_final_proj/data/video' # iterates through every file in this directory

def get_frame(sec, vidcap, directory_name):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("../data/images/" + directory_name + "/" + str(count)+".jpg", image)     # save frame as JPG file
    return hasFrames


for file in os.listdir(directory):
    count = 1
    sec = 0

    file_name = os.fsdecode(file)
    video_url = directory + "/" + file_name  

    vidcap = cv2.VideoCapture(video_url)

    if (file_name != ".DS_Store"):
        directory_name = file_name.split('.')[0]
        os.mkdir("../data/images/" + directory_name)

        success = get_frame(sec, vidcap, directory_name)
        while success:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success = get_frame(sec, vidcap, directory_name)