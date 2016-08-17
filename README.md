# releasewarrior

your assistant while on releaseduty

![squirrel spartan](https://pbs.twimg.com/profile_images/571907614906310658/HDB_I-Nr.jpeg)

In the spirit of [taskwarrior](https://taskwarrior.org/), releasewarrior is a tool that manages and provides a checklist for human decision tasks with releases in flight while providing documentation and troubleshooting for each task.

Rather than manually managing a wiki of releases, releasewarrior provides a set of commands to do this work for you.

## Installing

get copy of releasewarrior
```
git clone https://github.com/mozilla/releasewarrior
cd releasewarrior
```
install it in your virtual python environment
```
mkvirtualenv --python=/path/to/python3 releasewarrior
python setup.py develop
```
Using the develop target ensures that you get code updates along with data when pulling in changes.

## Overview Flow

releasewarrior is made up of a number of subcommands. `create`, `update`, and `postmortem` are the main ones.

Each of those commands will do the following in order:

1. create/update a data json data file that tracks a current release in flight
2. that data file is then rendered against a wiki template for a nice presentation layer.
3. finally, the command's changes to the data and wiki file are automatically committed using your user git config so each change is tracked.


## Using Commands

**pro tip**: use `release --help` and `release <subcommand> --help` lots

prior to each command your local master can not be behind origin/master. this is enforced and by design so that you always have the most up to date state

#### create new release checklist

usage:

`$ release create $PRODUCT $BRANCH $VERSION`

example:

`$ release create fennec release 17.0`

what happens:

1. date file created:  [releasewarrior/releases/fennec-release-17.0.json](https://github.com/mozilla/releasewarrior/blob/c640cef85bfc7e81d8b1c03ac0a7e0e2d39b81d1/releases/fennec-release-17.0.json)
2. wiki file rendered from data:  [releasewarrior/releases/fennec-release-17.0.md](https://github.com/mozilla/releasewarrior/blob/c640cef85bfc7e81d8b1c03ac0a7e0e2d39b81d1/releases/fennec-release-17.0.md)
3. change is committed: [commit](https://github.com/mozilla/releasewarrior/commit/c640cef85bfc7e81d8b1c03ac0a7e0e2d39b81d1)

#### update existing release checklist

usage:

`$ release update $PRODUCT $BRANCH $VERSION --$UPD`

example: 

say you want to update ff 18.0b3 by checking off submitted to shipit, adding a link to taskcluster graphid, and add an issue that came up with timing out.

`$ release update firefox beta 18.0b3 --shipit --graphid 1234567 --issue "win64 l10n hg timeout, retriggered"`

notice: you can update a release with many things at once. use `release update --help` to see all the update options

what happens:

1. data file updated:  [releasewarrior/releases/firefox-beta-18.0b3.json](https://github.com/mozilla/releasewarrior/blob/2c8f52f780349c5c2993533dcc6eac3cef7176e8/releases/firefox-beta-18.0b3.json)
2. wiki file rendered:  [releasewarrior/releases/firefox-beta-18.0b3.md](https://github.com/mozilla/releasewarrior/blob/2c8f52f780349c5c2993533dcc6eac3cef7176e8/releases/firefox-beta-18.0b3.md)
3. change is committed: [commit](https://github.com/mozilla/releasewarrior/commit/2c8f52f780349c5c2993533dcc6eac3cef7176e8)

#### more update examples: aborting current buildnum

example:

this time RC 15.0 current buildnum has been abandoned. you can simply pass --buildnum-aborted and a new buildnum will start being tracked

`$ release update firefox release-rc 15.0 --buildnum-aborted`

what happens:

1. data file updated:  [releasewarrior/releases/firefox-release-rc-15.0.json](https://github.com/mozilla/releasewarrior/blob/b40f423a5cebe72d46aeb25d8c7f0c2a8625e5b7/releases/firefox-release-rc-15.0.json)
2. wiki file rendered:  [releasewarrior/releases/firefox-release-rc-15.0.md](https://github.com/mozilla/releasewarrior/blob/b40f423a5cebe72d46aeb25d8c7f0c2a8625e5b7/releases/firefox-release-rc-15.0.md)
3. change is committed: [commit](https://github.com/mozilla/releasewarrior/commit/b40f423a5cebe72d46aeb25d8c7f0c2a8625e5b7)


#### checking current state of releases

now let's do some more interesting things

usage:

`$ release status`

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

usage:

`$ release postmortem $DATE_OF_POSTMORTEM`

example:

`$ release postmortem 2012-01-01`

what happens:

1. create a postmortem data file: [releases/POSTMORTEMS/2012-1-1.json](https://github.com/mozilla/releasewarrior/blob/d9517ce494cae610d17dc08c2d213eb12e088cb4/releases/POSTMORTEMS/2012-1-1.json)
2. for all releases that have all human tasks completed
  a. add their issues to the postmortem data file
  b. move the original release tracking data/wiki files into [releases/ARCHIVES](https://github.com/mozilla/releasewarrior/tree/examples/releases/ARCHIVE)
3. generate postmortem wiki file based on equivalent data file: [releases/POSTMORTEMS/2012-1-1.md](https://github.com/mozilla/releasewarrior/blob/d9517ce494cae610d17dc08c2d213eb12e088cb4/releases/POSTMORTEMS/2012-1-1.md)
4. change is committed: [commit](https://github.com/mozilla/releasewarrior/commit/d9517ce494cae610d17dc08c2d213eb12e088cb4)

**bonus: one nice thing about this is the command is idempotent. in other words, you can call this as many times as you and it will only append to the given $date postmortem file as it finds completed releases!**

## semi-manually updating releasewarrior

of course, given that the data is just a json file and changes are tracked by this repo's revision history, you can always manually update the data and have the tool re-create the wiki presentation against your data changes

usage:

`$ vim releases/firefox-esr-27.0esr.json  # change some value from false to true`
`$ release sync firefox esr 27.0esr`

what happens:

1. data file is re-read but not updated
2. wiki file is re-rendered with the data is just got from current file
3. change is committed (if there was any change)

## completely manually updating releasewarrior

if commands scare you and you want full control, you could even update the data manually, update a wiki manually, and just commit the changes yourself.


## tracking special requirements for upcoming releases

Sometimes you might need to have special requirements or steps for a future release. Since they are one offs, you don't want to add them to the templates.
The solution is to add upcoming releases to the releases/FUTURE/ dir. See [future release support](releases/FUTURE/README.md) for more details.

## hand waving

* releasewarrior only knows about the `origin` remote (whatever that points to in your local copy's .git/config. It also doesn't have knowledge of any branches so best stay on `master`.
  * however saying that, feel free to fork this repo to play around. that way you don't need to rewrite revision history after you are done experimenting
* there are not templates for Thunderbird yet. I'll add support for that soon
* there are no tests because I'm a bad developer
