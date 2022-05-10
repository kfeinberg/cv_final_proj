#TODO: iterate through images, for each pair of image use algos to calculate speed
#TODO: maybe returns all the images with the speed labelled on them?
#TODO: maybe have command line arguments? if they input just one directory 
# we do physics way
# and if we they do 2 directories then we do camera projection algo way
import os
import xml.etree.ElementTree
from tkinter.tix import ButtonBox
import camera_projection_algo
import diameter_algo
import helpers

directory = '/Users/kallifeinberg/Documents/Senior/Semester2/CS1430/cv_final_proj/data/train/annotations' # iterates through every file in this directory

def parse_xml(filename):
    et = xml.etree.ElementTree.parse(directory + '/' + filename)
    root = et.getroot()
    bounding_box = root.find('object').find('bndbox')
    xmin = int(bounding_box.find('xmin').text)
    ymin = int(bounding_box.find('ymin').text)
    xmax = int(bounding_box.find('xmax').text)
    ymax = int(bounding_box.find('ymax').text)
    return xmin, ymin, xmax, ymax

def get_image_name(filename):
    et = xml.etree.ElementTree.parse(directory + '/' + filename)
    root = et.getroot()
    return root.find('filename').text

def sort_files(filename):
    split_name = filename.split('_')
    last_section = split_name.pop()
    number = last_section.split('.')[0]
    return int(number)

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
        num_images = len(image_xmls)

        physics_speeds = []

        if not os.path.exists("../output/" + video_name):

            os.mkdir("../output/" + video_name)

            for i in range(num_images - 1):
                curr_image = image_xmls[i]
                next_image = image_xmls[i+1]
                curr_xmin, curr_ymin, curr_xmax, curr_ymax = parse_xml(curr_image)
                next_xmin, next_ymin, next_xmax, next_ymax = parse_xml(next_image)

                next_image_name = get_image_name(next_image)

                curr_centroid = [(curr_xmin + curr_xmax)/2, (curr_ymin + curr_ymax)/2]
                next_centroid = [(next_xmin + next_xmax)/2, (next_ymin + next_ymax)/2]

                # camera_proj_speed = camera_projection_algo.get_camera_projection_speed(curr_centroid, next_centroid) 
                camera_proj_speed = 5

                frisbee_pixel_width = ((next_xmax - next_xmin) + (curr_xmax - curr_xmin))/2

                physics_speed = diameter_algo.get_physics_algo_speed(frisbee_pixel_width, curr_centroid, next_centroid)
                physics_speeds.append(physics_speed)
                # calculate speed traveled with both algorithms --> get_camera_projection_speed() and get_physics_algo_speed()
                # display bounding box and both physics and camera geometry speeds on next image --> kallis_function(cp_speed, physics_speed, image_filename, bbox_coords)
                helpers.draw_on_image(next_xmin, next_ymin, next_xmax, next_ymax, physics_speed, camera_proj_speed, "../data/train/images/" + next_image_name, "../output/" + video_name + "/" + next_image_name)
            
            avg_speed = sum(physics_speeds)/len(physics_speeds)
            helpers.draw_on_image(next_xmin, next_ymin, next_xmax, next_ymax, physics_speed, camera_proj_speed, "../data/train/images/" + next_image_name, "../output/" + video_name + "/" + next_image_name.split(".")[0] + "_avg.jpg", avg_speed=avg_speed)


    # for each throw:
    #     for each image until n - 1 (where n is # of images):
    #         get coordinates of bounding box of both current and next image # parse_xml_files()
    #         calculate speed traveled with both algorithms # get_camera_projection_speed() and get_physics_algo_speed()
    #         display bounding box and both physics and camera geometry speeds on next image # kallis_function(cp_speed, physics_speed, image_filename, bbox_coords)


if __name__ == '__main__':
    main()