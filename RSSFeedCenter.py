import json
from feedWordCounter import feedWordCounter

class RSSFeedCenter:

    def getJSONFeeds(self):
        jsonArr = []
        services = []
        feedTitlesByService = []
        feedURLsByService = []

        services.append("CNN")
        feedTitlesByService.append(["Top Stories", "World", "U.S.", "Business", "Politics", "Technology", "Health", "Entertainment", "Travel", "Living", "Video", "CNN Student News", "Most Recent"])
        feedURLsByService.append(["http://rss.cnn.com/rss/cnn_topstories.rss", "http://rss.cnn.com/rss/cnn_world.rss", "http://rss.cnn.com/rss/money_latest.rss", "http://rss.cnn.com/rss/cnn_allpolitics.rss", "http://rss.cnn.com/rss/cnn_tech.rss", "http://rss.cnn.com/rss/cnn_health.rss", "http://rss.cnn.com/rss/cnn_showbiz.rss", "http://rss.cnn.com/rss/cnn_travel.rss", "http://rss.cnn.com/rss/cnn_living.rss", "http://rss.cnn.com/rss/cnn_freevideo.rss", "http://rss.cnn.com/services/podcasting/studentnews/rss.xml", "http://rss.cnn.com/rss/cnn_latest.rss"])
        x = 0
        for serviceTitle in services:
            currServiceFeeds = []
            titles = feedTitlesByService[x]
            y = 0
            for feedURL in feedURLsByService[x]:
                currServiceFeeds.append({"title": titles[y], "url": feedURL})
                y = y + 1
            service = {"name": serviceTitle, "id": serviceTitle, "feeds": currServiceFeeds}
            jsonArr.append(service)
            x = x + 1
        return json.dumps({'RSS': jsonArr}, indent=4)

    def getResultsFromFeed(self, feed):

        feedAnalyzer = feedWordCounter(feed)
        wordFrequencyData = feedAnalyzer.getSortedItemList()
        jsonReturnArray = []

        jsonWords = []
        for wordFrequencyObject in wordFrequencyData:
            wordFreq = {"word":wordFrequencyObject[0],"occurrences":wordFrequencyObject[1]}
            jsonWords.append(wordFreq)

        jsonReturnArray.append({"url": feed, "words": jsonWords})
        return json.dumps({'RSS': jsonReturnArray}, indent = 4)
