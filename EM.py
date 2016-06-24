import sys, os
import pytumblr
import json
from tumblrUtil import TumblrAgent as TA

# api key
TUMBLR_CONSUMER_KEY = "ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk"
TUMBLR_CONSUMER_SECRET = "PpHRSKUKqBMNp4bjchW8EkxQNcQvyVyDYDWiz7gROzVERsOYAs"

# OAuth
# ACCESS_TOKEN = 'sSG3qISDXvahdO3qr8LbWy5SXXg3Ts0BBNRHCHDaksN9MSlbsy',
# ACCESS_SECRET = 'VCOF3mVfSQ7dHufNw3nCi5kW10bu5BrhGfgu8hlVU0Prvekr0R'
ACCESS_TOKEN = "v5e5U3tEOgZL37TGNbuhlUF3nMzaQV2zCVumRfd7wjkyN7ht4x"
ACCESS_SECRET = "FvHzFRwhZQLumDnrjXhvsiEDZ0mPSbbDtoFG15kX1x70MaFw8V"

if __name__ == "__main__":
	# create client
	client = pytumblr.TumblrRestClient(
		TUMBLR_CONSUMER_KEY,
		TUMBLR_CONSUMER_SECRET,
		ACCESS_TOKEN,
		ACCESS_SECRET
	)

	# use TumblrAgent
	ta = TA()
	b_list = ta.getAllBlogs()
	for blog in b_list:
		p_list = ta.getBlogByName(blog).getAllPosts()
		for post in p_list:
			p = ta.getPostById(blog, post)
			print '{} {}'.format(post, p.getType())

	sys.exit(0)
