#TODO: iterate through images, for each pair of image use algos to calculate speed
#TODO: maybe returns all the images with the speed labelled on them?
#TODO: maybe have command line arguments? if they input just one directory 
# we do physics way
# and if we they do 2 directories then we do camera projection algo way
import os
import xml.etree.ElementTree
from tkinter.tix import ButtonBox


directory = '/Users/ailitaeddy/Senior_Year_School_Stuff/Spring_22/CV/cv_final_proj/data/train/annotations' # iterates through every file in this directory

def parse_xml(filename):
    et = xml.etree.ElementTree.parse(directory + '/' + filename)
    root = et.getroot()
    bounding_box = root.find('object').find('bndbox')
    xmin = int(bounding_box.find('xmin').text)
    ymin = int(bounding_box.find('ymin').text)
    xmax = int(bounding_box.find('xmax').text)
    ymax = int(bounding_box.find('ymax').text)
    return xmin, ymin, xmax, ymax

def sort_files(filename):
    split_name = filename.split('_')
    return split_name.pop()

def main():
    xml_files = os.listdir(directory)
    # get set of all video/throw names
    video_names = set()
    for file in xml_files:
        filename = os.fsdecode(file)
        split_name = filename.split('_')
        split_name.pop()
        video_names.add('_'.join(split_name))
    
    for video_name in video_names:
        # select all xml files for that video
        image_xmls = [
            os.fsdecode(file)
            for file in xml_files
            if os.fsdecode(file).startswith(video_name)
        ]
        # parse each xml file for that video in order by appending _[number] to the video name
        image_xmls = sorted(image_xmls, key=sort_files)
        for image_xml in image_xmls:
            xmin, ymin, xmax, ymax = parse_xml(image_xml)
            print(image_xml)
            print(xmin, ymin, xmax, ymax)
            print('--------')
            # calculate speed traveled with both algorithms --> get_camera_projection_speed() and get_physics_algo_speed()
            # display bounding box and both physics and camera geometry speeds on next image --> kallis_function(cp_speed, physics_speed, image_filename, bbox_coords)

    # for each throw:
    #     for each image until n - 1 (where n is # of images):
    #         get coordinates of bounding box of both current and next image # parse_xml_files()
    #         calculate speed traveled with both algorithms # get_camera_projection_speed() and get_physics_algo_speed()
    #         display bounding box and both physics and camera geometry speeds on next image # kallis_function(cp_speed, physics_speed, image_filename, bbox_coords)


if __name__ == '__main__':
    main()