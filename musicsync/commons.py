# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from mutagen import File
import json
import base64
import sys
import warnings
reload(sys)
sys.setdefaultencoding('utf-8')

key = b'#14ljk_!\]&0U<\'('

PADDING = '{'

cipher = AES.new(key)

white_space = ' \t\n\r'
for i in range(0, 32):
    white_space += chr(i)


def decode_aes(encrypted_content):
    return cipher.decrypt(base64.b64decode(encrypted_content)).rstrip(PADDING).rstrip()


def parse_netease_music_artist(music_tags):
    artist = ''
    artist_array = music_tags['artist']
    for i in range(len(artist_array)):
        artist = artist + artist_array[i][0]
        if i < len(artist_array) - 1:
            artist += ', '
    return artist


def print_netease_music_tags(music_tags):
    print music_tags
    line = ''
    line += parse_netease_music_artist(music_tags)
    title = music_tags['musicName']
    line += '|' + title
    album = music_tags['album']
    line += '|' + album
    print line


def json_loads(meta):
    json_str = meta.strip(white_space)
    try:
        music_tags = json.loads(json_str, encoding="UTF8")
        return music_tags
    except ValueError:
        print repr(json_str)
        return None


def parse_tags(track_file):
    if track_file.lower().endswith("mp3") is not True:
        raise ValueError(u'File type is not supported: %s', track_file)

    track = File(track_file)
    if "COMM::XXX" in track:
        meta_json = str(track["COMM::XXX"])
        if meta_json.startswith("163 key"):
            encrypted_json = meta_json.split(':')[1]
            meta_json = decode_aes(encrypted_json)
        meta = meta_json.split(':', 1)
        if meta[0] == 'music':
            json_str = meta[1].strip(white_space)
            # print json_str
            music_tags = json.loads(json_str, encoding="UTF8")
            return music_tags
        else:
            raise ValueError(u'Music tag not found: %s', track_file)
    else:
        warnings.warn(u"Track not identified: {0}".format(track_file))


def append_metadata(track_file, expected_tags):
    if track_file is None or expected_tags is None:
        return
    metadata = File(track_file, easy=True)
    # print unicode(track_file), "=============>",
    if 'musicName' in expected_tags:
        if 'title' in metadata and len(metadata['title']) > 0:
                metadata['title'][0] = expected_tags['musicName']
        else:
            title = list()
            title.append(expected_tags['musicName'])
            metadata['title'] = title

    if 'album' in expected_tags:
        if 'album' in metadata and len(metadata['album']) > 0:
                metadata['album'][0] = expected_tags['album']
        else:
            album = list()
            album.append(expected_tags['album'])
            metadata['album'] = album

    # album artist is not correct
    if 'artist' in expected_tags:
        artists = []
        artist_array = expected_tags['artist']
        for artist in artist_array:
            artists.append(artist[0])

        metadata['performer'] = artists

    if 'genre' in metadata:
        del(metadata['genre'])

    if 'copyright' in metadata:
        del(metadata['copyright'])

    metadata.save()


def parse_file(track_file):
    if track_file.lower().endswith("mp3") is not True:
        raise ValueError(u'File type is not supported: %s', track_file)
    music_name = track_file.lower()
    music_name = music_name[:music_name.rindex(".mp3")]
    return music_name


def check_iTunes_music(tracks, music_name):
    for song in tracks:
        song_music_name = "{0} - {1}".format(song.artist, song.name).lower()
        if music_name == song_music_name:
            return u"Found"
        elif music_name.find(song.name) >= 0:
            return u"Possible: " + song_music_name
    return u"Nope"


def cp_itunes(iTunes_path, netease_music_path):
    # print "cp_itunes", iTunes_library_xml, netease_music_path

    # Unicode path is not supported for the xml file
    iTunes_library_xml = iTunes_path + '/iTunes Music Library.xml'
    tracks = load_iTunes_library(iTunes_library_xml)

    for filename in os.listdir(netease_music_path):
        music_name = parse_file(filename)
        if check_iTunes_music(tracks, music_name) == u"Nope":
            track_file = netease_music_path + u"/" + filename
            # with open(track_file, "r") as f:
            #     print f.name
            if os.path.exists(track_file):
                tags = parse_tags(track_file)
                # print_netease_music_tags(tags)
                append_metadata(track_file, tags)
                copy_2_iTunes(track_file, iTunes_path)


