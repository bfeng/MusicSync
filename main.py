#!/usr/bin/env python
# -*- coding: utf-8 -*-

from musicsync.actions import FixAction, CopyAction, Copy2iTunesAction, PrintAction, DeleteID3Action
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def attach_actions(main_parser, action_dict, action):
    action_dict[action.get_name()] = action
    action_parser = main_parser.add_parser(action.get_name(), help=action.get_help())
    action.attach_arguments(action_parser)


def main():
    action_dict = {}
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    attach_actions(subparsers, action_dict, FixAction())
    attach_actions(subparsers, action_dict, PrintAction())
    attach_actions(subparsers, action_dict, CopyAction())
    attach_actions(subparsers, action_dict, Copy2iTunesAction())
    attach_actions(subparsers, action_dict, DeleteID3Action())

    args = parser.parse_args()

    args = vars(args)

    action_key = args['action']

    if action_key in action_dict:
        action = action_dict[action_key]
        action.execute(args)


if __name__ == "__main__":
    main()
