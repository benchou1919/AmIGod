from tumblrUtil import TumblrAgent as TA
from vocabUtil import VocabAgent as VA
from collections import defaultdict
import math

BlogFre = defaultdict(float)
db = 0.75
dk = 2.5

class BlogVSM(object):
	
	def __init__(self, blog_name):
		self.blog_name = blog_name
		self.blog_length = 0
		self.relativity = 0
		self.vector = defaultdict(float)

	def getBlogName(self):
		return self.blog_name

	def getBlogVector():
		pass

	def queryByBlogName():
		pass

if __name__ == "__main__":
	global BlogFre, db, dk
	totallength = 0
	blog_num = 0

	ta = TA()
	Blogs = []

	# go through all blog's post
	for bn in ta.getAllBlogs():

		Blogs.append(BlogVSM(bn))

		b = ta.getBlogByName(bn)
		pid_list = b.getAllPosts()
		
		for pid in pid_list:
			
			p = ta.getPostById(bn, pid)

			terms = VA.extractTermsFromPost(p)

			for term in terms:
				Blogs[index].vector[term] += 1
				Blogs[index].blog_length += 1
				BlogFre[term] += 1
				totallength += 1

		blog_num += 1

	# trans blog's vector weight RawTF into NormTF*IDF
	avglength = totallength/blog_num
	
	for bs in Blogs:
		for key,value in bs.vector.iteritems():
			bs.vector[key] = (dk+1)*value / (value+dk*(1-db+db*bs.blog_length/avglength)) * math.log(blog_num/BlogFre[key])

	while userinput!="EXIT":
		userinput = raw_input("")
		b = ta.getBlogByName(userinput)
		Query = BlogVSM(userinput)

		pid_list = b.getAllPosts()
		
		for pid in pid_list:
			
			p = ta.getPostById(user, pid)

			terms = VA.extractTermsFromPost(p)

			for term in terms:
				Query.vector[term] += 1
				Query.blog_length += 1

		for key,value in Query.vector.iteritems():
			Query.vector[key] = (dk+1)*value / (value+dk*(1-db+db*Query.blog_length/avglength))

		for bs in Blogs:
			temprel = 0
			d_v_l = 0

			for key,value in bs.vector.iteritems():
				temprel += value * Query.vector[key]
				d_v_l += value

			bs.relativity = temprel/d_v_l

		Blogs.sort(key=lambda x: x.relativity,reverse=True)

		for i in range(10):
			print "%d %s" %(i+1, Blogs[i].getBlogName())








