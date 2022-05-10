# Given a list of dirs', this will walk through each directory and make copies of the files with the dir's name as a prefix
## The purpose is to have all the images/annotation live in either the train or validation folders with corresponding names

from asyncio.windows_events import NULL
import shutil
import os
import numpy as np
import os
from check_label import *
import xml.etree.ElementTree


def split_three(lst, ratio=[0.8, 0.1, 0.1]):
    train_r, val_r, test_r = ratio
    assert(np.sum(ratio) == 1.0)  # makes sure the splits make sense
    # note we only need to give the first 2 indices to split, the last one it returns the rest of the list or empty
    indicies_for_splitting = [int(len(lst) * train_r), int(len(lst) * (train_r+val_r))]
    train, val, test = np.split(lst, indicies_for_splitting)
    print(f"train, val, test: {len(train)}, {len(val)}, {len(test)}")
    return train, val, test

def img_copy(dirs: list, destination: str, folder: str):
    dir_cnt = 0
    file_cnt = 0

    for dir in dirs:       
        print(f"Directory: {dir}")
        
        # getting all the files in the source directory
        files = os.listdir(dir)
        subdir_ind = dir.rfind("/")
        subdir = dir[subdir_ind+1:]
        shutil.copytree(dir, destination + "/" + folder + "/" + subdir)
        # check and create img, annot, check folders within each split:
        if not os.path.exists(destination + '/' + folder + '/images'):
            os.makedirs(destination + '/' + folder + '/images')
        if not os.path.exists(destination + '/' + folder + '/annotations'):
            os.makedirs(destination + '/' + folder + '/annotations')
        if not os.path.exists(destination + '/' + folder + '/check'):
            os.makedirs(destination + '/' + folder + '/check')

        #rename all the files in this dir with folder name prefix
        for file in files:
            new_file = destination + "/" + folder + "/" + str(subdir) + "_" + file
            if not os.path.exists(new_file): #if file already exist, remove it (due to windows overwrite issue with 'rename')
                os.rename(destination + "/" + folder + "/" + str(subdir) + "/" + file, new_file) #add clean
                print(f"Renamed {new_file}")
            else:
            #    print(new_file)
                os.remove(new_file) #remove
                os.rename(destination + "/" + folder + "/" + str(subdir) + "/" + file, new_file) #add after remove
            ####### up until here the code is doing what is expected######
            
            if file.endswith('.xml'):
                #shutil.move(destination + "/" + folder + "/" + str(subdir) + "_" + file, 
                #                destination + "/" + folder + "/" + "annotations" + "/" + file) #not sure why this name gets changed 
                os.replace(new_file, destination + "/" + folder + "/" + "annotations" + "/" + str(subdir)+ "_" + file)
                #Now we have to change where the XML is directing the address for the file:
                # Open original file
                et = xml.etree.ElementTree.parse(destination + "/" + folder + "/" + "annotations" + "/" + str(subdir)+ "_" + file)
                xml_folder = et.find('folder')
                xml_filename = et.find('filename')

                xml_filename.text = xml_folder.text + "_" + xml_filename.text
                # Write back to file
                et.write(destination + "/" + folder + "/" + "annotations" + "/" + str(subdir)+ "_" + file)

                #print(f"XML moved from {destination}/{folder}/{subdir}/{file} to \n {new_file}")
            elif file.endswith('.jpg'):
                #shutil.move(destination + "/" + folder + "/" + str(subdir) + "_" + file, 
                #                destination + "/" + folder + "/" + "images" + "/" + subdir + "_" + file)
                os.replace(new_file, destination + "/" + folder + "/" + "images" + "/" + str(subdir)+ "_" + file)
            else:
                #shutil.move(destination + "/" + folder + "/" + subdir + "_" + file, 
                #                destination + "/" + folder + "/" + "check" + "/" + subdir + "_" + file)
                os.replace(new_file, destination + "/" + folder + "/" + "check" + "/" + str(subdir)+ "_" + file)
            
            file_cnt += 1
        os.rmdir(destination + "/" + folder + "/" + subdir)
        dir_cnt += 1
    return dir_cnt, file_cnt


def img_split(dirs: list, destination: str, ratio = [0.8, 0.1, 0.1]):
    
    # split the files into train and validation (note test might need to be added to this as well)
    train, val, test = split_three(dirs, ratio = ratio)
    # check to see if the train, validation, test folder exist, else create it in current dest dir given
    for folder in ['train', 'validation', 'test']:
        if not os.path.exists(destination + '/' + folder):
            os.makedirs(destination + '/' + folder)
            print(f"The {folder} dir doesn't exist, so it has been created, successfully in the data dir!")
        else:
            for subdir in os.listdir(destination + '/' + folder):
                path = os.path.join(destination + '/' + folder, subdir)
                #print(f"path {path}")
                try:
                    shutil.rmtree(path)
                except OSError:
                    try:
                        for files in os.listdir(destination + '/' + folder + '/' + subdir):
                            path = os.path.join(destination + '/' + folder + '/' + subdir, files)
                            os.rmdir(path)
                    except OSError:
                        os.remove(path)
            print(f"The {folder} dir did exist, so it has been removed")


    if len(train) > 0: #not empty
        train_dir_cnt, train_file_cnt = img_copy(dirs= train, destination = destination, folder = 'train')
    else:
        train_dir_cnt, train_file_cnt = 0,0
    if len(val) > 0: #not empty
        val_dir_cnt, val_file_cnt = img_copy(dirs= val, destination = destination, folder = 'validation')
    else:
        val_dir_cnt, val_file_cnt = 0, 0
    if len(test) > 0: #not empty
        test_dir_cnt, test_file_cnt = img_copy(dirs= test, destination = destination, folder = 'test')
    else:
        test_dir_cnt, test_file_cnt = 0,0

    print(f"Was able to move {train_dir_cnt} folders & {train_file_cnt} files into TRAIN")
    print(f"& able to move {val_dir_cnt} folders & {val_file_cnt} files into VALIDATION")
    print(f"& able to move {test_dir_cnt} folders & {test_file_cnt} files into TEST")

if __name__ == "__main__":
    dirs = getDirectoryList('./data/images/')
    #print(dirs)
    dest = "./data"
    ratio = [1.0, 0.0, 0.0]

    img_split(dirs, dest, ratio)