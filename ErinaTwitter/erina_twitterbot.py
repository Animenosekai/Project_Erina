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
import sys
sys.path.append('..')

import tweepy
import lifeeasy

import config
import erina_log
from . import erina_twitter_infoparser

class ErinaTwitter():
    def __init__(self) -> None:
        self.authentification = tweepy.OAuthHandler(config.twitter_consumer_key, config.twitter_consumer_secret)
        self.authentification.set_access_token(config.twitter_access_token_key, config.twitter_access_token_secret)

        self.api = tweepy.API(self.authentification)

def TwitterClient():
    '''
    Erina Twitter Client for the Erina Project\n

    @author: Anime no Sekai\n
    Erina Project - 2020
    '''

    ##### AUTH
    authentification = tweepy.OAuthHandler(config.twitter_consumer_key, config.twitter_consumer_secret)
    authentification.set_access_token(config.twitter_access_token_key, config.twitter_access_token_secret)

    api = tweepy.API(authentification)

    ###### BOT

    class TweetListener(tweepy.StreamListener):
        """
        TweetListener Class (Twitter Stream Handler)

        Erina Project\n
        © Anime no Sekai - 2020
        """

        def on_status(self, tweet):

####### VERIFY IF THERE IS A MEDIA ON TWEET
            def check_tweet(tweet):
                if config.twitter_ignore_rt:
                    if tweet.text[:4] == 'RT @' or hasattr(tweet, 'retweeted_status'):
                        erina_log.logtwitter("Tweet ignored becuase RT")
                        return []
                answer = []
                for media in tweet.entities.get("media",[{}]):
                    #checks if there is any picture in the tweet
                    if media.get("type", None) == "photo":
                        erina_log.logtwitter(f'Picture found on this tweet ({tweet.id} by @{tweet.user.screen_name})', add_to_media_hit=True)
                        searching_image = media['media_url']
                        anime_info = erina_twitter_infoparser.search_anime_by_imageurl(searching_image)

                        if 'error' in anime_info:
                            return ["Sorry, I searched everywhere but couldn't find it"]
                        
                        if float(anime_info['similarity']) < config.twitter_search_similarity_threshold:
                            str_similarity = str(anime_info['similarity'])
                            erina_log.logtwitter(f'Not enough similarities ({str_similarity}) ({tweet.id} by @{tweet.user.screen_name})')
                        
                        else:
                            erina_log.logtwitter(f'Creating reply... ({tweet.id} by @{tweet.user.screen_name})')
                            answer.append(anime_info['reply'])
                return answer



####### MONITORED MODE
            if config.twitter_monitored_accounts != []:
                if config.twitter_monitored_check_all_tweets:
                    if config.twitter_monitored_check_replies:
                        erina_log.logtwitter(f'→ New tweet ({tweet.id} by @{tweet.user.screen_name})', add_to_stream_hit=True, add_to_hit=True)
                        answers = check_tweet(tweet)
                        if answers != []:
                            try:
                                for answer in answers:
                                    if answer == "Sorry, I searched everywhere but couldn't find it":
                                        continue
                                    erina_log.logtwitter(f'← Sending reply... ({tweet.id} by @{tweet.user.screen_name})', add_to_successful_hit=True)
                                    api.update_status(status=answer[:280], in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                            except Exception as exception:
                                erina_log.logerror(f'[ErinaTwitter] An error occured while sending back the reply. ({tweet.id} by @{tweet.user.screen_name}) --> Error details: {exception}')
                    else:
                        if tweet.user.screen_name == config.twitter_username:
                            erina_log.logtwitter(f'→ New tweet ({tweet.id})', add_to_stream_hit=True, add_to_hit=True)
                            if answers != []:
                                try:
                                    for answer in answers:
                                        erina_log.logtwitter(f'← Sending reply... ({tweet.id} by @{tweet.user.screen_name})', add_to_successful_hit=True)
                                        api.update_status(status=answer[:280], in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                                except Exception as exception:
                                    erina_log.logerror(f'[ErinaTwitter] An error occured while sending back the reply. ({tweet.id} by @{tweet.user.screen_name}) --> Error details: {exception}')
                    return


####### IF MENTIONNED
            if tweet.text.replace(' ', '').find(f'@{config.twitter_username}') != -1 or tweet.text.replace(' ', '').lower().find(f'{config.twitter_username.lower()}') != -1:
                erina_log.logtwitter('', add_to_stream_hit=True, add_to_mention_hit=True)
                if tweet.in_reply_to_status_id is not None:
                    if api.get_status(tweet.in_reply_to_status_id).user.screen_name == config.twitter_username:
                        erina_log.logtwitter('Tweet Ignored because it replies to Erina')
                        return
                if tweet.user.screen_name == config.twitter_username:
                    erina_log.logtwitter('Tweet Ignored because it is sent by Erina')
                    return
                erina_log.logtwitter(f'→ New tweet ({tweet.id} by @{tweet.user.screen_name})', add_to_hit=True)
                erina_log.logtwitter(f'High tweet priority because {config.twitter_username} got mentionned. ("{tweet.text}" @{tweet.user.screen_name})')
                answers = check_tweet(tweet)
                if answers != []:
                    try:
                        for answer in answers:
                            erina_log.logtwitter(f'← Sending reply... ({tweet.id} by @{tweet.user.screen_name})', add_to_successful_hit=True, add_to_asking_mention_hit=True)
                            api.update_status(status=answer[:280], in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                    except Exception as exception:
                        erina_log.logerror(f'[ErinaTwitter] An error occured while sending back the reply. ({tweet.id} by @{tweet.user.screen_name}) --> Error details: {exception}')
                else:
                    erina_log.logtwitter(f'No media found on tweet... ({tweet.id} by @{tweet.user.screen_name})')
                    if tweet.in_reply_to_status_id is not None:
                        parent_tweet = api.get_status(tweet.in_reply_to_status_id)
                        answers = check_tweet(parent_tweet)
                        if answers != []:
                            try:
                                for answer in answers:
                                    erina_log.logtwitter(f'← Sending reply... ({tweet.id} by @{tweet.user.screen_name})', add_to_successful_hit=True, add_to_successful_parent_hit=True, add_to_asking_mention_hit=True)
                                    api.update_status(status=answer[:280], in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                            except Exception as exception:
                                erina_log.logerror(f'[ErinaTwitter] An error occured while sending back the reply. ({tweet.id} by @{tweet.user.screen_name}) --> Error details: {exception}')
                        else:
                            erina_log.logtwitter(f'No media found on parent tweet... ({parent_tweet.id} by @{parent_tweet.user.screen_name})')
                    else:
                        erina_log.logtwitter(f'No parent tweet found... ({tweet.id} by @{tweet.user.screen_name})')
            
####### OTHER (Search for flag)
            else:
                if tweet.in_reply_to_status_id is not None:
                    if api.get_status(tweet.in_reply_to_status_id).user.screen_name == config.twitter_username:
                        erina_log.logtwitter('Tweet Ignored because it replies to Erina')
                        return
                if tweet.user.screen_name == config.twitter_username:
                    erina_log.logtwitter('Tweet Ignored because it is sent by Erina')
                    return
                flag_found = False
                for flag in config.twitter_flags:
                    if tweet.text.lower().find(flag) != -1:
                        flag_found = True
                        erina_log.logtwitter(f'Found flag {flag} in tweet {tweet.text} (index {str(tweet.text.lower().find(flag))})', add_to_stream_hit=True)
                        if tweet.user.screen_name not in config.twitter_ignored_users:
                            erina_log.logtwitter(f'→ New tweet ({tweet.id} by @{tweet.user.screen_name})', add_to_hit=True)
                            answers = check_tweet(tweet)
                            if answers != []:
                                try:
                                    for answer in answers:
                                        if answer == "Sorry, I searched everywhere but couldn't find it":
                                            continue
                                        erina_log.logtwitter(f'← Sending reply... ({tweet.id} by @{tweet.user.screen_name})', add_to_successful_hit=True)
                                        api.update_status(status=answer[:280], in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                                except Exception as exception:
                                    erina_log.logerror(f'[ErinaTwitter] An error occured while sending back the reply. ({tweet.id} by @{tweet.user.screen_name}) --> Error details: {exception}')
                            else:
                                erina_log.logtwitter(f'No media found on tweet... ({tweet.id} by @{tweet.user.screen_name})')
                                if tweet.in_reply_to_status_id is not None:
                                    parent_tweet = api.get_status(tweet.in_reply_to_status_id)
                                    answers = check_tweet(parent_tweet)
                                    if answers != []:
                                        try:
                                            for answer in answers:
                                                if answer == "Sorry, I searched everywhere but couldn't find it":
                                                    continue
                                                erina_log.logtwitter(f'← Sending reply... ({tweet.id} by @{tweet.user.screen_name})', add_to_successful_hit=True, add_to_successful_parent_hit=True)
                                                api.update_status(status=answer[:280], in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                                        except Exception as exception:
                                            erina_log.logerror(f'[ErinaTwitter] An error occured while sending back the reply. ({tweet.id} by @{tweet.user.screen_name}) --> Error details: {exception}')
                                    else:
                                        erina_log.logtwitter(f'No media found on parent tweet... ({parent_tweet.id} by @{parent_tweet.user.screen_name})')
                                else:
                                    erina_log.logtwitter(f'No parent tweet found... ({tweet.id} by @{tweet.user.screen_name})')
                        else:
                            erina_log.logtwitter(f'Tweet Ignored because User in ignored list ({tweet.id} by @{tweet.user.screen_name})')
                    if not flag_found:
                        erina_log.logtwitter(f'Tweet ignored because not in flags. ({tweet.id} by @{tweet.user.screen_name} --> {tweet.text})', add_to_stream_hit=True)

####### WHEN THERE IS AN EXPECTED ERROR
        def on_error(self, status_code):
            if status_code == 420:
                erina_log.logerror('[ErinaTwitter] Twitter Stream Error -- HTTP 420 Stream Error')
            else:
                erina_log.logerror('[ErinaTwitter] Twitter Stream Error - Unknown Error')
            erina_log.logtwitter(f'Waiting before reconnecting... ({str(config.twitter_time_to_wait_before_reconnect_when_error)} seconds)')
            lifeeasy.sleep(config.twitter_time_to_wait_before_reconnect_when_error)
            erina_log.logtwitter('Reconnecting...')
            start_stream()

####### Starting the stream
    def start_stream():
        global api
        try:
            api = tweepy.API(authentification)
            #api.update_status('Erina is ready!')
            erina_log.logtwitter('Erina is ready!')
            erina = TweetListener()
            erina_stream = tweepy.Stream(auth = api.auth, listener=erina)
            if config.twitter_monitored_accounts != []:
                users = api.lookup_users(screen_names=config.twitter_monitored_accounts)
                user_ids = [user.id_str for user in users]
                erina_stream.filter(follow=user_ids)
            else:
                if config.twitter_stream_track_flags is None or config.twitter_stream_track_flags == []:
                    erina_stream.filter(languages=config.twitter_stream_languages, track=config.twitter_flags)
                else:
                    erina_stream.filter(languages=config.twitter_stream_languages, track=config.twitter_stream_track_flags)

        
        except KeyboardInterrupt:
            if config.output_to_console:
                print('')
            erina_log.logtwitter('Stopping...')
        except Exception as exception:
            erina_log.logerror(f'[ErinaTwitter] Exception: {str(exception)}')
            erina_log.logtwitter(f'Waiting {str(config.twitter_time_to_wait_before_reconnect_when_error)} seconds before reconnection...')
            lifeeasy.sleep(config.twitter_time_to_wait_before_reconnect_when_error)
            if config.output_to_console:
                print('')
            erina_log.logtwitter('Reconnecting...')
            start_stream()
        

    start_stream()

if __name__ == '__main__':
    TwitterClient()