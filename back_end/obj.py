from flask import Flask, make_response, session, request
from flask_cors import CORS
import matrix, json

app = Flask(__name__)
app.config["SECRET_KEY"] = "captcha"
CORS(app,supports_credentials=True)


@app.route("/get_file")
def make_file():
    objtext, position = matrix.get_obj()
    response = make_response(objtext, 200)
    session['captcha'] = position
    return response


@app.route("/check", methods=['POST'])
def check_pos():
    a = json.loads(request.data)
    response = make_response(str(
        (a["posx"]/30)**2 + (a["posy"]/50)**2 < 2
        and
        a["posz"] < -90
    ))
    return response


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
