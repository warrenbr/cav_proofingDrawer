from flask import Flask, render_template, request, jsonify
#from ProofingDrawer_01 import *
# commented out for testing
from threading import Thread

app = Flask(__name__)
proofLoopOff = True

class HTMLglobals():
    proofLoopOff = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ProofingPage/<int:val>')
def proofing(val):
    val = bool(val)
#    ProofingDrawer.loopOn = val
# commented out for testing
    if(val == True and HTMLglobals.proofLoopOff):
        HTMLglobals.proofLoopOff = False
        t = Thread(target=startDrawer)
        t.start() 
        print("drawer START!")
    elif(val == False):
#        ProofingDrawer(False)
# commented out for testing
        HTMLglobals.proofLoopOff = True
        print("drawer STOP!")
        
    return render_template('ProofingPage.html')

    #here to be a thread target
def startDrawer():
    print ("yo")
#    ProofingDrawer(True)
# commented out for testing

if __name__ == '__main__':
  app.run(debug=True, host='192.168.1.119')
