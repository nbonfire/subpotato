#subpotato.py


import simplejson as json
import urllib2
import feedparser

URL_BASE="https://couchpotato/"
#get this from URL_BASE/docs
API_KEY=
FEED_URL="http://http://rss.imdb.com/user/ur#######/watchlist"


feedDict = feedparser.parse(FEED_URL)["entries"]

#Make the set of  movie names and imdb numbers
movieSet = set()
feedLength = len(feedDict)
for j in range(feedLength):
    imdbID=feedDict[j]['link'][26:35]
    movieSet.append({'title' : feedDict[j]['title'], 'id' : imdbID})

#get the set of movie names available from couchpotato
releaseSet= set()
for k in range(feedLength):
    url=URL_BASE+"/api/"+API_KEY+"/"+"movie.get?id="+movieSet[k]['id']
    json_string = urllib2.urlopen(url).read()
    the_data=json.loads(json_string)
    releaseSet.append(the_data["movie"]["releases"])

#get filenames to be synced
filesList = set()
for v in range(len(releaseSet)):
    release=releaseSet[v]
    for x in range(len(release)) :
        for y in range(len(release[x]["files"])) :
            filesList.append( release[x]["files"][y]["path"] )
        
print filesList

#TBD: actually copy the files, rsync or something.
