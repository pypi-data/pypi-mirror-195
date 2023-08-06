import astroalign as aa
import numpy as np
from astropy.io import fits
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob


def input_file():
    dir_path = input("\nEnter path of the working directory: ")
    print("Working directory is: " +dir_path)
    print( )
    while os.path.isdir(dir_path) != True:
        print( )
        print("Please choose correct directory!\n")
        dir_path = input("Enter path of the working directory: ")
        print("Working directory is: " + dir_path)

    source_path = input("Enter path of the Source image: ")
    print("Source image: " +source_path)
    print( )
    while os.path.isfile(source_path) != True:
        print( )
        print("Please provide correct Source image path!\n")
        source_path = input("Enter path of the Source image: ")
        print("Source image is: " +source_path)

    target_path = input("Enter path of the Target directory: ")
    print("Target directory is: " +target_path)
    print( )
    while os.path.isdir(target_path) != True:
        print( )
        print("Please provide correct Target directory path!\n")
        target_path = input("Enter path of the Target directory: ")
        print("Target directory is: " +target_path)
    target_files = glob.glob(target_path+'/*.fits') # read target files from directory

    mode = input("Type d for Default or m for Manual: ")
    while mode != 'd' and mode != 'D' and mode != 'm' and mode != 'M':
        mode = input("Type d for Default or m for Manual: ")
    operation(mode, dir_path, source_path, target_files)

def operation(mode, dir_path, source_path, target_files):
    os.chdir(dir_path)
    source = fits.getdata(source_path)
    source_array = np.array(source,dtype = "float64")
    if mode == 'd' or mode =='D':
        for tar_list in range(0, int(len(target_files)), 1):
            target_name = os.path.basename(target_files[tar_list])
            print("\nTarget image: "+target_name)
            target = fits.getdata(target_files[tar_list])
            target_array = np.array(target, dtype = "float64")
            transf, (source_list, target_list) =aa.find_transform(source_array, target_array)
            print("Translation: (x, y) = ({:.2f}, {:.2f})".format(*transf.translation))
            df_trans = pd.DataFrame(transf.translation).transpose()
            df_targ_list = pd.DataFrame(target_list)
            df_targ_list.to_csv('{}.csv'.format(os.path.splitext(target_name)[0]), header=False, index=False)
            print("\n\n")
    if mode == 'm' or mode =='M': 
        #max_control_points
        try:
            max_control_points = int(input("Enter The value of max_control_points:"))
        except:
            print("Enter Numbers Only")
            max_control_points = int(input("Enter The value of max_control_points:"))
        while max_control_points == 0:
            try:
                max_control_points = int(input("Enter The value of max_control_points:"))
            except:
                print("Enter Numbers Only")
                max_control_points = int(input("Enter The value of max_control_points:"))
        #detection sigma        
        try:
            detection_sigma = int(input("Enter The value of detection_sigma:"))
        except:
            print("Enter Numbers Only")
            detection_sigma = int(input("Enter The value of detection_sigma:"))
        while detection_sigma == 0:
            try:
                detection_sigma = int(input("Enter The value of detection_sigma:"))
            except:
                print("Enter Numbers Only")
                detection_sigma = int(input("Enter The value of detection_sigma:"))
        #min_area
        try:
            min_area = int(input("Enter The value of min_area:"))
        except:
            print("Enter Numbers Only")
            min_area = int(input("Enter The value of min_area:"))
        while min_area == 0:
            try:
                min_area = int(input("Enter The value of min_area:"))
            except:
                print("Enter Numbers Only")
                min_area = int(input("Enter The value of min_area:"))
        #passing parameters        
        for tar_list in range(0, int(len(target_files)), 1):
            target_name = os.path.basename(target_files[tar_list])
            print("Target image: "+target_name)
            target = fits.getdata(target_files[tar_list])
            target_array = np.array(target, dtype = "float64")
            transf, (source_list, target_list) =aa.find_transform(source_array, target_array,max_control_points, detection_sigma, min_area)
            print("Translation: (x, y) = ({:.2f}, {:.2f})".format(*transf.translation))
            df_trans = pd.DataFrame(transf.translation).transpose()
            df_targ_list = pd.DataFrame(target_list)
            df_targ_list.to_csv('{}.csv'.format(os.path.splitext(target_name)[0]), header=False, index=False)
            print("\n\n")