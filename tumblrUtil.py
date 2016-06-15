import pytumblr
import os, pickle, sys
import json

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

	def __str__(self):
		s = "%d blogs, %d posts\n" % (len(self.__data['blogs']), len(self.__data['posts']))
		s += "The blogs are:\n"
		s += str(self.getAllBlogs()) + "\n"
		return s

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

	def getAllBlogs(self):
		return self.__data['blogs'].keys()

	def getAllPosts(self):
		return self.__data['posts'].keys()

	def deleteBlogData(self, blog_name):
		if blog_name in self.__data['blogs']:
			# remove all the posts of this blog
			for pid in self.__data['blogs'][blog_name].getAllPosts():
				del self.__data['posts'][pid]
			del self.__data['blogs'][blog_name]


"""
this class stores the information of Tumblr blogs
"""
class TumblrBlog(object):
	def __init__(self, raw_dictionary):
		self.raw = json.dumps(raw_dictionary) # raw data as json string
		self.name = raw_dictionary['name']
		self.title = raw_dictionary['title']
		self.url = raw_dictionary['url']
		self.total_posts = raw_dictionary['total_posts']
		self.updated = raw_dictionary['updated']
		self.is_nsfw = raw_dictionary['is_nsfw']
		self.description = raw_dictionary['description']
		self.posts = [] # list of post_id
		self.ask = raw_dictionary['ask'] # whether allowing questions
		self.ask_page_title = raw_dictionary['ask_page_title']
		self.ask_anon = raw_dictionary['ask_anon'] # whether allowing anonynous questions
	
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

	def canAsk(self):
		"""
		return whether this blog allows questions
		"""
		return self.ask
	
	def getAskPageTitle(self):
		return self.ask_page_title

	def canAskAnon(self):
		"""
		return whether this blog allows anonymous questions
		"""
		return self.ask_anon


"""
this class stores the information of Tumblr posts
"""
class TumblrPost(object):
	def __init__(self, raw_dictionary):
		self.raw = json.dumps(raw_dictionary) # raw data as json string
		self.id = raw_dictionary['id']
		self.url = raw_dictionary['post_url']
		self.tags = raw_dictionary['tags']
		self.type = raw_dictionary['type']
		self.total_notes = raw_dictionary['note_count']
		self.blog_name = raw_dictionary['blog_name']
		self.timestamp = raw_dictionary['timestamp'] # seconds since epoch
		self.format = raw_dictionary['format'] # either HTML or Markdown
		self.notes = raw_dictionary['notes']
		#
		if self.type == "text":
			self.title = raw_dictionary['title']
			self.body = raw_dictionary['body']
		elif self.type == "photo":
			self.photos = raw_dictionary['photos']
			self.caption = raw_dictionary['caption']
		elif self.type == "quote":
			self.text = raw_dictionary['text']
			self.source = raw_dictionary['source']
		elif self.type == "link":
			self.title = raw_dictionary['title']
			self.url = raw_dictionary['url']
			self.author = raw_dictionary['author']
			self.publisher = raw_dictionary['publisher']
			self.photos = raw_dictionary['photos']
			self.description = raw_dictionary['description']
		elif self.type == "chat":
			self.title = raw_dictionary['title']
			self.body = raw_dictionary['body']
			self.dialogue = raw_dictionary['dialogue']
		elif self.type == "audio":
			self.caption = raw_dictionary['caption']
			self.player = raw_dictionary['player']
			self.plays = raw_dictionary['plays']
			self.artist = raw_dictionary['artist']
			self.album = raw_dictionary['album']
			self.track_name = raw_dictionary['track_name']
			self.year = raw_dictionary['year']
		elif self.type == "video":
			self.caption = raw_dictionary['caption']
			self.player = raw_dictionary['player']
		elif self.type == "answer":
			self.asking_name = raw_dictionary['asking_name']
			self.asking_url = raw_dictionary['asking_url']
			self.question = raw_dictionary['question']
			self.answer = raw_dictionary['answer']

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


