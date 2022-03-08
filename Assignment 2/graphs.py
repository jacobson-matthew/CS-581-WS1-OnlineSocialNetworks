"""jacobson.py: CS591WS assignment 04
Author: Matthew Jacobson 
"""
#Imports
from readline import set_completion_display_matches_hook
from sys import argv
import csv 
# use this package to time my program ( important to stay under 15 mins per program spec)
import time
from tracemalloc import start

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
    triads,first,second,third = [],[],[],[]
    ttt,ttd,tdd,ddd = 0,0,0,0
    total = ttt + ttd + tdd + ddd
    #now go through the list and find triads (yes I know this is O(N^3))
    #this can be further optimized by sorting the list and using buckets to find triads faster 
    for edgeone in storage: 
        for edgetwo in storage:
            print(edgetwo)
            #check all of the other edges to see if we can find the next one in the triad
            if edgeone[1] == edgetwo[0]: 
                for edgethree in storage:
                    print(edgethree)
                    #now find the edge that connects to the end of edge two and to the first node in edge one that we started with. 
                    if edgetwo[1] == edgethree[0] & edgethree[1] == edgeone[0]:
                        #now add the triad to our triad storage for further analysis 
                        triads.append([edgeone,edgetwo,edgethree])
    #analysis on the triads
    print(triads)
    for triad in triads:
        #for each triad identify what kind of triad
        #ttt has a trust factor of 3, ttd has a trust factor of 1, tdd has a trust factor of -1, and ddd has a trust factor of
        trust = triad[0][2]+triad[1][2]+triad[2][2]
        if trust == 3:            
            ttt+=1
        elif trust == 1: 
            ttd+=1
        elif trust == -1:
            tdd+=1
        elif trust == -3:
            ddd+=3 
        else: 
            print("How did you get something different???")
    #now do the theortical amount based off of the # of triads found (total)
    
    #now print the real numbers that were found. 
    
                
                
                
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
    start = time.time()
    calculations(storage)
    print("The calculations took : %s seconds" % (time.time() - start))
    
    

if __name__ == "__main__":
    main()   
    

        # print(str(edge))
        #get information from the edge
        # first = edge
        # a = first[0]
        # b = first[1]
        # trust = first[2]
        # print(str(a) + " " + str(b) +" "+ str(trust))
        #now begins identifying triads, in a triad edges must connect with a common number
        # with the first edge, search other edges ()
        #my inital approach will be to connect the b in the first triad with the A in the second triad and then make sure they connect in the end when finding the 3rd edge
        #I know this is O(n^3) so I will have to find a way for it to run faster
        #now we have the first edge, now find the next edge that connects