from flask import Flask, make_response, session, request, render_template
from math import atan
from flask_cors import CORS
import matrix
import json


app = Flask(__name__,template_folder = "./dist",static_folder='./dist')
app.config["SECRET_KEY"] = "captcha"
CORS(app)


@app.route('/')
def root():
    return render_template('index.html')




@app.route("/get_file")
def make_file():
    objtext, position = matrix.get_obj()
    response = make_response(objtext, 200)
    session['captcha'] = position
    return response


@app.route("/check", methods=['POST'])
def check_pos():
    a = json.loads(request.data)
    # 纬度
    theta = atan(( a["posx"]**2 + a["posy"]**2 )**0.5 / a["posz"] + 1e-10)
    # 经度
    phi = atan(a["posy"] / (a["posx"] + 1e-10))
    print(a)
    response = make_response(str(0<theta<0.12).lower())
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
