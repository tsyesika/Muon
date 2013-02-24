import curses

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

if __name__ == '__main__':
    interflace = Muon()
