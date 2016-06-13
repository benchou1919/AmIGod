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
	info = tClient.getBlogInfo(blog_url)['blog']
	# posts = tClient.getBlogPostById(blog_name=blog_url, post_id=145759083652, include_reblog=True, include_notes=True)
	posts = tClient.getBlogPostsByTag(blog_name=blog_url, tag="magneto", limit=100, offset=0, include_reblog=False, include_notes=False)
	return render_template('search.html', blog_name=blog_url, info=info, posts=posts), 200

if __name__ == "__main__":
	app.run(port=8080)
	app.debug = True

