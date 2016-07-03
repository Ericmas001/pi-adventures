###References:

* [What's So Great About Sudoedit?](http://www.wingtiplabs.com/blog/posts/2013/03/13/sudoedit/)

***

When you exit, `sudoedit` overwrites the original. (`sudoedit` does not update the real file every time you write changes to the temp file. It waits until you exit your editor.)

`sudoedit` lets the admin tighten sudoers with a “least privilege” model, while still letting the user choose which editor to use.

`sudoedit` preserves all your editor customizations, `sudo $EDITOR` doesn’t.

# Manually set favorite editor

`export EDITOR=/usr/bin/vim`

`export EDITOR=/usr/bin/emacs`

`export EDITOR=/bin/nano`

# Automatically set favorite editor

`~/.bashrc`
```
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

EDITOR=/bin/nano
```