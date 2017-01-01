# -*- coding: utf-8 -*-

from termcolor import cprint
from models import SyncManager, MusicMeta, NeteaseMusicMeta
from util import append_horizontal_line


def print_ID3(track_file):
    mm = MusicMeta(track_file)
    cprint(track_file, "blue")
    print mm


def fix_ID3(track_file, dryrun=True):
    nmm = NeteaseMusicMeta(track_file)
    nmm.fix_ID3()
    if dryrun:
        cprint(track_file, "blue")
        print nmm
    else:
        nmm.save()


def del_ID3(track_file, skip=[]):
    mm = MusicMeta(track_file)
    for tag in mm.track:
        if tag not in skip:
            del(mm.track[tag])
    mm.track.save()


class BaseAction(object):

    def __init__(self, name, help_line):
        self.name = name
        self.help = help_line

    def get_name(self):
        return self.name

    def get_help(self):
        return self.help

    def attach_arguments(self, parser):
        pass

    def execute(self, args):
        pass


class FixAction(BaseAction):

    def __init__(self):
        super(FixAction, self).__init__("fix", "fix id3 tags for Netease music file/files")

    def attach_arguments(self, parser):
        parser.add_argument("-dryrun", action='store_true', help="Print ID3 tags before and after fixing")
        parser.add_argument("path", nargs='+', type=str, help="specify file path")

    def execute(self, args):
        input_path = args['path']
        for track_path in input_path:
            if args['dryrun']:
                append_horizontal_line("Before fixing", "=", 'red')
                print_ID3(track_path)
                append_horizontal_line("After fixing", "=", 'green')
                fix_ID3(track_path, True)
            else:
                fix_ID3(track_path, False)


class PrintAction(BaseAction):

    def __init__(self):
        super(PrintAction, self).__init__("print", "print id3 tags")

    def attach_arguments(self, parser):
        parser.add_argument("path", nargs='+', type=str, help="specify file path")

    def execute(self, args):
        input_path = args['path']
        for track_path in input_path:
            print_ID3(track_path)


class CopyAction(BaseAction):

    def __init__(self):
        super(CopyAction, self).__init__("cp", "copy files and fix id3 tags")

    def attach_arguments(self, parser):
        parser.add_argument("from", help="from path")
        parser.add_argument("to", help="to path")

    def execute(self, args):
        print "cp", args['from'], args['to']


class Copy2iTunesAction(BaseAction):

    def __init__(self):
        super(Copy2iTunesAction, self).__init__("cp_itunes", "Copy files to iTunes library")

    def attach_arguments(self, parser):
        parser.add_argument("netease", help="Netease Music Folder")
        parser.add_argument("iTunes", help="Path to iTunes root folder")

    def execute(self, args):
        print "cp_itunes", args['netease'], args['iTunes']
        netease_manager = SyncManager.new_library_manager('Netease', args['netease'])
        itunes_manager = SyncManager.new_library_manager('iTunes', args['iTunes'])
        # itunes_manager.pprint()
        for track in netease_manager.get_all_tracks():
            if track.is_fixable():
                track.fix_ID3()
                track.save()
            one = itunes_manager.find_by_album_and_name(track.get_album(), track.get_name())
            if one is not None:
                # print track
                cprint(one[1], 'green')
                # pass
            else:
                itunes_manager.copy_2_iTunes(track.get_track_file())
                cprint(track.get_track_file(), 'red')


class DeleteID3Action(BaseAction):

    def __init__(self):
        super(DeleteID3Action, self).__init__("rm_id3", "Delete ID3 tags from files")

    def attach_arguments(self, parser):
        parser.add_argument("path", nargs='+', type=str, help="Folders or file path")

    def execute(self, args):
        input_path = args['path']
        for track_path in input_path:
            del_ID3(track_path, skip=["COMM::XXX"])
