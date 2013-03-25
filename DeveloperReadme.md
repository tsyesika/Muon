== Coding guidelines
This is fairly simple actually most of the standard python stuff to be honest. Seporate methods/functions with a single blank line.
Ensure all methods and functions have doc blocks at the start explaining. Use the class _ and __ to denote protected and private 
respectively. I use upper case for the first letter of class names but always lower case for variables (thoughout). Opt for accessing the variable directly than getters/setters (unless there is a reason why). Finally naming variables, methods and functions if it is a multiword name split it with underscores (do not do hungarian notation).

== Design of Muon 
Muon is quite modular and there are some strict design decisions (to make our lives easier now and in the future). I will just give a run down below of what each thing is, what the shorthand is (if there is any) and also any important things to note for developers touching that code.

=== Views
These are suppose to be super thin. It is important these take preformatted items and display them, they should not do anything more. This is meant to handle the urwid/ncurses stuff and nothing else.

=== Display 
This just will keep the main display around and set the background. Views talk to it, really this is just so we can smoothly transistion between views. Keep this thin, it probably will not change much from here on out.

=== Graphics Controller(s) 
I often refer to these as GCs. They are meant to take in unformatted, unprepared information, do any conversions needed and take just the relivent things out and pass it to the View when it is ready to be displayed. They also handle user input. This is really the glue between the backend and the front end, it will handle things of ensuring the focus is in the correct place, it will handle when it should update. They should take things like "Here is a note, I want it displayed" and convert it to something the View can actually display.

=== Translater 
Fairly self explanatory. Two things can happen, you give it a string and it gives you it translated into the set language, or you tell it which language the user wants to see. It really only will do that, it's job is simple.

=== Configuration 
This is really a small layer, the idea taken from MegBot. This in python will act like a list or dictionary. It will work as a glue between Muon and the config, the idea is as soon as we change something, we want it written back. We won't be changing much that often so the IO overhead is not worth thinking about. 

== Copyright 
This project is under the GPL v3, any code submitted must be licenced under the GPL v3. Please read the licence in the file COPYING to understand what this means if you're unsure about this software licence.

