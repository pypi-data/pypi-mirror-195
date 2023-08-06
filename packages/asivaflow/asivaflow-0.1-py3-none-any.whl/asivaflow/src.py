import os
import sys
import glob
import time
import shutil
from asivaflow.clean import Pipeline

global iwd

def workDir():
    global wd

    cwd = os.getcwd()
    print('Current working directory: '+cwd+'\n')

    print("Do you want to continue with the current working directory?\n"
        "\n Select any one option of the following:\n"
        " 1) n for new working directory\n 2) q to Quit\n 3) anything else to continue\n")
    action = input(f"Type your preferred option: ")
    if action == "n":
        print("Note: Do not put quotes ('') or backslash (/) in the end of the working directory\n")
        wd = input("Enter your working directory: ")
        if wd == "":
            print("\nBlank input! Thank you for using ASIVAFLOW!\n")
            sys.exit()
    elif action == "q":
        print("\nThank you for using ASIVAFLOW!\n")
        sys.exit()
    else:
        print("\ncontinuing with current working directory...\n")
        wd = cwd
    print('\n')
    os.chdir(wd)
    return wd

def wipe():

    dirs = ["badImages", "bias", "flat", "light", "object", "results"]

    for i in dirs:
        shutil.rmtree(wd+"/"+i, ignore_errors=True)

    for i in glob.glob(wd+"/log*"):
        os.remove(i)

def reset():

    bias = glob.glob(wd+"/bias/*.fits")
    flats = glob.glob(wd+"/flat/*.fits")
    lights = glob.glob(wd+"/light/*.fits")

    badImages = glob.glob(wd+"/badImages/*.fits")
    biasbadImages = glob.glob(wd+"/bias/badImages/*.fits")
    flatbadImages = glob.glob(wd+"/flat/badImages/*.fits")
    lightbadImages = glob.glob(wd+"/light/badImages/*.fits")

    files = [bias, flats, lights, badImages, biasbadImages, flatbadImages, lightbadImages]

    for i in files:
        for j in i:
            try:
                shutil.move(j, wd+"/")
            except:
                ip = os.path.basename(j)
                op = os.path.join(wd+"/")
                mv = os.path.join(op, ip)
                shutil.move(ip, mv)
    wipe()

def backup():
    backup_file = "backup_"+str(time.time())
    backup_dir = wd+"/backup"
    os.mkdir(backup_dir)

    assets = ["badImages", "bias", "flat", "light", "object", "results", "log.csv", "logfile"]

    for i in assets:
        try:
            shutil.move(wd+"/"+i, backup_dir)
        except:
            pass

    shutil.make_archive(backup_file, 'zip', root_dir=wd, base_dir=backup_dir)

def dirCheck():
    files = glob.glob(wd+'/'+'*.fits')

    if os.path.exists(wd):
        if(len(files) != 0):
            if "results" and "badImages" not in os.listdir(wd):
                os.mkdir(wd+"/results")
                os.mkdir(wd+'/badImages')
            else:
                print("WARNING: Results of a previous run has been found in this working directory!\n"
                    "\n Select any one option of the follwowing:\n"
                    " 1) r for Reset previous data & exit\n 2) a for Append previous data & proceed\n 3) w for Wipe previous data & proceed\n 4) b for Backup previous data & proceed\n 5) q for Quit\n")
                action = input(f"Type your preferred option: ")
                if action == "r":
                    print("\nResetting previous data...")
                    reset()
                    print("\nReset successful!\n")
                    sys.exit()
                elif action == "a":
                    print("\nAppending previous data...")
                    reset()
                    print("\nAppend successful!")
                    print("\nProceeding for next steps...\n")
                    os.mkdir(wd+"/results")
                    os.mkdir(wd+'/badImages')
                    time.sleep(3)
                elif action == "w":
                    print("\nWiping previous data...")
                    wipe()
                    print("\nWipe successful!\n")
                    print("\nProceeding for next steps...\n")
                    os.mkdir(wd+"/results")
                    os.mkdir(wd+'/badImages')
                    time.sleep(3)
                elif action == "b":
                    print("\nBackuping previous data...")
                    backup()
                    shutil.rmtree(wd+"/backup", ignore_errors=True)
                    print("\nBackup successful!")
                    print("\nProceeding for next steps...\n")
                    os.mkdir(wd+"/results")
                    os.mkdir(wd+'/badImages')
                    time.sleep(3)
                else:
                    print("\nThank you for using ASIVAFLOW!\n")
                    sys.exit()                    
        else:
            if "results" and "badImages" in os.listdir(wd):
                print('\nNo FITS images found in the working directory!\n')
                print("WARNING: Results of a previous run has been found in this working directory!\n"
                    "\n Select any one option of the follwowing:\n"
                    " 1) r for Reset previous data\n 2) w for Wipe previous data\n 3) b for Backup previous data\n 4) q for Quit\n")
                action = input(f"Type your preferred option: ")
                if action == "r":
                    print("\nResetting previous data...")
                    reset()
                    print("\nReset successful!\n")
                    sys.exit()
                elif action == "w":
                    print("\nWiping previous data...")
                    wipe()
                    print("\nWipe successful!\n")
                    sys.exit()
                elif action == "b":
                    print("\nBackuping previous data ...")
                    backup()
                    shutil.rmtree(wd+"/backup", ignore_errors=True)
                    print("\nBackup successful!")
                    sys.exit()
                elif action == "q":
                    print("\nThank you for using ASIVAFLOW!\n")
                    sys.exit()
                else:
                    print("\nThank you for using ASIVAFLOW!\n")
                    sys.exit()
            else:
                print('No FITS images found! The working directory is empty!')
                print("\nThank you for using ASIVAFLOW!\n")
                sys.exit()
    else:
        print("Directory doesn't exists!")
        print("\nThank you for using ASIVAFLOW!\n")
        sys.exit()