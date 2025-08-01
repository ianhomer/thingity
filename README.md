# thingity

Terminal based thing and to do management.

## Getting started

```sh
brew install fzf ripgrep the_silver_searcher bat
pipx install -e .
```

Create a thing with

```sh
thing
```

Search things with

```sh
things
```

Create a todo with

```sh
todo a task
```

See todos with

```sh
todo
```

## Configuration

Edit `~/.config/thingity/thingity.ini` to configure thingity. For example:

```ini
[DEFAULT]
MY_NOTES = my-notes
MY_DO = -GEE,-PER:PER>FAM,DIY
THINGS_DIR = /Users/me/projects/things
```

- MY_NOTES: Name of your primary repository relative to the things directory
- MY_DO: Todo default configuration (see below)
- THINGS_DIR: Location of your things repositories

Todo default configuration is context filter that filters out specific todo
contexts by default. It is of the form `(part0):(part):(part)` where

- part0 = -A,-B => exclude A and B as default context
- part = A>B,C => context A should also include B and Create

For example `-A,-B:B>C,D:E>F,G` would not show todos for "A" and "B" by
default. Furthermore B implies C and D, so C and D would also be excluded by
default. Note that you can show all todos, even excluded contexts, with `todo -a`.

## Development

Set up pre-commit checks

```sh
pip install pre-commit
pre-commit install
```

### Test

```sh
ptw
```

Or watch with a specific task

```sh
ptw -- -k task
```

### Exploratative tests

Start up thingity in a container

```sh
./isolation-test.sh
```

### Linting

Linting should take place before each commit, however it can be run on all files with

```sh
pre-commit run --all-files
```
