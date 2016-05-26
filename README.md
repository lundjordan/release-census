# releasewarrior

your assistant while on releaseduty

![squirrel spartan](https://pbs.twimg.com/profile_images/571907614906310658/HDB_I-Nr.jpeg)

In the spirit of [taskwarrior](https://taskwarrior.org/), releasewarrior is a tool that manages and provides a checklist for human decision tasks with releases in flight while providing documentation and troubleshooting for each task.

Rather than manually managing a wiki of releases, releasewarrior provides a set of commands to do this work for you.

## Installing

get copy of releasewarrior
```
git clone https://github.com/lundjordan/releasewarrior
cd releasewarrior
```
install it in your virtual python environment
```
mkvirtualenv --python=/path/to/python3 releasewarrior
python setup.py install
```

## Overview Flow

releasewarrior is made up of a number of subcommands. `create`, `update`, and `postmortem` are the main ones.

Each of those commands will do the follwoing in order:

1. create/update a data json data file that tracks a current release in flight
2. that data file is then rendered against a wiki template for a nice presentation layer.
3. finally, the command's changes to the data and wiki file are automatically committed using your user git config so each change is tracked.


## Using Commands

**pro tip**: use `release --help` and `release <subcommand> --help` lots

prior to each command your local master can not be behind origin/master. this is enforced and by design so that you always have the most up to date state

#### create new release checklist

usage: `release create $PRODUCT $BRANCH $VERSION`

example: `release create fennec release 17.0`

what happens:

 1. date file created:  [releasewarrior/releases/fennec-release-17.0.json](releasewarrior/releases/fennec-release-17.0.json)
2. wiki file rendedered from data:  [releasewarrior/releases/fennec-release-17.0.md](releasewarrior/releases/fennec-release-17.0.md)
3. change is commited: [commit](https://github.com/lundjordan/releasewarrior/commit/2b4d6b4c9631fbaf63da9afe939c54214aa1d603)

#### update existing release checklist

usage: `release update $PRODUCT $BRANCH $VERSION --$UPD`

example: `release update firefox beta 18.0b3 --graphid 1234567 --shipit --issue "win64 l10n hg timeout, retriggered"`

what happens:

1. data file updated:  [releasewarrior/releases/firefox-beta-18.0b3.json](releasewarrior/releases/firefox-beta-18.0b3.json)
2. wiki file rendered:  [releasewarrior/releases/firefox-beta-18.0b3.md](releasewarrior/releases/firefox-beta-18.0b3.md)
3. change is commited: [commit](https://github.com/lundjordan/releasewarrior/commit/64b53f215607a3f0ecb75394737acac9bce44c64)

#### checking current state of releases

now let's do some more interesting things

usage: `release status`

what happens:

`status` will tell you all of the current releases in flight. It does this by telling you which tasks remain and what the current issues are:

```
releasewarrior: DEBUG    RUNNING with args: status
releasewarrior: INFO     getting incomplete releases
releasewarrior: INFO     ensuring releasewarrior repo is up to date and in sync with origin
releasewarrior: INFO     fetching new csets from origin to origin/master
releasewarrior: INFO     RELEASE IN FLIGHT: firefox 46.0b1 16-05-19
releasewarrior: INFO            incomplete human tasks:
releasewarrior: INFO                    * submitted_shipit
releasewarrior: INFO                    * emailed_cdntest
releasewarrior: INFO                    * post_released
releasewarrior: INFO            latest issues:
releasewarrior: INFO                    * testing 1 2 3
releasewarrior: INFO     RELEASE IN FLIGHT: fennec 46.0 16-05-19
releasewarrior: INFO            incomplete human tasks:
releasewarrior: INFO                    * submitted_shipit
releasewarrior: INFO                    * pushed_mirrors
releasewarrior: INFO                    * post_released
releasewarrior: INFO            latest issues:
releasewarrior: INFO                    * none
```

#### creating a postmortem

and my favorite command..

usage: `release postmortem $DATE_OF_POSTMORTEM`

example: `release postmortem 2012-01-01`

what happens:

1. create a postmortem data file: [releases/POSTMORTEMS/2012-1-1.json](releases/POSTMORTEMS/2012-1-1.json)
2. for all releases that have all human tasks completed
  a. add their issues to the postmortem data file
  b. move the original release tracking data/wiki files into [releases/ARCHIVES](releases/ARCHIVES)
3. generate postmortem wiki file based on equivalent data file: [releases/POSTMORTEMS/2012-1-1.md](releases/POSTMORTEMS/2012-1-1.md)

bonus: one nice thing about this is the command is idopodent. in other words, you can call this as many times as you and it will only append to the given $date postmortem file as it finds completed releases!

## semi-manually updating releasewarrior

of course, given that the data is just a json file and changes tracked by this repo's revision history itself, you can always manually update the data and have the tool re-create the wiki

usage: `release sync firefox esr 27.0esr`

what happens:

1. data file is re-read but not updated
2. wiki file is re-rendered with the data is just got from current file
3. change is commited (if there was any change)

## completely manually updating releasewarrior

since this tool simply updates json and renders wiki files from it, you could even update the data manually, update a wiki manually, and just commit the changes yourself.

## hand waving

* releasewarrior only knows about the `origin` remote (whatever that points to in your local copy's .git/config. It also doesn't have knowledge of any branches so best stay on `master`.
  * however saying that, feel free to fork this repo to play around. that way you don't need to rewrite revision history after you are done experimenting
* there are not templates for Thunderbird yet. I'll add support for that soon
* there are no tests because I'm a bad developer
* the [how-tos](how-tos) docs for releaseduty are not up to date. I intend to fix that up this week
