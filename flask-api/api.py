from flask import Flask, request
from flask_cors import CORS, cross_origin
import subprocess

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

# @app.route('/logo', methods=['POST'])
# def logo():
#     # do logo things
#     return "logo pls"

if __name__ == "__main__":
    app.run()
