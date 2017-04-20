# Twitter Sentiment Endpoint
This 21 endpoint is based on the article ['Twitter Sentiment Analysis using Python'](http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/) and can currently be viewed on the [21 marketplace](https://21.co/mkt/).
## Installation:
### Clone repository
```
git clone https://github.com/PhillRob/twitter-sentiment-21.git
cd twitter-sentiment-21
```

### Install dependencies
#### Tweepy
Tweepy is the python client for the official Twitter API.
Install it using following pip command:
`pip install tweepy`

#### TextBlob
Textblob is the python library for processing textual data.
Install it using following pip command: ```pip install textblob```

### Plugin your twitter OAuth credentials
Authentication:
To fetch twitter data through the API, a couple of steps are required. 
 * Go to [https://apps.twitter.com/](https://apps.twitter.com/) to set up a App based on your twitter account
 * Click ‘Create New App’
* Fill the details. The callback url field is not required.
* Go to the ‘Keys and Access Tokens’ tab.
* Copy ‘Consumer Key’, ‘Consumer Secret’, ‘Access token’ and ‘Access Token Secret’ and place it in the header of `sentiment-server.py`