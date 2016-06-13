import sys, os
import pytumblr
import json


# api key
TUMBLR_CONSUMER_KEY = "ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk"
TUMBLR_CONSUMER_SECRET = "PpHRSKUKqBMNp4bjchW8EkxQNcQvyVyDYDWiz7gROzVERsOYAs"

# OAuth
ACCESS_TOKEN = "sVF038jN4AjBN1sUJ9RiqE0PUKnQDcgVBCOvEkiblXwSROiEIO"
ACCESS_SECRET = "NXYoBsNQBW3b6yqNS1VuxKixMoktAADZfPGJ72wIZOSx62P5OO"

if __name__ == "__main__":
	# create client
	client = pytumblr.TumblrRestClient(
		TUMBLR_CONSUMER_KEY,
		TUMBLR_CONSUMER_SECRET,
		ACCESS_TOKEN,
		ACCESS_SECRET
	)
	# get the client information
# client_info = client.info()
# print json.dumps(client_info, indent=4)
# print json.dumps(client.tagged('sex'), indent=4)
	print json.dumps(client.blog_info('marvelentertainment.tumblr.com'), indent=4)


