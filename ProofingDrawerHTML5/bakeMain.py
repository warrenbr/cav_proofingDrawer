from flask import Flask, render_template, request, jsonify
from ProofingDrawer_01 import *
from threading import Thread
import json
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#-----Proofing stuff----------
@app.route('/ProofingPage')
def proofingPage():
    return render_template('proofing.html')
    
@app.route('/ProofingPage/proofOn', methods=['POST'])
def proofOn():
    if(PDGlobals.proofLoopOff):
        PDGlobals.proofLoopOff = False
        t = Thread(target=startDrawer)
        t.start() 
    return("drawer START!")
    
    
@app.route('/ProofingPage/proofOff', methods=['POST'])
def proofOff():
    PDGlobals.proofLoopOff = True
    ProofingDrawer()
    return("drawer STOP!")

#sending temperature to pi
@app.route('/ProofingPage/getTemp', methods=['GET'])
def getTemp():
    temp = str(PDGlobals.temperature)
    return(temp)
    
@app.route('/ProofingPage/getHumid', methods=['GET'])
def getHumid():
    humid = str(PDGlobals.humidity)
    return(humid)
    
#getting desired temperature from pi
@app.route('/ProofingPage/setTemp/<direction>', methods=['GET'])
def setTemp(direction):
    if(direction == 'plus'):
        PDGlobals.desiredTemp += 1
    elif(direction == 'minus'):
        PDGlobals.desiredTemp -= 1
    return(str(PDGlobals.desiredTemp))
    
#----Recipie stuff----------

def getDBItems(Thing):
    fileLocation = 'breadData/breadData.json'
    file = open(fileLocation)
    fileString = file.read()
    data = json.loads(fileString)
    sendList  = []
    sendName = ''

    if(Thing == 'bName'):
        for breadN in data:
            sendList.append([breadN, data[breadN]["Name"]])
        file.close()
        return(sendList)
    else:
        breadDict = data[Thing]
        
        sendList = breadDict["ingredients"]
        notes = breadDict["notes"]
        name = breadDict["Name"]
        file.close()

        return(name, sendList, notes)

        
@app.route('/RecipesPage')
def initRecipe():
    breadList = getDBItems("bName")
    return render_template('recipes.html', breadList = breadList)
    
@app.route('/RecipesPage/<bread>')
def getIngredents(bread):
    breadName, ingredientList, notes = getDBItems(bread)
    return render_template('onebread.html', breadName = breadName, ingredientList = ingredientList,
                            notes = notes)
    

#here to be a thread target
def startDrawer():
   ProofingDrawer()

if __name__ == '__main__':
  app.run(debug=True, host='10.0.0.13')