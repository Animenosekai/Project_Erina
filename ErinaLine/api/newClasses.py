"""
Used to add endpoints to the Flask RESTful API\n

Project Erina - 2020\n
© Anime no Sekai
"""

list_of_classes = []

def new_endpoint(api_class, endpoint_path):
    global list_of_classes
    list_of_classes.append({'api_class': api_class, 'endpoint_path': endpoint_path})