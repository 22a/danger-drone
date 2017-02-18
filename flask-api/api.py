from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Hello World!"

@app.route('/control', methods=['POST'])
def control():
    val_string = request.get_data()[1:-1]
    val = int(val_string)
    return str(val)

# @app.route('/logo', methods=['POST'])
# def logo():
#     # do logo things
#     return "logo pls"

if __name__ == "__main__":
    app.run()
