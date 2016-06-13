import pytumblr

class TumblrClient(object):
	# api key
	TUMBLR_CONSUMER_KEY = "ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk"
	TUMBLR_CONSUMER_SECRET = "PpHRSKUKqBMNp4bjchW8EkxQNcQvyVyDYDWiz7gROzVERsOYAs"
	# OAuth
	ACCESS_TOKEN = "sVF038jN4AjBN1sUJ9RiqE0PUKnQDcgVBCOvEkiblXwSROiEIO"
	ACCESS_SECRET = "NXYoBsNQBW3b6yqNS1VuxKixMoktAADZfPGJ72wIZOSx62P5OO"

	def __init__(self):
		self.client = pytumblr.TumblrRestClient(
			type(self).TUMBLR_CONSUMER_KEY,
			type(self).TUMBLR_CONSUMER_SECRET,
			type(self).ACCESS_TOKEN,
			type(self).ACCESS_SECRET
		)
	def getBlogInfo(self, blog_name=None):
		if blog_name:
			return self.client.blog_info(blog_name)
		return None
	def getBlogAvatar(self, blog_name=None, size=512):
		if blog_name:
			return self.client.avatar(blog_name, size)
		return None
	def getBlogLikes(self, blog_name=None, limit=20):
		if blog_name:
			return self.client.blog_likes(blog_name, limit=limit)
		return None
	def getBlogFollowers(self, blog_name=None, limit=20, offset=0):
		if blog_name:
			return self.client.followers(blog_name, limit=limit, offset=offset)
		return None
	def getBlogPosts(self, blog_name=None, limit=20, offset=0, include_reblog=False, include_notes=False):
		if blog_name:
			return self.client.posts(blog_name, limit=limit, offset=offset, reblog_info=include_reblog, notes_info=include_notes)
		return None
	def getBlogPostById(self, blog_name=None, post_id=-1, limit=20, offset=0, include_reblog=False, include_notes=False):
		if blog_name:
			return self.client.posts(blog_name, id=post_id, limit=limit, offset=offset, reblog_info=include_reblog, notes_info=include_notes)
		return None
	def getBlogPostsByTag(self, blog_name=None, tag="", limit=20, offset=0, include_reblog=False, include_notes=False):
		if blog_name:
			return self.client.posts(blog_name, tag=tag, limit=limit, offset=offset, reblog_info=include_reblog, notes_info=include_notes)
		return None
	def getTaggedPosts(self, tag="", limit=20):
		if len(tag) > 0:
			return self.client.tagged(tag, limit=limit)
		return None
