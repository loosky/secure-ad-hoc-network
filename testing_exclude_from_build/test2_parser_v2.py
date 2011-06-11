#!/usr/bin/env python

import sys
import fileinput
import string

global startTimer
startTimer = 0
global endTimer
endTimer = 0
global deltaTimeList
deltaTimeList = []


if __name__ == "__main__":

    file = fileinput.input()
    
    for line in file:
        
        if 'Received BATMAN packet via NB: 10.0.0.77, IF: eth1 10.0.0.55 (from OG: 10.0.0.77, via old OG: 10.0.0.77,' in line:
            file.readline()
            line = file.readline()
            if 'Creating new last-hop neighbour of originator' in line:
                line = line.split(']')
                line = line[0].split('[')
                startTimer = int(line[1].strip())/10
            else:
                line = file.readline()
                if 'Creating new last-hop neighbour of originator' in line:
                    line = line.split(']')
                    line = line[0].split('[')
                    startTimer = int(line[1].strip())/10
                
        if startTimer > 0:
            if 'Adding route to 10.0.0.3/32 via 10.0.0.77 (table 66 - eth1)' in line:
                line = line.split(']')
                line = line[0].split('[')
                endTimer = int(line[1].strip())/10
                deltaTimeList.append(int(endTimer) - int(startTimer))
                print int(endTimer), " - ", int(startTimer), " = ", (int(endTimer) - int(startTimer))
                startTimer = 0
                endTimer = 0
    
    for index, time in enumerate(deltaTimeList):
        print index+1, time

