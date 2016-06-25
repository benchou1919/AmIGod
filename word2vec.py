from tumblrUtil import TumblrAgent as TA 
from vocabUtil import VocabAgent as VA
import sys
import numpy as np
import math

def loadModel(number):
    model = {}
    f = open('GN-300-neg.txt','r')
    tmp = f.readline()
    tmp = f.readline()
    ### Take only the first @number of words ###
    for i in range(number):
        line = f.readline()
        tmp = line.split()
        vec = []
        if i % 10000 == 0:
            print >> sys.stderr, i, tmp[0]
        for j in range(1, 301):
            vec.append(float(tmp[j]))
        model[tmp[0]] = np.array(vec)

    return model

def cosineDistance(v1, v2):
    eucV1 = math.sqrt(sum(x**2 for x in v1))
    eucV2 = math.sqrt(sum(x**2 for x in v2))
    if eucV1 == 0 or eucV2 == 0:
        return float('-inf')
    return np.dot(v1, v2) / (eucV1 * eucV2) 


def loadVecs(names):
    vecs = []
    f = open('w2v_for_blogs.txt','r')
    for i, line in enumerate(f):
        v = line.strip().split()
        v = [float(x) for x in v]
        vecs.append((names[i], v))
    return vecs
    

if __name__ == '__main__':
    ta = TA()
    print >> sys.stderr, 'Done loading TumblrAgent' 
    model = loadModel(30000)
    print >> sys.stderr, 'Done loading word2vec model'
    blognames = ta.getAllBlogs()
    # blogs = []
    w = open('w2v_for_blogs.txt', 'w')
    w2v = []
    vecs = []
    for name in blognames:
        blog = ta.getBlogByName(name)
        postIds = blog.getAllPosts()
        count = 0
        v = np.zeros(300)
        
        for postId in postIds:
            post = ta.getPostById(blog.getName(), postId)
            tags = post.getTags()
            ### tags ###
            for tag in tags:
                if tag in model:
                    count += 1
                    v += model[tag]
            ### other terms ###
            otherTerms = VA.extractTermsFromPost(post)
            for term in otherTerms:
                if term in model:
                    count += 1
                    v += model[term]

        vecs.append((name, v))
        for element in v:
            w.write(str(element) + " ")
        w.write("\n")
        print count

    topK = 10
    while True:
        queryName = raw_input()
        if queryName == "EXIT":
            break
        blog = ta.getBlogByName(queryName)
        postIds = blog.getAllPosts()
        v = np.zeros(300)
        for Id in postIds:
            post = ta.getPostById(blog.getName(), Id)
            for tag in post.getTags():
                if tag in model:
                    v += model[tag]
        # Now I have the vector
        dists = []
        for bv in vecs:
            tmp = cosineDistance(bv[1], v)
            dists.append((bv[0], tmp))
        dists.sort(key=lambda tup: tup[1], reverse=True)
        for i in range(topK):
            print dists[i][0], dists[i][1]








