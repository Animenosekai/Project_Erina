"""
Twitter Stream Manager
"""

import tweepy
from ErinaTwitter.utils.Errors import TwitterError

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
            pass

        def on_status(self, tweet):
            """
            Tweet Receiving
            """
            pass

        def on_direct_message(self, status):
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