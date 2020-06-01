#!/usr/bin/env python3

from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/seed", methods=['GET', 'POST'])
def seed():
    if request.method == 'GET':
        return "1337\n"
    else:
        return "\"ok\"\n"

if __name__ == "__main__":
    app.run(host='192.168.0.2', port=8081)
