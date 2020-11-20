import datetime

def erina_from_data(image_hash, database_path, similarity, anilist_id):
    cache_content = f"""
AniList ID: {str(anilist_id)}
Path: {str(database_path)}
Hash: {str(image_hash)}
Similarity: {str(similarity)}

Cache Timestamp: {str(datetime.timestamp(datetime.today()))}
"""
    return cache_content