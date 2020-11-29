import time
import requests

print("")
print("")
print("")
print("Timing Test")
print("[Erina Search API] query: Konosuba")
print("")

old_start_time = time.time()
requests.get("https://animenosekai.herokuapp.com/erina/api/search?title=konosuba")
old_end_time = time.time()
print("Current API: " + str(round(old_end_time - old_start_time, 2)) + "sec.")

new_start_time = time.time()
requests.get("http://127.0.0.1:5000/erina/api/search?anime=konosuba&minify=true")
new_end_time = time.time()
print("New API: " + str(round(new_end_time - new_start_time, 2)) + "sec.")

print("")
print("--> " + str(round(float(old_end_time - old_start_time) / float(new_end_time - new_start_time), 2)) + "x faster")

print("")
print("© Anime no Sekai — 2020")
print("")
print("")
print("")
print("")