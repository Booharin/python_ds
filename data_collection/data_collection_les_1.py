# 1
import requests
import json

repos_url = 'https://api.github.com/users/Booharin/repos'
file_name = 'data.json'
repo_name_key = 'name'


def saveJsonFromUrl(url, json_file_name):
    repos_request = requests.get(url)
    json_data = repos_request.json()
    with open(json_file_name, 'w') as json_file:
        json.dump(json_data, json_file)


def getReposNames(json_file_name):
    with open(json_file_name) as json_file:
        repos_data = json.load(json_file)
        for repo in repos_data:
            try:
                print(repo[repo_name_key])
            except KeyError:
                print(f"{repo_name_key} is unknown key")


saveJsonFromUrl(repos_url,
                file_name)
getReposNames(file_name)

# 2
api_key = 'Your_api_key'


def getVideosForYouTubeChanel(chanelId, max_result, your_api_key):

    params = {'key': your_api_key,
              'channelId': chanelId,
              'order': 'date',
              'maxResults': max_result}

    response = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
    data = response.json()

    try:
        for item in data['items']:
            print(f"https://www.youtube.com/watch?v={item['id']['videoId']}")
    except KeyError:
        print('unknown key')


getVideosForYouTubeChanel('UCE_M8A5yxnLfW0KghEeajjw', 3, api_key)
