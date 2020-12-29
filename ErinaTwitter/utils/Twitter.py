from io import BytesIO
from ErinaTwitter.erina_twitterbot import ErinaTwitter
import requests
from PIL import Image
from Erina.Errors import TwitterError
from Erina.config import Twitter as TwitterConfig
from Erina.config import Erina as ErinaConfig

def findImage(tweet):
    """
    Searches for an image in the tweet
    """
    print("ErinaDebug — Twitter.py line 13: " + str(tweet.entities.get("media", [])))
    for media in tweet.entities.get("media", []):
        print("ErinaDebug — Twitter.py line 15: " + str(media))
        print("ErinaDebug — Twitter.py line 16: " + str(media.get("type", "None")))
        if media.get("type", None) == "photo":
            return media['media_url']
    return None

def findParentImage(tweet):
    """
    Searches for an image in the parent tweet (if reply)
    """
    parent = parentTweet(tweet)
    if parent is not None:
        return findImage(parent)
    return None

def isRetweet(tweet):
    """
    Checks if the given tweet is an RT
    """
    if hasattr(tweet, 'retweeted_status') or tweet.text[:4] == 'RT @':
        return True
    return False

def isAskingForSauce(tweet):
    """
    Checks if the given tweet is really asking for the sauce
    """
    accountsChain = []
    currentStatus = tweet
    while currentStatus is not None:
        print("ErinaDebug — Twitter.py line 45: " + str(currentStatus))
        accountsChain.append(currentStatus.user.id)
        currentStatus = parentTweet(currentStatus)
    print("ErinaDebug — Twitter.py line 48: " + str(accountsChain))
    if ErinaTwitter.me.id in accountsChain:
        return False
    if tweet.user.id == ErinaTwitter.me.id:
        return False

    cleanText = tweet.text.replace(" ", '').lower()
    if ErinaTwitter._screen_name in cleanText:
        return True
    elif any([flag in cleanText for flag in ([str(word).lower().replace(" ", "") for word in list(TwitterConfig.flags)] if str(TwitterConfig.flags).replace(" ", "") not in ["None", "", "[]"] else [str(word).lower().replace(" ", "") for word in list(ErinaConfig.flags)])]):
        return True
    return False

def isMention(tweet):
    """
    Checks if the given tweet is mentionning me
    """
    cleanText = tweet.text.replace(" ", '').lower()
    if '@' + ErinaTwitter._screen_name in cleanText:
        return True
    elif "user_mentions" in tweet._json and any([currentMention["id"] == ErinaTwitter.me.id for currentMention in tweet._json["user_mentions"]]):
        return True
    return False

def isReplyingToErina(tweet):
    """
    Checks if the given tweet is replying to Erina
    """
    if isReply(tweet):
        if ErinaTwitter.api.get_status(tweet.in_reply_to_status_id).user.id == ErinaTwitter.me.id:
            return True
    return False

def isReply(tweet):
    """
    Checks if the given tweet is a reply
    """
    if tweet is None:
        return False
    if tweet.in_reply_to_status_id is not None:
        return True
    return False

def parentTweet(tweet):
    """
    Returns the parent tweet
    """
    try:
        if isReply(tweet):
            return ErinaTwitter.api.get_status(tweet.in_reply_to_status_id)
        return None
    except:
        return None

def dmAskingForSauce(dm):
    """
    Checks if the given direct message is asking for the sauce
    """
    cleanText = dm.text.replace(" ", '').lower()
    if any([flag in cleanText for flag in ([str(word).lower().replace(" ", "") for word in list(TwitterConfig.flags)] if str(TwitterConfig.flags).replace(" ", "") not in ["None", "", "[]"] else [str(word).lower().replace(" ", "") for word in list(ErinaConfig.flags)])]):
        return True

def getDirectMedia(dm):
    """
    Returns the media associated with a direct message if existing
    """
    if "message_data" in dm.message_create and "attachment" in dm.message_create["message_data"]:
        attachment = dm.message_create["message_data"]["attachment"]
        if dict(attachment) != {} and "media" in attachment:
            if "media_url_https" in attachment["media"]:
                mediaURL = attachment["media"]["media_url_https"]
            elif "media_url" in attachment["media"]:
                mediaURL = attachment["media"]["media_url"]
            else:
                return None
            mediaRequest = requests.get(mediaURL, auth=ErinaTwitter.authentification.apply_auth())
            if mediaRequest.status_code == 200:
                return Image.open(BytesIO(mediaRequest.content))
            else:
                return TwitterError(f"Not able to get DM media: Status Code {mediaRequest.status_code}")
        else:
            return None
    return None