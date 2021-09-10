from flask import Flask, make_response
import matrix

app = Flask(__name__)


@app.route("/get_file")
def make_file():
    response = make_response(matrix.MatrixToObj(
        matrix.ImageToMatrix(matrix.randstrToImage()).tolist()), 200)
    response.mimetype = "text/plain"
    return response


@app.route("/check")
def check_file():
    pass


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
