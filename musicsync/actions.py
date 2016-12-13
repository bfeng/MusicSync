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
        parser.add_argument("path", help="specify file path")

    def execute(self, args):
        print "fix", args['path']


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
