# thingity

Terminal based thing and to do management.

## tl;dr

    brew install fzf ripgrep the_silver_searcher bat
    pip3 install -e .

Create a thing with

    thing

Search things with

    things

Create a todo with

    todo a task

See todos with

    todo

## Configuration

Edit ``~/.config/thingity/thingity.ini` to configure thingity. For example:

```ini
[DEFAULT]
MY_NOTES = my-notes
MY_DO = -GEE,-PER:PER>FAM,DIY
THINGS_DIR = /Users/me/projects/things
```

- MY_NOTES: Name of your primary repository relative to the things directory
- MY_DO: Todo defualt configuration (see below)
- THINGS_DIR: Location of your things repositories

Todo default configuration is context filter that filters out specific todo
contexts by default.  It is of the form `(part0):(part):(part)` where

- part0 = -A,-B => exclude A and B as default context
- part = A>B,C => context A should also include B and Create

For example `-A,-B:B>C,D:E>F,G` would not show todos for "A" and "B" by
default. Furthermore B implies C and D, so C and D would also be excluded by
default. Note that you can show all todos, even excluded contexts, with `todo -a`.

## test

    ptw

## exploratative tests

Start up thingity in a container

    ./isolation-test.sh
