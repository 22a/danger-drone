from flask import Flask, request
from flask_cors import CORS, cross_origin
import subprocess
import httplib, urllib, base64
import json

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
    bashCommand = "gpio -g pwm 18 " + map_range(int(val_string),0,100,50,200)
    # run the command
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    # get the output, if it returns anything
    output, error = process.communicate()
    # pass that output back to the browser
    return output

@app.route('/detect', methods=['POST'])
def detect():
    # do bash thing to get frame from video
    ### bash thing

    with open('happy_plus_sad.jpg', 'r') as frame:
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
            emotions = categorise_faces(data)
            return str(emotions)

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return "err"

def map_range(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def max_emotion(face):
    scores = face["scores"]
    max_emotion_val = float("-inf")
    strongest_emotion = None
    for emotion, value in scores.iteritems():
        current_emotion_val = float(value)
        if current_emotion_val > max_emotion_val:
            max_emotion_val = current_emotion_val
            strongest_emotion = emotion
    return strongest_emotion


def categorise_faces(emotion_json_string):
    faces = json.loads(emotion_json_string)
    num_people = len(faces)
    emotions = {
            "sadness":0,
            "neutral":0,
            "contempt":0,
            "disgust":0,
            "anger":0,
            "surprise":0,
            "fear":0,
            "happiness":0
            }
    for face in faces:
        max_e = max_emotion(face)
        emotions[max_e] += 1
    human_emotions = {
            "sadness":"sad",
            "neutral":"😐",
            "contempt":"insolent",
            "disgust":"disgusted",
            "anger":"angry",
            "surprise":"surprised",
            "fear":"scared",
            "happiness":"happy"
            }    
     #TODO
     # Replace default emotions with human emotions
    return emotions

if __name__ == "__main__":
    app.run()
