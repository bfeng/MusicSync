# -*- coding: utf-8 -*-
from __future__ import print_function

import time

from musicsync.models import SyncManager

try:
    import Tkinter as tk
    from Tkinter import ttk
    from Tkinter import tkFileDialog as filedialog
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog


class MusicSyncApp(ttk.Frame):

    @staticmethod
    def insert_track(tree, track, missing):
        status = 'Missing' if missing else 'Okay'
        iid = tree.insert('', 'end',
                          text=track.get_name(),
                          values=(track.get_name(), track.get_artists(), track.get_album(), status))
        return iid

    def run_sync(self):
        self.SYNC['state'] = "disabled"
        self.PB["value"] = 0
        self.PB["maximum"] = len(self.source_tree.selection())
        for item in self.source_tree.selection():
            # print(self.source_tree.item(item))
            track_file = self.to_copy[item].get_track_file()
            self.itunes.copy_2_iTunes(track_file)
            print(track_file)
            self.PB["value"] += 1
            time.sleep(.1)
            self.update()
        self.SYNC['text'] = "Done"

    def reset_tree(self):
        self.to_copy.clear()
        map(self.source_tree.delete, self.source_tree.get_children())
        self.SYNC['state'] = "normal"
        self.SYNC['text'] = 'Sync'
        self.PB['value'] = 0

    def populate_trees(self):
        self.reset_tree()
        music_dir = filedialog.askdirectory()
        if music_dir:
            self.PATHVAR.set(music_dir)
            self.netease = SyncManager.new_library_manager('Netease', music_dir)
            self.itunes = SyncManager.new_library_manager('iTunes', '/Users/bfeng/Music/iTunes')
            tracks = self.netease.get_all_tracks()
            for t in tracks:
                if self.itunes.find_by_album_and_name(t.get_album(), t.get_name()) is None:
                    iid = MusicSyncApp.insert_track(self.source_tree, t, True)
                    self.source_tree.selection_add(iid)
                    self.to_copy[iid] = t
                else:
                    iid = MusicSyncApp.insert_track(self.source_tree, t, False)

    def create_widgets(self):
        top_frame = ttk.Frame(self, height=40, padding=(0, 0, 0, 20))
        top_frame.pack(side='top', fill=tk.X, expand=False)

        bwn_frame = ttk.Frame(self, height=55, padding=(0, 20, 0, 0))
        bwn_frame.pack(side='bottom', fill=tk.X, expand=False)

        main_frame = ttk.Frame(self)
        main_frame.pack(side='top', fill=tk.BOTH, expand=True)

        self.CHO = ttk.Button(top_frame, width=20, text="Choose path...", command=self.populate_trees)
        self.CHO.pack(side='left')

        self.PATHVAR = tk.StringVar()
        self.PATHVAR.set("Please choose a path to load your songs")
        self.PATH = ttk.Entry(top_frame, state='readonly', textvariable=self.PATHVAR)
        self.PATH.pack(side='left', fill=tk.X, expand=True)

        self.SYNC = ttk.Button(bwn_frame, width=10, text="Sync", default='active', style='BlueButton.TButton',
                               command=self.run_sync)
        self.SYNC.pack(side='right')

        self.PB = ttk.Progressbar(bwn_frame, value=0, orient=tk.HORIZONTAL, mode='determinate')
        self.PB.pack(side='left', fill=tk.X, expand=True)

        column_names = ["Name", "Artist", "Album", "Status"]
        self.source_tree = ttk.Treeview(main_frame, columns=column_names, show="headings")
        for h in column_names:
            self.source_tree.heading(h, text=h)

        self.source_tree.pack(fill=tk.BOTH, expand=True)

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=20)
        master.title("Music Synchronization Toolkit")
        master.geometry('1280x720')

        s = ttk.Style()
        s.configure('.', font=('Helvetica', 13))
        s.configure('BlueButton.TButton', foreground='white', height=20, width=98)

        self.pack(fill=tk.BOTH, expand=True)
        self.source_tree = None
        self.SYNC = None
        self.PB = None
        self.to_copy = {}

        self.create_widgets()


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicSyncApp(root)
    app.mainloop()
