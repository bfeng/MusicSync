from mutagen import File


class MusicTrackNumber:

    def __init__(self, a, b):
        self.__a = a
        self.__b = b


class DiscTrackNumber:

    def __init__(self, a, b):
        self.__a = a
        self.__b = b


class NeteaseMusicInfo:

    def __init__(self, track_file):
        self.__song_name = u''
        self.__artist = []
        self.__album = u''
        self.__album_artist = []
        self.__composer = []
        self.__grouping = u''
        self.__genre = u''
        self.__year = None
        self.__track = MusicTrackNumber(0, 0)
        self.__disc = DiscTrackNumber(0, 0)
        self.__kind = "MP3"
        self.__comment = u''
        self.__track_file = track_file
        self.parse_tags(track_file)

    def parse_tags(self, track_file):
        if track_file.upper().endswith(self.__kind):
            raise ValueError('File kind not supported: %s', track_file)

        track = File(track_file)
        if "COMM::XXX" in track:
            raise ValueError("Track not identified: %s", track_file)
