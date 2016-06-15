import sys
import pytumblr

client = pytumblr.TumblrRestClient(
    "ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk",
    "PpHRSKUKqBMNp4bjchW8EkxQNcQvyVyDYDWiz7gROzVERsOYAs",
    "sVF038jN4AjBN1sUJ9RiqE0PUKnQDcgVBCOvEkiblXwSROiEIO",
    "NXYoBsNQBW3b6yqNS1VuxKixMoktAADZfPGJ72wIZOSx62P5OO"
)


if __name__ == "__main__":
    b_list = []
    with open(sys.argv[1]) as f:
        for line in f:
            b_list.append(line.strip())
    for bn in b_list:
        res = client.blog_info(bn)
        print bn,
        if u'blog' not in res.keys():
            print "False"
            print "="*50
        else:
            print "True"
