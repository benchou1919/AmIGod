from tumblrUtil import TumblrAgent as TA 
import sys
import numpy as np

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


if __name__ == '__main__':
    ta = TA()
    print >> sys.stderr, 'Done loading TumblrAgent' 
    model = loadModel(300000)
    print >> sys.stderr, 'Done loading word2vec model'
    blognames = ta.getAllBlogs()
    # blogs = []
    w = open('w2v_for_blogs.txt', 'w')
    w2v = []
    for name in blognames:
        #blogs.append(ta.getBlogByName(name))
        blog = ta.getBlogByName(name)
        postIds = blog.getAllPosts()
        count = 0
        v = np.zeros(300)
        
        for postId in postIds:
            post = ta.getPostById(blog.getName(), postId)
            tags = post.getTags()
            for tag in tags:
                if tag in model:
                    count += 1
                    v += model[tag]
        for element in v:
            w.write(str(element) + " ")
        w.write("\n")
            # count += len(post.getTags())
        print count
