from secrets import tidal_id, tidal_id_2, tidal_username, tidal_username_2, tidal_pwd, tidal_pwd_2, spotify_id, spotify_id_2, spotify_username, spotify_username_2, spotify_discover_weekly_id, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import sys
import tidalapi
import time
from pprint import pprint

# Options:
# connect_to_spotify()
# connect_to_tidal(tidal_username, tidal_pwd)
# delete_all_tidal_playlists(tidal_id, tidal_session)
# move_all_tidal_playlists_to_spotify()
# move_one_tidal_playlist_to_spotify(playlist_id)
# move_all_spotify_playlists_to_tidal()
# move_favourites_from_spotify_to_tidal()
# move_discover_weekly_from_spotify_to_tidal()
# copy_tidal_playlists_to_another_tidal_account()
# MIGRATE SPOTIFY ACCOUNT = COPY PLAYLISTS + SAVED TRACKS
# copy_spotify_playlists_to_another_spotify_account()
# copy_spotify_saved_tracks_to_another_spotify_account()

# Endpoints not in tidalapi
def get_tidal_create_playlist_url(tidal_id):
    return 'https://listen.tidal.com/v1/users/' + tidal_id + '/playlists'
def get_tidal_add_track_to_playlist_url(playlist_id):
    return 'https://listen.tidal.com/v1/playlists/' + playlist_id + '/items'
def get_tidal_find_track_url():
    return 'https://listen.tidal.com/v1/search/tracks'
def get_tidal_playlist(playlist_id):
    return 'https://listen.tidal.com/v1/playlists/' + playlist_id
def get_tidal_user_playlists(tidal_id):
    return 'https://listen.tidal.com/v1/users/' + tidal_id + '/playlists'


tidal_oldplaylists = []


def connect_to_tidal(tidal_username, tidal_pwd):
    tidal_session = tidalapi.Session()
    try:
        tidal_session.login(tidal_username, tidal_pwd)
    except requests.exceptions.HTTPError as e:
        print("Can't login to tidal for username=" + tidal_username + ", password=" + tidal_pwd)
        sys.exit()
    return tidal_session

    offset = 0
    spotify_favourites = _get_spotify_favourites(offset)
    while spotify_favourites:
        for item in spotify_favourites['items']:
            track = item['track']
            track_id = _search_for_track_on_tidal(
                track['name'], track['artists'][0]['name']
            )
            if track_id > 0:
                user_favourites.add_track(track_id)
        offset = offset + 20
        spotify_favourites = _get_spotify_favourites(offset)


def delete_all_tidal_playlists(tidal_id, tidal_session):
    try:
        r = requests.request(
            'GET',
            get_tidal_user_playlists(tidal_id),
            headers={
                'x-tidal-sessionid': tidal_session.session_id,
                'if-none-match': '*'
            },
            params={
                'countryCode': 'US',
                'limit': 999
            }
        )
        playlists = [item['uuid'] for item in r.json()['items']]
    except requests.exceptions.RequestException as e:
        print("Could not get list of playlists")

    if playlists:
        for playlist in playlists:
            try:
                r = requests.request(
                    'DELETE',
                    get_tidal_playlist(playlist),
                    headers={
                        'x-tidal-sessionid': tidal_session.session_id,
                    },
                    params={
                        'countryCode': 'US'
                    }
                )
            except requests.exceptions.RequestException as e:
                print("Could not delete playlist " + playlist_id)


def move_all_tidal_playlists_to_spotify():
    pass
    # _add_tracks_to_spotify_playlist(track_ids, spotify_playlist_id)


def move_one_tidal_playlist_to_spotify(playlist_id):
    pass
    # _add_tracks_to_spotify_playlist(track_ids, spotify_playlist_id)

def copy_tidal_playlists_to_another_tidal_account():
    get_tidal_old_playlists(tidal_id_2, tidal_session_2)
    playlists_to_copy = tidal_session_2.get_user_playlists(tidal_id)
    i=1
    for playlist in playlists_to_copy:
        #check if playlist with a same name already exists
        if playlist.name not in tidal_oldplaylists:
                print("Working on playlist " + str(i) + "/" + str(len(playlists_to_copy)) + ": " + playlist.name)
                playlist_id = _create_tidal_playlist(playlist.name, tidal_id_2, tidal_session_2)
                tracks = tidal_session_2.get_playlist_tracks(playlist.id)
                #add tracks to playlist_id
                _add_tracks_to_tidal_playlist(playlist_id, tracks, tidal_session_2)
        else:
                print("A playlist with name " + playlist.name + " already exists in TIDAL. Skipping...")
        i+=1

def _add_playlist_to_tidal(playlist, tidal_session, tracks=None, playlist_name=None):
    playlist_name_catch = playlist_name if playlist_name else playlist['name']
    playlist_id = _create_tidal_playlist(playlist_name_catch, tidal_id, tidal_session)

    if not playlist_id:
        return

    sanitized_tracks = []
    def _add_track_to_sanitized_list(tracks):
        for i, item in enumerate(tracks['items']):
            track = item['track']
            sanitized_tracks.append([
                track['name'], track['artists'][0]['name']
            ])

    tracks_catch = tracks if tracks else sp.user_playlist(playlist['owner']['id'], playlist['id'], fields="tracks,next")['tracks']
    _add_track_to_sanitized_list(tracks_catch)
    while tracks_catch['next']:
        tracks_catch = sp.next(tracks_catch)
        _add_track_to_sanitized_list(tracks_catch)
    _add_tracks_to_tidal_playlist(playlist_id, sanitized_tracks, tidal_session)


def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

def _add_tracks_to_tidal_playlist(playlist_id, tracks, tidal_session):
    url = get_tidal_add_track_to_playlist_url(playlist_id)
    #print(len(tracks))
    #for track in tracks:
#	print("INIZIO")
#	dump(track)
#	print("FINE")
    for track in tracks:
        tidal_track_id = track.id
        if tidal_track_id > -1:
            try:
                r = requests.request(
                    'POST',
                    url,
                    data={'trackIds':tidal_track_id, 'toIndex':1},
                    headers={
                        'x-tidal-sessionid': tidal_session.session_id,
                        'if-none-match': "*"
                    },
                    params={
                        'countryCode': 'US'
                    }
                )
            except requests.exceptions.RequestException as e:
                print('Error adding tracks to playlist: ' + e)
                # TODO: should add playlist name to CSV of failures

def get_tidal_old_playlists(tidal_id, tidal_session):
    try:
        r = requests.request(
            'GET',
            get_tidal_user_playlists(tidal_id),
            headers={
                'x-tidal-sessionid': tidal_session.session_id,
                'if-none-match': '*'
            },
            params={
                'countryCode': 'US',
                'limit': 999
            }
        )
        playlists = [item['title'] for item in r.json()['items']]
    except requests.exceptions.RequestException as e:
        print("Could not get list of playlists")
    if playlists:
        for playlist in playlists:
                tidal_oldplaylists.append(playlist)


def _search_for_track_on_tidal(name, artist):
    id = -1;
    artist = artist.lower()

    def _artist_in_response(track):
        for response_artist in track['artists']:
            if response_artist['name'].lower() == artist:
                return True
        return False

    matched_artist = False
    offset = 0
    limit = 300
    end_of_track_list = False
    while not matched_artist and not end_of_track_list:
        try:
            r = requests.request(
                'GET',
                get_tidal_find_track_url(),
                headers={
                    'x-tidal-sessionid': tidal_session.session_id
                },
                params={
                    'offset': offset,
                    'countryCode': 'US',
                    'limit': limit,
                    'query': name
                }
            )

            if len(r.json()['items']) == 0:
                end_of_track_list = True

            for track in r.json()['items']:
                if _artist_in_response(track):
                    id = track['id']
                    matched_artist = True
                    break
            offset = offset + 300
            limit = offset + 300
        except requests.exceptions.RequestException as e:
            print('Could not make request for track name=' + name + ", artist=" + artist)
            # TODO: should add track name to CSV of failures

    if not matched_artist:
        print('Could not find track name=' + name + ", artist=" + artist)
        # TODO: should add track name to CSV of failures

    return id;


def _create_tidal_playlist(playlist_name, tidal_id, tidal_session):
    try:
        r = requests.request(
            'POST',
            get_tidal_create_playlist_url(tidal_id),
            data={'title':playlist_name, 'description':''},
            headers={
                'x-tidal-sessionid': tidal_session.session_id
            },
            params={
                'sessionId': tidal_session.session_id,
                'countryCode': 'US',
                'limit': '999'
            }
        )
    except requests.exceptions.RequestException as e:
        print('Error creating playlist: ' + e)
        # TODO: should add playlist name to CSV of failures
        return None

    return r.json()['uuid']


start = time.time()
#sp, sp_token = connect_to_spotify() #NEEDED ONLY FOR MOVING FROM SPOTIFY TO TIDAL
#tidal_session = connect_to_tidal(tidal_username, tidal_pwd) #NEEDED ONLY FOR 1) MOVING FROM SPOTIFY TO TIDAL 2) MOVING FROM TIDAL1 TO TIDAL2
#tidal_session_2 = connect_to_tidal(tidal_username_2, tidal_pwd_2) #NEEDED ONLY FOR MOVING FROM TIDAL1 TO TIDAL2
# move_discover_weekly_from_spotify_to_tidal()
#move_all_spotify_playlists_to_tidal()
#copy_tidal_playlists_to_another_tidal_account()
#MIGRATE SPOTIFY ACCOUNT = COPY PLAYLISTS + SAVED TRACKS
end = time.time()
print("Time elapsed: " + str(end - start) + " s (" + str((end-start)/60) + " min)")