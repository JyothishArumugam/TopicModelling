import os

term="e commerce"

os.mkdir("models"+"/"+term)

with open("models/"+term+'/'+term+'.dat') as wrt:
    wrt.write("done")