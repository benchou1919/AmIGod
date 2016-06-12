import sys, os
import pytumblr
import json


# api key
TUMBLR_CONSUMER_KEY = "ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk"
TUMBLR_CONSUMER_SECRET = "PpHRSKUKqBMNp4bjchW8EkxQNcQvyVyDYDWiz7gROzVERsOYAs"

# OAuth
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
	# get the client information
	client_info = client.info()
	print json.dumps(client_info, indent=4)
