import urllib.request
from xml.dom import minidom



class feedWordCounter:
	def __init__(self, address):
		self.address = address
		self.data = []
		self.words = []
		self.wordFrequencyDictionary = dict()
		self.parseData()

	def parseData(self):
		file_request = urllib.request.Request(self.address)
		file_opener = urllib.request.build_opener()
		file_feed = file_opener.open(file_request).read()
		file_xml = minidom.parseString(file_feed)
		item_node = file_xml.getElementsByTagName("item")

		titles = []
		descriptions = []
		for i in range(item_node.length):
			item = item_node[i]
			hasChild = item.hasChildNodes()
			for child in item.childNodes:
				for grandchild in child.childNodes:
					if grandchild.parentNode.nodeName == "title":
						titles.append(grandchild.nodeValue)
					elif grandchild.parentNode.nodeName == "description":
						descriptions.append(grandchild.nodeValue)

		for title in titles:
			newTitle = self.trimHTMLAndNonAlphaNumericChars(title)
			self.data.append(newTitle)
		for description in descriptions:
			newDescription = self.trimHTMLAndNonAlphaNumericChars(description)
			self.data.append(newDescription)
		self.prepareWordsList()

	def trimHTMLAndNonAlphaNumericChars(self, stringToTrim):
		#trim html

		htmlBeginsIndex = stringToTrim.find("<")
		returnStr = ''
		if htmlBeginsIndex == -1:
			returnStr = stringToTrim
		else:
			returnStr = str(stringToTrim)[0:htmlBeginsIndex]
			#print "returnStr:'" + str(returnStr) + "' htmlBeginsIndex:" + str(htmlBeginsIndex)
		
		alphaNumericCharacters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890 "

		stringOfBadCharactersFound = ""
		for char in returnStr:
			if alphaNumericCharacters.find(char) == -1 and stringOfBadCharactersFound.find(char) == -1:
				stringOfBadCharactersFound = stringOfBadCharactersFound + char
		for badChar in stringOfBadCharactersFound:
			returnStr.replace(badChar, "")

		return returnStr

	def prepareWordsList(self):

		for stringInData in self.data:
			if not(stringInData == None):
				self.words.extend(stringInData.split(" "))

		wordIndex = 0
		for word in self.words:
			if word.__class__.__name__ == "unicode":
				newWord = word.encode("utf-8")
				self.words[wordIndex] = newWord
				self.foundWord(newWord)
			else:
				self.foundWord(word)
			wordIndex += 1

	def foundWord(self, word):
		if(word in self.wordFrequencyDictionary):
			self.wordFrequencyDictionary[word] = self.wordFrequencyDictionary[word] + 1
		else:
			self.wordFrequencyDictionary[word] = 1


	def getSortedItemList(self):
		sortedItemList = list()

		for key in self.wordFrequencyDictionary.keys():
		    currentValue = self.wordFrequencyDictionary[key]

		    i = 0
		    itemWasPlaced = False
		    while(not(itemWasPlaced)):
		        if(i == len(sortedItemList)):
		            sortedItemList.insert(i, [key, currentValue])
		            itemWasPlaced = True
		        elif(sortedItemList[i] and sortedItemList[i][1] and sortedItemList[i][1] <= currentValue):
		            sortedItemList.insert(i, [key, currentValue])
		            itemWasPlaced = True
		        i = i+1



		return sortedItemList;




