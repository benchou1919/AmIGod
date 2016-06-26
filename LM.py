import sys, os
import pytumblr
import json
from math import log
from tumblrUtil import TumblrAgent as TA
from vocabUtil import VocabAgent as VA
from imageUtil import parser, OCR

# use TumblrAgent
va = VA()
va.load('data/VocabAgentCache')
ta = TA()

def legalImageType(url):
	path = url.split('.')
	iType = path[len(path)-1]
	if iType == 'jpg' or iType == 'png':
		return True;
	return False;

def addBlog(blog, _wordCount):
	_wordCount[blog] = {}
	_wordCount[blog]['length'] = 0
	_wordCount[blog]['unique_length'] = 0
	_wordCount[blog]['words'] = {}
	_wordCount[blog]['terms'] = []
	print "Parsing", blog
	b = ta.getBlogByName(blog)
	pid_list = b.getAllPosts()
	for pid in pid_list:
		p = ta.getPostById(blog, pid)
		terms = va.extractTermsFromPost(p)
		terms += va.extractTermsFromPhoto(p)
		for term in terms:
			if term not in _wordCount[blog]['words']:
				_wordCount[blog]['words'][term] = 1
			else:
				_wordCount[blog]['words'][term] += 1
		_wordCount[blog]['terms'] += terms
	_wordCount[blog]['unique_length'] = len(_wordCount[blog]['words'].keys())
	for key in _wordCount[blog]['words']:
		# if key not in Terms:
		# 	Terms.append(key)
		_wordCount[blog]['length'] += _wordCount[blog]['words'][key]
	# print blog, _wordCount[blog]['length'], _wordCount[blog]['unique_length'], len(Terms)

if __name__ == "__main__":

	output_file = open('../LMresult', 'w')
	input_file = open('../blogList_test', 'r').read().split('\n')
	if input_file[len(input_file)-1] == '':
		input_file = input_file[:len(input_file)-1]

	SMOOTHING = 0.05
	TREM_LENGTH = 400000
	Terms = []
	wordCount = {}

	for bn in ta.getAllBlogs():
		addBlog(bn, wordCount)
		# wordCount[bn] = {}
		# wordCount[bn]['length'] = 0
		# wordCount[bn]['unique_length'] = 0
		# wordCount[bn]['words'] = {}
		# wordCount[bn]['terms'] = []
		# print "Parsing", bn
		# b = ta.getBlogByName(bn)
		# pid_list = b.getAllPosts()
		# for pid in pid_list:
		# 	p = ta.getPostById(bn, pid)
		# 	terms = va.extractTermsFromPost(p)
		# 	terms += va.extractTermsFromPhoto(p)
		# 	for term in terms:
		# 		if term not in wordCount[bn]['words']:
		# 			wordCount[bn]['words'][term] = 1
		# 		else:
		# 			wordCount[bn]['words'][term] += 1
		# 	wordCount[bn]['terms'] += terms
		# wordCount[bn]['unique_length'] = len(wordCount[bn]['words'].keys())
		# for key in wordCount[bn]['words']:
		# 	# if key not in Terms:
		# 	# 	Terms.append(key)
		# 	wordCount[bn]['length'] += wordCount[bn]['words'][key]
		# # print bn, wordCount[bn]['length'], wordCount[bn]['unique_length'], len(Terms)

	# naive Bayes

	# C_plus_D = float(len(Topic)+len(Label))
	# def topicPriorProbability(topic):
	# 	topicDocs = len(Train[topic])
	# 	return float(1+topicDocs) / C_plus_D
	
	def wordProbability(word, blog):
		wordInTopic = 0
		if word in wordCount[blog]['words']:
			wordInTopic = wordCount[blog]['words'][word]
		blogLength = wordCount[blog]['length']
		#print word, float(0.2+wordInTopic), "/", float(0.2*len(Terms)+blogLength), float(0.2+wordInTopic) / float(0.2*len(Terms)+blogLength)
		# return float(SMOOTHING+wordInTopic) / float(SMOOTHING*len(Terms)+blogLength)
		return float(SMOOTHING+wordInTopic) / float(SMOOTHING*TREM_LENGTH+blogLength)
	
	def countBlogProbability(blog, content):
		# blog_P = log(topicPriorProbability(blog))
		blog_P = 0
		probability_pi = 0
		for word in content:
			probability_pi += log(wordProbability(word, blog))
		return blog_P + probability_pi

	def makeProbabilityDict(testBn):
		blogProbability = {}
		for bn in ta.getAllBlogs():
			blogProbability[bn] = countBlogProbability(bn, wordCount[testBn]['terms'])
		return blogProbability

	def sortDict(blogProbability):
		rankingDict = []
		for key, value in sorted(blogProbability.iteritems(), key=lambda (k,v): (v,k)):
			rankingDict.append((key, value))
		return rankingDict

	def findMax(dictionary):
		maxKey = ''
		maxValue = -float("inf")
		for key in dictionary:
			print key, dictionary[key]
			if dictionary[key] > maxValue:
				maxValue = dictionary[key]
				maxKey = key
		return maxKey

	# LM
	for testBn in input_file:
		print "Evaluate", testBn

		if testBn not in ta.getAllBlogs():
			addBlog(testBn, wordCount)

		# blogProbability = {}
		# for bn in ta.getAllBlogs():
		# 	blogProbability[bn] = countBlogProbability(bn, wordCount[testBn]['terms'])
		# maxTopic = findMax(blogProbability)
		blogProbability = makeProbabilityDict(testBn)

		print "Sorting", testBn
		rankingDict = sortDict(blogProbability)
		# for key, value in sorted(blogProbability.iteritems(), key=lambda (k,v): (v,k)):
		# 	rankingDict.append((key, value))

		output_file.write(str(testBn) + '\n')

		lower_bound = len(rankingDict)-12
		if lower_bound < -1:
			lower_bound = -1

		for i in range(len(rankingDict)-1, lower_bound, -1):
			if rankingDict[i][0] == testBn:
				continue
			else:
				output_file.write(str(rankingDict[i][0]) + ' ' + str(rankingDict[i][1]) + '\n')	
	output_file.close()

	while True:
		blogname_input = raw_input("Blogname Input: ")
		print "Evaluate", blogname_input

		if blogname_input not in ta.getAllBlogs():
			addBlog(blogname_input, wordCount)

		blogProbability = makeProbabilityDict(blogname_input)

		print "Sorting", blogname_input
		rankingDict = sortDict(blogProbability)

		lower_bound = len(rankingDict)-12
		if lower_bound < -1:
			lower_bound = -1

		for i in range(len(rankingDict)-1, lower_bound, -1):
			if rankingDict[i][0] == blogname_input:
				continue
			else:
				print str(rankingDict[i][0]) + ' ' + str(rankingDict[i][1]) + '\n'

		# blogProbability = {}
		# for bn in ta.getAllBlogs():
		# 	blogProbability[bn] = countBlogProbability(bn, wordCount[blogname_input]['terms'])

		# rankingDict = []
		# print "Sorting", blogname_input
		# for key, value in sorted(blogProbability.iteritems(), key=lambda (k,v): (v,k)):
		# 	rankingDict.append((key, value))
		# for i in range(len(rankingDict)-1, len(rankingDict)-12, -1):
		# 	if rankingDict[i][0] == blogname_input:
		# 		continue
		# 	else:
		# 		print str(rankingDict[i][0]) + ' ' + str(rankingDict[i][1]) + '\n'

	sys.exit(0)
