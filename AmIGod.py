from flask import Flask, render_template, redirect, request
import tumblrUtil

app = Flask(__name__)
tClient = tumblrUtil.TumblrClient()

@app.route("/")
def index():
	return render_template('index.html'), 200

@app.route("/search", methods=['POST'])
def search():
	global tClient
	blog_url = request.form['blog_url']
	detail = tClient.getBlogInfo(blog_url)['blog']
	return render_template('search.html', blog_name=blog_url, detail=detail), 200

if __name__ == "__main__":
	app.run(port=8080)
	app.debug = True

