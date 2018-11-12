#! /usr/bin/env python3

import spotipy
import spotipy.util as util


def add_songs_to_playlist(sp):
    failed_songs = []
    with open('./songs.csv', 'r') as file:
        contents = file.read().strip()
        songs = contents.split('\n')
        for song in songs:
            song = song.split(',')
            print('trying ' + song[0])
            result = sp.search(song[0])
            try:
                print('added %s as %s ' % (song[0], result['tracks']['items'][0]['id']))
                # todo add song to playlist
            except IndexError:
                failed_songs.append(','.join(song))
                print('could not add ' + song[0])
                pass
    return failed_songs


# login and get
def login():
    scope = 'playlist-modify-private user-read-private'
    clientID = "4dd19b32eb8549d584eaf92352937014"
    clientSecret = "8aafe169c208461890468df65d53d04f"

    token = util.prompt_for_user_token('kingsukhoi', scope, clientID, clientSecret, 'http://localhost')
    if not token:
        raise SystemError
    return spotipy.Spotify(auth=token)


def main():
    sp = login()
    failed_songs = add_songs_to_playlist(sp)
    print('\n'.join(failed_songs))

# todo add new playlist
# todo add songs to playlist

main()