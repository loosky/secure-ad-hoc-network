#!/usr/bin/env python

import sys
import fileinput
import string

global id
global addr
global selfAddr
global lastDelete
global firstAdd
global prevTQ
global convergenceTime

id = []
addr = []
selfAddr = ''
lastDelete = [0, 0, 0]
firstAdd = [0, 0, 0]
prevTQ = [0, 0, 0]
convergenceTime = [[], [], []]

def setSelfAddr(line):
    lineArray = line.split()
    global selfAddr
    selfAddr = lineArray[5].strip()

def addNodeFromAl(file):
    idLine = file.readline()
    idLine = idLine.strip()
    idArray = idLine.rsplit(" ", 2)
    global id
    id.append(idArray[2])
    
    addrLine = file.readline()
    addrLine = addrLine.strip()
    addrArray = addrLine.rsplit(" ", 2)
    global addr
    addr.append(addrArray[2])
    
def addNode(line):
    if len(addr) < 3:
        lineArray = line.split(': ')
        addr.append(lineArray[1].strip())
        
def delNeigh(line):
    if 'via 0.0.0.0' in line:
        for index, node in enumerate(addr):
            if node in line:
                line = line.strip('[').strip()
                lineArray = line.split(']')
                time = lineArray[0].strip()
                lastDelete[index] = time
                firstAdd[index] = 0
                prevTQ[index] = 0

def addNeigh(line, file):
    line = line.strip('[').strip()
    lineArray = line.split('from OG: ')
    neighArray = lineArray[0].split()
    neigh = neighArray[6].strip()
    toProcess = False
#    file.readline()
#    bidirectionalLine = file.readline()
    for index, node in enumerate(addr):
        if node in neigh:
            file.readline()
            bidirectionalLine = file.readline()
            if firstAdd[index] == 0:
                if selfAddr in lineArray[1]:
                    toProcess = True
                elif neigh in lineArray[1]:
                    toProcess = True
            elif 'own_bcast =  0, real recv =  0' in bidirectionalLine:
                if selfAddr in lineArray[1]:
                    toProcess = True
                elif neigh in lineArray[1]:
                    toProcess = True
            elif neigh in lineArray[1]:
                file.readline()
                file.readline()
                file.readline()
                file.readline()
                forwardingLine = file.readline()
                if 'tq_avg: ' in forwardingLine:
                    forwardingArray = forwardingLine.split('tq_avg: ')
                    forwardingArray2 = forwardingArray[1].split(',')
                    forwardTQ = forwardingArray2[0].strip()
                    if(forwardTQ < prevTQ[index]):
                        toProcess = True
                    prevTQ[index] = forwardTQ
            if toProcess == True:
                lineArray = line.split(']')
                time = lineArray[0].strip()
                firstAdd[index] = time
                    
def addRoute(line):
    lineArray = line.split('via')
    if '0.0.0.0' in lineArray[1]:
        for index, node in enumerate(addr):
            if node in lineArray[0]:
                line = line.strip('[').strip()
                lineArray2 = line.split(']')
                time = lineArray2[0].strip()
                if firstAdd[index] > 0:
                    convergenceTime[index].append(int(time) - int(firstAdd[index]))
                    firstAdd[index] = 0
                    lastDelete[index] = 0


if __name__ == "__main__":

    file = fileinput.input()
    
    secureVersion = False
    file.readline()
    line = file.readline()
    if 'Secure Ad Hoc Network extension enabled' in line:
        secureVersion = True
        file.readline()
        line = file.readline()
        setSelfAddr(line)
    else:
        line = file.readline()
        setSelfAddr(line)
    
    
    for line in file:

        if secureVersion == True:      
            if 'Added new node to AL:' in line:
                addNodeFromAl(file)
        else:
            if 'Creating new originator:' in line:
                addNode(line)    
        
        if len(addr) == 3:
            break
        
    for line in file:
        
        if 'Deleting route to ' in line:
            delNeigh(line)
        
        if 'Received BATMAN packet via NB: ' in line:
            addNeigh(line, file)
            
        if 'Adding route to ' in line:
            addRoute(line)

    print "\n======================================================================================"
    print "Node: " + addr[0]
    print "Times to place node as direct neighbor:"
    print convergenceTime[0]
    print "\n"
    print "Node: " + addr[1]
    print "Times to place node as direct neighbor:"
    print convergenceTime[1]
    print "\n"
    print "Node: " + addr[2]
    print "Seconds used to declare node as direct neighbor:"
    print convergenceTime[2]
    print "======================================================================================\n"


