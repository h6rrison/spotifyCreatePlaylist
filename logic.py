import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred


def get_artist_id(sp,artist:str)->str:
    result = sp.search(q=artist, type='artist')
    artist = result['artists']['items'][0]
    artist_id = artist['id']
    return artist_id


def get_artist_top_tracks(sp,id):
    all_tracks = []
    for a in id:
        tracks = sp.artist_top_tracks(a)['tracks']
        all_tracks.append(tracks)
    return all_tracks


def create_playlist(sp,selection,playlist_name,playlist_des,id): #takes a list of track uris
    playlists = sp.current_user_playlists()
    for p in playlists['items']:
        if p['name'] == playlist_name:
            playlist_id = p['id']
            sp.user_playlist_add_tracks(user = sp.current_user()['id'], playlist_id=playlist_id,tracks=id)
            return

    pl = sp.user_playlist_create(user= sp.current_user()['id'], name = playlist_name, description= playlist_des)
    sp.user_playlist_add_tracks(user = sp.current_user()['id'], playlist_id=pl['id'],tracks=id)


def handle_selection(selection):
    scopes = 'user-top-read user-read-recently-played playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id,
                        client_secret=cred.client_secret, redirect_uri=cred.redirect_url, scope=scopes))
    recent = False
    if selection == 'top artists':
        results = sp.current_user_top_artists(limit=50) #time range
    elif selection == 'top songs':
        results = sp.current_user_top_tracks(limit=50)
    else:
        recent = True #requires new scope
        results = sp.current_user_recently_played()

    track_uris=[]
    names = []
    if recent:
        for item in results['items']:
            track = item['track']
            track_uris.append(track['uri'])
            names.append(track['name'])
    else:
        for item in results['items']:
            names.append(item['name'])
            try:
                track_uris.append(item['uri'])
            except spotipy.exceptions.SpotifyException:
                print("Track selection is unsuccessful")

    return {'sp': sp, 'names' : names, 'ids' : track_uris}
