"""
Twitter Stream Manager
"""

import sys
from threading import Thread

from safeIO import TextFile
from ErinaParser.utils.tracemoe_parser import TraceMOECache
from time import sleep, time
import traceback
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
from Erina.env_information import erina_dir

from Erina.erina_stats import StatsAppend
from Erina.erina_stats import twitter as TwitterStats
from Erina.utils import convert_to_int

sinceID = TextFile(erina_dir + "/ErinaTwitter/lastStatusID.erina").read().replace("\n", "")
lastDM = convert_to_int(TextFile(erina_dir + "/ErinaTwitter/lastDM.erina").read().replace("\n", ""))

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

    def on_status(self, tweet, force=False):
        """
        Tweet Receiving
        """
        global sinceID
        StatsAppend(TwitterStats.streamHit)
        if TwitterConfig.ignore_rt and Twitter.isRetweet(tweet):
            return
        try:
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
        except:
            traceback.print_exc()
            
        
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
            if imageURL is not None and Twitter.isAskingForSauce(tweet) or force:
                log("ErinaTwitter", "New asking hit from @" + str(tweet.user.screen_name))
                StatsAppend(TwitterStats.askingHit, str(tweet.user.screen_name))
                searchResult = imageSearch(imageURL)
                tweetResponse = makeTweet(searchResult)
                if tweetResponse is not None:
                    StatsAppend(TwitterStats.responses)
                    responseImageURL = None
                    if isinstance(searchResult.detectionResult, TraceMOECache):
                        if TwitterConfig.image_preview:
                            if not searchResult.detectionResult.hentai:
                                responseImageURL = f"https://trace.moe/thumbnail.php?anilist_id={str(searchResult.detectionResult.anilist_id)}&file={str(searchResult.detectionResult.filename)}&t={str(searchResult.detectionResult.timing.at)}&token={str(searchResult.detectionResult.tokenthumb)}"
                    ErinaTwitter.tweet(tweetResponse, replyID=tweet.id, imageURL=responseImageURL)
                elif Twitter.isMention(tweet):
                    ErinaTwitter.tweet("Sorry, I searched everywhere but coudln't find it...", replyID=tweet.id)
        TextFile(erina_dir + "/ErinaTwitter/lastStatusID.erina").write(str(tweet.id))
        sinceID = tweet.id
        return

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

ErinaStreamListener = Listener()
Erina = tweepy.Stream(auth=ErinaTwitter.api.auth, listener=ErinaStreamListener)
def _startStream():
    """
    Starts the stream
    """
    if isinstance(TwitterConfig.monitoring.accounts, (list, tuple)) and len(TwitterConfig.monitoring.accounts) > 0:
        user_ids = [user.id_str for user in ErinaTwitter.api.lookup_users(screen_names=list(TwitterConfig.monitoring.accounts))]
        Erina.filter(follow=user_ids)
    else:
        if not isinstance(TwitterConfig.stream.flags, (list, tuple)) or len(TwitterConfig.stream.flags) <= 0:
            flags = (list(TwitterConfig.flags) if str(TwitterConfig.flags).replace(" ", "") not in ["None", "", "[]"] else list(ErinaConfig.flags))
            flags.append(ErinaTwitter.me.screen_name)
            flags.append(str(ErinaTwitter.me.screen_name).lower())
            Erina.filter(languages=TwitterConfig.stream.languages, track=flags)
        else:
            Erina.filter(languages=TwitterConfig.stream.languages, track=list(TwitterConfig.stream.flags))

directMessagesHistory = []
def on_direct_message(message):
    """
    DM Receiving
    """
    directMessagesHistory.append(message)
    log("ErinaTwitter", "New direct message from @" + str(message.message_create['sender_id']))
    if Twitter.dmAskingForSauce(message):
        StatsAppend(TwitterStats.directMessagingHit, str(message.message_create['sender_id']))
        image = Twitter.getDirectMedia(message)
        if image is not None:
            searchResult = imageSearch(image)
            ErinaTwitter.dm(makeImageResponse(searchResult), message.message_create['sender_id'])
        elif isAnError(image):
            ErinaTwitter.dm("An error occured while retrieving information on the anime", message.message_create['sender_id'])
        else:
            ErinaTwitter.dm("You did not send any image along with your message", message.message_create['sender_id'])


def startStream():
    global sinceID
    global lastDM
    Thread(target=_startStream, daemon=True).start()
    while True:
        if TwitterConfig.check_mentions:
            try:
                if sinceID is not None and sinceID != "":
                    for message in tweepy.Cursor(ErinaTwitter.api.mentions_timeline, since_id=sinceID, count=200, include_entities=True).items():
                        try:
                            ErinaStreamListener.on_status(message)
                        except:
                            log("ErinaTwitter", f"Error while reading a mention {str(sys.exc_info()[0])}: {str(sys.exc_info()[1])}", True)
                else:
                    for message in tweepy.Cursor(ErinaTwitter.api.mentions_timeline, count=200, include_entities=True).items():
                        try:
                            ErinaStreamListener.on_status(message)
                        except:
                            log("ErinaTwitter", f"Error while reading a mention {str(sys.exc_info()[0])}", True)
            except:
                log("ErinaTwitter", f"Error while reading mentions {str(sys.exc_info()[0])}", True)
                if str(sys.exc_info()[0]).replace(" ", "").lower() == "<class'tweepy.error.ratelimiterror'>":
                    sleep(3600)
        
        if TwitterConfig.check_dm:
            try:
                for message in tweepy.Cursor(ErinaTwitter.api.list_direct_messages, count=50).items():
                    try:
                        timestamp = convert_to_int(message.created_timestamp)
                        if message not in directMessagesHistory and timestamp > lastDM:
                            on_direct_message(message)
                            lastDM = timestamp
                    except:
                        log("ErinaTwitter", f"Error while reading a DM {str(sys.exc_info()[0])}", True)
            except:
                log("ErinaTwitter", f"Error while reading DMs {str(sys.exc_info()[0])}", True)
                if str(sys.exc_info()[0]).replace(" ", "").lower() == "<class'tweepy.error.ratelimiterror'>":
                    sleep(3600)
        sleep(60)
    

def endStream():
    """
    Ends the stream
    """
    Erina.running = False