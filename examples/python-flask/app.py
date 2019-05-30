import os

import planforge
from flask import Flask, render_template
from planforge import Customer

planforge.api_key = os.environ['PLANFORGE_API_KEY']

app = Flask(__name__)


@app.route("/")
def hello():
    customer = Customer.get('cus_Epgd3XNJn0NU1P')
    return render_template('index.html', customer=customer)
