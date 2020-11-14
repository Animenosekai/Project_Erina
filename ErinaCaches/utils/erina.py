import datetime

def erina_from_data(image_hash, database_path, similarity):
    cache_content = f"""
Path: {str(database_path)}
Hash: {str(image_hash)}
Similarity: {str(similarity)}

Cache Timestamp: {str(datetime.timestamp(datetime.today()))}
"""
    return cache_content