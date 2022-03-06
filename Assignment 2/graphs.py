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
    triads = []
    first = []
    second = []
    third =[]
    ttt = 0
    ttd = 0 
    tdd = 0 
    ddd = 0
    total = ttt + ttd + tdd + ddd
    for edge in storage: 
        # print(str(edge))
        #get information from the edge
        first = edge
        a = first[0]
        b = first[1]
        # trust = first[2]
        # print(str(a) + " " + str(b) +" "+ str(trust))
        #now begins identifying triads, in a triad edges must connect with a common number
        # with the first edge, search other edges ()
        #my inital approach will be to connect the b in the first triad with the A in the second triad and then make sure they connect in the end when finding the 3rd edge
        #I know this is O(n^3) so I will have to find a way for it to run faster
        #now we have the first edge, now find the next edge that connects
        for edgetwo in storage:
            #check all of the other edges to see if we can find the next one in the triad
            second = edgetwo
            c = second[0]
            d = second[1]
            #TODO: Figure out how to prevent checking itself (nevermind this is a nonissue because nodes have to be different numbers)
            #if the current node is = to the 
            if b == c:
                for edgethree in storage: 
                    
                    
                
                
                
                            
                
    
                       
                
                
                
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
    start_time = time.time()
    calculations(storage)
    print("The calculations took : %s seconds" % (time.time() - start_time))
    
    

if __name__ == "__main__":
    main()   
    
