from flask import Flask, render_template, request, jsonify
from ProofingDrawer_01 import *
# commented out for testing
from threading import Thread

app = Flask(__name__)
proofLoopOff = True

class HTMLglobals():
    proofLoopOff = True


@app.route('/')
def index():
    return render_template('index.html')

#-----Proofing stuff----------
@app.route('/ProofingPage')
def proofingPage():
    return render_template('proofing.html')
    
@app.route('/ProofingPage/proofOn', methods=['POST'])
def proofOn():
    ProofingDrawer.loopOn = True
    if(HTMLglobals.proofLoopOff):
        HTMLglobals.proofLoopOff = False
        t = Thread(target=startDrawer)
        t.start() 
    return("drawer START!")
    
@app.route('/ProofingPage/proofOff', methods=['POST'])
def proofOff():
    ProofingDrawer.loopOn = False
    ProofingDrawer(False)
    HTMLglobals.proofLoopOff = True
    return("drawer STOP!")

@app.route('/ProofingPage/getTemp', methods=['GET'])
def getTemp():
    temp = str(PDGlobals.temperature)
    return(temp)
    
@app.route('/ProofingPage/getHumid', methods=['GET'])
def getHumid():
    humid = str(PDGlobals.humidity)
    return(humid)
    
    #here to be a thread target
def startDrawer():
   ProofingDrawer(True)

if __name__ == '__main__':
  app.run(debug=True, host='10.0.0.13')