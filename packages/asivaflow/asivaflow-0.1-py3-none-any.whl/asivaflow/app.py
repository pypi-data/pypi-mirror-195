import sys
import time
import asivaflow.src as src
import asivaflow.align as align
from asivaflow.clean import Pipeline

def run():
    
    print('\n')
    print('--------------------------------------------------')
    print('| Welcome to ASIVAFLOW - Designed by Team ASIVA! |')
    print('--------------------------------------------------')
    print('\n')

    print("Select any one option of the following:\n"
        " 1) r for Data Reduction\n 2) a for Image Alignment\n 3) Anything else to Quit\n")
    action = input(f"Type your preferred option: ")

    if action == "r":
        iwd = src.workDir()
        st = time.time()
        src.dirCheck()
        asiva = Pipeline(fileDirectory=iwd+'/', resultDirectory=iwd+'/results', badImages=iwd+'/badImages')
        asiva.prepareData()
        et = time.time()

        elapsed_time = et - st
        print('Execution time:', "{:.2f}".format(elapsed_time), 'seconds')

        print("\nThank you for using ASIVAFLOW!\n")

    elif action == 'a':
        align.input_file()

    else:
        print("\nThank you for using ASIVAFLOW!\n")
        sys.exit()