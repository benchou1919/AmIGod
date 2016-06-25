import os, sys
import json, re, unidecode

class VocabAgent(object):

	@staticmethod
	def stripHTML(src_str):
		if not src_str:
			return ""
		pattern = re.compile(r'<.*?>')
		return pattern.sub('', src_str)

	@staticmethod
	def sanitize(src_str):
		ret = unidecode.unidecode(src_str)
		ret = re.sub(r'[^a-zA-Z0-9 _]','', ret) # to remove symbols
		ret = ret.lower()
		return ret

	@staticmethod
	def extractTermsFromPost(tumblrPost):
		terms = []

		# add tags into terms
		for tag in tumblrPost.getTags():
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tag)).split()
		
		# add information according to the type of the post
		if tumblrPost.getType() == 'text':
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.title)).split()
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.body)).split()
		elif tumblrPost.getType() == 'photo':
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.caption)).split()
			for photo in tumblrPost.photos:
				terms += VocabAgent.sanitize(VocabAgent.stripHTML(photo['caption'])).split()
		elif tumblrPost.getType() == 'quote':
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.text)).split()
		elif tumblrPost.getType() == 'link':
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.title)).split()
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.description)).split()
			if tumblrPost.photos:
				for photo in tumblrPost.photos:
					terms += VocabAgent.sanitize(VocabAgent.stripHTML(photo['caption'])).split()
		elif tumblrPost.getType() == 'chat':
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.title)).split()
			if tumblrPost.dialogue:
				for d in tumblrPost.dialogue:
					terms += VocabAgent.sanitize(VocabAgent.stripHTML(d['phrase'])).split()
		elif tumblrPost.getType() == 'audio':
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.caption)).split()
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.artist)).split()
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.album)).split()
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.track_name)).split()
		elif tumblrPost.getType() == 'video':
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.caption)).split()
		elif tumblrPost.getType() == 'answer':
			if tumblrPost.asking_name != "Anonymous":
				terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.asking_name)).split()
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.question)).split()
			terms += VocabAgent.sanitize(VocabAgent.stripHTML(tumblrPost.answer)).split()
		# return the list
		return terms

	def __init__(self):
		pass

	def load(self, path):
		pass
