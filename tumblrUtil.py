import pytumblr
import os, pickle, sys

"""
this class should be the only interface between our program and Tumblr data
"""
class TumblrAgent(object):
	
	# the cache file path
	CACHE_FILE_PATH = "data/TumblrAgentCache"

	# api key
	TUMBLR_CONSUMER_KEY = "ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk"
	TUMBLR_CONSUMER_SECRET = "PpHRSKUKqBMNp4bjchW8EkxQNcQvyVyDYDWiz7gROzVERsOYAs"
	# OAuth
	ACCESS_TOKEN = "sVF038jN4AjBN1sUJ9RiqE0PUKnQDcgVBCOvEkiblXwSROiEIO"
	ACCESS_SECRET = "NXYoBsNQBW3b6yqNS1VuxKixMoktAADZfPGJ72wIZOSx62P5OO"

	def __init__(self):
		"""
		constructor: initialize variables
		"""
		# data cache
		self.__data = self.__read_cache()
		if self.__data == None:
			self.__data = {'blogs' : {}, 'posts' : {}}
		# tumblr client
		self.__client = pytumblr.TumblrRestClient(
			type(self).TUMBLR_CONSUMER_KEY,
			type(self).TUMBLR_CONSUMER_SECRET,
			type(self).ACCESS_TOKEN,
			type(self).ACCESS_SECRET
		)

	def __del__(self):
		"""
		destructor
		"""
		self.__write_cache(self.__data)

	def __read_cache(self):
		"""
		to read the cached data and return
		"""
		if os.path.exists(type(self).CACHE_FILE_PATH):
			return pickle.load(open(type(self).CACHE_FILE_PATH, "r"))
		return None

	def __write_cache(self, data):
		"""
		to write the given data to cache
		"""
		pickle.dump(data, open(type(self).CACHE_FILE_PATH, "w"))

	def __get_data_from_tumblr(self, blog_name):
		my_offset = 0
		raw = self.__client.posts(blog_name, limit=20, offset=my_offset, reblog_info=True, notes_info=True)
		self.__data['blogs'][blog_name] = TumblrBlog(raw['blog'])
		for raw_p in raw['posts']:
			p = TumblrPost(raw_p)
			self.__data['posts'][p.getId()] = p
			self.__data['blogs'][blog_name].addPost(p.getId())
		print >> sys.stderr, "processed %d posts for this blog: %s" % (len(raw['posts']), blog_name)
		# check whether there are still posts to retrieve
		while len(raw['posts']) >= 20 and my_offset < 200:
			my_offset += len(raw['posts'])
			raw = self.__client.posts(blog_name, limit=20, offset=my_offset, reblog_info=True, notes_info=True)
			for raw_p in raw['posts']:
				p = TumblrPost(raw_p)
				self.__data['posts'][p.getId()] = p
				self.__data['blogs'][blog_name].addPost(p.getId())
			print >> sys.stderr, "processed %d posts for this blog: %s" % (len(raw['posts']), blog_name)

	def getBlogByName(self, blog_name):
		# if not found in __data
		if blog_name not in self.__data['blogs']:
			self.__get_data_from_tumblr(blog_name)
		return self.__data['blogs'][blog_name]

	def getPostById(self, blog_name, post_id):
		# 1) check if the blog exists in __data
		if blog_name not in self.__data['blogs']:
			self.__get_data_from_tumblr(blog_name)
		# 2) check if the post exists
		if post_id in self.__data['posts']:
			return self.__data['posts'][post_id]
		return None

	def getBlogCount(self):
		return len(self.__data['blogs'])

	def getPostCount(self):
		return len(self.__data['posts'])


"""
this class stores the information of Tumblr blogs
"""
class TumblrBlog(object):
	def __init__(self, raw_dictionary):
		self.name = raw_dictionary['name']
		self.title = raw_dictionary['title']
		self.url = raw_dictionary['url']
		self.total_posts = raw_dictionary['total_posts']
		self.is_nsfw = raw_dictionary['is_nsfw']
		self.description = raw_dictionary['description']
		self.posts = [] # list of post_id
	
	def getName(self):
		return self.name

	def getTitle(self):
		return self.title

	def getUrl(self):
		return self.url

	def getTotalPosts(self):
		return self.total_posts

	def isNSFW(self):
		return self.is_nsfw

	def getDescription(self):
		return self.description

	def addPost(self, post_id):
		self.posts.append(post_id)

	def getAllPosts(self):
		return self.posts


"""
this class stores the information of Tumblr posts
"""
class TumblrPost(object):
	def __init__(self, raw_dictionary):
		self.id = raw_dictionary['id']
		self.url = raw_dictionary['post_url']
		self.tags = raw_dictionary['tags']
		self.type = raw_dictionary['type']
		self.total_notes = raw_dictionary['note_count']
		self.blog_name = raw_dictionary['blog_name']
	
	def getId(self):
		return self.id
	
	def getUrl(self):
		return self.url

	def getTags(self):
		return self.tags

	def getType(self):
		return self.type

	def getTotalNotes(self):
		return self.total_notes

	def getBlogName(self):
		return self.blog_name


