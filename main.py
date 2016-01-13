import json

from bottle import Bottle, route, run, request, get, post, response
from htmlStrings import Forms
from RSSFeedCenter import RSSFeedCenter


app = Bottle()
htmlStringsForm = Forms()
addNewRowBtnString = '<button id="newRowButton" style="background-color:orange;" class="btn btn-primary btn-block">Add more feeds</button>;'

@app.get('/')
def landingPage():
    s = htmlStringsForm.getHeader() + '<body onload="start()">'
    s = s + htmlStringsForm.getPageTitleHeader() + '<div id="grid-container"></div>' + addNewRowBtnString + '</body></html>'
    return s

@app.get('/echo/<id:int>')
def reqFeedMenuGet(id):
    print(id)
    return 'j'

@app.route('/getFeeds/', methods=['GET'])
def getFeeds():
    return RSSFeedCenter().getJSONFeeds()

@app.route('/getResults/', methods=['GET'])
def getResults():
    print('a')
    print(request.url)
    return 'k'

@app.route('/getResults/<feedURL>', methods=['GET'])
def getResults(feedURL):
    feedURL = feedURL.replace('$@$@', '/')
    #feedCenter = RSSFeedCenter()
    return RSSFeedCenter().getResultsFromFeed(feedURL)


run(app, host='localhost', port=8080)