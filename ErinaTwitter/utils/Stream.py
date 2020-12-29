"""
Twitter Stream Manager
"""

from time import time
from Erina.erina_log import log
import tweepy
from pattern.text.en import sentiment

from Erina.config import Twitter as TwitterConfig
from Erina.config import Erina as ErinaConfig
from Erina.Errors import TwitterError, isAnError
from ErinaTwitter.utils import Twitter
from ErinaTwitter.erina_twitterbot import ErinaTwitter, latestResponses
from ErinaTwitter.utils.Parser import makeTweet, makeImageResponse
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
            log("ErinaTwitter", "ErinaTwitter is connected to the Twitter API")

        def on_status(self, tweet):
            """
            Tweet Receiving
            """
            StatsAppend(TwitterStats.streamHit)
            if TwitterConfig.ignore_rt and Twitter.isRetweet(tweet):
                return

            if Twitter.isReplyingToErina(tweet): # If replying, analyze if it is a positive or a negative feedback
                responseSentiment = sentiment(tweet.text)[0]
                StatsAppend(TwitterStats.responsePolarity, responseSentiment)
                latestResponses.append({
                    "timestamp": time(),
                    "user": tweet.user.screen_name,
                    "text": tweet.text,
                    "sentiment": responseSentiment,
                    "url": "https://twitter.com/twitter/statuses/" + str(tweet.id),
                })
                
            
            if isinstance(TwitterConfig.monitoring.accounts, (list, tuple)) and len(TwitterConfig.monitoring.accounts) > 0:
                if TwitterConfig.monitoring.check_replies and Twitter.isReplyingToErina(tweet): # Monitor Mode ON, Check Replies to Monitored ON
                    log("ErinaTwitter", "New monitoring hit from @" + str(tweet.user.screen_name))
                    StatsAppend(TwitterStats.askingHit, str(tweet.user.screen_name))
                    imageURL = Twitter.findImage(tweet)
                    if imageURL is None:
                        imageURL = Twitter.findParentImage(tweet)
                    if imageURL is not None:
                        searchResult = imageSearch(imageURL)
                        tweetResponse = makeTweet(searchResult)
                        if tweetResponse is not None:
                            StatsAppend(TwitterStats.responses)
                            ErinaTwitter.tweet(tweetResponse, replyID=tweet.id)
                elif tweet.user.screen_name in TwitterConfig.monitoring.accounts: # Monitor Mode ON, Check Replies to Monitored OFF
                    log("ErinaTwitter", "New monitoring hit")
                    StatsAppend(TwitterStats.askingHitstr(tweet.user.screen_name))
                    imageURL = Twitter.findImage(tweet)
                    if imageURL is not None:
                        searchResult = imageSearch(imageURL)
                        tweetResponse = makeTweet(searchResult)
                        if tweetResponse is not None:
                            StatsAppend(TwitterStats.responses)
                            ErinaTwitter.tweet(tweetResponse, replyID=tweet.id)
            
            
            
            else: # Monitor Mode OFF, Public Account
                imageURL = Twitter.findImage(tweet)
                if imageURL is None:
                    imageURL = Twitter.findParentImage(tweet)
                if imageURL is not None and Twitter.isAskingForSauce(tweet):
                    log("ErinaTwitter", "New asking hit from @" + str(tweet.user.screen_name))
                    StatsAppend(TwitterStats.askingHit, str(tweet.user.screen_name))
                    searchResult = imageSearch(imageURL)
                    tweetResponse = makeTweet(searchResult)
                    if tweetResponse is not None:
                        StatsAppend(TwitterStats.responses)
                        ErinaTwitter.tweet(tweetResponse, replyID=tweet.id)
                    elif Twitter.isMention(tweet):
                        ErinaTwitter.tweet("Sorry, I searched everywhere but coudln't find it...", replyID=tweet.id)
            return


        def on_direct_message(self, message):
            """
            DM Receiving
            """
            log("ErinaTwitter", "New direct message from @" + str(message.user.screen_name))
            if Twitter.dmAskingForSauce(message):
                StatsAppend(TwitterStats.directMessagingHit, str(message.user.screen_name))
                image = Twitter.getDirectMedia(message)
                if image is not None:
                    searchResult = imageSearch(image)
                    ErinaTwitter.dm(makeImageResponse(searchResult), message.sender_id)
                elif isAnError(image):
                    ErinaTwitter.dm("An error occured while retrieving information on the anime", message.sender_id)
                else:
                    ErinaTwitter.dm("You did not send any image along with your message", message.sender_id)



        # Error handling
        def on_error(self, status_code):
            """
            Classic Error
            """
            log("ErinaDebug", "Access Token Key: " + str(TwitterConfig.keys.access_token_key))
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