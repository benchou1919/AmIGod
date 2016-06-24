import sys, os
import pytumblr
import json
from tumblrUtil import TumblrAgent as TA
from imageUtil import parser

if __name__ == "__main__":

	# use TumblrAgent
	ta = TA()
	for bn in ta.getAllBlogs():
		b = ta.getBlogByName(bn)
		pid_list = b.getAllPosts()
		for pid in pid_list:
			p = ta.getPostById(bn, pid)
			if p.getType() == 'photo':
				for photo in p.photos:
					print photo['original_size']['url']
			# print p.blog_name, p.id, p.getType()

	sys.exit(0)
