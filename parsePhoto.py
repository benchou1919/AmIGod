import sys, os
import pytumblr
import json
from tumblrUtil import TumblrAgent as TA
# from vocabUtil import VocabAgent as VA
from imageUtil import parser, OCR

def legalImageType(url):
	path = url.split('.')
	iType = path[len(path)-1]
	if iType == 'jpg' or iType == 'png':
		return True;
	return False;

if __name__ == "__main__":

	output_file = open('photoText', 'a')

	# use TumblrAgent
	ta = TA()
	for bn in ta.getAllBlogs():
		if bn == 'ayee-erbear' or bn == 'afinefashionfrenzy' or bn == 'hipsterizeddolls' or bn == 'sexy-animegirls':
			continue
		b = ta.getBlogByName(bn)
		pid_list = b.getAllPosts()
		for pid in pid_list:
			p = ta.getPostById(bn, pid)
			if p.getType() == 'photo':
				if bn == 'stfuconservatives' and int(pid) > 57718974777:
					continue
				output_file.write('b=' + str(bn) + '\n')
				output_file.write('p=' + str(pid) + '\n')
				ocrData = []
				parserData = []
				for photo in p.photos:
					photoUrl = photo['original_size']['url']
					if legalImageType(photoUrl):
						ocrData += OCR(photoUrl)
						parserData += parser(photoUrl)
				print bn, pid
				print str(ocrData)
				print str(parserData)
				print '\n'
				output_file.write('OCR=' + str(ocrData) + '\n')
				output_file.write('caffe=' + str(parserData) + '\n')
			# print p.blog_name, p.id, p.getType()

	output_file.close()
	sys.exit(0)
