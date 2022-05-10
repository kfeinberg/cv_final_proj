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

def camera_projection_calculation(video1name, video2name):
    xml_files = os.listdir(directory)
    image1_xmls = [
        os.fsdecode(file)
        for file in xml_files
        if os.fsdecode(file).startswith(video1name)
    ]
    image2_xmls = [
        os.fsdecode(file)
        for file in xml_files
        if os.fsdecode(file).startswith(video2name)
    ]
    # parse each xml file for that video in order by appending _[number] to the video name
    image1_xmls = sorted(image1_xmls, key=sort_files)
    image1_xmls = sorted(image2_xmls, key=sort_files)
    num_images = len(image1_xmls)

    physics_speeds = []
    proj_speeds = []

    if not os.path.exists("../output/" + video1name):

        os.mkdir("../output/" + video1name)

        for i in range(num_images - 1):

            curr_image1 = image1_xmls[i]
            next_image1 = image1_xmls[i+1]
            curr_xmin1, curr_ymin1, curr_xmax1, curr_ymax1 = parse_xml(curr_image1)
            next_xmin1, next_ymin1, next_xmax1, next_ymax1 = parse_xml(next_image1)

            curr_centroid1 = [(curr_xmin1 + curr_xmax1)/2, (curr_ymin1 + curr_ymax1)/2]
            next_centroid1 = [(next_xmin1 + next_xmax1)/2, (next_ymin1 + next_ymax1)/2]

            curr_image2 = image2_xmls[i]
            next_image2 = image2_xmls[i+1]
            curr_xmin2, curr_ymin2, curr_xmax2, curr_ymax2 = parse_xml(curr_image2)
            next_xmin2, next_ymin2, next_xmax2, next_ymax2 = parse_xml(next_image2)

            curr_centroid2 = [(curr_xmin2 + curr_xmax2)/2, (curr_ymin2 + curr_ymax2)/2]
            next_centroid2 = [(next_xmin2 + next_xmax2)/2, (next_ymin2 + next_ymax2)/2]

            camera_proj_speed = camera_projection_algo.get_camera_projection_speed([curr_centroid1, next_centroid1], [curr_centroid2, next_centroid2])

            next_image_name = get_image_name(next_image1)
            frisbee_pixel_width = ((next_xmax1 - next_xmin1) + (curr_xmax1 - curr_xmin1))/2
            physics_speed = diameter_algo.get_physics_algo_speed(frisbee_pixel_width, curr_centroid1, next_centroid1)

            physics_speeds.append(physics_speed)
            proj_speeds.append(camera_proj_speed)

            helpers.draw_on_image(next_xmin1, next_ymin1, next_xmax1, next_ymax1, physics_speed, camera_proj_speed, "../data/train/images/" + next_image_name, "../output/" + video1name + "/" + next_image_name)
        
        avg_phys_speed = sum(physics_speeds)/len(physics_speeds)
        avg_proj_speed = sum(proj_speeds)/len(proj_speeds)
        helpers.draw_on_image(next_xmin1, next_ymin1, next_xmax1, next_ymax1, physics_speed, camera_proj_speed, "../data/train/images/" + next_image_name, "../output/" + video1name + "/" + next_image_name.split(".")[0] + "_avg.jpg", avg_phys_speed=avg_phys_speed, avg_proj_speed=avg_proj_speed)

def main():
    camera_projection_calculation("mgvid8", "a_mgvid8")
    # xml_files = os.listdir(directory)
    # # get set of all video/throw names
    # video_names = set()
    # for file in xml_files:
    #     filename = os.fsdecode(file)
    #     split_name = filename.split('_')
    #     split_name.pop()
    #     video_names.add('_'.join(split_name))
    
    # for video_name in video_names:
    #     # select all xml files for that video
    #     image_xmls = [
    #         os.fsdecode(file)
    #         for file in xml_files
    #         if os.fsdecode(file).startswith(video_name)
    #     ]
    #     # parse each xml file for that video in order by appending _[number] to the video name
    #     image_xmls = sorted(image_xmls, key=sort_files)
    #     num_images = len(image_xmls)

    #     physics_speeds = []

    #     if not os.path.exists("../output/" + video_name):

    #         os.mkdir("../output/" + video_name)

    #         for i in range(num_images - 1):
    #             curr_image = image_xmls[i]
    #             next_image = image_xmls[i+1]
    #             curr_xmin, curr_ymin, curr_xmax, curr_ymax = parse_xml(curr_image)
    #             next_xmin, next_ymin, next_xmax, next_ymax = parse_xml(next_image)

    #             next_image_name = get_image_name(next_image)

    #             curr_centroid = [(curr_xmin + curr_xmax)/2, (curr_ymin + curr_ymax)/2]
    #             next_centroid = [(next_xmin + next_xmax)/2, (next_ymin + next_ymax)/2]

    #             camera_proj_speed = 0

    #             frisbee_pixel_width = ((next_xmax - next_xmin) + (curr_xmax - curr_xmin))/2

    #             physics_speed = diameter_algo.get_physics_algo_speed(frisbee_pixel_width, curr_centroid, next_centroid)

    #             physics_speeds.append(physics_speed)
    #             helpers.draw_on_image(next_xmin, next_ymin, next_xmax, next_ymax, physics_speed, camera_proj_speed, "../data/train/images/" + next_image_name, "../output/" + video_name + "/" + next_image_name)
            
    #         avg_speed = sum(physics_speeds)/len(physics_speeds)
    #         helpers.draw_on_image(next_xmin, next_ymin, next_xmax, next_ymax, physics_speed, camera_proj_speed, "../data/train/images/" + next_image_name, "../output/" + video_name + "/" + next_image_name.split(".")[0] + "_avg.jpg", avg_phys_speed=avg_speed)


if __name__ == '__main__':
    main()