Muon
====

This is a command line pump.io client using urwid, a curses library. The client
is inspired by how mutt works, the look feel and even keybindings are similiar to
Mutt. This is still in alpha and I only work on it during my free time, because of
that it is likely going to be a while before It's usable for the general public.

If you do wish to try it, awesome! Do remember things won't work, it won't be
feature complete and it is likely to be increadably buggy.

Installation
============

Installing this is currently going to mean basic use of git, which means you need
to install git. Once you've got git do:

```
$ git clone https://github.com/xray7224/Muon.git && cd Muon
$ virtualenv . && source bin/activate && pip install pypump urwid xudd
```

To update you can then just do:

```
$ git pull
```

Continue to check here as I could add more dependences or instructions.

Running muon
------------

To run muon currently you just do
```
$ ./src/muon
```


Bugs || Feature requests
------------------------

So, any new bugs, feel free to report using GitHubs issue tracker.
I don't want any feature requests yet, I will in time but not this
early on in the development.

Licence
-------

This is under the GPLv3. For more information please check out [this](https://www.gnu.org/licenses/gpl.html)
