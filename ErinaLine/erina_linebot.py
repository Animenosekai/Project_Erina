"""
Erina Line Client for the Erina Project
Now contains also the API.

@author: Anime no Sekai
Erina Project - 2020
"""
import sys
sys.path.append('..')

import json

import filecenter

from flask import Flask, request, abort
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

import config
import env_information
import erina_log
from ErinaHash import erinahash
from ErinaSearch import erinasearch
from . import erina_line_infoparser
from . import erina_lineimages_check
from .api import newClasses

if config.flask_disable_console_messages:
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

def ApiClient():
    '''
    Erina Line Client and API Client for the Erina Project\n

    @author: Anime no Sekai\n
    Erina Project - 2020
    '''

    images_path = env_information.erina_dir + '/ErinaLine/images/'
    line_images_path = env_information.erina_dir + '/ErinaLine/images/'
    stats_path = env_information.erina_dir + '/ErinaStats.json'
    
    # Creating a Flask App
    app = Flask(__name__)
    CORS(app)
    ## API
    api = Api(app)
    api.app.config['RESTFUL_JSON'] = {
        'ensure_ascii': False,
        'indent': 5,
        'sort_keys': True
    }

    if config.run_line_client:
        if config.line_channel_access_token == '':
            erina_log.logerror('[ErinaLine] No Channel Access Token provided.')
        elif config.line_channel_secret == '':
            erina_log.logerror('[ErinaLine] No Channel Secret provided.')

        from linebot import (LineBotApi, WebhookHandler)
        from linebot.exceptions import (InvalidSignatureError)
        from linebot.models import (MessageEvent, TextSendMessage)
        
        # API Keys
        line_bot_api = LineBotApi(config.line_channel_access_token)
        handler = WebhookHandler(config.line_channel_secret)

        # Connecting to LINE API
        @app.route("/callback", methods=['POST'])
        def callback():
            # get X-Line-Signature header value
            signature = request.headers['X-Line-Signature']

            # get request body as text
            body = request.get_data(as_text=True)

            # handle webhook body
            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                erina_log.logerror("[ErinaLine] Invalid signature. Please check your channel access token/channel secret.")
                abort(400)

            return 'OK'

        # When I receive a message from user
        @handler.add(MessageEvent)
        def handle_message(event):

            if event.message.type == 'image': # If it is an image
                erina_log.logline(f'Received an image from {event.source.user_id}', stattype='image_reception', value=event.source.user_id)
                image_message_content = line_bot_api.get_message_content(event.message.id) # Get the image
                
                if filecenter.isfile(images_path + event.source.user_id + '.erina_image'): # Delete the last image
                    filecenter.delete(images_path + event.source.user_id + '.erina_image')
                
                with open(images_path + event.source.user_id + '.erina_image', 'wb') as output_file: # Write the image to a file
                    for chunk in image_message_content.iter_content():
                        output_file.write(chunk)
                erina_lineimages_check.add_to_check(event.source.user_id)

            elif event.message.type == 'text': # If it is a text
                source_flags = config.line_flags
                asking_for_anime_source = False
                
                for flag in source_flags: # Check if the user wants to know the anime source
                    if event.message.text.lower().find(flag) != -1:
                        asking_for_anime_source = True
                        erina_log.logline(f'→ Anime source search came from {event.source.user_id}', stattype='source_search', value=event.source.user_id)
                        break
                
                if asking_for_anime_source: # If the user wants
                    if filecenter.isfile(images_path + event.source.user_id + '.erina_image'): # Check if the user has sent an image

                        anime_info = erina_line_infoparser.search_anime_by_image_path(images_path + event.source.user_id + '.erina_image') # Get the infos about the image --> assuming that it is an anime scene

                        reply_messages = []
                        for reply in anime_info:
                            reply_messages.append(TextSendMessage(text=reply))

                        # Sending the messages
                        line_bot_api.reply_message(
                            event.reply_token,
                            reply_messages
                        )
                        erina_log.logline(f"← Search result sent to {event.source.user_id}", stattype='successful_source_search', value=event.source.user_id)

                    else: # If the user hasn't sent images yet
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="You haven't sent any image yet!")
                        )
                
                elif event.message.text[:10] == 'anime_info':
                    erina_log.logline(f"→ Request of Anime Info came from {event.source.user_id}", stattype='anime_info_request', value=event.source.user_id)
                    anime_info = erina_line_infoparser.search_anime_by_title(event.message.text.replace('anime_info ', ''))
                    reply_text = ''
                    if anime_info['anime'] != 'unknown':
                        anime = anime_info['anime']
                        reply_text += f'Anime: {anime}\n'
                    if anime_info['year'] != 'unknown':
                        if anime_info['season'] != 'unknown':
                            season = anime_info['season']
                            year = anime_info['year']
                            reply_text += f'Season: {season} of {year}\n'
                        else:
                            year = anime_info['year']
                            reply_text += f'Year: {year}\n'
                    if anime_info['episodes'] != 'unknown':
                        episodes = anime_info['episodes'] 
                        reply_text += f'Number of episodes: {episodes}\n'
                    if anime_info['average_duration'] != 'unknown':
                        avg_duration = anime_info['average_duration']
                        reply_text += f'Average Duration: {avg_duration}\n'
                    if anime_info['status'] != 'unknown':
                        status = anime_info['status']
                        reply_text += f'Status: {status}\n'
                    if anime_info['genres'] != 'unknown':
                        genres = anime_info['genres']
                        reply_text += f'Genres: {genres}\n'
                    if anime_info['studios'] != 'unknown':
                        studios = anime_info['studios']
                        reply_text += f'Studio: {studios}\n'
                    if anime_info['description'] != 'unknown':
                        description = anime_info['description']
                        if len(description) > 200:
                            reply_text += '\n' + description[:200] + '...' + '\n'
                        else:
                            reply_text += '\n' + description + '\n'
                    if anime_info['is_hentai'] != 'unknown':
                        if str(anime_info['is_hentai']) == 'True':
                            reply_text += '⚠️ Seems to be a Hentai!\n'
                    if anime_info['anilist_url'] != 'unknwon':
                        reply_text += anime_info['anilist_url'] 

                    # Sending the messages
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)
                    )
                    erina_log.logline(f"← Anime Info sent to {event.source.user_id}", stattype='successful_anime_info', value=event.source.user_id)


                elif event.message.text[:17] == 'anime_description':
                    erina_log.logline(f"→ Request of Anime Description came from {event.source.user_id}", stattype='anime_description_request', value=event.source.user_id)
                    anime_info = erina_line_infoparser.search_anime_by_title(event.message.text.replace('anime_description ', ''))
                    reply_text = ''
                    anime = anime_info['anime']
                    description = anime_info['description']
                    if len(description) > 1500:
                        reply_text += '\n' + description[:1500] + '...' + '\n'
                    else:
                        reply_text += '\n' + description + '\n'
                    if anime_info['anilist_url'] != 'unknwon':
                        reply_text += anime_info['anilist_url']

                    # Sending the messages
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)
                    )

                    erina_log.logline(f"← Anime Description sent to {event.source.user_id}", stattype='successful_anime_description', value=event.source.user_id)

    if config.enable_lineimages_api:
        ## LINE CLIENT API to retrieve images 
        class LINEImages(Resource):
            """
            LineImages API.
            Used to retrieve images from user and send (for example) to trace.moe API.
            """
            def get(self):
                """
                HTTP GET Requests Handler (Retrieve Images)
                """
                erina_log.logapi('[ErinaLine] GET Request received for Images API', apitype='line_images')
                parser = reqparse.RequestParser()
                parser.add_argument('id', required=False)
                parser.add_argument('base64', required=False)
                parser.add_argument('hash', required=False)
                args = parser.parse_args()
                if args['id'] is not None:
                    if filecenter.isfile(line_images_path + args['id'] + '.erina_image'):
                        results = {}
                        results['id'] = args['id']
                        results['filename'] = args['id'] + '.erina_image'
                        results['filepath'] = line_images_path + args['id'] + '.erina_image'
                        if args['base64'] is not None:
                            base64 = erinahash.base64_from_image(line_images_path + args['id'] + '.erina_image')
                            results['base64'] = str(base64)
                            if args['hash'] is not None:
                                image_hash = erinahash.hash_image_from_path(line_images_path + args['id'] + '.erina_image')
                                results['hash'] = str(image_hash)
                            return results, 200
                        elif args['hash'] is not None:
                            image_hash = erinahash.hash_image_from_path(line_images_path + args['id'] + '.erina_image')
                            results['hash'] = str(image_hash)
                            return results, 200
                        else:
                            return results, 200
                    else:
                        return {'error': 'File not found.', 'explanation': 'You might have requested the wrong LINE User ID or the file has been deleted because too old.'}, 404
                else:
                    return {'error': "'id' is required"}, 404
        api.add_resource(LINEImages, '/erina/line/api/image')

    if config.enable_erinastats_api:
        class ErinaStats(Resource):
            """
            ErinaStats API.
            Used to retrieve stats infos.
            """
            def get(self):
                """
                HTTP GET Requests Handler (Retrieve Stats as JSON)
                """
                erina_log.logapi('[Erina] GET Request received for Stats API', apitype='erina_stats')
                with open(stats_path, 'r') as statsJSON:
                    data = json.load(statsJSON)
                return data, 200
        api.add_resource(ErinaStats, '/erina/api/stats')

    if config.enable_animesearch_api:
        ## ERINA SEARCHANIME API
        class SearchAnime(Resource):
            """
            Searches the given anime scene/attribute.
            """
            def get(self):
                '''
                HTTP GET Requests Handler
                '''
                parser = reqparse.RequestParser()
                parser.add_argument('anilistID', required=False)
                parser.add_argument('title', required=False)
                parser.add_argument('hash', required=False)
                parser.add_argument('imageURL', required=False)
                parser.add_argument('imagePath', required=False)
                parser.add_argument('imageBase64', required=False)
                args = parser.parse_args()
                erina_log.logapi(f'[ErinaSearch] GET Request received for Anime Search API', apitype='anime_search')
                results = {}
                if args['anilistID'] is not None:
                    results = erinasearch.search_anime_by_anilist_id(int(args['anilistID']))
                elif args['title'] is not None:
                    results = erinasearch.search_anime_by_title(str(args['title']))
                elif args['hash'] is not None:
                    results = erinasearch.search_anime_by_hash(str(args['hash']))
                elif args['imageURL'] is not None:
                    results = erinasearch.search_anime_by_imageurl(str(args['imageURL']))
                elif args['imagePath'] is not None:
                    results = erinasearch.search_anime_from_image_path(str(args['imagePath']))
                elif args['imageBase64'] is not None:
                    results = erinasearch.search_anime_by_base64(str(args['imageBase64']))
                if results == {}:
                    return {'error': 'The anime attribute or the image attribute is missing', 'details': "You didn't specified any attribute from the list of available attributes.", 'list_of_attributes': ['anilistID', 'title', 'hash', 'imageURL', 'imagePath', 'imageBase64']}, 404
                else:
                    return results, 200

        #api.add_resource(SearchAnime, '/erina/api/searchanime')
        api.add_resource(SearchAnime, '/erina/api/search')
        #api.add_resource(SearchAnime, '/erina/api/anime')
        #api.add_resource(SearchAnime, '/erina/api/animesearch')

    class nosleep(Resource):
        """
        If you have a server which sleeps (stops) when inactive, use the /keepalive endpoint to keep it "active".
        """
        def get(self):
            """
            To keep the server up.
            """
            erina_log.logapi('[Keep Alive] GET Request received', apitype='nosleep')
            return {'message': 'success'}, 200
    api.add_resource(nosleep, '/keepalive')



    ##### ADDING USER's CONFIGURED ENDPOINTs FROM CONFIG FILE
    for endpoint in newClasses.list_of_classes:
        api.add_resource(endpoint['api_class'], endpoint['endpoint_path'])

    app.run(host=config.host, port=config.port) # Run the flask app

if __name__ == '__main__':
    ApiClient()