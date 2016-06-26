import os, sys


class LanguageModel(object):
	def __init__(self, ta=None, va=None, sm=0.05, termlen=400000):
		self.SMOOTHING = sm
		self.TREM_LENGTH = termlen
		self.ta = ta
		self.va = va
		self.wordCount = {}
		self.rankingResult = {}
		self.__construct_data_from_file() # fill in self.wordCount, self.rankingResult
		pass

	def __construct_data_from_file(self):
		"""
		fill in:
			self.wordCount
			self.rankingResult
		"""
		pass

	def __update_wordCount(self, blogName):
		if blogName in self.wordCount.keys():
			return
		self.wordCount[blogName] = {}
		self.wordCount[blogName]['length'] = 0
		self.wordCount[blogName]['unique_length'] = 0
		self.wordCount[blogName]['words'] = {}
		self.wordCount[blogName]['terms'] = []
		print >> sys.stderr, "Parsing", blogName
		b = self.ta.getBlogByName(blogName)
		pid_list = b.getAllPosts()
		for pid in pid_list:
			p = self.ta.getPostById(blogName, pid)
			terms = self.va.extractTermsFromPost(p)
			terms += self.va.extractTermsFromPhoto(p)
			for term in terms:
				if term not in self.wordCount[blogName]['words']:
					self.wordCount[blogName]['words'][term] = 1
				else:
					self.wordCount[blogName]['words'][term] += 1
			self.wordCount[blogName]['terms'] += terms
		self.wordCount[blogName]['unique_length'] = len(self.wordCount[blogName]['words'].keys())
		for key in self.wordCount[blogName]['words']:
			self.wordCount[blogName]['length'] += self.wordCount[blogName]['words'][key]
		print >> sys.stderr, blogName, self.wordCount[blogName]['length'], self.wordCount[blogName]['unique_length']

	def __make_probability_dict(self, blogName):
		blogProbability = {}
		for bn in self.ta.getAllBlogs():
			blogProbability[bn] = self.__countBlogProbability(bn, self.wordCount[blogName]['terms'])
		return blogProbability

	def __countBlogProbability(self, blogName, content):
		blog_P = 0
		probability_pi = 0
		for word in content:
			probability_pi += log(self.__wordProbability(word, blogName))
		return blog_P + probability_pi

	def __wordProbability(self, word, blogName):
		wordInTopic = 0
		if word in self.wordCount[blogName]['words']:
			wordInTopic = self.wordCount[blogName]['words'][word]
		blogLength = self.wordCount[blogName]['length']
		return float(self.SMOOTHING+wordInTopic) / float(self.SMOOTHING*self.TREM_LENGTH+blogLength)

	def __sort_probability_dict(blogProbability):
		ranking_list = []
		for key, value in sorted(blogProbability.iteritems(), key=lambda (k,v): (v,k)):
			ranking_list.append((key, value))
		return ranking_list

	def query(self, blogName, topK=10):
		if blogName in self.rankingResult.keys():
			return self.rankingResult[blogName][0:topK]
		# update self.wordCount
		self.__update_wordCount(blogName)
		d = self.__make_probability_dict(blogName)
		ranking_list = self.__sort_probability_dict(d)
		# update self.rankingResult
		self.rankingResult[blogName] = ranking_list
		return ranking_list[0:topK]

