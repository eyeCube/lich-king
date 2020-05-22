'''
    ccg -- convert collision geometry
    convert geometry into collision geometry by adding tag to .egg files
'''

import os
import sys

curdir = os.getcwd()
if len(sys.argv)>=2:
    directory = sys.argv[1]
    curdir = os.path.join(curdir,directory)
files = [f for f in os.listdir(curdir) if os.path.isfile(os.path.join(curdir,f))]

if __name__=="__main__":
    for file in files:
        tagNextLine = False
        if (".egg"==file[-4:] and "_collision" in file):
            filedir = os.path.join(curdir,file)
            needToWrite=False
            with open(filedir, "r") as f:
                newstring=""
                for line in f.readlines():
                    if tagNextLine:
                        tagNextLine = False
                        if "collide" in line.lower():
                            continue
                        newstring += '''    <Collide> { Polyset keep descend }
'''
                        needToWrite=True
                    if "group" in line.lower():
                        tagNextLine = True
                    newstring+=line
            if needToWrite:
                with open(filedir, "w+") as f:
                    f.write(newstring)
                print("Wrote to file '{}'.".format(filedir))
            # end with
    # end for
#


                    
                
    
