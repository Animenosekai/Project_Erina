"""
Twitter Stream Manager
"""

from Erina.erina_log import log
import tweepy
from pattern.text.en import sentiment

from Erina.config import Twitter as TwitterConfig
from Erina.config import Erina as ErinaConfig
from ErinaTwitter.utils.Errors import TwitterError
from ErinaTwitter.utils import Twitter
from ErinaTwitter.erina_twitterbot import ErinaTwitter
from ErinaTwitter.utils.Parser import makeTweet
from ErinaSearch.erinasearch import imageSearch

from Erina.erina_stats import StatsAppend
from Erina.erina_stats import twitter as TwitterStats


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
            StatsAppend(TwitterStats.streamHit, "New Hit")
            if TwitterConfig.ignore_rt and Twitter.isRetweet(tweet):
                return

            if Twitter.isReplyingToErina(tweet): # If replying, analyze if it is a positive or a negative feedback
                StatsAppend(TwitterStats.responsePolarity, sentiment(tweet.text)[0])
                
            
            if isinstance(TwitterConfig.monitoring.accounts, (list, tuple)) and len(TwitterConfig.monitoring.accounts) > 0:
                if TwitterConfig.monitoring.check_replies and Twitter.isReplyingToErina(tweet): # Monitor Mode ON, Check Replies to Monitored ON
                    log("ErinaTwitter", "New monitoring hit from @" + str(tweet.user.screen_name))
                    StatsAppend(TwitterStats.askingHit, f"From {str(tweet.user.screen_name)}")
                    imageURL = Twitter.findImage(tweet)
                    if imageURL is None:
                        imageURL = Twitter.findParentImage(tweet)
                    if imageURL is not None:
                        searchResult = imageSearch(imageURL)
                        tweetResponse = makeTweet(searchResult)
                        if tweetResponse is not None:
                            StatsAppend(TwitterStats.responses, "New Response")
                            ErinaTwitter.tweet(tweetResponse, replyID=tweet.id)
                elif tweet.user.screen_name in TwitterConfig.monitoring.accounts: # Monitor Mode ON, Check Replies to Monitored OFF
                    log("ErinaTwitter", "New monitoring hit")
                    StatsAppend(TwitterStats.askingHit, f"From {str(tweet.user.screen_name)}")
                    imageURL = Twitter.findImage(tweet)
                    if imageURL is not None:
                        searchResult = imageSearch(imageURL)
                        tweetResponse = makeTweet(searchResult)
                        if tweetResponse is not None:
                            StatsAppend(TwitterStats.responses, "New Response")
                            ErinaTwitter.tweet(tweetResponse, replyID=tweet.id)
            
            
            
            else: # Monitor Mode OFF, Public Account
                imageURL = Twitter.findImage(tweet)
                if imageURL is None:
                    imageURL = Twitter.findParentImage(tweet)
                if imageURL is not None and Twitter.isAskingForSauce(tweet):
                    log("ErinaTwitter", "New asking hit from @" + str(tweet.user.screen_name))
                    StatsAppend(TwitterStats.askingHit, f"From {str(tweet.user.screen_name)}")
                    searchResult = imageSearch(imageURL)
                    tweetResponse = makeTweet(searchResult)
                    if tweetResponse is not None:
                        StatsAppend(TwitterStats.responses, "New Response")
                        ErinaTwitter.tweet(tweetResponse, replyID=tweet.id)
                    elif Twitter.isMention(tweet):
                        ErinaTwitter.tweet("Sorry, I searched everywhere but coudln't find it...", replyID=tweet.id)
            return


        def on_direct_message(self, message):
            """
            DM Receiving
            """
            log("ErinaTwitter", "New direct message from @" + str(message.user.screen_name))
            StatsAppend(TwitterStats.directMessagingHit, f"From {str(message.user.screen_name)}")



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
def startStream():
    """
    Starts the stream
    """
    if isinstance(TwitterConfig.monitoring.accounts, (list, tuple)) and len(TwitterConfig.monitoring.accounts) > 0:
        user_ids = [user.id_str for user in ErinaTwitter.api.lookup_users(screen_names=list(TwitterConfig.monitoring.accounts))]
        Erina.filter(follow=user_ids)
    else:
        if not isinstance(TwitterConfig.stream.flags, (list, tuple)) or len(TwitterConfig.stream.flags) <= 0:
            Erina.filter(languages=TwitterConfig.stream.languages, track=(list(TwitterConfig.flags) if str(TwitterConfig.flags).replace(" ", "") not in ["None", ""] else list(ErinaConfig.flags)))
        else:
            Erina.filter(languages=TwitterConfig.stream.languages, track=list(TwitterConfig.stream.flags))

def endStream():
    """
    Ends the stream
    """
    Erina.running = False