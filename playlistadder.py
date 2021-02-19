import tidalapi
import os

csv = open("%s/tracks.csv" % os.getcwd(), "r")

contents = csv.read()
lines = contents.split('\n')
line_qty = len(lines)-2

data = []
all_playlists = ()
for line in lines:
    data.append(line.split('_'))
playlists_names = set()
for i in range(line_qty):
    playlists_names.add(data[i][0])

session = tidalapi.Session()
session.login("test_email", "env_pass") # Todo use .env / getopt

path = "users/{session.user.id}/playlists?countryCode=NL"
param = None
data ={"title": "%s" % "test", "numberOfTracks": 0, "numberOfVideos": 0, "creator": {"id": session.user.id}, "description": "", "type": "USER", "publicPlaylist": "false"}
req = session.request("POST", path, param, data)

print(req.headers, req.text)
# for playlists_name in playlists_names:
    # path = "users/{session.user.id}/playlists?countryCode=NL"
    # param = None
    # data ={"title": "%s" % playlists_name, "numberOfTracks": 0, "numberOfVideos": 0, "creator": {"id": {session.user.id}}, "description": "", "type": "USER", "publicPlaylist": "false"}
    # session.request("POST", path, param, data)

# Post request to https://listen.tidal.com/v1/users/{session.user.id}/playlists?countryCode=NL in order to create playlist
#
# uuid: "e16ea28c-cc13-404c-911a-17e9ed0f85e2"
# title: "Test"
# numberOfTracks: 0
# numberOfVideos: 0
# creator: {id: {session.user.id}}
#   id: {session.user.id}
# description: ""
# duration: 0
# lastUpdated: "2020-01-13T13:35:55.675+0000"
# created: "2020-01-13T13:35:55.675+0000"
# type: "USER"
# publicPlaylist: false
# url: "http://www.tidal.com/playlist/e16ea28c-cc13-404c-911a-17e9ed0f85e2"
# image: "e59903d7-94a7-454c-8a78-6a6586967dda"
# popularity: 0
# squareImage: "e9448a9a-3ade-4f79-93d2-12e6d8d4b2eb"

# Post request to https://listen.tidal.com/v1/playlists/e16ea28c-cc13-404c-911a-17e9ed0f85e2/items?countryCode=NL to add track to playlist
#
# lastUpdated: 1578922702477
# addedItemIds: [114833547]
#   0: 114833547