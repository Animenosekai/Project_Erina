"""
Manages your Twitter Profile
"""

from ErinaTwitter.erina_twitterbot import ErinaTwitter
from Erina.Errors import TwitterError

updateErinaTwitter = ErinaTwitter.api.update_profile

def changeName(new_name):
    """
    Changes the screen name of your bot
    """
    try:
        return updateErinaTwitter(name=new_name)
    except:
        return TwitterError("PROFILE_UPDATE", "An error occured while updating your Twitter name")

def changeDescription(new_description):
    """
    Changes the description on the bot account
    """
    try:
        return updateErinaTwitter(description=new_description)
    except:
        return TwitterError("PROFILE_UPDATE", "An error occured while updating your Twitter description")

def changeLocation(new_location):
    """
    Changes the location on the bot account
    """
    try:
        return updateErinaTwitter(location=new_location)
    except:
        return TwitterError("PROFILE_UPDATE", "An error occured while updating your Twitter location")

def changeLink(new_link):
    """
    Changes the bio link on the bot account
    """
    try:
        return updateErinaTwitter(url=new_link)
    except:
        return TwitterError("PROFILE_UPDATE", "An error occured while updating your Twitter bio link")
