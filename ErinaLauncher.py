"""
Erina Clients Wrapper for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

import threading
import asyncio
import sys

import lifeeasy
import config
import erina_log
from ErinaTwitter import erina_twitterbot
from ErinaDiscord import erina_discordbot
from ErinaLine import erina_linebot
from ErinaLine import erina_lineimages_check

def ErinaClients():
    """
    Erina Clients Wrapper Main Function for the Erina Project

    @author: Anime no Sekai
    Erina Project - 2020
    """
    if '--reset-stats' in sys.argv:
        print('Do you really want to delete the stats?')
        choice = input('> ')
        if choice.lower() == 'yes' or choice.lower() == 'yea' or choice.lower() == 'ya' or choice.lower() == 'yeah':
            erina_log.resetstats()
    try:
        erina_log.loglaunch('')

        try:
            erina_log.loglaunch('Opening a new thread with Line Image Checker')
            thread = threading.Thread(target=erina_lineimages_check.start_check)
            threading.daemon = True
            thread.start()
            erina_log.loglaunch('Opening a new thread with the API Client.')
            thread = threading.Thread(target=erina_linebot.ApiClient)
            thread.daemon = True
            thread.start()
        except Exception as exception:
            erina_log.logerror(f'[Erina] An error occured while running client: API, [Error Details] {str(exception)}')
    
        if config.run_twitter_client:
            try:
                if config.twitter_consumer_key == '':
                    erina_log.logerror('[ErinaTwitter] No consumer key provided.')
                elif config.twitter_consumer_secret == '':
                    erina_log.logerror('[ErinaTwitter] No consumer secret provided.')
                elif config.twitter_access_token_key == '':
                    erina_log.logerror('[ErinaTwitter] No access token key provided.')
                elif config.twitter_access_token_secret == '':
                    erina_log.logerror('[ErinaTwitter] No access token secret provided.')
                else:
                    erina_log.loglaunch('Opening a new thread with client: ErinaTwitter')
                    thread = threading.Thread(target=erina_twitterbot.TwitterClient)
                    thread.daemon = True
                    thread.start()
            except Exception as exception:
                erina_log.logerror(f'[Erina] An error occured while running client: ErinaTwitter, [Error Details] {str(exception)}')
        
        if config.run_discord_client:
            try:
                if config.discord_bot_token == '':
                    erina_log.logerror(f'[ErinaDiscord] No Bot Token Provided.')
                else:
                    erina_log.loglaunch('Running Discord Client...')
                    loop = asyncio.get_event_loop()
                    loop.create_task(erina_discordbot.client.start(config.discord_bot_token))
                    loop.run_forever()
            except Exception as exception:
                erina_log.logerror(f'[Erina] An error occured while running client: ErinaDiscord, [Error Details] {str(exception)}')
        else:
            while True:
                try:
                    lifeeasy.sleep(10)
                except:
                    erina_log.loglaunch('Exception Received.')
                    break

    except Exception as exception:
        erina_log.loglaunch('Exception Received.')
        erina_log.loglaunch(f'Exception Details: {str(exception)}')

if __name__ == '__main__':
    ErinaClients()