# -*- coding: utf-8 -*-
from mutagen import File
from mutagen import id3
from pyItunes import Library
import os
import warnings
import shutil
import json
from commons import decode_aes

white_space = ' \t\n\r'
for i in range(0, 32):
    white_space += chr(i)


class SyncManager(object):

    def __init__(self):
        pass

    @classmethod
    def new_library_manager(cls, kind, root_path):
        if kind is 'iTunes':
            return iTunesMusicLibraryManager(root_path)
        elif kind is 'Netease':
            return NeteaseMusicLibraryManager(root_path)
        else:
            return BaseLibraryManager(root_path)


class BaseLibraryManager(object):

    def __init__(self, root_path, name=None):
        if name is None:
            self.name = 'Unknown'
        else:
            self.name = name
        self.root_path = os.path.expanduser(root_path)
        self.root_path = unicode(self.root_path)
        print(self.name, self.root_path)

    def load_library(self):
        pass

    def get_all_tracks(self):
        pass


class iTunesMusicLibraryManager(BaseLibraryManager):

    def __init__(self, root_path, name='iTunes'):
        super(iTunesMusicLibraryManager, self).__init__(root_path, name)
        self.__iTunes_library_xml = root_path + '/iTunes Music Library.xml' # no unicode allowed
        self.__iTunes_auto_add_path = self.root_path + u'/iTunes Media/Automatically Add to iTunes.localized'
        self.__tracks = []
        self.load_library()

    def load_library(self):
        print self.__iTunes_library_xml
        l = Library(self.__iTunes_library_xml)
        for id, song in l.songs.items():
            if song.kind == 'MPEG audio file':
                self.__tracks.append(song)

    def pprint(self):
        for song in self.__tracks:
            print song.name, song.location

    def find_by_album_and_name(self, album, name):
        for song in self.__tracks:
            if song.name == name and song.album == album:
                return song.name, song.location
        return None

    def copy_2_iTunes(self, track_file):
        if os.path.isdir(self.__iTunes_auto_add_path) and os.path.exists(self.__iTunes_auto_add_path):
            shutil.copy(track_file, self.__iTunes_auto_add_path)


class NeteaseMusicLibraryManager(BaseLibraryManager):

    def __init__(self, root_path, name='NeteaseMusic'):
        super(NeteaseMusicLibraryManager, self).__init__(root_path, name)
        self.__tracks = []
        self.load_library()

    def load_library(self):
        for filename in os.listdir(self.root_path):
            track_file = self.root_path + u"/" + filename
            try:
                track = NeteaseMusicMeta(track_file)
                self.__tracks.append(track)
                # print track
            except ValueError:
                warnings.warn(u"Track not identified: {0}".format(track_file))

    def get_all_tracks(self):
        return self.__tracks


class MusicMeta(object):

    def __init__(self, track_file):
        self.__type = "MP3"
        self.__track_file = unicode(track_file)
        self.track = self.parse_tags(track_file)

    def parse_tags(self, track_file):
        if track_file.upper().endswith(self.__type) is not True:
            raise ValueError(u'File kind not supported: %s', track_file)

        track = File(unicode(track_file))
        return track

    def __repr__(self):
        return self.track.pprint()

    def get_album(self):
        try:
            return self.track['TALB']
        except KeyError:
            return None

    def set_album(self, album):
        self.track['TALB'] = id3.TALB(encoding=3, text=album)

    def get_name(self):
        try:
            return self.track['TIT2']
        except KeyError:
            return None

    def set_name(self, name):
        self.track['TIT2'] = id3.TIT2(encoding=3, text=name)

    def get_track_file(self):
        return self.__track_file

    def set_artists(self, artist_text):
        self.track['TPE1'] = id3.TPE1(encoding=3, text=artist_text)

    def inspect_tags(self, tags=['TALB', 'TIT2', 'TPE1']):
        if set(tags).issubset(self.track.keys()):
            return True
        else:
            return False

    def save(self):
        self.track.save()


class iTunesMusicMeta(MusicMeta):

    def __init__(self, track_file):
        super(iTunesMusicMeta, self).__init__(track_file)


class NeteaseMusicMeta(MusicMeta):

    def __init__(self, track_file):
        super(NeteaseMusicMeta, self).__init__(track_file)
        self.__music_tags = None
        self.__parse_music_tags()

    def __parse_music_tags(self):
        if "COMM::XXX" in self.track:
            meta_json = str(self.track["COMM::XXX"])
            if meta_json.startswith("163 key"):
                encrypted_json = meta_json.split(':')[1]
                meta_json = decode_aes(encrypted_json)
            meta = meta_json.split(':', 1)
            if meta[0] == 'music':
                json_str = meta[1].strip(white_space)
                # print json_str
                music_tags = json.loads(json_str, encoding="UTF8")
                self.__music_tags = music_tags

    def __parse_netease_music_artist(self):
        artist = ''
        artist_array = self.__music_tags['artist']
        for i in range(len(artist_array)):
            artist = artist + artist_array[i][0]
            if i < len(artist_array) - 1:
                artist += '/'
        return artist

    def is_fixable(self):
        return self.__music_tags is not None

    def fix_ID3(self):
        if self.is_fixable() is True:
            if "TALB" not in self.track or "TIT2" not in self.track or "TPE1" not in self.track:
                if "TALB" not in self.track and "album" in self.__music_tags:
                    self.set_album(self.__music_tags['album'])
                if "TIT2" not in self.track and "musicName" in self.__music_tags:
                    self.set_name(self.__music_tags['musicName'])
                if "TPE1" not in self.track and "artist" in self.__music_tags:
                    self.set_artists(self.__parse_netease_music_artist())
            # copyright
            if "TCOP" in self.track:
                del(self.track['TCOP'])
            # genre
            if "TCON" in self.track:
                del(self.track['TCON'])
