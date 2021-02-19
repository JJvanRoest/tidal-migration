import tidalapi
import os

session = tidalapi.Session()

session.login("test_email", "test_pass") # Todo: implement .env / getopt
user = tidalapi.User(session, session.user.id)
playlists = user.playlists()

# trackarray = []
# tracks = session.get_playlist_tracks("5a5fe3ff-2d4c-4bcd-90ab-0feb730cc27a")
print("Putting tracks in: %s/tracks.csv" % os.getcwd())
csv = open("%s/tracks.csv" % os.getcwd(), "w")

for playlist in playlists:
    tracks = session.get_playlist_tracks(playlist.id)
    for track in tracks:
        csv.write("%s_%d_%s\n" % (playlist.name, track.id, playlist.id))

csv.close()

