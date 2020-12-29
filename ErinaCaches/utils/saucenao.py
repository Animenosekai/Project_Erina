from datetime import datetime
from saucenao_api.containers import BookSauce, VideoSauce

def erina_from_api(api_results):
    cache_content = """   --- SAUCENAO CACHE ---   
Similarity: {similarity}
Index ID: {indexID}
Index Name: {indexName}
Title: {title}
URL: {link}
Author: {author}
Thumbnail: {thumbnail}
""".format(
    similarity=str(api_results.similarity),
    indexID=str(api_results.index_id),
    indexName=str(api_results.index_name),
    title=str(api_results.title),
    link=str(api_results.urls[0]),
    author=str(api_results.author),
    thumbnail=str(api_results.thumbnail)
)
    if isinstance(api_results, BookSauce):
        cache_content += "isManga: True\n"
        cache_content += "isAnime: False\n"
        cache_content += f"Part: {str(api_results.part)}\n"
    elif isinstance(api_results, VideoSauce):
        cache_content += "isManga: False\n"
        cache_content += "isAnime: True\n"
        cache_content += f"Part: {str(api_results.part)}\n"
        cache_content += f"Year: {str(api_results.year)}\n"
        cache_content += f"Estimated Time: {str(api_results.est_time)}\n"
    else:
        cache_content += "isManga: False\n"
        cache_content += "isAnime: False\n"
        
    cache_content += "\n"
    cache_content += f"Cache Timestamp: + {str(datetime.timestamp(datetime.today()))}"
    return cache_content