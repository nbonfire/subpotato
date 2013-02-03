#subpotato.py


import simplejson as json
import urllib2
import feedparser

def init() : 
    defaultUrl="https://couchpotato/"
    #get this from defaultUrl/docs
    defaultKey=
    defaultFeed="http://http://rss.imdb.com/user/ur#######/watchlist"

def processFileList(filesToCopy) :
    #just print for now, eventually send to rsync
    print filesToCopy

def subpotato(URL_BASE, API_KEY, FEED_URL) :
    
    feedDict = feedparser.parse(FEED_URL)["entries"]

    #Make the set of  movie names and imdb numbers
    movieSet = set()
    feedLength = len(feedDict)
    for j in range(feedLength):
        imdbID=feedDict[j]['link'][26:35]
        movieSet.append({'title' : feedDict[j]['title'], 'id' : imdbID})

    #get the set of movie names available from couchpotato
    releases= set()
    for k in range(feedLength):
        url=URL_BASE+"/api/"+API_KEY+"/"+"movie.get?id="+movieSet[k]['id']
        json_string = urllib2.urlopen(url).read()
        the_data=json.loads(json_string)
        releases.append(the_data["movie"]["releases"])

    #get filenames to be synced
    filesList = set()
    for release in releases:
        for x in release :
            for file in x["files"] :
                filesList.append( y["path"] )
    
    #process the list of files
    processFileList(filesList)
    
    
if __name__ == "__main__" : 
    init()
    subpotato(defaultURL, defaultKey, defaultFeed)
    #TBD: actually copy the files, rsync or something.
    
