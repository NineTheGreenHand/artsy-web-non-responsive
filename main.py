# This is for the Artsy Project
# This file serves as the backend for this web application
# where user can search for artist.

from flask import Flask
import json
import requests

# The methods below are the helper functions to get the desired information:
# ------------------------------------------------------------------------------------------------------------------
# Gets the token from Artsy: 
def get_token():
   post_url = 'https://api.artsy.net/api/tokens/xapp_token'
   post_keys = {'client_id' : '5b60a14d160f9083f4e3', 'client_secret' : '3a8b6de35a1f4fdca93189129f8d3f22'}
   token = requests.post(post_url, post_keys).json()['token']
   return token

# Gets the artist ids, name, and picture url depend on the user input:
def get_id_name_picURL(input):
   token = get_token()
   search_url = 'https://api.artsy.net/api/search'
   search_keys = {'q' : input, 'size' : '10'}
   headers = {'X-XAPP-Token' : token}
   search_result_dict = requests.get(search_url, search_keys, headers=headers).json()

   # need to check if there are any results, if no result, return empty dict:
   if (search_result_dict['total_count'] == 0):
      return {'artists' : []}

   # else, we continue:
   search_result = search_result_dict['_embedded']['results']
   # Filter the 'og_type' is 'artist' only:
   result_dict = [x for x in search_result if x['og_type'] == 'artist']
   result_len = len(result_dict)
   artists = [] # for each entry in the dict, the order is {'id' : id, 'name' : name, 'picURL' : picURL}
   for idx in range(result_len):
      id = result_dict[idx]['_links']['self']['href'].partition('https://api.artsy.net/api/artists/')[2]
      name = result_dict[idx]['title']
      picURL = result_dict[idx]['_links']['thumbnail']['href']
      artist = {'id' : id, 'name' : name, 'picURL' : picURL}
      artists.append(artist)
   return {'artists' : artists} # this is a python dict, need to use json.dumps() before send it back to frontend

# Gets the artist name, birthday, deathday, and biography depend on the artist id:
def get_bio(id):
   artist_url = 'https://api.artsy.net/api/artists/' + id
   token = get_token()
   headers = {'X-XAPP-Token' : token}
   artist_info = requests.get(artist_url, headers=headers).json()
   bio = {'name' : artist_info['name'], \
      'birthday' : artist_info['birthday'], \
      'deathday' : artist_info['deathday'], \
      'nationality' : artist_info['nationality'], \
      'bio' : artist_info['biography']}
   return bio  # this is a python dict, need to use json.dumps() before send it back to frontend
# ------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)

# This is the main page
@app.route('/')
def main_page():
   return app.send_static_file('artsyproject.html')

# When user insert input in the search bar, result returned into this page:
@app.route("/centaurus/search_info/<userInput>", methods=["GET"])
def search_info(userInput):
   artists = get_id_name_picURL(userInput)
   return json.dumps(artists)

@app.route("/centaurus/search_bio/<artistID>", methods=["GET"])
def search_bio(artistID):
   artist_bio = get_bio(artistID)
   return json.dumps(artist_bio)

if __name__ == '__main__':
   # This is used when running locally only. When deploying to Google App
   # Engine, a webserver process such as Gunicorn will serve the app. You
   # can configure startup instructions by adding `entrypoint` to app.yaml.
   app.run(debug=True)