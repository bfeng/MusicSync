# -*- coding: utf-8 -*-
from termcolor import cprint


def get_terminal_size():
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])


def get_terminal_width():
    size = get_terminal_size()
    return size[0]


def append_horizontal_line(msg, char, color):
    right_len = 0
    if len(msg) + 1 < get_terminal_width():
        right_len = get_terminal_width() - len(msg) - 1
    char_line = char * right_len
    line = msg + ' ' + char_line
    cprint(line, color)

