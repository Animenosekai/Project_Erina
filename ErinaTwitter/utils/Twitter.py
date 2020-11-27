from ErinaTwitter.erina_twitterbot import ErinaTwitter


def findImage(tweet):
    """
    Searches for an image in the tweet
    """
    for media in tweet.entities.get("media", [{}]):
        if media.get("type", None) == "photo":
            return media['media_url']
    return None

def isRetweet(tweet):
    """
    Checks if the given tweet is an RT
    """
    if hasattr(tweet, 'retweeted_status') or tweet.text[:4] == 'RT @':
        return True
    else:
        return False

def isAskingForSauce(tweet):
    """
    Checks if the given tweet is really asking for the sauce
    """
    if tweet.in_reply_to_status_id is not None:
        if ErinaTwitter.api.get_status(tweet.in_reply_to_status_id).user.screen_name == ErinaTwitter._screen_name:
            return False
    if tweet.user.screen_name == ErinaTwitter._screen_name:
        return False

    cleanText = tweet.text.replace(" ", '').lower()
    if '@' + ErinaTwitter._screen_name in cleanText:
        return True
    elif any([flag in cleanText for flag in ErinaTwitter._twitter_flags]):
        return True
    return False

def isMention(tweet):
    """
    Checks if the given tweet is mentionning me
    """
    cleanText = tweet.text.replace(" ", '').lower()
    if '@' + ErinaTwitter._screen_name in cleanText:
        return True
    else:
        return False

def isReplyingToErina(tweet):
    """
    Checks if the given tweet is replying to Erina
    """
    if isReply(tweet):
        if ErinaTwitter.api.get_status(tweet.in_reply_to_status_id).user.screen_name == ErinaTwitter._screen_name:
            return True
    return False

def isReply(tweet):
    """
    Checks if the given tweet is a reply
    """
    if tweet.in_reply_to_status_id is not None:
        return True
    return False

def parentTweet(tweet):
    """
    Returns the parent tweet
    """
    if isReply(tweet):
        return ErinaTwitter.api.get_status(tweet.in_reply_to_status_id)
    return False