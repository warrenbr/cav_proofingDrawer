from flask import Flask, render_template, request, jsonify
from ProofingDrawer_01 import *
# commented out for testing
from threading import Thread

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
    
    #here to be a thread target
def startDrawer():
   ProofingDrawer()

if __name__ == '__main__':
  app.run(debug=True, host='10.0.0.13')