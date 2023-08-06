from operator import index
from pyraf import iraf
from iraf import imred
from iraf import ccdred
import pandas as pd
import numpy as np
import os
import sys
import shutil
import glob

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


class Pipeline(object):

    def __init__(self, fileDirectory, resultDirectory, badImages):

        self.fileDirectory = fileDirectory
        self.resultDirectory = resultDirectory
        self.badImages = badImages

    def compatibilityCheck(self, df):
        
        counts = df["int_hjd"].value_counts() 
        drop = list()

        for key, value in counts.items():
            if value < 3:
                drop.append(key)
        
        if len(drop) != 0:
            print("WARNING: The below Julian dates have less than 3 frames\n{drop}\n"
                    "\n Select any one option of the follwowing:\n"
                    " 1) d for Drop the frames & proceed\n 2) q to Quit\n")
            action = input(f"Type your preferred option: ")

            if action == "d":
                df = df[~df.isin(drop)]
                df = df[df['int_hjd'].isnull()]
                for i in df['frames']:
                    shutil.move(i, self.fileDirectory+"/badImages")
                print("\nFrames are moved to badImages folder!")
                print('------------------------------------------------------------------------------')
            elif action == 'q':
                print("\nThank you for using ASIVAFLOW!\n")
                sys.exit()
            else:
                print("\nThank you for using ASIVAFLOW!\n")
                sys.exit()

    def seperateDir(self):
        if "bias" not in os.listdir(self.fileDirectory):
            os.mkdir(self.fileDirectory+"/bias")
            os.mkdir(self.fileDirectory+"bias/badImages")
        if "flat" not in os.listdir(self.fileDirectory):
            os.mkdir(self.fileDirectory+"/flat")
            os.mkdir(self.fileDirectory+"flat/badImages")
            os.mkdir(self.fileDirectory+"flat/u")
            os.mkdir(self.fileDirectory+"flat/b")
            os.mkdir(self.fileDirectory+"flat/v")
            os.mkdir(self.fileDirectory+"flat/r")
            os.mkdir(self.fileDirectory+"flat/i")
        if "light" not in os.listdir(self.fileDirectory):
            os.mkdir(self.fileDirectory+"/light")
            os.mkdir(self.fileDirectory+"light/badImages")
            os.mkdir(self.fileDirectory+"light/u")
            os.mkdir(self.fileDirectory+"light/b")
            os.mkdir(self.fileDirectory+"light/v")
            os.mkdir(self.fileDirectory+"light/r")
            os.mkdir(self.fileDirectory+"light/i")
        if "object" not in os.listdir(self.fileDirectory):
            os.mkdir(self.fileDirectory+"/object")

        self.biasImages = self.all_images[self.all_images["imagetype"] == "bias"]
        if len(self.biasImages) != 0:
            for i in self.biasImages['frames']:
                shutil.move(i, self.fileDirectory+"/bias")
        else:
            print('\nNo bias frames found to proceed!\n')
            sys.exit()

        self.flatImages = self.all_images[self.all_images["imagetype"] == "flat"]
        if len(self.flatImages) != 0:
            for i in self.flatImages['frames']:
                shutil.move(i, self.fileDirectory+"/flat")
        else:
            print('\nNo flat frames found to proceed!\n')
            sys.exit()

        self.lightImages = self.all_images[self.all_images["imagetype"] == "object"]
        if len(self.lightImages) != 0:
            for i in self.lightImages['frames']:
                shutil.move(i, self.fileDirectory+"/light")
        else:
            print('\nNo light frames found to proceed!\n')
            sys.exit()

        self.objectFolders = self.all_images[self.all_images["imagetype"] == "object"]["object"]
        # self.objectFilters = self.all_images[self.all_images["imagetype"] == "object"]["filter"]

        for i in self.objectFolders.unique():
            os.mkdir(self.fileDirectory+"/object/"+i)
            # for j in self.objectFilters.unique():
            #     os.mkdir(self.fileDirectory+"/object/"+i+"/"+j)

    def outlierRemoval(self, input_loc, output_loc, csv_name):
        input = glob.glob(input_loc)
        mean = []
        file_name = []
        for i in input:
            file_mean = iraf.imstat(i, fields="mean", Stdout=1)
            file_mean.pop(0)
            file_name.append(i)
            for x in file_mean:
                mean.append(x)
        df_mean = pd.DataFrame(mean, columns=["mean"])
        df_name = pd.DataFrame(file_name, columns=["name"])

        name_and_mean = pd.concat([df_name['name'], df_mean['mean']], axis=1)
        name_and_mean['mean'] = pd.to_numeric(
            name_and_mean['mean'], errors='coerce')

        q1, q3 = np.quantile(name_and_mean['mean'], [0.15, 0.85])
        iqr = q3-q1
        lowerFence = q1 - 3*iqr
        upperFence = q3 + 3*iqr
        errorFiles = name_and_mean.loc[name_and_mean['mean'].gt(
            lowerFence) ^ name_and_mean['mean'].lt(upperFence) & name_and_mean['mean'] > 0]

        print(len(errorFiles),'poor frames found! Moved to badImage directory!')

        for f in errorFiles['name']:
            shutil.move(f, output_loc)

        updatedList = []
        file = iraf.hselect(
            input_loc, 'date-obs,hjd,imagetyp,object,filter,exptime,$I', 'yes', Stdout=1)
        for i in file:
            updatedList.append(i.split('\t'))

        self.updated_file = pd.DataFrame(
            updatedList, columns=['date', 'hjd', 'imagetype', 'object', 'filter', 'exposure', 'frames']).sort_values(by=['filter', 'hjd'])
        self.updated_file['int_hjd'] = [
            i.split(".")[0] for i in self.updated_file["hjd"]]
        self.updated_file.to_csv(
            self.resultDirectory+"/"+csv_name, header=True, index=None)

    def masterBias(self):
        if "masterBias" not in os.listdir(self.fileDirectory+"bias"):
            os.mkdir(self.fileDirectory+"bias/masterBias")

        mas = []
        for i, j in enumerate((self.updated_file["int_hjd"].value_counts().keys()).sort_values()):
            file = self.updated_file[self.updated_file["int_hjd"] == j]
            hjd = pd.Series(file['hjd'])
            hjd = hjd.to_string(index=False)
            frames = pd.Series(file['frames'])
            frames = frames.to_string(index=False)

            with open(self.fileDirectory+"bias/temp.txt", "a") as f:
                for k in file["frames"]:
                    f.write(k+"\n")
            iraf.ccdred.zerocombine(input='@'+self.fileDirectory+'bias/temp.txt', output=self.fileDirectory +
                                    "bias/masterBias/zero"+str(i), ccdtype='', process='no', combine='average')

            mas.append(
                [hjd, frames, j, self.fileDirectory+"bias/masterBias/zero"+str(i)])
            os.remove(self.fileDirectory+"bias/temp.txt")

        self.mBias = pd.DataFrame(
            mas, columns=["hjd", "input", "int_hjd", "masterbias"]).sort_values(by=['int_hjd'])
        self.mBias.to_csv(self.resultDirectory +
                          '/master_Bias.csv', header=True, index=None)

    def biasCorrect(self, resultDir, nameOfOperation, csv_name):
        self.mBias['int_hjd'] = pd.to_numeric(self.mBias['int_hjd'])
        mas = []
        for i, j, k, l in zip(self.updated_file["int_hjd"], self.updated_file['frames'], self.updated_file['filter'], self.updated_file['hjd']):
            if i in self.mBias["int_hjd"].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i].values[0]
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with same night frame!\n')

            elif (i+1) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i+1].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i+1]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 1 night ahead frame!\n')

            elif (i-1) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i-1].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i-1]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 1 night previous frame!\n')

            elif (i+2) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i+2].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i+2]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 2 nights ahead frame!\n')

            elif (i-2) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i-2].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i-2]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 2 nights previous frame!\n')

            elif (i+3) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i+3].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i+3]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 3 nights ahead frame!\n')

            elif (i-3) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i-3].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i-3]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 3 nights previous frame!\n')

            elif (i+4) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i+4].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i+4]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 4 nights ahead frame!\n')

            elif (i-4) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i-4].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i-4]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 4 nights previous frame!\n')

            elif (i+5) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i+5].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i+5]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 5 nights ahead frame!\n')

            elif (i-5) in self.mBias['int_hjd'].values:
                mbias_file = self.mBias["masterbias"][self.mBias["int_hjd"]
                                                      == i-5].values[0]
                print('Looking for nearby nights...')
                print(i, j, (self.mBias[self.mBias['int_hjd'] == i-5]['int_hjd']).to_string(index=False), mbias_file)
                print('Mapped with 5 nights previous frame!\n')

            else:
                print(i, j)
                print(
                    'Mapped with 1st frame as no nearby frames were found beyond 5 nights!\n')
                mbias_file = self.mBias["masterbias"][0]

            iraf.imarith(operand1=j, op='-', operand2=mbias_file,
                         result=self.fileDirectory+resultDir+j.split('/')[-1])
            mas.append([l, i, k, j, mbias_file, self.fileDirectory+resultDir +
                        j.split('/')[-1]])
            self.biasCorrected = pd.DataFrame(
                mas, columns=["hjd", "int_hjd", "filter", "input", "MBias", nameOfOperation]).sort_values(by=['filter', 'int_hjd'])

            self.biasCorrected.to_csv(
                self.resultDirectory+'/' + csv_name, header=True, index=None)

    def masterFlat_normalization(self, file_name, filter_name):
        mas = []
        for i, j in enumerate((file_name['int_hjd'].value_counts().keys()).sort_values()):
            file = file_name[file_name["int_hjd"] == j]
            hjd = pd.Series(file['hjd'])
            hjd = hjd.to_string(index=False)
            frames = pd.Series(file['input'])
            frames = frames.to_string(index=False)

            with open(self.fileDirectory+"flat/temp.txt", "a") as f:
                for k in file["biasCorrectedflat"]:
                    f.write(k+"\n")

            iraf.ccdred.flatcombine(input='@'+self.fileDirectory+'flat/temp.txt', output=self.fileDirectory +
                                    "flat"+'/'+filter_name+'/mFlat'+str(i), ccdtype='', process='no', combine='average')

            mas.append([hjd, frames, j,  self.fileDirectory+'flat' +
                       '/'+filter_name+'/mFlat'+str(i)])
            os.remove(self.fileDirectory+'flat/temp.txt')

        self.mFlat = pd.DataFrame(
            mas, columns=["hjd", "input", "int_hjd", 'masterflat__'+filter_name])
        """Normalization"""

        normal = []
        for i, j, k in zip(self.mFlat['int_hjd'], self.mFlat['masterflat__'+filter_name], self.mFlat['hjd']):
            midpt = iraf.imstat(images=j, fields="midpt",
                                format='no', Stdout=1)
            iraf.imarith(operand1=j, op='/', operand2=float(
                midpt[0]), result=self.fileDirectory+'flat'+'/'+filter_name+'/n'+j.split('/')[-1])
            normal.append([k, j, float(midpt[0]), i, self.fileDirectory+'flat'+'/' +
                          filter_name+'/n'+j.split('/')[-1]])

        self.nFlat = pd.DataFrame(
            normal, columns=['hjd', 'input', 'median', 'int_hjd', 'normalizedflat__'+filter_name])

    def moveFilesBasedOnFilter(self, name, u, b, v, r, i):
        for _, row in self.biasCorrected.iterrows():
            if row['filter'] == 'u':
                shutil.move(row['biasCorrected'+name],
                            self.fileDirectory+name+'/'+u)
            elif row['filter'] == 'b':
                shutil.move(row['biasCorrected'+name],
                            self.fileDirectory+name+'/'+b)
            elif row['filter'] == 'v':
                shutil.move(row['biasCorrected'+name],
                            self.fileDirectory+name+'/'+v)
            elif row['filter'] == 'r':
                shutil.move(row['biasCorrected'+name],
                            self.fileDirectory+name+'/'+r)
            elif row['filter'] == 'i':
                shutil.move(row['biasCorrected'+name],
                            self.fileDirectory+name+'/'+i)
            else:
                print('Filter not supported!')

    def flatCorrectedLight(self, file_name, filter_name, flat_name):
        mas = []
        for i, j, k in zip(file_name['int_hjd'], file_name['biasCorrectedlight'], file_name['hjd']):
            if i in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i].values[0]
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i]['int_hjd']).to_string(index=False))
                print('Mapped with same night frame!\n')

            elif (i+1) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i+1].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i+1]['int_hjd']).to_string(index=False))
                print('Mapped with 1 night ahead frame!\n')

            elif (i-1) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i-1].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i-1]['int_hjd']).to_string(index=False))
                print('Mapped with 1 night previous frame!\n')

            elif(i+2) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i+2].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i+2]['int_hjd']).to_string(index=False))
                print('Mapped with 2 nights ahead frame!\n')

            elif (i-2) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i-2].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i-2]['int_hjd']).to_string(index=False))
                print('Mapped with 2 nights previous frame!\n')

            elif (i+3) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i+3].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i+3]['int_hjd']).to_string(index=False))
                print('Mapped with 3 nights ahead frame!\n')

            elif (i-3) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i-3].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i-3]['int_hjd']).to_string(index=False))
                print('Mapped with 3 nights previous frame!\n')

            elif (i+4) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i+4].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i+4]['int_hjd']).to_string(index=False))
                print('Mapped with 4 nights ahead frame!\n')

            elif (i-4) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i-4].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i-4]['int_hjd']).to_string(index=False))
                print('Mapped with 4 nights previous frame!\n')

            elif (i+5) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i+5].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i+5]['int_hjd']).to_string(index=False))
                print('Mapped with 5 nights ahead frame!\n')

            elif (i-5) in flat_name['int_hjd'].values:
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][flat_name['int_hjd'] == i-5].values[0]
                print('Looking for nearby nights...')
                print(i, j, nFlat_file, (flat_name[flat_name['int_hjd'] == i-5]['int_hjd']).to_string(index=False))
                print('Mapped with 5 nights previous frame!\n')

            else:
                print(i,j)
                print(
                    'Mapped with 1st frame as no nearby frames were found beyond 5 nights!\n')
                nFlat_file = flat_name['normalizedflat__' +
                                       filter_name][0]
            iraf.imarith(operand1=j, op='/', operand2=nFlat_file,
                         result=self.fileDirectory+'light'+'/'+filter_name+'/f'+j.split('/')[-1])

            mas.append([k, i, filter_name, j, nFlat_file, self.fileDirectory+'light'+'/' +
                        filter_name+'/f'+j.split('/')[-1]])

        self.mLight = pd.DataFrame(
            mas, columns=["hjd", 'int_hjd', 'filter', 'biasCorrectedlight', 'nmFlat', 'cleanedLight'])

        self.objectImages = self.mLight['cleanedLight']
        for i in self.objectImages:
            shutil.copy(i, self.fileDirectory+'object/')

    def moveFilesBasedOnObject(self, name):
        list3 = []
        file3 = iraf.hselect(self.fileDirectory+name+'/'+'fb*.fits','object,filter,$I', 'yes', Stdout=1)
        for i in file3:
            list3.append(i.split('\t'))

        self.objectNames = pd.DataFrame(list3, columns=['object', 'filter', 'frames']).sort_values(by=['object'])
        for i in (self.objectNames['object']).unique():
            for j in self.objectNames[self.objectNames['object'] == i]['frames']:
                shutil.move(j, self.fileDirectory+name+'/'+i+'/')

    def dataCheck(self):
        # removing the bad image at early stage
        for x in os.listdir():
            if x.endswith(".fits"):
                try:
                    file_mean = iraf.imstat(x, fields="mean", Stdout=1)
                    file_mean.pop(0)
                except Exception as e:
                    print(
                        'Warning:', x, 'is moved to badImage directory as it is a corrupt frame!')
                    print(
                        '------------------------------------------------------------------------------')
                    print('\n')
                    shutil.move(x, self.badImages)

        # taking raw good images
        list1 = []
        file1 = iraf.hselect(self.fileDirectory+'*.fits',
                            'date-obs,hjd,imagetyp,object,filter,exptime,$I', 'yes', Stdout=1)
        for i in file1:
            list1.append(i.split('\t'))
        # all_images
        self.raw_images = pd.DataFrame(list1, columns=[
            'date', 'hjd', 'imagetype', 'object', 'filter', 'exposure', 'frames']).sort_values(by=['hjd', 'imagetype'])

        self.raw_images['int_hjd'] = [
            i.split(".")[0] for i in self.raw_images["hjd"]]

        print('\nA total of ', len(self.raw_images.index), ' frames found!')
        print(
            '------------------------------------------------------------------------------')

        # saving all images to csv
        self.raw_images.to_csv(self.resultDirectory+'/raw_images.csv',
                               index=None, header=True)

        # checking minimum no. of frames to proceed
        bias_frames = self.raw_images[self.raw_images["imagetype"] == "bias"]
        if len(bias_frames) !=0:
            print('\nChecking bias frames...')
            self.compatibilityCheck(self.raw_images[self.raw_images["imagetype"] == "bias"])
        else:
            print('\nNo bias frames found to check!\n')
            sys.exit()

        flat_frames = self.raw_images[self.raw_images["imagetype"] == "flat"]
        flat_filters = flat_frames['filter'].unique()
        if len(flat_frames) !=0:
            for i in flat_filters:
                print('\nChecking '+i+' filter flat frames...')
                self.compatibilityCheck(flat_frames[self.raw_images['filter']==i])
        else:
            print('\nNo flat frames found to check!\n')
            sys.exit()

    """THIS IS THE MAIN FUNCTION"""

    def prepareData(self):

        self.dataCheck()
        print('\nData check completed!')
        print('------------------------------------------------------------------------------')

        # taking good images
        list2 = []
        file2 = iraf.hselect(self.fileDirectory+'*.fits',
                            'date-obs,hjd,imagetyp,object,filter,exptime,$I', 'yes', Stdout=1)
        for i in file2:
            list2.append(i.split('\t'))
        # all_images
        self.all_images = pd.DataFrame(list2, columns=[
            'date', 'hjd', 'imagetype', 'object', 'filter', 'exposure', 'frames']).sort_values(by=['hjd', 'imagetype'])

        self.all_images['int_hjd'] = [
            i.split(".")[0] for i in self.all_images["hjd"]]

        print('\nA total of ', len(self.all_images.index), ' frames loaded!')
        print(
            '------------------------------------------------------------------------------')
        # saving all images to csv
        self.all_images.to_csv(self.resultDirectory+'/all_images.csv',
                               index=None, header=True)

        # making seperate Directory for flat/bias/light file
        self.seperateDir()

        """BIAS"""
        print('\n')
        print('Detecting poor Bias frames...')
        self.outlierRemoval(self.fileDirectory+"bias/*.fits",
                            self.fileDirectory+"bias/badImages", 'bias_images.csv')
        print('\n')

        # making master bias
        print('Creating Master Bias frames...')
        self.masterBias()
        print('A total of ', len(self.mBias.index),
              ' Master Bias frames created!')
        master_biasFile = self.mBias
        print(
            '------------------------------------------------------------------------------')

        """FLAT"""
        print('\n')
        print('Detecting poor Flat-field frames...')
        self.outlierRemoval(self.fileDirectory+"flat/*.fits",
                            self.fileDirectory+"flat/badImages", 'flat_images.csv')
        print('\n')

        # making the flat Corrected
        self.updated_file['int_hjd'] = pd.to_numeric(
            self.updated_file['int_hjd'])

        print('Cleaning Flat-field frames...')
        self.biasCorrect("flat/b", "biasCorrectedflat",
                         "biasCorrectedFlat.csv")
        print('A total of ', len(self.biasCorrected.index),
              ' Flat frames cleaned!')
        print('\n')
        flat_files_updated = self.biasCorrected

        u_flat = flat_files_updated[flat_files_updated['filter'] == 'u']
        b_flat = flat_files_updated[flat_files_updated['filter'] == 'b']
        v_flat = flat_files_updated[flat_files_updated['filter'] == 'v']
        r_flat = flat_files_updated[flat_files_updated['filter'] == 'r']
        i_flat = flat_files_updated[flat_files_updated['filter'] == 'i']

        # calling master Flat and normalization together

        print('Creating Master Flat-field frames & Normalizing it for U filter...')
        self.masterFlat_normalization(u_flat, 'u')
        m_flatU = self.mFlat
        n_flatU = self.nFlat
        print('A total of ', len(n_flatU.index),
              ' Normalized Master Flat-field frames created!')
        print('\n')

        print('Creating Master Flat-field frames & Normalizing it for B filter...')
        self.masterFlat_normalization(b_flat, 'b')
        m_flatB = self.mFlat
        n_flatB = self.nFlat
        print('A total of ', len(n_flatB.index),
              ' Normalized Master Flat-field frames created!')
        print('\n')

        print('Creating Master Flat-field frames & Normalizing it for V filter...')
        self.masterFlat_normalization(v_flat, 'v')
        m_flatV = self.mFlat
        n_flatV = self.nFlat
        print('A total of ', len(n_flatV.index),
              ' Normalized Master Flat-field frames created!')
        print('\n')

        print('Creating Master Flat-field frames & Normalizing it for R filter...')
        self.masterFlat_normalization(r_flat, 'r')
        m_flatR = self.mFlat
        n_flatR = self.nFlat
        print('A total of ', len(n_flatR.index),
              ' Normalized Master Flat-field frames created!')
        print('\n')

        print('Creating Master Flat-field frames & Normalizing it for I filter...')
        self.masterFlat_normalization(i_flat, 'i')
        m_flatI = self.mFlat
        n_flatI = self.nFlat
        print('A total of ', len(n_flatI.index),
              ' Normalized Master Flat-field frames created!')

        masterFlat = pd.concat(
            [m_flatB, m_flatR, m_flatI, m_flatU, m_flatU, m_flatV], ignore_index=True, axis=1)

        normalisedFlat = pd.concat(
            [n_flatB, n_flatR, n_flatI, n_flatU, n_flatV], ignore_index=True, axis=1)

        masterFlat.to_csv(self.resultDirectory+'/master_Flat.csv',
                          header=True, index=None)

        normalisedFlat.to_csv(self.resultDirectory +
                              '/normalized_Flat.csv', header=True, index=None)
        print(
            '------------------------------------------------------------------------------')
        print('\n')
        # move files based on FILTER for flat
        self.moveFilesBasedOnFilter("flat", "u", "b", "v", "r", "i")

        """LIGHT"""
        # for light
        print('Detecting poor Light frames...')
        self.outlierRemoval(self.fileDirectory+"light/*.fits",
                            self.fileDirectory+"light/badImages", 'light_images.csv')
        print('\n')

        self.updated_file['int_hjd'] = pd.to_numeric(
            self.updated_file['int_hjd'])
        print('Cleaning Light frames...')
        # making the light corrected
        self.biasCorrect("light/b", "biasCorrectedlight",
                         "biasCorrectedlight.csv")
        print('A total of ', len(self.biasCorrected.index),
              ' Light frames cleaned!')
        print('\n')
        lightFiles = self.biasCorrected

        u_light = lightFiles[lightFiles['filter'] == 'u']
        b_light = lightFiles[lightFiles['filter'] == 'b']
        v_light = lightFiles[lightFiles['filter'] == 'v']
        r_light = lightFiles[lightFiles['filter'] == 'r']
        i_light = lightFiles[lightFiles['filter'] == 'i']

        # calling flat corrected light

        print('Flat-fielding Light frames for U filter...')
        self.flatCorrectedLight(u_light, 'u', n_flatU)
        u_correctLight = self.mLight
        print('A total of ', len(u_correctLight.index),
              ' Light frames flat-fielded!')
        print('\n')

        print('Flat-fielding Light frames for B filter...')
        self.flatCorrectedLight(b_light, 'b', n_flatB)
        b_correctLight = self.mLight
        print('A total of ', len(b_correctLight.index),
              ' Light frames flat-fielded!')
        print('\n')

        print('Flat-fielding Light frames for V filter...')
        self.flatCorrectedLight(v_light, 'v', n_flatV)
        v_correctLight = self.mLight
        print('A total of ', len(v_correctLight.index),
              ' Light frames flat-fielded!')
        print('\n')

        print('Flat-fielding Light frames for R filter...')
        self.flatCorrectedLight(r_light, 'r', n_flatR)
        r_correctLight = self.mLight
        print('A total of ', len(r_correctLight.index),
              ' Light frames flat-fielded!')
        print('\n')

        print('Flat-fielding Light frames for I filter...')
        self.flatCorrectedLight(i_light, 'i', n_flatI)
        i_correctLight = self.mLight
        print('A total of ', len(i_correctLight.index),
              ' Light frames flat-fielded!')

        flatCorrectedLight = pd.concat(
            [b_correctLight, r_correctLight, u_correctLight, v_correctLight, i_correctLight], ignore_index=True)

        flatCorrectedLight.to_csv(
            self.resultDirectory+'/flatCorrectedLight.csv', header=True, index=None)

        # move files based of FILTER for light
        self.moveFilesBasedOnFilter("light", "u", "b", "v", "r", "i")
        self.moveFilesBasedOnObject("object")

        print(
            '------------------------------------------------------------------------------')

        print('______________________________________________')
        print('| Job Done! Data Reduction complete! Cheers! |')
        print('``````````````````````````````````````````````')


        # make log file

        # append empty row in each dataFrame
        flat_files_updated = flat_files_updated.append(
            pd.Series(), ignore_index=True)

        masterFlat = masterFlat.append(
            pd.Series(), ignore_index=True)

        normalisedFlat = normalisedFlat.append(
            pd.Series(), ignore_index=True)

        lightFiles = lightFiles.append(
            pd.Series(), ignore_index=True)

        flatCorrectedLight = flatCorrectedLight.append(
            pd.Series(), ignore_index=True)

        # make log file
        df = pd.concat([flat_files_updated, masterFlat,
                        normalisedFlat, lightFiles, flatCorrectedLight], axis=0)

        df.to_csv(self.fileDirectory+'log.csv', header=None, index=None)
