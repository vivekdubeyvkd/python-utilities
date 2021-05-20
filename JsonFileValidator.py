'''
    /**
      ************************************************************************************************************************
      * Script Name : JsonFileValidator.py
      * Purpose : This script can validate JSON file for it's correctness
      * Author : Vivek Dubey
      * Copyright : Intuit Inc @ 2021
      ************************************************************************************************************************
    **/
'''

import sys
import getopt
import json
import os.path
from os import path

def parseArgs(argv):
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
   except getopt.GetoptError:
      print('Usage: JsonFileValidator.py -i <input Json file Path>')
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print('Usage: JsonFileValidator.py -i <input Json file Path>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         return arg


def validateJson(inputJsonfilePath):
    if path.exists(inputJsonfilePath):
        jsonContent = open(inputJsonfilePath,)
        try:
            json.load(jsonContent)
            print(inputJsonfilePath, " is a valid Json file")
        except ValueError as err:
            print(inputJsonfilePath, " is an invalid Json file, kindly correct and rerun validation ...... ")
            sys.exit(4)
    else:
        print("Input Json file ", inputJsonfilePath, " does not exist")
        sys.exit(3)

def main(argv):
    if argv:
       inputJsonfilePath = parseArgs(argv)
       validateJson(inputJsonfilePath)
    else:
        print('Usage: JsonFileValidator.py -i <input Json file Path>')
        sys.exit(5)

if __name__ == "__main__":
   main(sys.argv[1:])
