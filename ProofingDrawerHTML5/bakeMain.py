from flask import Flask, render_template, request, jsonify, redirect
from ProofingDrawer_01 import *
from threading import Thread
import json
from collections import OrderedDict
import io
import subprocess

app = Flask(__name__)

fileLocation = 'breadData/breadData.json'


@app.route('/')
def index():
    #gets current IP address and sends it to web server
    systemIP = (subprocess.check_output(["hostname", "-I"]))
    systemIP = str(systemIP).split(" ")[0][2:]
    systemIP = systemIP + ":5000"
    return render_template('index.html', systemIP = systemIP)

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
    file = open(fileLocation)
    fileString = file.read()
    data = json.loads(fileString, object_pairs_hook=OrderedDict)
    sendList  = []

    if(Thing == 'bName'):
        for breadN in data:
            sendList.append([breadN, data[breadN]["Name"]])
        file.close()
        # print("pain in the butt json order -------\n {}\n".format(sendList))
        return(sendList)
    else:
        breadDict = data[Thing]
        
        name = breadDict["Name"]
        breadYield = breadDict["breadYield"]
        sendList = breadDict["ingredients"]
        notes = breadDict["notes"]
        
        file.close()

        return(name, breadYield, sendList, notes)

        
@app.route('/RecipesPage')
def initRecipe():
    breadList = getDBItems("bName")
    return render_template('recipes.html', breadList = breadList)
    
@app.route('/RecipesPage/<bread>')
def getIngredents(bread):
    breadName, breadYield, ingredientList, notes = getDBItems(bread)
    return render_template('onebread.html', breadName = breadName, ingredientList = ingredientList,
                            notes = notes, breadYield = breadYield)
                            
@app.route('/RecipesPage/new')
def newRecipie():
    return render_template('newbread.html')
    
@app.route('/RecipesPage/Remove/<number>', methods=['POST'])
def RemoveBread():
    file = open(fileLocation)
    fileString = file.read()
    data = json.loads(fileString, object_pairs_hook=OrderedDict)
    number = str(4)

    del data[number]

    writeJson(data)
    
    file.close()
    return redirect('/RecipesPage')
    
@app.route('/RecipesPage/addNew', methods=['POST'])
def addNew():
    ingredientName = request.form
    ingredientPair = []

    for ing in ingredientName:
        returnIngredient = []

        returnIngredient.append(ing)
        returnIngredient.append(ingredientName[str(ing)])
        ingredientPair.append(returnIngredient)
    returnIngredient = sorted(ingredientPair)
    
    ingredents = []
    notes = []
    other = []
    #seperate out the differnt types of inputs (ingredent, yield, name, notes)
    for x in returnIngredient:
        if x[0][:2] == "in":
            ingredents.append(x)
        elif x[0][:2] == "no":
             notes.append(x[1])
        else:
            other.append(x[1])
    onlyIngredents = []
    amountOfIngredents = int(len(ingredents)/2)
    #arrange the ingredetns so they share the same array
    for i in range(amountOfIngredents):
        onlyIngredents.append([ingredents[i+amountOfIngredents][1], float(ingredents[i][1])])

    amountOfBread = str(len(getDBItems("bName")) + 1)
    
    newBreadDict = {amountOfBread:{ "Name": other[0],
                    "breadYield": float(other[1]),
                    "ingredients": onlyIngredents,
                    "notes": notes}}

    print(newBreadDict)         

    #write the file

    file = open(fileLocation)
    fileString = file.read()
    data = json.loads(fileString, object_pairs_hook=OrderedDict)
    data.update(newBreadDict)


    writeJson(data)
        
    file.close()
    
    return redirect('/RecipesPage')
    
def writeJson(data):
    with open(fileLocation, 'w') as fp:
        json.dump(data, fp, sort_keys=True, indent=4)
    file.close()


    #here to be a thread target
def startDrawer():
   ProofingDrawer()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')