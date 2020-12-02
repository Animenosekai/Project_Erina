"""
Erina Twitter Client\n

Erina Project\n
© Anime no Sekai - 2020
"""

# APIs
# -------------------------
# https://www.reddit.com/r/whatanime/comments/8fplog/a_guide_to_find_your_anime/ ✅
# - Twitter API https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data https://developer.twitter.com/en/docs https://developer.twitter.com/en  ✅
# 
# - Trace.moe https://soruly.github.io/trace.moe/#/  https://trace.moe/about  ✅
# - SauceNAO ✅
# - IQDB ✅
# - ascii2d
# - Pixiv (?)
# - Yandex
# - Google
#
# - AniList API  ✅
# - Manami DB  ✅
#
import tweepy
import requests
from io import BytesIO

from Erina.config import Erina, Twitter as TwitterConfig

class ErinaTwitterAPI():
    def __init__(self) -> None:
        self.authentification = tweepy.OAuthHandler(TwitterConfig.keys.consumer_key, TwitterConfig.keys.consumer_secret)
        self.authentification.set_access_token(TwitterConfig.keys.access_token_key, TwitterConfig.keys.access_token_secret)

        self.api = tweepy.API(self.authentification)
        self.me = self.api.me()
        self._screen_name = str(self.me.screen_name).lower().replace(" ", '')
        self._twitter_flags = [flag.lower().replace(" ", '') for flag in (TwitterConfig.flags if str(TwitterConfig.flags).replace(" ", "") not in ["None", ""] else Erina.flags)]

    def tweet(self, message, replyID=None, imageURL=None):
        """
        Tweets something
        """
        twitterImage = None
        if imageURL is not None:
            image = BytesIO(requests.get(str(imageURL)).content)
            filename = imageURL[imageURL.rfind("/"):]
            twitterImage = self.api.media_upload(filename=filename, file=image)
        
        if replyID is not None:
            if twitterImage is None:
                return self.api.update_status(status=str(message)[:280], in_reply_to_status_id=replyID, auto_populate_reply_metadata=True, media_ids=[twitterImage.media_id])
            else:
                return self.api.update_status(status=str(message)[:280], in_reply_to_status_id=replyID, auto_populate_reply_metadata=True)
        else:
            if twitterImage is None:
                return self.api.update_status(status=str(message)[:280])
            else:
                return self.api.update_status(status=str(message)[:280], media_ids=[twitterImage.media_id])

ErinaTwitter = ErinaTwitterAPI()
