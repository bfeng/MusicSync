#!/usr/bin/env python
# -*- coding: utf-8 -*-

from musicsync.actions import FixAction, CopyAction, Copy2iTunesAction

import os
import argparse
import sys
import shutil
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('pyitunes')

# from convert import parse_tags, print_netease_music_tags, append_metadata
from pyItunes import Library


def load_iTunes_library(iTunes_library_xml):
    l = Library(iTunes_library_xml)
    return l.getPlaylist('All Music').tracks


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


def copy_2_iTunes(track_file, iTunes_path):
    iTunes_auto_add_path = iTunes_path + u'/iTunes Media/Automatically Add to iTunes.localized'
    if os.path.isdir(iTunes_auto_add_path) and os.path.exists(iTunes_auto_add_path):
        shutil.copy(track_file, iTunes_auto_add_path)
        print track_file, 'OK'


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


def attach_actions(main_parser, action_dict, action):
    action_dict[action.get_name()] = action
    action_parser = main_parser.add_parser(action.get_name(), help=action.get_help())
    action.attach_arguments(action_parser)


def main():
    action_dict = {}
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    attach_actions(subparsers, action_dict, FixAction())
    attach_actions(subparsers, action_dict, CopyAction())
    attach_actions(subparsers, action_dict, Copy2iTunesAction())

    args = parser.parse_args()

    args = vars(args)

    action_key = args['action']

    if action_key in action_dict:
        action = action_dict[action_key]
        action.execute(args)


if __name__ == "__main__":
    main()
