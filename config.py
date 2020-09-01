"""
Erina Project Configuration File

You can add your API Keys and Configure Erina with this file.

Erina Project
© Anime no Sekai - 2020
"""

import os
from flask_restful import Resource
from ErinaLine.api.newClasses import new_endpoint

#################### Erina ####################
### Client to run
run_twitter_client = True
run_discord_client = True
run_line_client = False

### Logs
output_to_console = True
output_to_file = True
keep_stats = True

### ErinaSearch
anilist_priority = True
erina_database_similarity_threshold = 100
tracemoe_similarity_threshold = 87
saucenao_similarity_threshold = 90
iqdb_similarity_threshold = 90

#################### Twitter Client ####################
### API Keys
twitter_consumer_key = os.environ['twitter_consumer_key']
twitter_consumer_secret = os.environ['twitter_consumer_secret']
twitter_access_token_key = os.environ['twitter_access_token_key']
twitter_access_token_secret = os.environ['twitter_access_token_secret']

### Stream Options
twitter_username = 'ErinaSauce' # (the @ of your twitter bot account)
twitter_ignored_users = ['Crunchyroll'] # Their @ without the @
twitter_stream_languages = ['en'] # In two letters
twitter_flags = twitter_flags = ['what is this anime', "what's this anime", 'anime sauce', 'anime source', 'what anime this is', 'what anime is this', 'called this anime', 'name of this anime', "what's that anime", 'what anime is it', 'name of anime', 'sauce to that anime']
twitter_ignore_rt = True

### Monitored Mode
twitter_monitored_accounts = []
twitter_monitored_check_all_tweets = True
twitter_monitored_check_replies = False

### Advanced Options
twitter_anilist_priority = True
twitter_stream_track_flags = ['what is this anime', "what's this anime", "Anime Source?", "ErinaSauce", "ErinaBot", "Erina Sauce", "Erina Source", "@ErinaSauce", 'erina bot test', 'anime sauce'] # Keep this empty or None if you want the same flags as twitter_flags
twitter_time_to_wait_before_reconnect_when_error = 900 # In seconds
twitter_search_similarity_threshold = 87 # Range: 0 〜 100

#################### Discord Client ####################
### Bot Token
discord_bot_token = os.environ['discord_bot_token']

### Options
discord_flags = ['what is this anime', "what's this anime", 'anime sauce', 'anime source', 'tell me what anime this is', 'what anime is this', 'how is called this anime', 'name of this anime', "what's that anime", 'what anime is it']
discord_anilist_priority = True

#################### Line Client and API ####################
### API Keys
line_channel_access_token = os.environ['line_channel_access_token']
line_channel_secret = os.environ['line_channel_secret']

### Options
line_flags = ['what is this anime', "what's this anime", 'anime sauce', 'anime source', 'tell me what anime this is', 'what anime is this', 'how is called this anime', 'name of this anime', "what's that anime", 'what anime is it', "what's the title", 'what is the title']
line_anilist_priority = True
line_images_deletion_time = 3600 # The number of seconds before deleting the image from the database

#### Flask Options
host = "0.0.0.0"
port = os.environ['PORT']
flask_disable_console_messages = True

enable_lineimages_api = True
enable_erinastats_api = True
enable_animesearch_api = True

"""
# Add new API endpoints #
Steps:
 - Create your API Classes here are import them from another file (follow Flask-RESTful documentation)
 - Add a new endpoint like so:
    Example: new_endpoint(api_class=<Your API Class>, endpoint_path=<Your API Endpoint Path (i.e: "/erina/api/search")>)
"""

### Adding an endpoint test and example
class Hey(Resource):
    def get(self):
        return {'message': 'hey'}, 200

new_endpoint(api_class=Hey, endpoint_path='/hey')


#################### Trace.moe ####################
### API Keys
tracemoe_api_key = ''

#################### Sauce.nao ####################
### API Keys
saucenao_api_key = os.environ['saucenao_api_key']

#################### AniList ####################
'''
NO CONFIG FOR ANILIST
'''