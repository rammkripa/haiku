# hello world web app
from flask import Flask, url_for, redirect, request         # import flask
import shakey as Shakes
app = Flask(__name__)             # create an app instance
@app.route("/haiku")
def printy():
	try:
		return Shakes.create_random_haiku() 
	except:
		return printy()

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)                     # run the app