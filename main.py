# main.py
from flask import Flask,session

app = Flask(__name__)
app.secret_key = '123'

import arvorePesquisaCPF as aCpf
import arvorePesquisaNome as aNome
from routes import *

if __name__ == "__main__":
    app.run(debug=True)