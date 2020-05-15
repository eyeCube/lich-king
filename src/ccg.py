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
        if "_collision.egg" in file:
            filedir = os.path.join(curdir,file)
            with open(filedir, "r") as f:
                newstring=""
                for line in f.readlines():
                    if tagNextLine:
                        if "collide" in line.lower():
                            continue
                        newstring += '''    <Collide> { Polyset keep descend }
'''
                        tagNextLine = False
                    if "group" in line.lower():
                        tagNextLine = True
                    newstring+=line
            with open(filedir, "w+") as f:
                f.write(newstring)
            # end with
    # end for
#


                    
                
    
