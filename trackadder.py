import tidalapi
import os
from time import sleep
import requests

csv = open("%s/tracks.csv" % os.getcwd(), "r")

contents = csv.read()
lines = contents.split('\n')
line_qty = len(lines)-2

data = []
all_playlists = ()
for line in lines:
    data.append(line.split('_'))
# playlists_id = set()
# track_id = list()
# playlists_name = list()
# for i in range(line_qty):
#     playlists_id.add(data[i][2])
#     track_id.append(data[i][1])
#     playlists_name.append(data[i][0])

# print(playlists_id)
# print(track_id)

session = tidalapi.Session()
session.login("test_email", "test_pass") # Todo: .env / getopt implementation

user = tidalapi.User(session, session.user.id)
user_playlists = user.playlists()
index = 0
for playlist in user_playlists:
    for i in range(line_qty):
        if playlist.name in data[i][0]:
            index += 1
            data[i][2] = playlist.id

# playlist1 = session.get_playlist(user_playlists[0].id)
# print(playlist1.id, playlist1.name, data[0][2])

# print(session.get_track(111034165).name)

# print(data)

# path = "playlists/%s/items" % data[0][2]
# param = None #{"trackIds":94101671, "onDupes":"FAIL"}
# data = {"lastUpdated":1578934573932, "addedItemIds": [111034165]}
# response = session.request("POST", path, param, data)
# playlist5_id = data[0][2]
# print(data[0][2])

# playlist5_id = data[0][2]
# url = 'https://api.tidal.com/v1/playlists/' + playlist5_id + '/items'
# r = requests.request(
#                     'POST',
#                     url,
#                     data={'trackIds':data[0][1]},
#                     headers={
#                         'x-tidal-sessionid': session.session_id,
#                         'if-none-match': "*"
#                     },
#                     params={
#                         'countryCode': 'NL'
#                     }
#                 )

for i in range(line_qty):
    playlist_id = data[i][2]
    url = 'https://api.tidal.com/v1/playlists/' + playlist_id + '/items'
    r = requests.request(
                        'POST',
                        url,
                        data={'trackIds':data[i][1]},
                        headers={
                            'x-tidal-sessionid': session.session_id,
                            'if-none-match': "*"
                        },
                        params={
                            'countryCode': 'NL'
                        }
                    )

# Post request to https://listen.tidal.com/v1/playlists/e16ea28c-cc13-404c-911a-17e9ed0f85e2/items?countryCode=NL to add track to playlist
#
# lastUpdated: 1578922702477
# addedItemIds: [114833547]
#   0: 114833547
