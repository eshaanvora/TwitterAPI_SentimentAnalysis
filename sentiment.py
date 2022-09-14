# Twitter Sentiment Analysis
#
# Generates sentiment scores for two user inputted terms and prints the
# sentiment score that is more positive
#
# Author: Eshaan Vora
# Email: EshaanVora@gmail.com
# Date: March 8, 2022

import twitter
import sys
import codecs

# https://developer.twitter.com/docs/auth/oauth Twitter's OAuth implementation

# Go to http://developer.twitter.com/apps/new to create an app and get values
# for the credentials defined below

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

#To protect author's credentials, part of the credentials are hidden
CONSUMER_KEY = 'SL4QpwX7W0B3Gfs**********'
CONSUMER_SECRET = 'DxGqIfC2gGQuSNO0RbTZtc16RtvUmkD0qZcEAy1U**********'
ACCESS_TOKEN = '1498391448516845571-RjjbxFHD9E2UIIKSNnBq**********'
ACCESS_TOKEN_SECRET = 'XSzP7ZLf6ajaBeNlMNLmHF0Z6esJhNFpjDq**********'


auth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)


term1 = input('Enter a search term: ')
term2 = input('Enter another search term: ')
print("-------------------------------------------")

# Method to generate & print sentiment score given a word
def printSentiment(term1):
    # Define the number of Tweets to query
    count = 1000

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=term1, count=count)
    statuses = search_results['statuses']

    # Iterate through 5 more batches of results by following the cursor
    for _ in range(5):
        # print("Length of statuses", len(statuses))
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError:
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

    # Retrieve text from Tweets
    status_texts = [status['text']
                    for status in statuses]

    # Compute collection of all words from all tweets
    words = [w
             for t in status_texts
             for w in t.split()]

    # Use AFINN-111 lexicon for valence of a word's sentiment
    sent_file = open('AFINN-111.txt')

    scores = {}  # initialize empty dictionary to count scores
    for line in sent_file:
        term, score = line.split("\t")
        # The file is tab-delimited.
        # "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    score = 0
    # Compare words in the Tweets with the AFINN-111 word sentiment
    for word in words:
        if word in scores.keys():
            score = score + scores[word]

    return(float(score))


# Generate sentiment scores
score1 = printSentiment(term1)
score2 = printSentiment(term2)

# Determine which was most positive and print the results
if score1 > score2:
    print("'" + term1 + "' has the more positive sentiment score")
else:
    print("'" + term2 + "' has the more positive sentiment score")

print("Sentiment Analysis on the term '" + term1 + "': " + str(score1))
print("Sentiment Analysis on the term '" + term2 + "': " + str(score2))
