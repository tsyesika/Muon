import curses
import locale
import random
from time import sleep

locale.resetlocale(locale.LC_ALL)
code = locale.getpreferredencoding()

class Interface:
    def __init__(self):
        self.windows = []
        self.char = []
        self.position = 0
        curses.wrapper(self.mainloop)

    def next_pos(self):
        npos = self.position + 1
        if npos > len(self.windows)-1:
            npos = 0
        self.position = npos

    def add_example(self, screen, height, width, begin_col):
        name = random.choice(["Tsyesika", "Matt Molyneaux", "Evan Prodromou", "David Nelson", "angryearthling"])
        action = random.choice(["watered", "planted", "harvested"])
        crop = random.choice(["Tomatoes", "Potatoes", "Strawberries", "Wheat", "Beans", "Pumpkins", "Corn", "Beets"])
        self.windows = [
            {
                "win":screen.subwin(height, width, 1, begin_col),
                "name":name,
                "text":["%s %s" % (action, crop)]
            }
        ] + self.windows
        self.redraw()

    def prev_pos(self):
        ppos = self.position - 1
        if ppos < 0:
            ppos = len(self.windows)-1
        self.position = ppos

    def write_text(self, win, name, text):
        # first write name
        name = "[%s] " % name
        lname = len(name)
        win.addstr(0, 0, name)

        # now the lines of text
        for p, line in enumerate(text):
            win.addstr(p, lname, line)
        win.refresh()

    def redraw(self):
        self.windows[0]["win"].mvderwin(1, self.begin_col)
        for i, win in enumerate(self.windows[1:]):
            prev = self.windows[i]["win"]
            height = prev.getparyx()[0]+prev.getmaxyx()[0]
            win["win"].mvderwin(height, self.begin_col)
            win["win"].refresh()

    def fix(self):
        x = False
        for pos, win in enumerate(self.windows):
            if pos == self.position:
                win["win"].bkgd(curses.color_pair(1))
                self.write_text(win["win"], win["name"], win["text"])
            else:
                win["win"].bkgd(curses.A_NORMAL)
                self.write_text(win["win"], win["name"], win["text"])
    
    def mainloop(self, screen):
        self.begin_col = 5
        begin_line = 1
        height = 1
        width = 128
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self.windows.append({
            "win":screen.subwin(height+2, width, begin_line, self.begin_col),
            "name":"Tsyesika",
            "text":["I've just released PyPump on my github, you should check it out here:", "http://github.com/xray7224/PyPump", "I Love you lots!"]
        })

        self.windows.append({
            "win":screen.subwin(height, width, begin_line+3, self.begin_col),
            "name":"moggers87",
            "text":["I love Tsyesika"]
        })

        self.fix()
       
        running = True
        screen.nodelay(1)

        while running:
            screen.refresh()
            c = screen.getch()
            if curses.KEY_DOWN == c:
                # Down key!
                self.next_pos()
                self.fix()
            elif curses.KEY_UP == c:
                # up key!
                self.prev_pos()
                self.fix()
            elif c == ord('q'):
                running = False
            elif c == ord('e'):
                self.add_example(screen, height, width, self.begin_col)
                self.fix()
            curses.napms(50)

if __name__ == '__main__':
    interflace = Interface()
    print(interflace.char)
