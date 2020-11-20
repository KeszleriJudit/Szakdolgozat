import json
import pandas
import os

class jsonObject:

    tag = ""
    patterns = []
    responses = []
    context = []

    def __init__(self):
        self.tag = ""
        self.patterns = []
        self.responses = []
        self.context = []

    def setTag(self, newTag):
        self.tag = newTag

    def addPattern(self, newPattern):
        self.patterns.append(newPattern)

    def addPatternAsArray(self, newPattern):
        for s in newPattern:
            self.patterns.append(s)   

    def addResponse(self, newResponse):
        self.responses.append(newResponse)

    def addContext(self, newContext):
        self.context.append(newContext)

    def getObjectAsJSON(self):
        x = {
            "tag": "{}".format(self.tag),
            "patterns":[s for s in self.patterns],
            "responses":[s for s in self.responses],
            "context":[s for s in self.context]
        }
        return json.dumps(x)

class excelFileReader:
    filePath = ""

    def __init__(self, filePath):
        thisFolder = os.path.dirname(os.path.abspath(__file__))
        self.filePath = os.path.join(thisFolder, filePath)
    
    def getShopInfo(self):
        excelFile = pandas.read_excel(self.filePath, header=None).values

        shopInfo = []

        for i in range(len(excelFile)):
            if i < 8 :
                oneRow = excelFile[i]

                x = jsonObject()
                x.setTag("shopInfo_{}".format(oneRow[0]))
                x.addPattern("What is the shops's {}".format(oneRow[0]))
                x.addResponse("{}: {}".format(oneRow[0], oneRow[1]))
                x.addContext("")
                
                shopInfo.append(x)

        return shopInfo

    def getOpenHours(self):
        excelFile = pandas.read_excel(self.filePath, header=None).values

        openHours = []

        for i in range(len(excelFile)):
            if 8 < i and i < 16:
                oneRow = excelFile[i]

                x = jsonObject()
                x.setTag("openHour_{}".format(oneRow[0]))
                x.addPatternAsArray(["Open hours on {}".format(oneRow[0])])
                x.addResponse("{}: {} - {}".format(oneRow[0], oneRow[1], oneRow[2]))
                x.addContext("")

                openHours.append(x)

        return openHours

    def getStoreItems(self):
        excelFile = pandas.read_excel(self.filePath, header=None).values

        storeItems = []

        for i in range(len(excelFile)):
            if i > 17:
                oneRow = excelFile[i]
                storeItems.append(oneRow[0])

        storeItems = list(dict.fromkeys(storeItems))
        
        storeItems_str = ", ".join(storeItems)

        x = jsonObject()
        x.setTag("storeItems")
        x.addPatternAsArray(["What are you selling?", "Show me what you got!", "What is in the store?", "Give me your merchandise!"])
        x.addResponse("{}".format(storeItems_str))
        x.addContext("")

        mylist = []
        mylist.append(x)

        return mylist

    def getItemValuePairs(self):
        excelFile = pandas.read_excel(self.filePath, header=None).values

        storeItems = []

        counter = 1
        for i in range(len(excelFile)):
            if i > 16:
                oneRow = excelFile[i]

                x = jsonObject()
                x.setTag("item_{}".format(counter))
                x.addPatternAsArray(["{}".format(oneRow[1])])
                x.addResponse("{}: {} HUF".format(oneRow[1], oneRow[2]))
                x.addContext("")

                storeItems.append(x)
                counter += 1

        return storeItems