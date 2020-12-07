"""
Erina Line Client for the Erina Project
Now contains also the API.

@author: Anime no Sekai
Erina Project - 2020
"""
import filecenter
from flask import request, abort

from Erina.config import Erina, Line as LineConfig
import Erina.env_information as env_information
from Erina import erina_log
from ErinaSearch import erinasearch
from ErinaServer.Server import ErinaServer
from ErinaLine.utils import Parser
from ErinaLine.utils import Images

from Erina.erina_stats import StatsAppend
from Erina.erina_stats import line as LineStats

def LineClient():
    '''
    Erina Line Client and API Client for the Erina Project\n

    @author: Anime no Sekai\n
    Erina Project - 2020
    '''

    images_path = env_information.erina_dir + '/ErinaLine/images/'
    
    from linebot import (LineBotApi, WebhookHandler)
    from linebot.exceptions import (InvalidSignatureError)
    from linebot.models import (MessageEvent, TextSendMessage)
    
    # API Keys
    line_bot_api = LineBotApi(LineConfig.keys.channel_access_token)
    handler = WebhookHandler(LineConfig.keys.channel_secret)

    # Connecting to LINE API
    @ErinaServer.route("/callback", methods=['POST'])
    def callback():
        if LineConfig.run:
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
        else:
            return 'OK'

    @handler.add(MessageEvent)
    def handle_message(event):

        if event.message.type == 'image': # If it is an image
            image_message_content = line_bot_api.get_message_content(event.message.id) # Get the image
            
            if filecenter.isfile(images_path + event.source.user_id + '.erina_image'): # Delete the last image
                filecenter.delete(images_path + event.source.user_id + '.erina_image')
            
            with open(images_path + event.source.user_id + '.erina_image', 'wb') as output_file: # Write the image to a file
                for chunk in image_message_content.iter_content():
                    output_file.write(chunk)
            Images.check(event.source.user_id)

        elif event.message.type == 'text': # If it is a text
            if any([flag in str(event.message.text).lower() for flag in (LineConfig.flags if str(LineConfig.flags).replace(" ", "") not in ["None", ""] else Erina.flags)]):
                if filecenter.isfile(images_path + event.source.user_id + '.erina_image'): # Check if the user has sent an image
                    # Sending the messages
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=Parser.makeImageResponse(erinasearch.imageSearch(images_path + event.source.user_id + '.erina_image')))
                    )
                else: # If the user hasn't sent images yet
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="You haven't sent any image yet!")
                    )
                StatsAppend(LineStats.imageSearchHit, f"From {line_bot_api.get_profile(event.source.user_id).display_name}")
                
            elif event.message.text[:10] == 'anime_info':
                # Sending the messages
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=Parser.makeInfoResponse(erinasearch.searchAnime(event.message.text[10:])))
                )
                StatsAppend(LineStats.infoHit, f"{str(event.message.text[10:])} from {line_bot_api.get_profile(event.source.user_id).display_name}")

            elif event.message.text[:17] == 'anime_description':
                # Sending the messages
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=Parser.makeDescriptionResponse(erinasearch.searchAnime(event.message.text[17:])))
                )
                StatsAppend(LineStats.descriptionHit, f"{str(event.message.text[17:])} from {line_bot_api.get_profile(event.source.user_id).display_name}")