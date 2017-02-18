from flask import Flask, request
from flask_cors import CORS, cross_origin
import subprocess
import httplib, urllib, base64

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Hello World!"

@app.route('/control', methods=['POST'])
def control():
    # the value from the slider
    val_string = request.get_data()[1:-1]
    # the command we want to run to move the motor
    bashCommand = "echo \"you want to send " + val_string + " to the motor\""
    # run the command
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    # get the output, if it returns anything
    output, error = process.communicate()
    # pass that output back to the browser
    return output

@app.route('/detect', methods=['GET'])
def detect():
    # do bash thing to get frame from video
    ### bash thing

    with open('smiles.jpg', 'r') as frame:
        # load into variable
        body = frame.read()
        # set api request headers
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': 'API_KEY',
            }
        # set api request params, empty
        params = urllib.urlencode({})
        # send the request
        try:
            conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return data

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return "hello"

if __name__ == "__main__":
    app.run()
