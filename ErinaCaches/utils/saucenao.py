import datetime
from saucenao_api.containers import BookSauce, VideoSauce

def erina_from_api(api_results):
    cache_content = f"""   --- SAUCENAO CACHE ---   
Similarity: {str(api_results.similarity)}
Index ID: {str(api_results.index_id)}
Index Name: {str(api_results.index_name)}
Title: {str(api_results.title)}
URL: {str(api_results.url)}
Author: {str(api_results.author)}
Thumbnail: {str(api_results.thumbnail)}
"""
    if isinstance(api_results, BookSauce):
        cache_content += "isManga: True\n"
        cache_content += "isAnime: False\n"
        cache_content += f"Part: {str(api_results.part)}\n"
    elif isinstance(api_results, VideoSauce):
        cache_content += "isManga: False\n"
        cache_content += "isAnime: True\n"
        cache_content += f"Episode: {str(api_results.part)}\n"
        cache_content += f"Year: {str(api_results.year)}\n"
        cache_content += f"Estimated Time: {str(api_results.est_time)}\n"
    else:
        cache_content += "isManga: False\n"
        cache_content += "isAnime: False\n"
        
    cache_content += "\n"
    cache_content += f"Cache Timestamp: + {str(datetime.timestamp(datetime.today()))}"
    return cache_content