import sys
import fileinput
import string

global id
global addr

id = []
addr = []

def addNode(file):
    idLine = file.readline()
    idLine = idLine.strip()
    idArray = idLine.rsplit(" ", 2)
    id.append(idArray[2])
    
    addrLine = file.readline()
    addrLine = addrLine.strip()
    addrArray = addrLine.rsplit(" ", 2)
    addr.append(addrArray[2])



if __name__ == "__main__":
    
    file = fileinput.input()
    
    for line in file:
        if 'Added new node to AL:' in line:
            addNode(file)
            
        if 'Adding route to 10.0.0.77' in line:
            line = line.strip()
            print(line)
        
    print(id)
    print(addr)