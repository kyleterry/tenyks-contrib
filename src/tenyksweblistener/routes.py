from flask import Blueprint, request, abort


app = Blueprint('TenyksWebListener', __name__)

@app.route('/', methods=['GET', 'POST'])
def acceptor():
    return "Hello"
