"""jacobson.py: CS591WS assignment 04
Author: Matthew Jacobson 
"""
#Imports
from sys import argv
import csv 

def calculations(storage):
    # Number of edges
    numEdges = len(storage)
    #Number of positive edges and negative edges
    posedges = 0
    negedges = 0 
    for x in storage:
        if int(x[2]) == -1:
            negedges+=1
        else:
            posedges+=1
    print("pos edges= "+str(posedges)+" Neg edges= "+str(negedges))
    if posedges+negedges==numEdges: #ensure that everything was read properly
        print("Perfect")
    #Probability of positve and negative edges
    #posprob = # of positive edges / Total edges
    probpos = float(posedges)/float(numEdges)
    probneg = 1 - probpos # prob that an edge will be negative 1 - p 
    print(str(format(probpos,".3%"))+" "+str(format(probneg,".3%")))
    # number of triangles of each type, and total number of triangles
    for edge in storage: 
        # print(str(edge))
        #get information from the edge
        a = edge[0]
        b = edge[1]
        trust = edge[2]
        # print(str(a) + " " + str(b) +" "+ str(trust))
        #now begins identifying triads, in a triad edges must connect with a common number
        # with the first edge, search other edges ()
        #my inital approach will be to connect the b in the first triad with the A in the second triad and then make sure they connect in the end when finding the 3rd edge
        #I know this is O(n^3) so I will have to find a way for it to run faster
        triads = []
        for edgetwo in storage:
            
        


def main(): 
    print("Program to proccess social network data and identifying triads")
    print("Usage: graphs.py [filename](optional)")
    # check for optional filename before prompting the user
    storage = []
    if len(argv) > 1: 
        file = open(argv[1])
    else:
        filename = input("Enter filename here: ")
        file = open(filename)
    #where I learned about csvreader https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/
    csvreader = csv.reader(file) 
    for row in csvreader: 
        storage.append(row)
    calculations(storage)
    

if __name__ == "__main__":
    main()   
    
