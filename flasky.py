# hello world web app
from flask import Flask, url_for, redirect, request         # import flask
import shakes as Shakey
app = Flask(__name__) 
@app.route("/")
def index():
	return render_template('index.html')

@app.route("/generate")
def printy():
	try:
		return Shakey.create_random_haiku() 
	except:
		return printy()

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)                     # run the app