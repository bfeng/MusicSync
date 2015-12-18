#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from mutagen import File
import os
import json
import base64
import sys
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
    if track.has_key("COMM::XXX"):
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
        raise ValueError(u"Track not identified: %s", track_file)


def append_metadata(track_file, expected_tags):
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


def main():
    path = u'/Users/bfeng/Music/copy'
    for filename in os.listdir(path):
        track_file = path + '/' + filename
        try:
            tags = parse_tags(track_file)
            # print_netease_music_tags(tags)
            append_metadata(track_file, tags)
        except ValueError:
            pass


if __name__ == "__main__":
    main()
