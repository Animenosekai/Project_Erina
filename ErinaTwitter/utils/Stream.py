"""
Twitter Stream Manager
"""

import tweepy
import config
from ErinaTwitter.utils.Errors import TwitterError
from ErinaTwitter.utils import Twitter
from ErinaTwitter.erina_twitterbot import ErinaTwitter
from ErinaTwitter.utils.Parser import makeTweet
from ErinaSearch.erinasearch import imageSearch
class Listener(tweepy.StreamListener):
        """
        Tweet Listener Class (Twitter Stream Handler)

        Erina Project\n
        © Anime no Sekai - 2020
        """

        def on_connect(self):
            """
            Connection
            """
            print("ErinaTwitter is connected to the Twitter API")

        def on_status(self, tweet):
            """
            Tweet Receiving
            """
            if config.Twitter.ignore_rt and Twitter.isRetweet(tweet):
                return
            
            if isinstance(config.Twitter.monitored_accounts, (list, tuple)) and len(config.Twitter.monitored_accounts) > 0:
                if config.Twitter.monitored_check_replies and Twitter.isReplyingToErina(tweet): # Monitor Mode ON, Check Replies to Monitored ON
                    imageURL = Twitter.findImage(tweet)
                    if imageURL is None:
                        imageURL = Twitter.findParentImage(tweet)
                    if imageURL is not None:
                        searchResult = imageSearch(imageURL)
                        tweetResponse = makeTweet(searchResult)
                        if tweetResponse is not None:
                            ErinaTwitter.tweet(tweetResponse, replyID=tweet.id)
                elif tweet.user.screen_name == ErinaTwitter.me.screen_name: # Monitor Mode ON, Check Replies to Monitored OFF
                    imageURL = Twitter.findImage(tweet)
                    if imageURL is not None:
                        searchResult = imageSearch(imageURL)
                        tweetResponse = makeTweet(searchResult)
                        if tweetResponse is not None:
                            ErinaTwitter.tweet(tweetResponse, replyID=tweet.id)
            else: # Monitor Mode OFF, Public Account
                imageURL = Twitter.findImage(tweet)
                if imageURL is None:
                    imageURL = Twitter.findParentImage(tweet)
                if imageURL is not None and Twitter.isAskingForSauce(tweet):
                    searchResult = imageSearch(imageURL)
                    tweetResponse = makeTweet(searchResult)
                    if tweetResponse is not None:
                        ErinaTwitter.tweet(tweetResponse, replyID=tweet.id)
                    elif Twitter.isMention(tweet):
                        ErinaTwitter.tweet("Sorry, I searched everywhere but coudln't find it...", replyID=tweet.id)
            return


        def on_direct_message(self, message):
            """
            DM Receiving
            """
            pass



        # Error handling
        def on_error(self, status_code):
            """
            Classic Error
            """
            return TwitterError("STREAM_HTTP_ERROR", f"A {str(status_code)} status code got received from Erina's Twitter Stream")

        def on_exception(self, exception):
            """
            Unknown Exception from Tweepy
            """
            return TwitterError("STREAM_EXCEPTION", f"A {str(exception)} error occured while handling Erina's Twitter Stream")

        def on_warning(self, notice):
            """
            Disconnection Warning
            """
            return TwitterError("STREAM_DISCONNECTION_WARNING", f"A disconnection warning came: {str(notice)}")

        def on_limit(self, track):
            """
            Limit Reached
            """
            return TwitterError("STREAM_LIMIT_REACHED", f"A limitation notice came: {str(track)}")

        def on_timeout(self):
            """
            Connection Timeout
            """
            return TwitterError("STREAM_CONNECTION_TIMEOUT", f"Erina's Stream Connection timed out")
        
        def on_disconnect(self, notice):
            """
            Disconnection from Twitter
            """
            return TwitterError("STREAM_DISCONNECTION", f"A disconnection notice came: {str(notice)}")

Erina = tweepy.Stream(auth=ErinaTwitter.api.auth, listener=Listener())
if isinstance(config.twitter_monitored_accounts, list) and len(config.twitter_monitored_accounts) > 0:
    user_ids = [user.id_str for user in ErinaTwitter.api.lookup_users(screen_names=config.twitter_monitored_accounts)]
    Erina.filter(follow=user_ids)
else:
    if not isinstance(config.twitter_stream_track_flags, list) or config.twitter_stream_track_flags == []:
        Erina.filter(languages=config.twitter_stream_languages, track=config.twitter_flags)
    else:
        Erina.filter(languages=config.twitter_stream_languages, track=config.twitter_stream_track_flags)
