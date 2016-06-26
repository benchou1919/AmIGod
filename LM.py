import sys, os
import pytumblr
import json
from math import log
from tumblrUtil import TumblrAgent as TA
from vocabUtil import VocabAgent as VA
from imageUtil import parser, OCR

def legalImageType(url):
	path = url.split('.')
	iType = path[len(path)-1]
	if iType == 'jpg' or iType == 'png':
		return True;
	return False;

if __name__ == "__main__":

	output_file = open('../LMresult', 'w')
	input_file = open('../blogList', 'r').read().split('\n')
	if input_file[len(input_file)-1] == '':
		input_file = input_file[:len(input_file)-1]

	SMOOTHING = 0.2
	Terms = []
	wordCount = {}

	# use TumblrAgent
	ta = TA()
	blogNames = ta.getAllBlogs()
	for bn in blogNames:
		wordCount[bn] = {}
		wordCount[bn]['length'] = 0
		wordCount[bn]['unique_length'] = 0
		wordCount[bn]['words'] = {}
		print "Parsing", bn
		b = ta.getBlogByName(bn)
		pid_list = b.getAllPosts()
		for pid in pid_list:
			p = ta.getPostById(bn, pid)
			terms = VA.extractTermsFromPost(p)
			# if p.getType() == 'photo':
			# 	ocrData = []
			# 	parserData = []
			# 	for photo in p.photos:
			# 		photoUrl = photo['original_size']['url']
			# 		if legalImageType(photoUrl):
			# 			ocrData += OCR(photoUrl)
			# 			parserData += parser(photoUrl)
			# 	terms += ocrData
			# 	terms += parserData
			# print bn, pid, terms
			for term in terms:
				if term not in wordCount[bn]['words']:
					wordCount[bn]['words'][term] = 1
				else:
					wordCount[bn]['words'][term] += 1
		wordCount[bn]['unique_length'] = len(wordCount[bn]['words'].keys())
		for key in wordCount[bn]['words']:
			if key not in Terms:
				Terms.append(key)
			wordCount[bn]['length'] += wordCount[bn]['words'][key]
		print bn, wordCount[bn]['length'], wordCount[bn]['unique_length'], len(Terms)

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
		return float(SMOOTHING+wordInTopic) / float(SMOOTHING*len(Terms)+blogLength)
	
	def countBlogProbability(blog, content):
		# blog_P = log(topicPriorProbability(blog))
		blog_P = 0
		probability_pi = 0
		for word in content:
			probability_pi += log(wordProbability(word, blog))
		return blog_P + probability_pi

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
		b = ta.getBlogByName(testBn)
		# continue
		pid_list = b.getAllPosts()
		terms = []
		for pid in pid_list:
			p = ta.getPostById(testBn, pid)
			terms += VA.extractTermsFromPost(p)
		blogProbability = {}
		for bn in blogNames:
			blogProbability[bn] = countBlogProbability(bn, terms)
		# maxTopic = findMax(blogProbability)
		rankingDict = []
		print "Sorting", testBn
		for key, value in sorted(blogProbability.iteritems(), key=lambda (k,v): (v,k)):
			rankingDict.append((key, value))
		output_file.write(str(testBn) + '\n')
		for i in range(len(rankingDict)-1, len(rankingDict)-7, -1):
			if rankingDict[i][0] == testBn:
				continue
			else:
				output_file.write(str(rankingDict[i][0]) + ' ' + str(rankingDict[i][1]) + '\n')
		
	output_file.close()
	sys.exit(0)
