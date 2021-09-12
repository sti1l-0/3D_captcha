from flask import Flask, make_response, session, request
from flask_cors import CORS
from math import atan
import matrix
import json


app = Flask(__name__)
app.config["SECRET_KEY"] = "captcha"
CORS(app, supports_credentials=True)


@app.route("/get_file")
def make_file():
    objtext, position = matrix.get_obj()
    response = make_response(objtext, 200)
    session['captcha'] = position
    return response


@app.route("/check", methods=['POST'])
def check_pos():
    a = json.loads(request.data)
    theta = atan(( a["posx"]**2 + a["posy"]**2 )**0.5 / a["posz"])
    phi = atan(a["posy"] / a["posx"])
    cha = lambda x: abs(abs(x) - 3.14/2) < 0.2
    response = make_response(str(cha(theta) and cha(phi)))
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
