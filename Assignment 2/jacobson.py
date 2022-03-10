"""jacobson.py: CS591WS assignment 04
Author: Matthew Jacobson '
I pledge my honor that I have abided by the stevens honor system - Matthew Jaocbson
"""
#Imports
#this import was auto generated so not sure why I need it
from readline import set_completion_display_matches_hook
#to access command line inputs
from sys import argv
#to process csv's
import csv 
# use this package to time my program ( important to stay under 15 mins per program spec)
import time
import sys
# import networx can be installed via command line with the command "pip install networkx"
import networkx as nx

#method to preform all calculations
def calculations(storage):
    # Number of edges
    numEdges = len(storage)
    #Number of positive edges and negative edges
    posedges = 0
    negedges = 0 
    #Iterate through storage and find edge types
    for x in storage:
        if int(x[2]) == -1:
            negedges+=1
        else:
            posedges+=1
    # print("pos edges= "+str(posedges)+" Neg edges= "+str(negedges))
    # if posedges+negedges==numEdges: #ensure that everything was read properly
    #     print("Perfect")
    #Probability of positve and negative edges
    #posprob = # of positive edges / Total edges
    probpos = float(posedges)/float(numEdges)
    probneg = 1 - probpos # prob that an edge will be negative 1 - p    
    # print(str(format(probpos,".3%"))+" "+str(format(probneg,".3%")))
    # number of triangles of each type, and total number of triangles
    # triads,first,second,third = [],[],[],[]
    ttt,ttd,tdd,ddd = 0,0,0,0
    #make an easy total variable to store different totals throughout the program (its use will change when printing outputs)
    total = ttt + ttd + tdd + ddd
    #I left my old implementations/algorithims so you can see my thought proccess and for my own use when I go back and rewrite this code on my own with no time limit
    #now go through the list and find triads (yes I know this is O(N^3))
    #this can be further optimized by sorting the list and using buckets to find triads faster
    # current = 1  
    # storagesize = len(storage)
    #this solution doesnt work
    # for edgeone in storage: 
    #     progress(current,storagesize,'')
    #     for edgetwo in storage:
    #         # print(edgetwo)
    #         #check all of the other edges to see if we can find the next one in the triad
    #         if int(edgeone[1]) == int(edgetwo[0]): 
    #             # print(str(edgeone)+" equals "+str(edgetwo))
    #             for edgethree in storage: 
    #                 if int(edgetwo[1]) == int(edgethree[0]) and int(edgethree[1]) == int(edgeone[0]):
    #                     print(str(edgeone)+" equals "+str(edgetwo)+" equals "+str(edgethree))
    #                     print(edgethree[1] +" "+edgeone[0])
    #     current+=1
    
    #this solution is too slow, works perfectly for small dataset (0.18 seconds for epinions0.csv, but 20+ minutes before I stopped it during epinions1.csv) 
    # for edgeone in storage:
    #     for edgetwo in storage: 
    #         for edgethree in storage: #
    #             #lets find some triads (my other solution was all wrong)
    #             if int(edgeone[0]) == int(edgetwo[0]) and int(edgeone[1]) == int(edgethree[0]):
    #                 if edgetwo[1] == edgethree[1]:
    #                     print(str(edgeone) + " " + str(edgetwo) +" "+ str(edgethree))
    #                     triads.append([edgeone,edgetwo,edgethree])
    
    """
    I found a library called networkx because of its ability to work with weighted graphs (trust factor)
    https://networkx.org/documentation/stable/_downloads/networkx_reference.pdf
    documentation that I base my code off can be found here ^^^^
    https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python
    more instructions on how to use networkx^^
    I also found that clique.py in networkx/algorithims/ was very helpful
    I also used the documentation to discover the use of nx as an object (nx.~~~~) this initally was not clear to me
    """
    #make the network 
    G = nx.Graph()
    # add in the edges
    for edge in storage: # this operation is preformed in ~0.00022 seconds which is signifigantly faster than my previous implementation without the library
        G.add_edge(edge[0],edge[1], weight = edge[2])
    #now lets preform analysis 
    # I cast this as a list just so its easier to work with, its the same thing 
    listedges = list(nx.to_edgelist(G))
    # print(nx.info(G))
    #this returns all the cliques and I filter out all the ones that arent a length of three (ones that arent a triad)
    #sanity check the number of cliques on the previous attempt
    netcount = 0 
    #iterate through all cliques
    #two storage variables to store the triads and edges(temp)
    triad = []
    edges = []
    #iterate through all cliques
    for clique in list(nx.enumerate_all_cliques(G)):
        #if the clique is of size 3 keep it if not ignore it
        #create the trust factor var that we want to reset for each clique 
        #clique = ['x','y','z']
        # ex [5, 20, 50]
        trustfactor = 0 
        #check for size three (which are triads)
        if len(clique) == 3:
            #increment counter and then print it for debugging purposes
            netcount+=1
            #now we have to see what kind of clique by checking the trust factor of all the edge
            #first attempt (checking nodes against the list of edges to find the weight)
            #first to second, first to third, and then second to third
            # edge = ('x', 'y', {'weight': '1'})
            #ex 5 -> 20, 5 -> 50, 20->50
            for edge in listedges:   
                #this is slow but I didn't have time to make it faster, but much faster than O(n^3) this is O(n*#ofcliques)     
                #check and if its the right edge then add it to the triad
                #edge = ('x', 'y', {'weight': '1'})
                #clique = ['x','y','z']
                #first in edge == first in clique and second in edge equals second in clique
                if int(edge[0]) == int(clique[0]) and int(edge[1]) == int(clique[1]):
                    #then this is the first edge 
                    edges.append(edge)
                #first to third
                if int(edge[0]) == int(clique[0]) and int(edge[1]) == int(clique[2]):
                    #then this is the second edge
                    edges.append(edge)
                #second to third
                if int(edge[0]) == int(clique[1]) and int(edge[1]) == int(clique[2]):
                    #then this is the third edge
                    edges.append(edge)
                    triad.append(edges)
                    edges = []
    #Now that the triads have been found from the graph now take them and analyze them 
    # print(len(triad)) # check number of triads are correct         
    # for t in triad: 
    #     print(t)
    for tri in triad:
        #for each triad identify what kind of triad, to do this I realized I can use weight as a trust factor
        #ttt has a trust factor of 3, ttd has a trust factor of 1, tdd has a trust factor of -1, and ddd has a trust factor of
        # this will provent a dtt being different than a tdt or ttd which eliminates the need for extra checks
        #calculate trust
        trust = int(tri[0][2]['weight'])+int(tri[1][2]['weight'])+int(tri[2][2]['weight'])
        #check trust and add to corresponding triad counter
        if trust == 3:            
            ttt+=1
        elif trust == 1: 
            ttd+=1
        elif trust == -1:
            tdd+=1
        elif trust == -3:
            ddd+=1 
        else:
            #sanity check while testing
            print("How did you get something different???")
    # print("Total: "+str(ttt+ttd+tdd+ddd)+" Each:  "+str(ttt)+" "+str(ttd)+" "+str(tdd)+" "+str(ddd))
    # print("Net total = "+str(netcount))
    #now do the theoretical (expected) amount based off of the # of triads found (total)
    # and then actual distribution 
    #print assignment output
    #change total to be the string representation of the total number of triads 
    total =str(netcount)
    print("Triangles: " + str(total))
    print("TTT: "+str(ttt)+"\t\t"+"Edges used:       "+str(numEdges))
    print("TTD: "+str(ttd)+"\t\t"+"Trust Edges:      "+str(posedges)+"\t\t"+" probability trust %:     "+str(format(probpos,".3%")))
    print("TDD: "+str(tdd)+"\t\t"+"Distrust Edges:   "+str(negedges)+"\t"+"         probability distrust %:  "+str(format(probneg,".3%")))
    print("DDD: "+str(ddd)+"\t\t"+"Total:            "+str(posedges+negedges)+"\t\t"+"                          "+str(format((probpos+probneg),".3%")))
    print()
    print("Expected Distribution\t\tActualDistribution")
    print("      percent number\t\t\t percent number")
    #preform theoretical calculations
    #preform the chance that it will be each kind of triad
    #use *3 on TTD and TDD because they can have different orders (ie. DTD is the same as TDD)
    theoreticalttt = probpos*probpos*probpos
    theoreticalttd = 3*probpos*probpos*probneg
    theoreticaltdd = 3*probpos*probneg*probneg
    theoreticalddd = probneg*probneg*probneg
    #total should be 100 
    theoreticaltotal = theoreticalttt+theoreticalttd+theoreticaltdd+theoreticalddd
    #now the theoretical number of edges based off of the percent chance that it will occur
    theorttt = theoreticalttt*float(total)
    theorttd = theoreticalttd*float(total)
    theortdd = theoreticaltdd*float(total)
    theorddd = theoreticalddd*float(total)
    #this total number of edges
    totaltheor = theorttt+theorttd+theortdd+theorddd
    # preform actual calculations
    actualtttdis = float(ttt)/float(total)
    actualttddis = float(ttd)/float(total)
    actualtdddis = float(tdd)/float(total)
    actualddddis = float(ddd)/float(total)
    totalactualdis = actualtttdis+actualttddis+actualtdddis+actualddddis
    # now print it out 
    print("TTT:\t"+str(format(theoreticalttt,".2%"))+"     "+str('{:5.2f}'.format(theorttt))+"\t\tTTT: "+str(format(actualtttdis,".2%"))+"  "+str(ttt))
    print("TTD:\t"+str(format(theoreticalttd,".2%"))+"     "+str('{:5.2f}'.format(theorttd))+"\t\tTTD: "+str(format(actualttddis,".2%"))+"  "+str(ttd))
    print("TDD:\t"+str(format(theoreticaltdd,".2%"))+"     "+str('{:5.2f}'.format(theortdd))+"\t\tTDD: "+str(format(actualtdddis,".2%"))+"  "+str(tdd))
    print("DDD:\t"+str(format(theoreticalddd,".2%"))+"     "+str('{:5.2f}'.format(theorddd))+"\t\t       DDD: "+str(format(actualddddis,".2%"))+"  "+str(ddd))
    #now print totals line to ensure that all the numbers are right
    print("-"*20)
    print("TOTALS: "+str(format(theoreticaltotal,".2%"))+" "+str(totaltheor)+"\t\t"+str(format(totalactualdis,".2%"))+" "+str(ttt+ttd+tdd+ddd))
    print()
    print("*"*5+"END"+"*"*5)
    
    
    """
    documentation I used to write the sorting function
    https://www.w3schools.com/python/ref_list_sort.asp
    
    """
def sortingfunction(e):
    #translate string into int so the built in sort can sort numbers instead of strings
    """  if sorted by strings single digit numbers would appear in between large numbers
    76
    79
    8
    88
    84
    85
    """
    return int(e[0])

def main(): 
    print("Program to proccess social network data and identifying triads")
    print("Usage: graphs.py [filename](optional)")
    # check for optional filename before prompting the user
    storage = []
    filename = ""
    if len(argv) > 1: 
        file = open(argv[1])
        filename = argv[1]
    else:
        filename = input("Enter filename here: ")
        file = open(filename)
    #where I learned about csvreader https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/
    csvreader = csv.reader(file) 
    for row in csvreader: 
        storage.append(row)
    #to optimise the speed of finding triads I sorted the list of edges via the built in sort function
    storage.sort(key=sortingfunction)
    # for x in storage:
    #     print(x)
    #start the timer
    print("*"*5+"START"+"*"*5)
    print("Results for file: "+ filename)
    print()
    #now start a timer, I learned about the time class from https://www.programiz.com/python-programming/time
    #I got time.time() - start from https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
    start = time.time()
    #preform calculations
    calculations(storage)
    #then print the speed of my program
    print("The calculations took : %s seconds" % (time.time() - start))
    
    #main method
if __name__ == "__main__":
    main()   
    
    