import curses
import locale
from time import sleep

locale.resetlocale(locale.LC_ALL)
code = locale.getpreferredencoding()

class Muon:
    def __init__(self):
        curses.wrapper(self.mainloop)
    def mainloop(self, screen):
        begin_x = 20
        begin_y = 7
        height = 5
        width = 40
        win = screen.subwin(height, width, begin_y, begin_x)
        win.border()
        screen.border()
        running = True
        screen.nodelay(1)

        while running:
            screen.refresh()
            c = screen.getch()
            if c == ord('q'):
                running = False
            elif c == ord('w'):
                try:
                    win.clear()
                    screen.redrawwin()
                    del win
                except:
                    pass
            sleep(0.1)


if __name__ == '__main__':
    interflace = Muon()
