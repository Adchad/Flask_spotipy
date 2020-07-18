import flask
from plyer import notification
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import time


app = flask.Flask(__name__)


username = 'YOUR-USER-NAME'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id='YOUR-CLIENT-ID',
                                   client_secret='YOUR-CLIENT-SECRET',
                                   redirect_uri='YOUR-REDIRECT-URL')

def change_song(songQuery):
    msg = ""
    if token:
        sp = spotipy.Spotify(auth=token)
        devices = sp.devices()
        deviceID = devices['devices'][0]['id']
        print("Device Name : " + devices['devices'][0]['name'])
        track = sp.current_user_playing_track()
        artist = track['item']['artists'][0]['name']
        track = track['item']['name']

        if artist !="":
            print("Currently playing " + artist + " - " + track)

        searchQuery = songQuery
        searchResults = sp.search(searchQuery,1,0,"track")

        trackURI = searchResults['tracks']['items'][-1]['uri']
        print(trackURI)

        time.sleep(1)
        sp.start_playback(deviceID, None, [trackURI])

        time.sleep(1)
        track = sp.current_user_playing_track()
        artist = track['item']['artists'][0]['name']
        track = track['item']['name']

        if artist !="":
            msg = "Currently playing " + artist + " - " + track
            print(msg)

    else:
        print("Can't get token for", username)

    return artist, track




def ntfy(titl,msg):
    notification.notify(
        title=titl,
        message=msg,
        timeout=5,  # seconds
    )




@app.route('/test', methods =['POST'])
def test():
    print("test\n")
    data= flask.request.get_data()
    real_text = str(data)[2:-1]
    print(real_text)
    artist, track = change_song(real_text)
    ntfy("Currently Playing : ",artist + " - " + track)
    return ""
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
