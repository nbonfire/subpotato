#subpotato.py


import simplejson as json
import urllib2
import feedparser
import os.path as path

defaultUrl="https://couchpotato/"
    #get this from defaultUrl/docs
defaultKey=
defaultFeed="http://http://rss.imdb.com/user/ur#######/watchlist"
listFilename=path.expanduser("~/subpotato/filestocopy.txt")
pathPrefix="/mnt/samba/Videos/Movies"

def processFileList(filesToCopy) :
    #open the list file, read it in
    #print filesToCopy
    with open(listFilename) as f:
        d = {}
        lines = f.read().split('\n')
        #print lines
        f.close()
        #add unique filenames to the list 
        for files in filesToCopy:
            if files not in lines:
                lines.append(files)
        #rewrite the file with all unique filenames        
        with open(listFilename, 'w') as outputFile:
            for line in lines:
                outputFile.write("%s\n" % line)

def subpotato(URL_BASE, API_KEY, FEED_URL) :
    
    feedDict = feedparser.parse(FEED_URL)["entries"]

    #Make the set of  movie names and imdb numbers
    movies = []
    feedLength = len(feedDict)
    for j in range(feedLength):
        imdbID=feedDict[j]['link'][26:35]
        #print imdbID
        #print feedDict[j]['title']
        movies.append({'title' : feedDict[j]['title'], 'id' : imdbID})

    #get the set of movie names available from couchpotato
    releases= []
    for movie in movies:
        url=URL_BASE+"/api/"+API_KEY+"/"+"movie.get?id="+movie['id']
        json_string = urllib2.urlopen(url).read()
        the_data=json.loads(json_string)
        releases.append(the_data["movie"]["releases"])

    #get filenames to be synced
    filesList = []
    for release in releases:
        for x in release :
            for filename in x["files"] :
                filesList.append( filename["path"][len(pathPrefix):] )
    
    #process the list of files
    processFileList(filesList)
    
    
if __name__ == "__main__" : 
    
    subpotato(defaultURL, defaultKey, defaultFeed)
    #TBD: actually copy the files, rsync or something.
    
