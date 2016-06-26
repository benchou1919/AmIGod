from flask import Flask, render_template, redirect, request
from tumblrUtil import TumblrAgent as TA
import logging
from word2vecAsClass import W2V

# global variables
ta = None
w2v = None
app = Flask(__name__)

def initializeGlobalVariables():
	global ta, w2v
	logging.debug('initializing TumblrAgent ...')
	ta = TA()
	logging.debug('initializing W2V ...')
	w2v = W2V(ta=ta)

@app.route("/")
def index():
	return render_template('index.html'), 200

@app.route("/search", methods=['POST'])
def search():
	global w2v
	blogName = request.form['blogName']
	vsmResult = [('abcde', 0.99), ('cdefg', 0.83), ('asdf', 0.78), ('superbc28blog', 0.777), ('brianhuang', 0.54321)]
	lmResult = [('abcde', 0.99), ('cdefg', 0.83), ('asdf', 0.78), ('superbc28blog', 0.777), ('brianhuang', 0.54321)]
	w2vResult = w2v.queryByBlogName(blogName)
	return render_template('search.html', blogName=blogName, w2vResult=w2vResult, vsmResult=vsmResult, lmResult=lmResult), 200

if __name__ == "__main__":
	app.debug = True
	logging.basicConfig(level=logging.DEBUG)
	
	logging.debug('initializing global variables...')
	initializeGlobalVariables()

	logging.debug('running on port 8080 ...')
	app.run(port=8080)

