
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"hello": "world"})

@app.route('/mars', methods=['GET'])
def mars():
    return jsonify({"hello": "mars"})

if __name__ == '__main__':
    app.run(port=9090)
