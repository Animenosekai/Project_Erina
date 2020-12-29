"""
IQDB Results Parser\n
Also get results from iqdb database's sites\n


** DEPRECATED **

Erina Project\n
© Anime no Sekai - 2020
"""

from Erina.erina_stats import StatsAppend
from Erina.erina_stats import external as ExternalStats
import sys # to import from upper levels
sys.path.append('.') # appending the Erina Folder to the Python PATH
sys.path.append('..') # appending the Erina Folder to the Python PATH
import re # to use RegEx
from datetime import datetime
import requests # to make post requests with files
from lifeeasy import request, json_to_dict, write_file, today, current_time # to make requests, turn json results into python dictionnary and to write the final cache file out
from bs4 import BeautifulSoup # to manipulate html doms
from ErinaCaches.erinacache import create_erina_list
import env_information # to get informations about the current environment
import erina_log

def db_to_name(db):
    data = {
        "gelbooru": "Gelbooru",
        "danbooru": "Danbooru",
        "zerochan": "Zerochan",
        "konachan": "Konachan",
        "yandere": "Yande.re",
        "anime_pictures": "Anime-Pictures",
        "e_shuushuu": "E-Shuushuu"
    }
    try:
        return data[db]
    except:
        return "N/A"

def remove_space_before_and_after(text):
    """
    Removes any space before and after a string.
    """
    new_text = text
    for index, _ in enumerate(text):
        if text[index] != ' ':
            new_text = text[index:] + ' '
            break
    try:
        if new_text[-1] == ' ':
            for index, _ in enumerate(new_text):
                if new_text[-int(index + 1)] != ' ':
                    new_text = new_text[:-int(index)]
                    break
    except:
        pass
    return new_text

def remove_elements_from_list(list_to_update, list_of_element, delete_inside_string=False, remove_space_before_and_after_string=False):
    """
    Removes certain elements from a given list.
    """
    new_list = []
    for entry in list_to_update:
        if not entry in list_of_element:
            new_entry = entry
            if delete_inside_string:
                for element_to_delete in list_of_element:
                    new_entry = new_entry.replace(element_to_delete, '')
            if remove_space_before_and_after_string:
                new_list.append(remove_space_before_and_after(new_entry))
            else:
                new_list.append(new_entry)
    return new_list


############ GELBOORU RESULTS
def search_gelbooru(url):
    erina_log.logcaches(f'Searching for Gelbooru Data...')
    gelbooru_results = {}
    response = request(url)
    gelbooru = BeautifulSoup(response.text, 'html.parser')
    characters_containers = gelbooru.find_all('li', attrs={'class': 'tag-type-character'})
    characters = []
    for character in characters_containers:
        characters.append(character.findChildren('a')[1].get_text())
    gelbooru_results['characters'] = characters
        
    copyright_containers = gelbooru.find_all('li', attrs={'class': 'tag-type-copyright'})
    copyrights = []
    for copyright_text in copyright_containers:
        copyrights.append(copyright_text.findChildren('a')[1].get_text())
    gelbooru_results['copyrights'] = copyrights

    metadata_containers = gelbooru.find_all('li', attrs={'class': 'tag-type-metadata'})
    metadatas = []
    for metadata in metadata_containers:
        metadatas.append(metadata.findChildren('a')[1].get_text())
    gelbooru_results['metadatas'] = metadatas

    tag_containers = gelbooru.find_all('li', attrs={'class': 'tag-type-general'})
    tags = []
    for tag in tag_containers:
        tags.append(tag.findChildren('a')[1].get_text())
    gelbooru_results['tags'] = tags

    gelbooru_statistics_html = response.text.split('<h3>Statistics</h3>')[1].split('<h3>Options</h3>')[0]
    gelbooru_statistics = BeautifulSoup(gelbooru_statistics_html, 'html.parser')
    list_items = gelbooru_statistics.find_all('li')
    gelbooru_results['id'] = 'N/A'
    gelbooru_results['size'] = 'N/A'
    gelbooru_results['source'] = 'N/A'
    gelbooru_results['rating'] = 'N/A'
    gelbooru_results['date'] = 'N/A'
    gelbooru_results['uploader'] = 'N/A'
    gelbooru_results['score'] = 'N/A'
    for item in list_items:
        if item.get_text()[:3] == 'Id:':
            gelbooru_results['id'] = item.get_text()[4:]
        elif item.get_text()[:5] == 'Size:':
            gelbooru_results['size'] = item.get_text()[6:]
        elif item.get_text()[:7] == 'Source:':
            gelbooru_results['source'] = item.find('a')['href']
        elif item.get_text()[:7] == 'Rating:':
            gelbooru_results['rating'] = item.get_text()[8:]
        elif item.get_text()[:7] == 'Posted:':
            gelbooru_results['date'] = item.get_text()[8:].split(' by ')[0]
            gelbooru_results['uploader'] = item.get_text()[8:].split(' by ')[1]
        elif item.get_text()[:6] == 'Score:':
            gelbooru_results['score'] = re.sub('[^0123456789]', '', item.get_text()[7:])
    return gelbooru_results
        

############ DANBOORU RESULTS
def search_danbooru(url):        
    erina_log.logcaches(f'Searching for Danbooru Data...')
    danbooru_results = {}
    response = request(url)
    danbooru = BeautifulSoup(response.text, 'html.parser')
    artists = []
    for element in danbooru.find('ul', attrs={'class': 'artist-tag-list'}).findChildren('li'):
        artists.append(element.find_all('a', attrs={'class': 'search-tag'})[0].get_text())
    danbooru_results['artists'] = artists
    
    copyrights = []
    for element in danbooru.find('ul', attrs={'class': 'copyright-tag-list'}).findChildren('li'):
        copyrights.append(element.find_all('a', attrs={'class': 'search-tag'})[0].get_text())
    danbooru_results['copyrights'] = copyrights
    
    characters = []
    for element in danbooru.find('ul', attrs={'class': 'character-tag-list'}).findChildren('li'):
        characters.append(element.find_all('a', attrs={'class': 'search-tag'})[0].get_text())
    danbooru_results['characters'] = characters
    
    tags = []
    for element in danbooru.find('ul', attrs={'class': 'general-tag-list'}).findChildren('li'):
        tags.append(element.find_all('a', attrs={'class': 'search-tag'})[0].get_text())
    danbooru_results['tags'] = tags
    
    metadatas = []
    for element in danbooru.find('ul', attrs={'class': 'meta-tag-list'}).findChildren('li'):
        metadatas.append(element.find_all('a', attrs={'class': 'search-tag'})[0].get_text())
    danbooru_results['metadatas'] = metadatas
    
    danbooru_results['id'] = remove_space_before_and_after(danbooru.find_all('li', attrs={'id': 'post-info-id'})[0].get_text().replace('ID: ', '').replace('\n', ''))
    danbooru_results['uploader'] = remove_space_before_and_after(danbooru.find_all('li', attrs={'id': 'post-info-uploader'})[0].get_text().replace('Uploader: ', '').replace('\n', '')).replace('»', '')
    danbooru_results['date'] = remove_space_before_and_after(danbooru.find_all('li', attrs={'id': 'post-info-date'})[0].get_text().replace('Date: ', '').replace('\n', ''))
    danbooru_results['content_size'] = remove_space_before_and_after(danbooru.find_all('li', attrs={'id': 'post-info-size'})[0].get_text().replace('Size: ', '').split(' .')[0].replace('\n', ''))
    danbooru_results['format'] = remove_space_before_and_after('.' + danbooru.find_all('li', attrs={'id': 'post-info-size'})[0].get_text().replace('Size: ', '').split(' .')[1].split(' ')[0].replace('\n', ''))
    danbooru_results['size'] = remove_space_before_and_after(danbooru.find_all('li', attrs={'id': 'post-info-size'})[0].get_text().replace('Size: ', '').split(' (')[1][:-1].replace('\n', '').replace(')', ''))
    danbooru_results['source'] = danbooru.find_all('li', attrs={'id': 'post-info-source'})[0].find('a')['href']
    danbooru_results['rating'] = remove_space_before_and_after(danbooru.find_all('li', attrs={'id': 'post-info-rating'})[0].get_text().replace('Rating: ', '').replace('\n', ''))
    danbooru_results['score'] = remove_space_before_and_after(danbooru.find_all('li', attrs={'id': 'post-info-score'})[0].get_text().replace('Score: ', '').replace('\n', ''))
    danbooru_results['favorites'] = remove_space_before_and_after(danbooru.find_all('li', attrs={'id': 'post-info-favorites'})[0].get_text().replace('Favorites: ', '').replace('\n', ''))
    danbooru_results['status'] = remove_space_before_and_after(danbooru.find_all('li', attrs={'id': 'post-info-status'})[0].get_text().replace('\n', '').replace(' ', '').replace('Status:', ''))
    return danbooru_results
        

############ ZEROCHAN RESULTS
def search_zerochan(url):
    erina_log.logcaches(f'Searching for Zerochan Data...')
    zerochan_results = {}
    response = request(url)
    zerochan = BeautifulSoup(response.text, 'html.parser')
    zerochan_results['mangaka'] = 'N/A'
    zerochan_results['series'] = 'N/A'
    zerochan_results['character'] = 'N/A'
    zerochan_results['source'] = 'N/A'
    
    zerochan_info = json_to_dict(zerochan.find('script', attrs={'type': 'application/ld+json'}).get_text())

    zerochan_results['uploader'] = zerochan_info['author']
    zerochan_results['content_url'] = zerochan_info['contentUrl']
    zerochan_results['thumbnail'] = zerochan_info['thumbnail']
    zerochan_results['format'] = zerochan_info['encodingFormat']
    zerochan_results['post_date'] = zerochan_info['datePublished']
    zerochan_results['name'] = zerochan_info['name']
    zerochan_results['width'] = zerochan_info['width']
    zerochan_results['height'] = zerochan_info['height']
    zerochan_results['content_size'] = zerochan_info['contentSize']

    for tag in zerochan.find('ul', attrs={'id': "tags"}).findChildren('li'):
        if tag.get_text().find(' Mangaka') != -1:
            zerochan_results['mangaka'] = tag.get_text().replace(' Mangaka', '')
        elif tag.get_text().find(' Series') != -1:
            zerochan_results['series'] = tag.get_text().replace(' Series', '')
        elif tag.get_text().find(' Character') != -1:
            zerochan_results['character'] = tag.get_text().replace(' Character', '')
        elif tag.get_text().find(' Source') != -1:
            zerochan_results['source'] = tag.get_text().replace(' Source', '')

    return zerochan_results



############ KONACHAN RESULTS
def search_konachan(url):
    erina_log.logcaches(f'Searching for Konachan Data...')
    konachan_results = {}
    response = request(url)
    konachan = BeautifulSoup(response.text, 'html.parser')
    
    copyrights = []
    for element in konachan.find_all('li', attrs={'class': 'tag-type-copyright'}):
        copyrights.append(element.find_all('a')[1].get_text())
    konachan_results['copyrights'] = copyrights
    
    styles = []
    for element in konachan.find_all('li', attrs={'class': 'tag-type-style'}):
        styles.append(element.find_all('a')[1].get_text())
    konachan_results['styles'] = styles
    
    artists = []
    for element in konachan.find_all('li', attrs={'class': 'tag-type-artist'}):
        artists.append(element.find_all('a')[1].get_text())
    konachan_results['artists'] = artists
    
    characters = []
    for element in konachan.find_all('li', attrs={'class': 'tag-type-character'}):
        characters.append(element.find_all('a')[1].get_text())
    konachan_results['characters'] = characters

    tags = []
    for element in konachan.find_all('li', attrs={'class': 'tag-type-general'}):
        tags.append(element.find_all('a')[1].get_text())
    konachan_results['tags'] = tags
    
    konachan_statistics_html = response.text.split('<h5>Statistics</h5>')[1].split('<h5>Options</h5>')[0]
    konachan_statistics = BeautifulSoup(konachan_statistics_html, 'html.parser')
    list_items = konachan_statistics.find_all('li')
    konachan_results['id'] = 'N/A'
    konachan_results['size'] = 'N/A'
    konachan_results['source'] = 'N/A'
    konachan_results['rating'] = 'N/A'
    konachan_results['date'] = 'N/A'
    konachan_results['uploader'] = 'N/A'
    konachan_results['score'] = 'N/A'
    konachan_results['favorited_by'] = ['N/A']
    for item in list_items:
        if item.get_text()[:3] == 'Id:':
            konachan_results['id'] = item.get_text()[4:]
        elif item.get_text()[:5] == 'Size:':
            konachan_results['size'] = item.get_text()[6:]
        elif item.get_text()[:7] == 'Source:':
            konachan_results['source'] = item.find('a')['href']
        elif item.get_text()[:7] == 'Rating:':
            konachan_results['rating'] = remove_space_before_and_after(item.get_text()[8:])
        elif item.get_text()[:7] == 'Posted:':
            konachan_results['date'] = item.get_text()[8:].split(' by ')[0]
            konachan_results['uploader'] = item.get_text()[8:].split(' by ')[1]
        elif item.get_text()[:6] == 'Score:':
            konachan_results['score'] = re.sub('[^0123456789]', '', item.get_text()[7:])
        elif item.get_text()[:13] == 'Favorited by:':
            konachan_results['favorited_by'] = item.get_text()[14:].split(', ')

    return konachan_results


############ YANDE.RE RESULTS
def search_yandere(url):
    erina_log.logcaches(f'Searching for Yande.re Data...')
    yandere_results = {}
    response = request(url)
    yandere = BeautifulSoup(response.text, 'html.parser')

    copyrights = []
    for element in yandere.find_all('li', attrs={'class': 'tag-type-copyright'}):
        copyrights.append(element.find_all('a')[1].get_text())
    yandere_results['copyrights'] = copyrights
    
    styles = []
    for element in yandere.find_all('li', attrs={'class': 'tag-type-style'}):
        styles.append(element.find_all('a')[1].get_text())
    yandere_results['styles'] = styles
    
    artists = []
    for element in yandere.find_all('li', attrs={'class': 'tag-type-artist'}):
        artists.append(element.find_all('a')[1].get_text())
    yandere_results['artists'] = artists
    
    characters = []
    for element in yandere.find_all('li', attrs={'class': 'tag-type-character'}):
        characters.append(element.find_all('a')[1].get_text())
    yandere_results['characters'] = characters
    
    tags = []
    for element in yandere.find_all('li', attrs={'class': 'tag-type-general'}):
        tags.append(element.find_all('a')[1].get_text())
    yandere_results['tags'] = tags

    yandere_statistics_html = response.text.split('<h5>Statistics</h5>')[1].split('<h5>Options</h5>')[0]
    yandere_statistics = BeautifulSoup(yandere_statistics_html, 'html.parser')
    list_items = yandere_statistics.find_all('li')
    yandere_results['id'] = 'N/A'
    yandere_results['size'] = 'N/A'
    yandere_results['source'] = 'N/A'
    yandere_results['rating'] = 'N/A'
    yandere_results['date'] = 'N/A'
    yandere_results['uploader'] = 'N/A'
    yandere_results['score'] = 'N/A'
    yandere_results['favorited_by'] = ['N/A']
    for item in list_items:
        if item.get_text()[:3] == 'Id:':
            yandere_results['id'] = item.get_text()[4:]
        elif item.get_text()[:5] == 'Size:':
            yandere_results['size'] = item.get_text()[6:]
        elif item.get_text()[:7] == 'Source:':
            yandere_results['source'] = item.find('a')['href']
        elif item.get_text()[:7] == 'Rating:':
            yandere_results['rating'] = remove_space_before_and_after(item.get_text()[8:])
        elif item.get_text()[:7] == 'Posted:':
            yandere_results['date'] = item.get_text()[8:].split(' by ')[0]
            yandere_results['uploader'] = item.get_text()[8:].split(' by ')[1]
        elif item.get_text()[:6] == 'Score:':
            yandere_results['score'] = re.sub('[^0123456789]', '', item.get_text()[7:])
        elif item.get_text()[:13] == 'Favorited by:':
            yandere_results['favorited_by'] = item.get_text()[14:].split(', ')

    return yandere_results

############ ANIME-PICTURES RESULTS

def search_animepictures(url):
    erina_log.logcaches(f'Searching for Anime-Pictures Data...')
    animepictures_results = {}
    response = request(url)
    animepictures = BeautifulSoup(response.text, 'html.parser')
    
    animepictures_results['id'] = 'N/A'
    animepictures_results['uploader'] = 'N/A'
    animepictures_results['last_editing_user'] = 'N/A'
    animepictures_results['post_date'] = 'N/A'
    animepictures_results['published_date'] = 'N/A'
    animepictures_results['download_count'] = 'N/A'
    animepictures_results['size'] = 'N/A'
    animepictures_results['aspect_ratio'] = 'N/A'
    animepictures_results['content_size'] = 'N/A'
    animepictures_results['average_color_name'] = 'N/A'
    animepictures_results['average_color'] = ['N/A']
    animepictures_results['artefacts_degree'] = 'N/A'
    animepictures_results['smoothness_degree'] = 'N/A'
    animepictures_results['complexity'] = 'N/A'

    animepictures_results['id'] = remove_space_before_and_after(animepictures.find('div', attrs={'class': 'post_content'}).find('h1').get_text().split('№')[1]).replace('\n', '').replace('\t', '')

    all_content_titles = animepictures.find('div', attrs={'class': 'post_content'}).find_all('b')
    all_children = animepictures.find('div', attrs={"class": 'post_content'}).contents
    for element in all_content_titles:
        try:
            index = all_children.index(element) + 1
        except:
            index = -1
        if element.get_text().find('Posted by:') != -1:
            try:
                animepictures_results['uploader'] = animepictures.find('div', attrs={'class': 'post_content'}).find('div', attrs={'class': 'post_content_avatar'}).find('a').get_text()
            except:
                animepictures_results['uploader'] = 'N/A'
        elif element.get_text().find('Current status set by:') != -1:
            try:
                animepictures_results['last_editing_user'] = all_children[index + 1].get_text()
            except:
                animepictures_results['last_editing_user'] = 'N/A'
        elif element.get_text().find('Resolution:') != -1:
            try:
                animepictures_results['size'] = all_children[index + 1].get_text()
                animepictures_results['aspect_ratio'] = remove_space_before_and_after(all_children[index + 3].get_text()).replace('\n', '').replace('\t', '')
            except:
                animepictures_results['size'] = 'N/A'
                animepictures_results['aspect_ratio'] = 'N/A'
        elif element.get_text().find('Color:') != -1:
            try:
                animepictures_results['average_color_name'] = all_children[index + 1].get_text().split(' (')[0].replace('\t', '').replace('\n', '')
                animepictures_results['average_color'] = all_children[index + 1].get_text().split(' (')[1].replace(')', '').split(' ')
            except:
                animepictures_results['average_color_name'] = 'N/A'
                animepictures_results['average_color'] = ['N/A']
        elif element.get_text().find('Date Upload:') != -1:
            try:
                animepictures_results['post_date'] = all_children[index].strip()
            except:
                animepictures_results['post_date'] = 'N/A'
        elif element.get_text().find('Date Published:') != -1:
            try:
                animepictures_results['published_date'] = all_children[index].strip()
            except:
                animepictures_results['published_date'] = 'N/A'
        elif element.get_text().find('Downloads:') != -1:
            try:
                animepictures_results['download_count'] = all_children[index].strip()
            except:
                animepictures_results['download_count'] = 'N/A'
        elif element.get_text().find('Size:') != -1:
            try:
                animepictures_results['content_size'] = all_children[index].strip()
            except:
                animepictures_results['content_size'] = 'N/A'
        elif element.get_text().find('Artefacts Degree:') != -1:
            try:
                animepictures_results['artefacts_degree'] = all_children[index].strip()
            except:
                animepictures_results['artefacts_degree'] = 'N/A'
        elif element.get_text().find('Smoothness Degree:') != -1:
            try:
                animepictures_results['smoothness_degree'] = all_children[index].strip()
            except:
                animepictures_results['smoothness_degree'] = 'N/A'
        elif element.get_text().find('Complexity:') != -1:
            try:
                animepictures_results['complexity'] = all_children[index].strip()
            except:
                animepictures_results['complexity'] = 'N/A'

    """
    unclear_list_of_info = animepictures.find('div', attrs={'class': 'post_content'}).get_text().split('\n')
    new_list_of_info = remove_elements_from_list(unclear_list_of_info, ['', '  ', '   ', '\t', '\t\t', '\t\t\t', '\xa0\xa0\xa0\xa0', '\xa0', '№', 'Downloads:', 'Resolution:', 'Size:', 'Color:','Complexity:', 'Anime picture', 'Posted by: ', 'Current status set by:', 'Date Upload: ', 'Date Published:', 'Artefacts Degree: ', 'Smoothness Degree: '], delete_inside_string=True)
    new_list_of_info = remove_elements_from_list(new_list_of_info, ['', ' '], delete_inside_string=False, remove_space_before_and_after_string=True)

    keys_list = ['id', 'uploader', 'last_editing_user', 'post_date', 'published_date', 'download_count', 'size', 'aspect_ratio', 'content_size', 'average_color', 'artefacts_degree', 'smoothness_degree', 'complexity']
    iteration = 0
    for key in keys_list:
        if key == 'average_color':
            animepictures_results['average_color_name'] = new_list_of_info[iteration]
            animepictures_results['average_color'] = new_list_of_info[iteration]
        else:
            animepictures_results[key] = new_list_of_info[iteration]
        iteration += 1
    """

    tags_list = animepictures.find('ul', attrs={'class': 'tags'})
    animepictures_results['copyright'] = tags_list.find('a', attrs={'class': 'copyright'}).get_text()
    animepictures_results['artist'] = tags_list.find('a', attrs={'class': 'artist'}).get_text()

    references = []
    reference_tags_html = BeautifulSoup(response.text.split('<span>reference</span>')[1].split('<span>object</span>')[0], features='html.parser')
    for element in reference_tags_html.find_all('a'):
        references.append(element.get_text())

    animepictures_results['references'] = remove_elements_from_list(references, [''])

    objects = []
    object_tags_html = BeautifulSoup(response.text.split('<span>object</span>')[1].split('<div class="sidebar_block">')[0], features='html.parser')
    for element in object_tags_html.find_all('a'):
        objects.append(element.get_text())

    animepictures_results['objects'] = remove_elements_from_list(objects, [''])

    similar_images_id = []
    for picture in animepictures.find('div', attrs={'class': 'image_body'}).find_all('a'):
        if str(picture.parent)[:4] != '<div':
            similar_images_id.append(picture['href'].replace('/pictures/view_post/', '').split('?lang=')[0])
    animepictures_results['similar_images_id'] = similar_images_id

    artist_information_html = BeautifulSoup(response.text.split(f'<strong>{animepictures_results["artist"]}:</strong>')[1].split('<div class="post_content">')[0], features='html.parser')
    artist_links = []
    for link in artist_information_html.find_all('a'):
        artist_links.append(link['href'])
    
    animepictures_results['artist_links'] = artist_links

    return animepictures_results
        

############ E-SHUUSHUU RESULTS

def search_eshuushuu(url):
    erina_log.logcaches(f'Searching for E-Shuushuu Data...')
    e_shuushuu_results = {}
    response = request(url)
    e_shuushuu = BeautifulSoup(response.text, 'html.parser')


    e_shuushuu_results['uploader'] = ''
    e_shuushuu_results['post_date'] = ''
    e_shuushuu_results['filename'] = ''
    e_shuushuu_results['original_filename'] = ''
    e_shuushuu_results['content_size'] = ''
    e_shuushuu_results['size'] = ''
    e_shuushuu_results['favorites'] = ''

    meta_element = e_shuushuu.find('div', attrs={'class': 'meta'})
    for metadata in meta_element.find_all('dt'):
        
        if metadata.get_text() == 'Submitted By:':
            e_shuushuu_results['uploader'] = metadata.findNext('dd').get_text()

        if metadata.get_text() == 'Submitted On:':
            e_shuushuu_results['post_date'] = metadata.findNext('dd').get_text()

        if metadata.get_text() == 'Filename:':
            e_shuushuu_results['filename'] = metadata.findNext('dd').get_text()

        if metadata.get_text() == 'Original Filename:':
            e_shuushuu_results['original_filename'] = metadata.findNext('dd').get_text()

        if metadata.get_text() == 'File size:':
            e_shuushuu_results['content_size'] = remove_space_before_and_after(metadata.findNext('dd').get_text()).replace('\n', '').replace('\t', '')

        if metadata.get_text() == 'Dimensions:':
            e_shuushuu_results['size'] = metadata.findNext('dd').get_text()

        if metadata.get_text() == 'Favorites:':
            e_shuushuu_results['favorites'] = metadata.findNext('dd').get_text()

    e_shuushuu_results['tags'] = []
    e_shuushuu_results['sources'] = []
    e_shuushuu_results['characters'] = []
    e_shuushuu_results['artists'] = []
    e_shuushuu_results['image_rating'] = ''

    for metadata in meta_element.find_all('dd'):
        previous_sibling = metadata.find_previous_sibling('dt').get_text()

        if previous_sibling.find('Tags:') != -1:
            for tag in metadata.find_all('span', attrs={'class': 'tag'}):
                e_shuushuu_results['tags'].append(remove_space_before_and_after(tag.get_text()).replace('"', ''))
        
        elif previous_sibling.find('Source:') != -1:
            for tag in metadata.find_all('span', attrs={'class': 'tag'}):
                e_shuushuu_results['sources'].append(remove_space_before_and_after(tag.get_text()).replace('"', ''))
        
        elif previous_sibling.find('Characters:') != -1:
            for tag in metadata.find_all('span', attrs={'class': 'tag'}):
                e_shuushuu_results['characters'].append(remove_space_before_and_after(tag.get_text()).replace('"', ''))
        
        elif previous_sibling.find('Artist:') != -1:
            for tag in metadata.find_all('span', attrs={'class': 'tag'}):
                e_shuushuu_results['artists'].append(remove_space_before_and_after(tag.get_text()).replace('"', ''))
        
        elif previous_sibling.find('Rating:') != -1:
            e_shuushuu_results['image_rating'] = remove_space_before_and_after(metadata.get_text()).replace('"', '').replace('\t', '').replace('\n', '')

    return e_shuushuu_results
    


###### MAIN FUNCTION ######
def search_iqdb(image_hash, image_url='', file_io=None):
    """
    Searches and caches IQDB for anime/manga related images.

    Erina Project - 2020\n
    © Anime no Sekai
    """

    erina_log.logcaches(f'Searching for IQDB Data...', 'iqdb', str(image_hash))
    StatsAppend(ExternalStats.iqdbCalls, "New Call")
    results = {}

    ### If a file is given, send the file to iqdb.
    if file_io is not None:
        response = requests.post('https://iqdb.org/', files={'file': ('image_to_search',  file_io) })
    else:
        if image_url == '':
            erina_log.logerror('[ErinaCaches] [IQDB] No file or URL provided')
            return {'error': 'no file or url provided'}
        else:
            response = request(f'https://iqdb.org/?url={image_url}')

    ### If the image format is not supported by IQDB
    if 'Not an image or image format not supported' in response.text:
        print('Format not supported.')
        erina_log.logerror('[ErinaCaches] [IQDB] Format not supported')
        return {'error': 'format not supported'}


###### IQDB SCRAPING
    iqdb = BeautifulSoup(response.text, 'html.parser')

##### Search for the IQDB result
    try:
        tables = iqdb.find_all('table')
        search_result = tables[1].findChildren("th")[0].get_text()
    except Exception as e:
        erina_log.logerror(f'[ErinaCaches] [IQDB] Client Error, Error details: {str(e)}')
        return {'error': 'client error', 'error_details': e}

##### Verify if the result is relevant or not
    iqdb_tags = []
    if search_result == 'No relevant matches':
        erina_log.logerror('[ErinaCaches] [IQDB] No relevant matches found')
        return {'error': 'not found'}
    else:
        try:
            ### Getting the tags from IQDB
            alt_string = tables[1].findChildren("img")[0]['alt']
            iqdb_tags = alt_string.split('Tags: ')[1].split(' ')
        except:
            iqdb_tags = []
    
    #### Getting the Database URL from IQDB
    try:
        url = tables[1].find_all('td', attrs={'class': 'image'})[0].findChildren('a')[0]['href']
        url = 'https://' + url.split('//')[1]
    except:
        url = ''

    #### Getting the result image size
    try:
        size = tables[1].find_all('tr')[3].get_text().split(' [')[0]
    except:
        size = ''

    #### Getting the image rating (if it is NSFW or not) 
    if tables[1].find_all('tr')[3].get_text().split()[1].replace('[', '').replace(']', '').replace(' ', '') == 'Safe':
        is_safe = True
    else:
        is_safe = False

    #### Getting the similarity
    try:
        similarity = tables[1].find_all('tr')[4].get_text().replace('% similarity', '')
    except:
        similarity = ''


    #### Adding the results to the main result variable
    results['iqdb_tags'] = iqdb_tags
    results['url'] = url
    results['size'] = size
    results['is_safe'] = is_safe
    results['similarity'] = similarity


############ FUNCTION DEFINITION FOR RESULTS SCRAPING
    if url.find('gelbooru.') != -1:
        results['database'] = 'gelbooru'
        results['gelbooru_results'] = search_gelbooru(url)
    
    elif url.find('danbooru.') != -1:
        results['database'] = 'danbooru'
        results['danbooru_results'] = search_danbooru(url)

    elif url.find('zerochan.') != -1:
        results['database'] = 'zerochan'
        results['zerochan_results'] = search_zerochan(url)

    elif url.find('konachan.') != -1:
        results['database'] = 'konachan'
        results['konachan_results'] = search_konachan(url)

    elif url.find('yande.re') != -1:
        results['database'] = 'yandere'
        results['yandere_results'] = search_yandere(url)

    elif url.find('anime-pictures.') != -1:
        results['database'] = 'anime_pictures'
        results['anime_pictures_results'] = search_animepictures(url)

    elif url.find('e-shuushuu') != -1:
        results['database'] = 'e_shuushuu'
        results['e_shuushuu_results'] = search_eshuushuu(url)


#################### CACHING ########## 

    new_cache_content = []
    new_cache_content.append('   --- IQDB CACHE ---   ')
    new_cache_content.append('')
    
    new_cache_content.append('IQDB Tags: ' + create_erina_list(results['iqdb_tags']))
    new_cache_content.append('URL: ' + results['url'])
    new_cache_content.append('Size: ' + results['size'])
    new_cache_content.append('isSafe: ' + str(results['is_safe']))
    new_cache_content.append('Similarity: ' + results['similarity'])
    new_cache_content.append('Database: ' + results['database'])
    new_cache_content.append('')

    if results['database'] == 'gelbooru':
        
        new_cache_content.append('Gelbooru Characters: ' + create_erina_list(results['gelbooru_results']['characters']))
        new_cache_content.append('Gelbooru Copyrights: ' + create_erina_list(results['gelbooru_results']['copyrights']))
        new_cache_content.append('Gelbooru Metadatas: ' + create_erina_list(results['gelbooru_results']['metadatas']))
        new_cache_content.append('Gelbooru Tags: ' + create_erina_list(results['gelbooru_results']['tags']))

        new_cache_content.append('Gelbooru ID: ' + results['gelbooru_results']['id'])
        new_cache_content.append('Gelbooru Size: ' + results['gelbooru_results']['size'])
        new_cache_content.append('Gelbooru Source: ' + results['gelbooru_results']['source'])
        new_cache_content.append('Gelbooru Rating: ' + results['gelbooru_results']['rating'])
        new_cache_content.append('Gelbooru Date: ' + results['gelbooru_results']['date'])
        new_cache_content.append('Gelbooru Uploader: ' + results['gelbooru_results']['uploader'])
        new_cache_content.append('Gelbooru Score: ' + results['gelbooru_results']['score'])
        

    elif results['database'] == 'danbooru':

        new_cache_content.append('Danbooru Artists: ' + create_erina_list(results['danbooru_results']['artists']))
        new_cache_content.append('Danbooru Characters: ' + create_erina_list(results['danbooru_results']['characters']))
        new_cache_content.append('Danbooru Copyrights: ' + create_erina_list(results['danbooru_results']['copyrights']))
        new_cache_content.append('Danbooru Metadatas: ' + create_erina_list(results['danbooru_results']['metadatas']))
        new_cache_content.append('Danbooru Tags: ' + create_erina_list(results['danbooru_results']['tags']))

        new_cache_content.append('Danbooru ID: ' + results['danbooru_results']['id'])
        new_cache_content.append('Danbooru Uploader: ' + results['danbooru_results']['uploader'])
        new_cache_content.append('Danbooru Date: ' + results['danbooru_results']['date'])
        new_cache_content.append('Danbooru Content Size: ' + results['danbooru_results']['content_size'])
        new_cache_content.append('Danbooru Format: ' + results['danbooru_results']['format'])
        new_cache_content.append('Danbooru Size: ' + results['danbooru_results']['size'])
        new_cache_content.append('Danbooru Source: ' + results['danbooru_results']['source'])
        new_cache_content.append('Danbooru Rating: ' + results['danbooru_results']['rating'])
        new_cache_content.append('Danbooru Score: ' + results['danbooru_results']['score'])
        new_cache_content.append('Danbooru Favorites: ' + results['danbooru_results']['favorites'])
        new_cache_content.append('Danbooru Status: ' + results['danbooru_results']['status'])
        
        
    elif results['database'] == 'zerochan':
        new_cache_content.append('Zerochan ID: ' + results['zerochan_results']['id'])
        new_cache_content.append('Zerochan Uploader: ' + results['zerochan_results']['uploader'])
        new_cache_content.append('Zerochan Content URL: ' + results['zerochan_results']['content_url'])
        new_cache_content.append('Zerochan Thumbnail: ' + results['zerochan_results']['thumbnail'])
        new_cache_content.append('Zerochan Format: ' + results['zerochan_results']['format'])
        new_cache_content.append('Zerochan Post Date: ' + results['zerochan_results']['post_date'])
        new_cache_content.append('Zerochan Name: ' + results['zerochan_results']['name'])
        new_cache_content.append('Zerochan Width: ' + results['zerochan_results']['width'])
        new_cache_content.append('Zerochan Height: ' + results['zerochan_results']['height'])
        new_cache_content.append('Zerochan Content Size: ' + results['zerochan_results']['content_size'])
        new_cache_content.append('Zerochan Mangaka: ' + results['zerochan_results']['mangaka'])
        new_cache_content.append('Zerochan Series: ' + results['zerochan_results']['series'])
        new_cache_content.append('Zerochan Character: ' + results['zerochan_results']['character'])
        new_cache_content.append('Zerochan Source: ' + results['zerochan_results']['source'])
    

    elif results['database'] == 'konachan':
        
        new_cache_content.append('Konachan Copyrights: ' + create_erina_list(results['konachan_results']['copyrights']))
        new_cache_content.append('Konachan Styles: ' + create_erina_list(results['konachan_results']['styles']))
        new_cache_content.append('Konachan Artists: ' + create_erina_list(results['konachan_results']['artists']))
        new_cache_content.append('Konachan Characters: ' + create_erina_list(results['konachan_results']['characters']))
        new_cache_content.append('Konachan Tags: ' + create_erina_list(results['konachan_results']['tags']))
        new_cache_content.append('Konachan Favorited By: ' + create_erina_list(results['konachan_results']['favorited_by']))
        
        new_cache_content.append('Konachan ID: ' + results['konachan_results']['id'])
        new_cache_content.append('Konachan Size: ' + results['konachan_results']['size'])
        new_cache_content.append('Konachan Source: ' + results['konachan_results']['source'])
        new_cache_content.append('Konachan Rating: ' + results['konachan_results']['rating'])
        new_cache_content.append('Konachan Date: ' + results['konachan_results']['date'])
        new_cache_content.append('Konachan Uploader: ' + results['konachan_results']['uploader'])
        new_cache_content.append('Konachan Score: ' + results['konachan_results']['score'])

    elif results['database'] == 'yandere':
        
        new_cache_content.append('Yandere Copyrights: ' + create_erina_list(results['yandere_results']['copyrights']))
        new_cache_content.append('Yandere Styles: ' + create_erina_list(results['yandere_results']['styles']))
        new_cache_content.append('Yandere Artists: ' + create_erina_list(results['yandere_results']['artists']))
        new_cache_content.append('Yandere Characters: ' + create_erina_list(results['yandere_results']['characters']))
        new_cache_content.append('Yandere Tags: ' + create_erina_list(results['yandere_results']['tags']))
        new_cache_content.append('Yandere Favorited By: ' + create_erina_list(results['yandere_results']['favorited_by']))
        
        new_cache_content.append('Yandere ID: ' + results['yandere_results']['id'])
        new_cache_content.append('Yandere Size: ' + results['yandere_results']['size'])
        new_cache_content.append('Yandere Source: ' + results['yandere_results']['source'])
        new_cache_content.append('Yandere Rating: ' + results['yandere_results']['rating'])
        new_cache_content.append('Yandere Date: ' + results['yandere_results']['date'])
        new_cache_content.append('Yandere Uploader: ' + results['yandere_results']['uploader'])
        new_cache_content.append('Yandere Score: ' + results['yandere_results']['score'])

    elif results['database'] == 'anime_pictures':

        new_cache_content.append('Anime-Pictures ID: ' + results['anime_pictures_results']['id'])
        new_cache_content.append('Anime-Pictures Uploader: ' + results['anime_pictures_results']['uploader'])
        new_cache_content.append('Anime-Pictures Last Editing User: ' + results['anime_pictures_results']['last_editing_user'])
        new_cache_content.append('Anime-Pictures Post Date: ' + results['anime_pictures_results']['post_date'])
        new_cache_content.append('Anime-Pictures Published Date: ' + results['anime_pictures_results']['published_date'])
        new_cache_content.append('Anime-Pictures Download Count: ' + results['anime_pictures_results']['download_count'])
        new_cache_content.append('Anime-Pictures Size: ' + results['anime_pictures_results']['size'])
        new_cache_content.append('Anime-Pictures Aspect Ratio: ' + results['anime_pictures_results']['aspect_ratio'])
        new_cache_content.append('Anime-Pictures Content Size: ' + results['anime_pictures_results']['content_size'])
        new_cache_content.append('Anime-Pictures Artefacts Degree: ' + results['anime_pictures_results']['artefacts_degree'])
        new_cache_content.append('Anime-Pictures Smooth Degree: ' + results['anime_pictures_results']['smoothness_degree'])
        new_cache_content.append('Anime-Pictures Complexity: ' + results['anime_pictures_results']['complexity'])
        new_cache_content.append('Anime-Pictures Copyright: ' + results['anime_pictures_results']['copyright'])
        new_cache_content.append('Anime-Pictures Artist: ' + results['anime_pictures_results']['artist'])
        new_cache_content.append('Anime-Pictures Average Color: ' + create_erina_list(results['anime_pictures_results']['average_color']))
        new_cache_content.append('Anime-Pictures References: ' + create_erina_list(results['anime_pictures_results']['references']))
        new_cache_content.append('Anime-Pictures Objects: ' + create_erina_list(results['anime_pictures_results']['objects']))
        new_cache_content.append('Anime-Pictures Similar Images: ' + create_erina_list(results['anime_pictures_results']['similar_images_id']))
        new_cache_content.append('Anime-Pictures Artist Links: ' + create_erina_list(results['anime_pictures_results']['artist_links']))

    elif results['database'] == 'e_shuushuu':

        new_cache_content.append('E-Shuushuu Posting Uploader: ' + results['e_shuushuu_results']['uploader'])
        new_cache_content.append('E-Shuushuu Posting Post Date: ' + results['e_shuushuu_results']['post_date'])
        new_cache_content.append('E-Shuushuu Posting Filename: ' + results['e_shuushuu_results']['filename'])
        new_cache_content.append('E-Shuushuu Posting Original Filename: ' + results['e_shuushuu_results']['original_filename'])
        new_cache_content.append('E-Shuushuu Posting Content Size: ' + results['e_shuushuu_results']['content_size'])
        new_cache_content.append('E-Shuushuu Posting Size: ' + results['e_shuushuu_results']['size'])
        new_cache_content.append('E-Shuushuu Posting Favorites: ' + results['e_shuushuu_results']['favorites'])
        new_cache_content.append('E-Shuushuu Posting Image Rating: ' + results['e_shuushuu_results']['image_rating'])

        new_cache_content.append('E-Shuushuu Tags: ' + create_erina_list(results['e_shuushuu_results']['tags']))
        new_cache_content.append('E-Shuushuu Sources: ' + create_erina_list(results['e_shuushuu_results']['sources']))
        new_cache_content.append('E-Shuushuu Characters: ' + create_erina_list(results['e_shuushuu_results']['characters']))
        new_cache_content.append('E-Shuushuu Artists: ' + create_erina_list(results['e_shuushuu_results']['artists']))


    new_cache_content.append('')
    new_cache_content.append('Cache Timestamp: ' + str(datetime.timestamp(datetime.today())))
    new_cache_content.append('Cache Timestamp (formatted): ' + today() + ' at ' + current_time())

    new_cache_destination  = env_information.erina_dir + '/ErinaCaches/IQDB_Cache/'
    new_cache_filename = str(image_hash) + '.erina'
    erina_log.logcaches(f'Caching IQDB and {results["database"]} data...')
    write_file(file_title=new_cache_filename, text=new_cache_content, destination=new_cache_destination)
    return results