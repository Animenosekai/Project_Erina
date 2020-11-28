from datetime import datetime

def erina_from_data(image_hash, database_path, similarity, anilist_id):
    cache_content = """   --- ERINA CACHE ---   
AniList ID: {anilistID}
Path: {path}
Hash: {hash}
Similarity: {similarity}

Cache Timestamp: {cache_timestamp}
""".format(
    anilistID=str(anilist_id),
    path=str(database_path),
    hash=str(image_hash),
    similarity=str(similarity),
    cache_timestamp=str(datetime.timestamp(datetime.today()))
)
    return cache_content