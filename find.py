#search a directory's files looking for a particular string

import os
import sys

#arg1 is the directory to search.
#arg2 is the string to search for.

#curdir=os.path.dirname(__file__)
searchdir=sys.argv[1]
find=sys.argv[2]
for filename in os.listdir(searchdir):
    try:
        with open( os.path.join(searchdir,filename)) as file:
            lineNum=1
            for line in file.readlines():
                if find in line:
                    print(filename,"| ln",lineNum)
                lineNum+=1
    except Exception as err:
        pass

input()
