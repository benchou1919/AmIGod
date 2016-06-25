# tmp = raw_input()
from tumblrUtil import TumblrAgent as TA


def loadVecs(names):
    model = []
    f = open('w2v_for_blogs.txt','r')
    for i, line in enumerate(f):
        v = line.split().strip()
        v = [float(x) for x in v]
        model.append((names[i], v))
    return model

ta = TA()
model = loadVecs(ta.getAllBlogs())

while True:
    queryName = raw_input()
    blog = ta.getBlogByName(queryName)

