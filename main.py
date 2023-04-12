from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import random

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    else:
        return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def search_for_show(token, show_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={show_name}&type=show&limit=1&market=US"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["shows"]["items"]
    if len(json_result) == 0:
        print("No show with this name exists...")
        return None
    else:
        return json_result[0]
def get_episodes_by_show(token, show_id, offsetNum):
    # url = f"https://api.spotify.com/v1/shows/{show_id}"
    url = f"https://api.spotify.com/v1/shows/{show_id}/episodes?offset={offsetNum}&limit=50&market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

token = get_token()
podcastName = input("Please enter a podcast: ")
result = search_for_show(token, podcastName)
# print(result["name"])
# print(result["id"])

show_id = result["id"]
num_episodes = result["total_episodes"]
offsetNum = 0
episodeList = []

if(num_episodes > 500):
    print("This might take a couple seconds...")

while offsetNum < num_episodes:
    episodes = get_episodes_by_show(token, show_id, offsetNum)
    for idx, episode in enumerate(episodes):
        # print(f"{idx + 1}. {episode['name']}, {episode['release_date']}")
        episodeList.append(episode)
    offsetNum +=50

done = ""
while done != "done":
    randomEp = random.randint(0,num_episodes - 1)
    print("You should watch '" + episodeList[randomEp]["name"] + "', released on " + episodeList[randomEp]["release_date"] + ".")
    done = input("Press enter to generate another episode or 'done' to exit:  ")
    print()

""" result = search_for_artist(token, "Taylor Swift")
print(result["name"])

artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}") """

