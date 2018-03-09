#!/usr/bin/env python

import numpy
import sys
import os.path


def parse(fname):
    f = open(fname)
    line = f.readline()
    while len(line) != 0:
            
        line = f.readline()

        if "Ground-State Mulliken Net Atomic Charges" in line:
            f.readline()
            f.readline()
            f.readline()
            line = f.readline()
            pop = []
            while "----------------------------------------" not in line:
                pop.append(float(line.split()[2]))
                line = f.readline()
            pop = numpy.array(pop)
    return pop

def invPartRat(fname1, fname2):
    pop1 =  parse(fname1)
    pop2 =  parse(fname2)
    pop = pop1-pop2

    monomerQ = numpy.zeros(6)
    
    for i in range(6):
        monomerQ[i] = numpy.sum(pop[(i*99):(i+1)*99])
    

    #compute the inverse participation ratio
    squarepop = numpy.square(monomerQ)
    invPartRat = 1/sum(squarepop)
    print invPartRat
    return invPartRat

results = open("/work/akohn/projects/ptb7/qm/gas_IPR.txt", "w")

results.write("ID\t\t\tElectron IPR\tHole IPR\n")

for i in os.listdir('/work/akohn/projects/ptb7/qm/gas/ptb7/neutral'):
    print i
    groundTarget = "/work/akohn/projects/ptb7/qm/gas/ptb7/neutral/" + i + "/" + i + ".out"
    catTarget = groundTarget.replace("neutral", "cation")
    anTarget = groundTarget.replace("neutral", "anion")
    if not os.path.isfile(groundTarget) or not os.path.isfile(catTarget) or not os.path.isfile(anTarget):
        continue
   
    if "Mulliken" not in open(groundTarget).read() or "Mulliken" not in open(catTarget).read() or "Mulliken" not in open(anTarget).read():
        continue
    print "My target is" + groundTarget
    eleIPR = invPartRat(groundTarget, anTarget)
    holeIPR = invPartRat(catTarget, groundTarget)

    results.write(i[-7:] + "\t\t" + str(round(eleIPR,3)) + "\t\t\t" + str(round(holeIPR,3)) + "\n")


results.close()





