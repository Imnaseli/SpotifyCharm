import json
from urllib import response
import requests
from secret import *
from refresh import *
from datetime import date

class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""
        
    def FindSongs(self):
        print("Finding songs in playlist...")
        
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_weekly_id)
        
        response = requests.get(query,
                               headers = {
                                   "Content-Type": "application/json",
                                   "Authorization": "Bearer {}".format(self.spotify_token)
                               })
        
        response_json = response.json()
        print(response)
        # print(response_json)
        
        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]
        
        self.AddToPlaylist()
        
    
    def CreatePlaylist(self):
        print("Trying to create Playlist...")
        
        today = date.today()
        todayformatted = today.strftime("%d/%m/%y")
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_token)
        
        request_body = json.dumps({
                'name' : todayformatted +  " discover",
                'description' :"Discover Weekly saved by That one night you didnt slle scripting python",
                'public':True
        })
        
        response = requests.post(
            query,
            data = request_body,
            headers={
                     "Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)
                     }
        )
        response_json = response.json()
        # return response_json["id"]
        print(response_json)
        print(response)

    def AddToPlaylist(self):
        print("Adding Songs to created playlist...")
        self.new_playlist_id = self.CreatePlaylist()
        
        
        
        query = "https://api.spotify.com/v1/playlists/{}/tracks?={}".format(self.new_playlist_id , self.tracks)
        response = requests.post(query ,  headers={
                                                    "Content-Type": "application/json",
                                                    "Authorization": "Bearer {}".format(self.spotify_token)
                                                    }
                                 )
        print(response)
        response_json = response.json
        
        
    def CallRefresh(self):
        print("Refreshing Token")
        refreshcaller = Refresh()
        
        self.spotify_token = refreshcaller.refresh()
        
        self.FindSongs()
        
        
        
# a = SaveSongs()
# a.CallRefresh()