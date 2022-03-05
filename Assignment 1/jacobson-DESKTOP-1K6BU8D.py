#Author Matthew Jacobson 
#Class: Online Social Networks
#I pledge my honor that I have abided by the stevens honor system - Matthew Jacobson

#input : Search Term and Maximum number of results
#output : 
# .csv = .csv file should contain raw datafeilds that were retrived, one row for each record
# First row should be header file that contains field names ( no calculated fields ) if something is missing 
# use 0 
#output in a user friendly report should be printed to console

#running instructions: python3 jacobson.py, enter search term and max results, make sure terminal is full screen so the table fits and will print correctly

#imports
#import to output as a CSV
import csv
#import pretty table for easy formatting for printing results in a table form.
#this can be easily installed via the "pip install prettytable"
from prettytable import PrettyTable
#api stuff for access to youtube data
from googleapiclient.discovery import build
#Item gettter for sorting
from operator import itemgetter
#code from given program youtube.py
# use build function to create a service object
# put your API key into the API_KEY field below, in quotes as well as name and version
API_KEY = "AIzaSyC6ALbKFSUgMvBX8GH1k7me9k9fI6Iq3b8"
API_NAME = "youtube"
API_VERSION = "v3"

#I was going to add a trimming system to return the duration in a pretty format but I just didnt have enough time
#I might go back later and add it
# def quicktrim(input):
    #need to test the type of string there are 3 formats based on the youtube API: 
    # < one hour ==  PT#M#S
    # > one hour ==  PT#H#M#S
    # > one day = P#DT#H#M#S
    # go back wards 
    
#function to preform the search given inputs
def preformsearch(term,max):
    #each search method starts with the given code by the professor from the previous assignment
    #this includes the "build" line as well as some of the basic data queries, I added my own as needed in the 
    #same format as the given code as a boilerplate. 
    # My if statements are also in the same format using the "in" keyword to see if things were there or not 
    #these comments are true for all 3 analysis methods, but for the sake of repetition I will not write them over each time

    #Construct a Resource for interacting with an API
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
    #now search for the given term and max number of results for the parts we require
    #this can be vid id view likes comments duration title 
    search_data = youtube.search().list(q=term, part="id,snippet", maxResults=max).execute()
    #make data structure to hold information, I will choose a 2D array, each row will be for a given videos information 
    storage = []
    # print(search_data.get("items",[]))    
    #now comb through the search results
    # line below selects all the items 
    for search_instance in search_data.get("items", []):
        #trim search to youtube videos
        if search_instance["id"]["kind"] == "youtube#video":
            #get information
            videoId = search_instance["id"]["videoId"]  
            title = search_instance["snippet"]["title"]
            #to access the duration, based on the API documentation, you have to acces the "contentDetails" portion of the information
            contentdetails = youtube.videos().list(id=videoId, part = "contentDetails").execute()
            #now go through the items and select the duration inside the content details part of the dict
            for x in contentdetails.get("items",[]):
                #store duration in a variable
                duration = x['contentDetails']['duration']
            #this call to get the video statistics contains the last bits of information we need which are views, comments, and likes
            #comments are under video_instance["statistics"]["commentCount"]
            #execute a query for the statistics of a given youtube video (identified by its videoID)
            video_data = youtube.videos().list(id=videoId,part="statistics").execute()
            # print(" ")
            # print(video_data)
            #not iterate through the found videos 
            for video_instance in video_data.get("items",[]):
                #view counts are always there so no need for if statement (may be zero but still exists)
                viewCount = video_instance["statistics"]["viewCount"]
                #if there are no likes the number is zero
                if 'likeCount' not in video_instance["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_instance["statistics"]["likeCount"]
                #now do the same for comments, if there are no comments then the answer is 0 
                if 'commentCount' not in video_instance["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_instance["statistics"]["commentCount"]          
            # print("")    
            # print(videoId, title, viewCount, likeCount)
            # print(videoId,viewCount,likeCount,commentCount,duration,title)
            #we need Video ID views Likes comments Duration Title
            #and also add the thousand seperator in the count feilds via the .format built in python function
            #'{:,}'.format() from the python docs, but you have to cast the feilds as ints because it doesnt recogonize string input
            #now add to storage all the video data we've gathered properly formatted with thousands seperators as per the project spec
            storage.append([videoId,'{:,}'.format(int(viewCount)),'{:,}'.format(int(likeCount)),'{:,}'.format(int(commentCount)),duration,title])
    return storage

#call to the 2nd analysis for information, sort by "Like percentage"
#need "like percentage ( like count / view count ), view count,like count, and title 
def preform2ndsearch(term,max):
    #Construct a Resource for interacting with an API
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
    #now search for the given term and max number of results for the parts we require
    #this can be vid id view likes comments duration title 
    search_data = youtube.search().list(q=term, part="id,snippet", maxResults=max).execute()
    #make data structure to hold information, I will choose a 2D array, each row will be for a given video 
    storage = []
    # print(search_data.get("items",[]))   
    #now comb through the search results
    # line below selects all the items 
    for search_instance in search_data.get("items", []):
        #trim search to youtube videos
        if search_instance["id"]["kind"] == "youtube#video":
            #get information
            videoId = search_instance["id"]["videoId"]  
            title = search_instance["snippet"]["title"]
            #video information
            #this call to get the video statistics contains the last bits of information we need which are Comments and duration 
            #comments are under video_instance["statistics"]["commentCount"]
            video_data = youtube.videos().list(id=videoId,part="statistics").execute()
            # print(" ")
            # print(video_data)
            #not interate through the found videos 
            for video_instance in video_data.get("items",[]):
                #now make the check for views if it has any
                if 'viewCount' not in video_instance["statistics"]:
                    viewCount = 0
                else:
                    viewCount = video_instance["statistics"]["viewCount"]
                #if there are no likes the number is zero
                if 'likeCount' not in video_instance["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_instance["statistics"]["likeCount"]
            # print("")    
            # print(videoId, title, viewCount, likeCount)
            # print(videoId,viewCount,likeCount,commentCount,duration,title)
            #we need Video ID views Likes comments Duration Title
            #now calculate likePercentage: like percentage = (like count/view count)
            tobeformat = 0 
            #check for devide by zero 
            if int(viewCount) == 0:
                likePercentage = 0
            else:
                #otherwise preform the operation, now when preforming the division operation cast to get ints and format the result as a percentage with 3 decimal places to the right 
                likePercentage = "{:.3%}".format(int(likeCount)/int(viewCount))
            #then add information to storage with correct formatting
            storage.append([likePercentage,'{:,}'.format(int(viewCount)),'{:,}'.format(int(likeCount)),title])
    #now preform sorting and ranking by inserting 1 -> 5 
    #first sort values in storage by like percentage
    #I tried to use itemgetter() to do it but I think the percentage sign was throwing it off
    #I came up with this line ( and the similar lines for the other two analysis types) on my own but refrencing the python docs @ https://docs.python.org/3/howto/sorting.html
    #I discovered I can use lambdas to trim and reformat input to the sort key, also need reverse to print largest to smallest (default oppsite of that)
    storage = sorted(storage,key=lambda x: float(x[0][:-1]),reverse=True)
    #now add ranks to the beginning of the entries 
    pos = 0 
    #iterate through the storage
    while pos < len(storage):
        #add rank #
        storage[pos].insert(0,pos+1)
        pos+=1
    #return answer
    return storage

#call to the 3rd analysis for information, sort by "Like percentage"
#need "like percentage ( like count / view count ), view count,like count, and title 
def preform3rdsearch(term,max):
    #Construct a Resource for interacting with an API
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
    #now search for the given term and max number of results for the parts we require
    #this can be vid id view likes comments duration title 
    search_data = youtube.search().list(q=term, part="id,snippet", maxResults=max).execute()
    #make data structure to hold information, I will choose a 2D array, each row will be for a given video 
    storage = []
    # print(search_data.get("items",[]))   
    #now comb through the search results
    # line below selects all the items 
    for search_instance in search_data.get("items", []):
        #trim search to youtube videos
        if search_instance["id"]["kind"] == "youtube#video":
            #get information
            videoId = search_instance["id"]["videoId"]  
            title = search_instance["snippet"]["title"]
            #video information
            #this call to get the video statistics contains the last bits of information we need which are Comments and duration 
            #comments are under video_instance["statistics"]["commentCount"]
            video_data = youtube.videos().list(id=videoId,part="statistics").execute()
            # print(" ")
            # print(video_data)
            #not interate through the found videos 
            for video_instance in video_data.get("items",[]):
                #now make the check for views if it has any
                if 'viewCount' not in video_instance["statistics"]:
                    viewCount = 0
                else:
                    viewCount = video_instance["statistics"]["viewCount"]
                
                if 'commentCount' not in video_instance["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_instance["statistics"]["commentCount"]

            #then add information to storage
            storage.append(['{:,}'.format(int(viewCount)),'{:,}'.format(int(commentCount)),title])
    #now preform sorting and ranking by inserting 1 -> 5 
    #first sort values in storage by comments
    #I tried to use item getter to do it but I think the percentage sign was throwing it off
    # storage.sort(key=int(itemgetter(1)), reverse = True)
    #like the previous method ended up using a lambda to trim values (get rid of , and keep it as a int which is easily compareable). Also added reverse = True to make sure greatest to smallest
    storage = sorted(storage,key = lambda stor: int(stor[1].replace(',','')), reverse = True)
    #now add ranks
    pos = 0 
    #iterate
    while pos < len(storage):
        #insert the rank to the begining
        storage[pos].insert(0,pos+1)
        pos+=1
    #return results
    return storage

def main(): 
    #prompt user for inputs
    searchterm = input("Input Search term: ")
    maxresults = input("Input Maximum Search Results: ")
    #print results
    print("-------------")
    print("Search term: "+searchterm)
    print("Maximum Search Results: "+maxresults)
    #now gather results from a search given the search term and the max results
    results = preformsearch(searchterm,maxresults)
    #now formulate a table for Analysis #1
    #create a table via PrettyTable (importstatement at the top of code)
    table = PrettyTable()
    #create headers 
    table.field_names = ["Video ID", "Views", "Likes", "Comments","Duration","Title"]
    # now row by row add data from results into the prettytable object
    for x in results: 
        table.add_row(x)
    #use pretty print to print information nicely from console.
    print(table)
    
    #now output to a CSV file with the results of the current search
    # learned how to output to a csv from this link https://www.geeksforgeeks.org/writing-csv-files-in-python/
    #define the first row of feilds
    csvfeilds = ["Video ID", "Views", "Likes", "Comments","Duration","Title"]
    #open file in writing mode
    with open(searchterm+"_results.csv",'w') as csvfile:
        #define csvwriter
        writetofile = csv.writer(csvfile)
        writetofile.writerow(csvfeilds)
        #add all the lines of inforamtion
        for line in results: 
            writetofile.writerow(line)

    print("") # need spacing
    #Analysis #2 
    #list the rank 1 -> 5 based on like percentage == (like count / view count)
    print("Like Ranking (Analysis #2):")
    #make pretty table
    analysis2table = PrettyTable()
    #make feild names
    analysis2table.field_names = ["Rank","like percentage (like count/view count)", "View Count", "Like count", "Title"]
    #preform search and hold results
    analysis2info = preform2ndsearch(searchterm,maxresults)
    keeptrack = 0
    #now only print the top 5 
    for y in analysis2info:
        if keeptrack < 5:
            #add it to the table
            analysis2table.add_row(y)
            keeptrack += 1
    #print with pretty formatting
    print(analysis2table)
    
    print("")
    #Analysis #3
    # #list the rank 1 -> 5 highest # of comments (highest # first)
    print("Comment Count & Ranking: ")
    analysis3table = PrettyTable()
    #make table and names of fields
    analysis3table.field_names = ["Rank", "View Count", "Comment count", "Title"]
    analysis3info = preform3rdsearch(searchterm,maxresults)
    keeptrack = 0 
    #only print top 5 
    for z in analysis3info:
        if keeptrack < 5:
            analysis3table.add_row(z)
            keeptrack += 1
    print(analysis3table)

if __name__ == "__main__":
    main()
    
    
    
#extra links
#https://pypi.org/project/prettytable/ - Pretty Table usage and documentation
#https://www.programiz.com/python-programming/nested-dictionary - python dict help
#https://www.w3schools.com/python/python_ref_dictionary.asp
# help finding "duration", took me a few hours to figure out it was under "contentDetails"
#https://stackoverflow.com/questions/33698776/how-can-i-get-the-duration-of-youtube-video-with-python
# sorting with pretty table
#https://stackoverflow.com/questions/37423445/python-prettytable-sort-by-multiple-columns
# I learned how to output to a CSV file with the following website
#https://www.pythontutorial.net/python-basics/python-write-csv-file/
# more sorting resources I refrenced
# https://discuss.codecademy.com/t/what-is-the-difference-between-sort-and-sorted/349679
