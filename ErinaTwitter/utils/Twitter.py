from ErinaTwitter.erina_twitterbot import ErinaTwitter

def findImage(tweet):
    """
    Searches for an image in the tweet
    """
    for media in tweet.entities.get("media", [{}]):
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
    currentStatus = "ErinaSauceRecursiveTweetSearching"
    while currentStatus is not None:
        accountsChain.append(currentStatus.user.id)
        currentStatus = parentTweet(currentStatus)
    if ErinaTwitter.me.id in accountsChain:
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
    elif "user_mentions" in tweet._json and any([currentMention["screen_name"].replace("", "").lower() == ErinaTwitter._screen_name for currentMention in tweet._json["user_mentions"]]):
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
    if isReply(tweet):
        return ErinaTwitter.api.get_status(tweet.in_reply_to_status_id)
    return None