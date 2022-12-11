from flask import Flask, render_template, request
from flask import redirect, url_for
from manage_subject_info import *
from mturk_utils import *
import urllib

"""
Import blueprints
"""
from memory.memory_tasks import memory_tasks

_thisDir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

"""
Register blueprints
"""

app.register_blueprint(memory_tasks)

@app.route('/')
def hello_world():
    return 'Hello from Flask'

@app.route('/thank_you')
def thank_you():
    return render_template('thankyou.html')

@app.route("/unauthorized_error", methods=["GET"])
def unauthorized_error():
    return render_template('unauthorized_error.html')


@app.route("/page_not_found", methods=["GET"])
def page_not_found():
    return render_template('404.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.debug = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(host='0.0.0.0', port=8000)
