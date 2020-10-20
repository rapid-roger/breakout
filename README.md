# PyGame Breakout

This is a simple implementation with Python 3 and PyGame of the classic
[Breakout](https://en.wikipedia.org/wiki/Breakout_(video_game)) game by
[Gigi Sayfan]((https://gitlab.com/the-gigi)) and [me]((https://github.com/rapid-roger)). The purpose is
to serve as a first project for my portfolio.

# New features

- Advanced collision detection mechanism
- Vertical paddle movement
- Hidden game mechanics
- Generation of new levels
- Visual level design
- Panoramic sound effects
- Relaxing background music
- Bugs fixed

# Installation and usage

The prerequisites are:
- [Python 3.8](https://docs.python.org/3.8/) 
- [Pipenv](https://pipenv.readthedocs.io/en/latest/) 

Then clone the [repository](https://github.com/rapid-roger/breakout) and type:

```
pipenv install
```

You should see something like:

```
$ pipenv install

Creating a virtualenv for this project…
Pipfile: /Users/user/git/pygame-breakout/Pipfile
Using /Users/user/.pyenv/versions/3.8.0/bin/python3 (3.8.0) to create virtualenv…
⠙ Creating virtual environment...Using base prefix '/Users/user/.pyenv/versions/3.8.0'
New python executable in /Users/user/.local/share/virtualenvs/pygame-breakout-mgkKDQCD/bin/python3
Also creating executable in /Users/user/.local/share/virtualenvs/pygame-breakout-mgkKDQCD/bin/python
Installing setuptools, pip, wheel...
done.
Running virtualenv with interpreter /Users/user/.pyenv/versions/3.8.0/bin/python3

✔ Successfully created virtual environment!
Virtualenv location: /Users/user/.local/share/virtualenvs/pygame-breakout-mgkKDQCD
Installing dependencies from Pipfile.lock (b269cc)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 1/1 — 00:00:08
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

To run the game type:

```
pipenv run python breakout.py
```

# Credits

- Source code: https://gitlab.com/the-gigi/pygame-breakout
- Color constants: https://www.webucator.com/blog/2015/03/python-color-constants-module/
- Palette: https://coolors.co/306b34-1c5253-f3ffc6-c3eb78-b6174b-bcabae
- Backgrounds source: https://craftpix.net/freebies/free-horizontal-2d-game-backgrounds/
- Icon source: https://iconarchive.com/show/teneo-icons-by-kawsone/Brick-3D-2-icon.html
- Sound effects source: https://freesound.org/
- Music source: https://www.fesliyanstudios.com/royalty-free-music/downloads-c/lofi-hip-hop-music/