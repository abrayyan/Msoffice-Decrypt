import msoffcrypto
import os
import errno
import re
import time
import threading
import multiprocessing
import time


class permutation:
    digits_c = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    lowerLetters_c = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'
        , 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r'
        , 's', 't', 'u', 'v', 'w', 'x', 'y']

    upperLetters_c = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'
        , 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R'
        , 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

    specialCharacters_c = ['!', '@', '#', '$', '%', '^', '&', '*']

    # typeMap = {'digits' : digits_c ,
    #          'lower' : lowerLetters_c,
    #          'upper' : upperLetters_c,
    #          'special' : specialCharacters_c}

    maxLinesPerFile = 500003
    progressBarStep = 50  # change this
    fileNameRule = re.compile(r'\b\d+_\d+\b')
    dirNameRule = re.compile(r'\b\d+\b')

    ##------------------------------------------------------------------------------
    ## Use this to generate different values to be used to generate the permutations
    # for i in range(ord('A'), ord('Z')):
    #    print('\'' + chr(i) + '\' ,' , end="")
    ##------------------------------------------------------------------------------

    def generate_n_perm(psswdLength, dirPath, combinationsList):

        numberOfCombinations = len(combinationsList) ** psswdLength
        print("\nNumber of possible combinations : {0}\n".format(numberOfCombinations))

        psubDirPath = os.path.join(dirPath, str(psswdLength))
        if (not os.path.exists(psubDirPath)):
            os.makedirs(psubDirPath)

        if (psswdLength == 1):

            fileOutPath = os.path.join(psubDirPath, "{}_0".format(psswdLength))

            try:
                fileOut = open(fileOutPath, 'w')
                for p in combinationsList:
                    fileOut.write(p + '\n')

                fileOut.close()
                print(
                    "Combintations successfully created for password length {0} and saved to '{1}'".format(psswdLength,
                                                                                                           fileOutPath))
                return 1

            except:
                print("error happen whilst creating/writing combinations of password length {0} to '{1}'".format(
                    psswdLength, fileOutPath))
                return 0

        else:

            prepsubDirPath = os.path.join(dirPath, str(psswdLength - 1))
            dirContentsList = os.listdir(prepsubDirPath)
            preFileList = []

            for preFileName in dirContentsList:
                if (permutation.fileNameRule.match(preFileName)):
                    # if("{}_".format(psswdLength-1) in preFileName):
                    preFileList.append(preFileName)

            try:
                fileOutFlow = 0
                fileOutFlowCount = 0
                fileOutPath = os.path.join(psubDirPath, "{0}_{1}".format(psswdLength, fileOutFlow))
                fileOut = open(fileOutPath, "w")

                percentagePrint = 0
                percentageCount = 0
                print("{}%".format(percentagePrint), end="")

                for i in range(len(preFileList)):

                    fileInPath = os.path.join(prepsubDirPath, "{0}_{1}".format(psswdLength - 1, i))
                    fileIn = open(fileInPath, "r")

                    for line in fileIn:

                        line = line.strip()

                        for p in combinationsList:

                            fileOut.write(line + p + "\n")
                            fileOutFlowCount += 1
                            percentageCount += 1

                            if (int((percentageCount / numberOfCombinations) * 100) > percentagePrint):
                                percentagePrint = int((percentageCount / numberOfCombinations) * 100)
                                print("\r{}%".format(percentagePrint), end="")

                            if (fileOutFlowCount >= permutation.maxLinesPerFile):
                                fileOutFlowCount = 0
                                fileOutFlow += 1
                                fileOut.close()
                                print(
                                    "\nFile out limit reached for file '{0}' , saving the file and opening another one".format(
                                        fileOutPath))

                                fileOutPath = os.path.join(psubDirPath, "{0}_{1}".format(psswdLength, fileOutFlow))
                                fileOut = open(fileOutPath, "w")

                fileOut.close()
                print("\n\nCombintations successfully created for password length {0} and saved to {1}".format(
                    psswdLength, psubDirPath))
                print("{} new files were created".format(fileOutFlow + 1))
                # for i in range(fileOutFlow+1):
                #    fileOutPath = os.path.join(dirPath, "{0}_{1}".format(psswdLength, i))
                #    print("'{}'".format(fileOutPath))

                return 1

            except:
                print("error happen whilst creating/writing combinations of password length {0} to '{1}'".format(
                    psswdLength, fileOutPath))
                return 0

    def create_perms_files(subDirPath, psswdLength, combinationsList):

        contents = os.listdir(subDirPath)

        maxSetPsswdLen = 1

        if (len(contents) == 0):
            maxSetPsswdLen = 1
        else:
            try:
                for f in contents:
                    if (os.path.isdir(os.path.join(subDirPath, f)) and permutation.dirNameRule.match(f)):
                        # if(permutation.fileNameRule.match(f)):
                        # fpl = int((f.split("_"))[0])
                        fpl = int(f)
                        if (fpl > maxSetPsswdLen):
                            maxSetPsswdLen = fpl

                maxSetPsswdLen += 1  # to start from the next password length since the current one exists

            except:
                print(
                    "Error happen while finidng the existing permutations files, the files will be generated from scratch for each length combination")
                maxSetPsswdLen = 1

        for i in range(1, maxSetPsswdLen):  # exisiting psswds 1, 2, 3 ..
            print("\nFound permutations files for password length {}".format(i))
            r = re.compile(r'\b{0}+_\d+\b'.format(i))  # file follow pswd
            psubDirPath = os.path.join(subDirPath, str(
                i))  # if(os.path.isdir(os.path.join(subDirPath, f)) and permutation.dirNameRule.match(f))
            innerContents = os.listdir(psubDirPath)

            numOfInnerFiles = 0
            for innerFile in innerContents:  # files within the inner directory

                if (r.match(innerFile)):
                    numOfInnerFiles += 1

            if (numOfInnerFiles > 0):
                print("\t{} combination files found".format(numOfInnerFiles))
            else:
                print("\t\t====>       SOMETHING LOOKS WRONG       <====\n"
                      "\t\t====> There were no files found inside  <====\n"
                      "\t\t====> the directory, combination will   <====\n"
                      "\t\t=> be calculated for this password length <==\n".format(numOfInnerFiles))

                maxSetPsswdLen = i
                break

        for i in range(maxSetPsswdLen, psswdLength + 1):
            print("\n    \t******* Finding combinations for {} length password ******* ".format(i))
            # psubDirPath = os.path.join(subDirPath, str(i))
            if not permutation.generate_n_perm(i, subDirPath, combinationsList):
                print("Problem happen in writing combinations for {} length password".format(i))
                exit(0)
            print("\n    \t*********************************************************** ".format(i))

        print("\n\n\t\t=========== FINISHED SUCCESSFULLY ================\n\n")

    def generate_permutaions(permutationsDirectoryPath,
                             psswdLength,
                             withDigits=True,
                             withLowerLetters=False,
                             withUpperLetters=False,
                             withSpecialCharacters=False):

        try:
            if (os.path.exists(permutationsDirectoryPath)):
                print("The directory '{0}' will be used to write/read permutations".format(permutationsDirectoryPath))
            else:
                print("The directory {0} is not valid, type 'yes' and press enter to do or 'no' to exit".format(
                    permutationsDirectoryPath))

                c = input()
                while (c != 'no' and c != 'yes'):
                    c = input("'yes' or 'no'\n")

                if c == 'no':
                    exit(0)

                os.makedirs(permutationsDirectoryPath)

            dirList = []
            combinationsList = []

            if withDigits:
                dirList.append('digits')
                combinationsList.extend(permutation.digits_c)

            if withLowerLetters:
                dirList.append('lower')
                combinationsList.extend(permutation.lowerLetters_c)

            if withUpperLetters:
                dirList.append('upper')
                combinationsList.extend(permutation.upperLetters_c)

            if withSpecialCharacters:
                dirList.append('special')
                combinationsList.extend(permutation.specialCharacters_c)

            subDirName = '_'.join(dirList)
            print("Generating permutations encryption with mode : {0}\n".format(subDirName.replace('_', ' , ')))

            subDirPath = os.path.join(permutationsDirectoryPath, subDirName)
            print("Saving/Reading permutations in the directory : '{0}'\n".format(subDirPath))

            if not os.path.exists(subDirPath):
                os.makedirs(subDirPath)
                print("'{0}' does not exist, created successfully\n".format(subDirPath))

            permutation.create_perms_files(subDirPath, psswdLength, combinationsList)

            return subDirPath


        except FileNotFoundError:
            print(FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    permutationsDirectoryPath))


fileIn = ""

def decrypt_single_password(psswd, fileOutName):
    try:
        fileIn.load_key(password=psswd)
        fileIn.decrypt(open(fileOutName, "wb"))
        return psswd
    except:
        return False

def decrypt_msoffice_file_multicore(msOfficeFilePath,
                                    permutationsDirectoryPath,
                                    psswdLength,
                                    withDigits=True,
                                    withLowerLetters=False,
                                    withUpperLetters=False,
                                    withSpecialCharacters=False,
                                    numberOfCores=None):


    if (not os.path.exists(msOfficeFilePath)):
        print("File {} does not exist".format(msOfficeFilePath))
        exit(0)

    permutaionsPath = permutation.generate_permutaions(permutationsDirectoryPath=permutationsDirectoryPath,
                                                       psswdLength=psswdLength,
                                                       withDigits=withDigits,
                                                       withLowerLetters=withLowerLetters,
                                                       withUpperLetters=withUpperLetters,
                                                       withSpecialCharacters=withSpecialCharacters)

    global fileIn
    fileIn = msoffcrypto.OfficeFile(open(msOfficeFilePath, "rb"))
    extension = os.path.splitext(msOfficeFilePath)[1]

    # read each file containig password in seperate thread to speed up ....

    if not numberOfCores:
        numberOfCores = os.cpu_count()
    else:
        if numberOfCores > os.cpu_count():
            print("Number of available Cores in this device" \
                  "is {0}, cant set cores to {1}, it will be set to {2}".
                  format(os.cpu_count(), numberOfCores, os.cpu_count()))
            numberOfCores = os.cpu_count()

    with multiprocessing.Pool(numberOfCores) as pool:

        for i in range(1, psswdLength + 1):
            print("Checking {} length password".format(i))
            psswdSubDirectory = os.path.join(permutaionsPath, str(i))

            if (os.path.isdir(psswdSubDirectory)):
                allFiles = os.listdir(psswdSubDirectory)

                for psswdFile in allFiles:

                    if (permutation.fileNameRule.match(psswdFile)):

                        print("\tSearching in {}".format(psswdFile))
                        psswdFilePath = os.path.join(psswdSubDirectory, psswdFile)
                        psswdFileIn = open(psswdFilePath, 'r')

                        EOF = False
                        while not EOF:
                            lines = [psswdFileIn.readline().strip() for _ in range(numberOfCores)]
                            t = [pool.apply_async(func=decrypt_single_password,
                                                  args=(psswd, "test_decrypt_now" + extension,))
                                 for psswd in lines]
                            for uu in t:
                                res = uu.get()
                                if res:
                                    return res

                            EOF = not lines[-1]

                        psswdFileIn.close()
                print("")

    return False


def decrypt_msoffice_file(msOfficeFilePath,
                          permutationsDirectoryPath,
                          psswdLength,
                          withDigits=True,
                          withLowerLetters=False,
                          withUpperLetters=False,
                          withSpecialCharacters=False):


    if (not os.path.exists(msOfficeFilePath)):
        print("File {} does not exist".format(msOfficeFilePath))
        exit(0)

    permutaionsPath = permutation.generate_permutaions(permutationsDirectoryPath=permutationsDirectoryPath,
                                                       psswdLength=psswdLength,
                                                       withDigits=withDigits,
                                                       withLowerLetters=withLowerLetters,
                                                       withUpperLetters=withUpperLetters,
                                                       withSpecialCharacters=withSpecialCharacters)
    global fileIn
    fileIn = msoffcrypto.OfficeFile(open(msOfficeFilePath, "rb"))
    extension = os.path.splitext(msOfficeFilePath)[1]

    # read each file containig password in seperate thread to speed up ....

    for i in range(1, psswdLength + 1):
        print("Checking {} length password".format(i))
        psswdSubDirectory = os.path.join(permutaionsPath, str(i))

        if (os.path.isdir(psswdSubDirectory)):
            allFiles = os.listdir(psswdSubDirectory)

            for psswdFile in allFiles:

                if (permutation.fileNameRule.match(psswdFile)):

                    print("\tSearching in {}".format(psswdFile))
                    psswdFilePath = os.path.join(psswdSubDirectory, psswdFile)
                    psswdFileIn = open(psswdFilePath, 'r')

                    for psswd in psswdFileIn:

                        psswd = psswd.strip()

                        try:
                            # print(psswd)
                            fileIn.load_key(password=psswd)
                            fileIn.decrypt(open("test_decrypt_now" + extension, "wb"))
                            return psswd

                        except:
                            pass

                    psswdFileIn.close()
            print("")
    return False



def decrypt_file(msOfficeFilePath,
                 permutationsDirectoryPath,
                 psswdLength,
                 minPsswd=1,
                 withDigits=True,
                 withLowerLetters=False,
                 withUpperLetters=False,
                 withSpecialCharacters=False,
                 multiCore=False,
                 numberOfCores=None,
                 psswdRange=None):
    # -------------------------------------------------------------------------
    # ------- psswdRange: tuple(min, max) is experimental do not use yet ------
    # -------------------------------------------------------------------------
    # 1) assert file exists
    # 2) assert file extinsion is xlsx, docx, csv ..
    # 3) if multi core call multi core else no ...

    assert os.path.exists(
        msOfficeFilePath), "The file you provided '{0}' does not exist, please provide a valid file".format(
        msOfficeFilePath)

    start = time.time()
    if (multiCore):

        password = decrypt_msoffice_file_multicore(msOfficeFilePath=msOfficeFilePath,
                                                   permutationsDirectoryPath=permutationsDirectoryPath,
                                                   psswdLength=psswdLength,
                                                   withDigits=withDigits,
                                                   withLowerLetters=withLowerLetters,
                                                   withUpperLetters=withUpperLetters,
                                                   withSpecialCharacters=withSpecialCharacters,
                                                   numberOfCores=numberOfCores)
    else:

        password = decrypt_msoffice_file(msOfficeFilePath=msOfficeFilePath,
                                         permutationsDirectoryPath=permutationsDirectoryPath,
                                         psswdLength=psswdLength,
                                         withDigits=withDigits,
                                         withLowerLetters=withLowerLetters,
                                         withUpperLetters=withUpperLetters,
                                         withSpecialCharacters=withSpecialCharacters)
    end = time.time() - start

    if password:
        print("\n\nPassowrd found : {0}\nOverall time : {1} seconds".format(password, end))
    else:
        print("\n\nPassword was not found")

    return password


#=======================================================================
pwd = decrypt_file(msOfficeFilePath="enccrypted.xlsx",
                   permutationsDirectoryPath="permutations/",
                   psswdLength=5,
                   multiCore = True,
                   numberOfCores = 6)
#=======================================================================
